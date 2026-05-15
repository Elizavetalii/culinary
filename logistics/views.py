from urllib.parse import quote
import math

from django.conf import settings
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, HttpResponseBadRequest
from accounts.utils import role_required
from communications.services import entity_comments_context
from crm.models import (
    Delivery,
    Route,
    RouteStatus,
    Courier,
    CourierStatus,
    RouteStop,
    CourierAssignment,
    Order,
    OrderStatus,
    Client,
    LogisticianProfile,
    AuditLog,
)
from .forms import (
    DeliveryForm,
    RouteForm,
    RouteStopForm,
    CourierAssignmentForm,
    LogisticianProfileForm,
    CourierStopStatusForm,
    ProofUploadForm,
    CourierProfileForm,
)


def _build_google_maps_dir_url(addresses):
    if len(addresses) < 2:
        return ""
    origin = quote(addresses[0])
    destination = quote(addresses[-1])
    waypoints = "|".join(quote(a) for a in addresses[1:-1])
    url = f"https://www.google.com/maps/dir/?api=1&origin={origin}&destination={destination}"
    if waypoints:
        url += f"&waypoints={waypoints}"
    return url


def _actor_role(user):
    if not user or not user.is_authenticated:
        return ""
    roles = list(user.roles.values_list("name", flat=True))
    return roles[0] if roles else ""


def _log_action(actor, obj, field_name="", old_value="", new_value="", reason=""):
    AuditLog.objects.create(
        actor=actor if actor and actor.is_authenticated else None,
        actor_role=_actor_role(actor),
        object_type=obj.__class__.__name__,
        object_id=obj.id,
        field_name=field_name,
        old_value=str(old_value or ""),
        new_value=str(new_value or ""),
        reason=reason or "",
    )


def _get_or_create_courier_profile(user):
    courier, created = Courier.objects.get_or_create(user=user)
    return courier, created


def _haversine_km(lat1, lon1, lat2, lon2):
    r = 6371.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)
    a = math.sin(d_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    return 2 * r * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def _route_metrics(route):
    stops = RouteStop.objects.filter(route=route).select_related("delivery")
    total_weight = sum([(s.delivery.cargo_weight_kg or 0) for s in stops])
    total_volume = sum([(s.delivery.cargo_volume_m3 or 0) for s in stops])
    total_stops = stops.count()
    service_minutes = sum([(s.service_time_minutes or 0) for s in stops])

    points = []
    for s in stops.order_by("sequence_index"):
        if s.latitude is not None and s.longitude is not None:
            points.append((float(s.latitude), float(s.longitude)))

    depot_lat = getattr(settings, "LOGISTICS_DEPOT_LAT", None)
    depot_lng = getattr(settings, "LOGISTICS_DEPOT_LNG", None)
    if depot_lat is not None and depot_lng is not None:
        points_with_depot = [(float(depot_lat), float(depot_lng))] + points
    else:
        points_with_depot = points

    distance_km = 0
    for idx in range(1, len(points_with_depot)):
        lat1, lon1 = points_with_depot[idx - 1]
        lat2, lon2 = points_with_depot[idx]
        distance_km += _haversine_km(lat1, lon1, lat2, lon2)

    if getattr(settings, "LOGISTICS_RETURN_TO_DEPOT", False) and depot_lat is not None and depot_lng is not None and points:
        lat1, lon1 = points[-1]
        distance_km += _haversine_km(lat1, lon1, float(depot_lat), float(depot_lng))

    avg_speed = getattr(settings, "LOGISTICS_AVG_SPEED_KMH", 35)
    travel_minutes = (distance_km / avg_speed) * 60 if avg_speed else 0
    duration_minutes = int(travel_minutes + service_minutes)

    return {
        "total_weight": total_weight,
        "total_volume": total_volume,
        "total_stops": total_stops,
        "distance_km": round(distance_km, 1),
        "duration_minutes": duration_minutes,
        "service_minutes": service_minutes,
        "travel_minutes": int(travel_minutes),
    }


def _route_validation(route):
    metrics = _route_metrics(route)
    errors = []
    warnings = []

    if metrics["duration_minutes"] > route.max_duration_minutes:
        errors.append(
            f"Превышение лимита времени: {metrics['duration_minutes']} мин > {route.max_duration_minutes} мин"
        )

    courier = None
    assignment = CourierAssignment.objects.filter(route=route).select_related("courier").first()
    if assignment:
        courier = assignment.courier
    capacity_weight = (courier.max_weight if courier else None) or (courier.payload_capacity_kg if courier else None)
    capacity_volume = (courier.max_volume if courier else None) or (courier.cargo_volume_m3 if courier else None)
    if capacity_weight and metrics["total_weight"] > capacity_weight:
        errors.append("Превышение лимита веса")
    if capacity_volume and metrics["total_volume"] > capacity_volume:
        errors.append("Превышение лимита объёма")

    if metrics["total_stops"] > route.soft_limit_stops:
        message = f"Превышен мягкий лимит точек: {metrics['total_stops']} > {route.soft_limit_stops}"
        if route.strict_mode:
            errors.append(message)
        else:
            warnings.append(message)

    return metrics, errors, warnings

def _courier_is_suitable(delivery, courier):
    if courier.status != CourierStatus.FREE:
        return False
    capacity_weight = courier.max_weight or courier.payload_capacity_kg
    capacity_volume = courier.max_volume or courier.cargo_volume_m3
    if delivery.cargo_weight_kg and not capacity_weight:
        return False
    if delivery.cargo_weight_kg and capacity_weight and delivery.cargo_weight_kg > capacity_weight:
        return False
    if delivery.cargo_volume_m3 and not capacity_volume:
        return False
    if delivery.cargo_volume_m3 and capacity_volume and delivery.cargo_volume_m3 > capacity_volume:
        return False
    for delivery_dim, courier_dim in [
        (delivery.cargo_length_cm, courier.cargo_length_cm),
        (delivery.cargo_width_cm, courier.cargo_width_cm),
        (delivery.cargo_height_cm, courier.cargo_height_cm),
    ]:
        if delivery_dim and not courier_dim:
            return False
        if delivery_dim and courier_dim and delivery_dim > courier_dim:
            return False
    return True


def _normalize_route_stop_sequence(route):
    stops = RouteStop.objects.filter(route=route).order_by("sequence_index", "id")
    for idx, stop in enumerate(stops, start=1):
        if stop.sequence_index != idx:
            RouteStop.objects.filter(pk=stop.pk).update(sequence_index=idx)


@role_required("Логист")
def deliveries_list(request):
    deliveries = Delivery.objects.select_related("order", "courier", "route").all()
    status = request.GET.get("status")
    date = request.GET.get("date")
    courier_id = request.GET.get("courier")
    route_id = request.GET.get("route")
    client_id = request.GET.get("client")
    sort = request.GET.get("sort")
    if status:
        deliveries = deliveries.filter(status=status)
    else:
        deliveries = deliveries.exclude(status__in=[Delivery.DeliveryStatus.DELIVERED, Delivery.DeliveryStatus.CANCELLED])
    if date:
        deliveries = deliveries.filter(planned_at__date=date)
    if courier_id:
        deliveries = deliveries.filter(courier_id=courier_id)
    if route_id:
        deliveries = deliveries.filter(route_id=route_id)
    if client_id:
        deliveries = deliveries.filter(order__client_id=client_id)
    if sort in ["planned_at", "-planned_at", "status", "-status"]:
        deliveries = deliveries.order_by(sort)
    if sort in ["client", "-client"]:
        deliveries = deliveries.order_by(f"{'-' if sort.startswith('-') else ''}order__client__name")
    orders_without_delivery = Order.objects.filter(
        is_archived=False,
        status__in=[
            OrderStatus.CONFIRMED,
            OrderStatus.IN_PRODUCTION,
            OrderStatus.READY_TO_SHIP,
            OrderStatus.SHIPPED,
        ],
        deliveries__isnull=True,
    ).select_related("client")
    couriers = Courier.objects.select_related("user").all()
    routes = Route.objects.all()
    clients = Client.objects.all()

    if request.GET.get("export") == "1":
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=deliveries.csv"
        response.write("Номер заказа;Клиент;Адрес;План;Курьер;Маршрут;Статус\n")
        for d in deliveries:
            response.write(
                f"{d.order.order_number};{d.order.client.name};{d.address or ''};"
                f"{d.planned_at or ''};{d.courier.user.full_name if d.courier else ''};"
                f"{d.route.planned_date if d.route else ''};{d.get_status_display()}\n"
            )
        return response
    return render(
        request,
        "logistics/list.html",
        {
            "deliveries": deliveries,
            "status_choices": Delivery.DeliveryStatus.choices,
            "orders_without_delivery": orders_without_delivery,
            "couriers": couriers,
            "routes": routes,
            "clients": clients,
        },
    )


@role_required("Логист")
def delivery_edit(request, pk):
    obj = get_object_or_404(Delivery, pk=pk)
    form = DeliveryForm(request.POST or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Доставка обновлена.")
        return redirect(f"/logistics/delivery/{obj.id}/")
    return render(request, "logistics/delivery_card.html", {"form": form, "delivery": obj, "title": "Карточка доставки"})


@role_required("Логист")
def delivery_by_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    delivery, _ = Delivery.objects.get_or_create(
        order=order,
        defaults={"address": order.address, "status": Delivery.DeliveryStatus.UNASSIGNED},
    )
    return redirect(f"/logistics/delivery/{delivery.id}/")


@role_required("Логист")
def delivery_card(request, pk):
    obj = get_object_or_404(Delivery, pk=pk)
    form = DeliveryForm(request.POST or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        delivery = form.save()
        if delivery.status == Delivery.DeliveryStatus.DELIVERED and not delivery.delivered_at:
            delivery.delivered_at = delivery.delivered_at or delivery.planned_at
            delivery.save(update_fields=["delivered_at"])
        messages.success(request, "Доставка обновлена.")
        return redirect(f"/logistics/delivery/{obj.id}/")
    couriers = Courier.objects.select_related("user").all()
    suitable_couriers = [c for c in couriers if _courier_is_suitable(obj, c)]
    profile, _ = LogisticianProfile.objects.get_or_create(user=request.user)
    destination = obj.address or obj.order.address
    origin = getattr(settings, "LOGISTICS_DEPOT_ADDRESS", "Химки")
    delivery_map_payload = {
        "origin": origin,
        "destination": destination,
    }
    context = {
        "form": form,
        "delivery": obj,
        "title": "Карточка доставки",
        "suitable_couriers": suitable_couriers,
        "delivery_map_payload": delivery_map_payload,
        "map_prefs": profile,
    }
    context.update(entity_comments_context(obj))
    return render(request, "logistics/delivery_card.html", context)

@role_required("Логист")
def couriers_list(request):
    couriers = Courier.objects.select_related("user").all()
    status = request.GET.get("status")
    transport = request.GET.get("transport")
    zone = request.GET.get("zone")
    min_payload = request.GET.get("min_payload")
    min_volume = request.GET.get("min_volume")
    sort = request.GET.get("sort")

    if status:
        couriers = couriers.filter(status=status)
    if transport:
        couriers = couriers.filter(transport_type__iexact=transport)
    if zone:
        couriers = couriers.filter(zone__icontains=zone)
    if min_payload:
        couriers = couriers.filter(payload_capacity_kg__gte=min_payload)
    if min_volume:
        couriers = couriers.filter(cargo_volume_m3__gte=min_volume)

    sort_map = {
        "name": "user__full_name",
        "-name": "-user__full_name",
        "status": "status",
        "-status": "-status",
        "payload": "payload_capacity_kg",
        "-payload": "-payload_capacity_kg",
        "updated": "location_updated_at",
        "-updated": "-location_updated_at",
    }
    if sort in sort_map:
        couriers = couriers.order_by(sort_map[sort])

    transport_types = (
        Courier.objects.exclude(transport_type="")
        .values_list("transport_type", flat=True)
        .distinct()
        .order_by("transport_type")
    )
    return render(
        request,
        "logistics/couriers.html",
        {
            "couriers": couriers,
            "status_choices": CourierStatus.choices,
            "transport_types": transport_types,
        },
    )


@role_required("Логист")
def routes_list(request):
    routes = Route.objects.select_related("logistician").all()
    return render(request, "logistics/routes.html", {"routes": routes})


@role_required("Логист")
def route_create(request):
    form = RouteForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        obj = form.save(commit=False)
        obj.logistician = request.user
        obj.save()
        messages.success(request, "Маршрут создан.")
        return redirect("/logistics/routes/")
    return render(request, "logistics/route_form.html", {"form": form, "title": "Новый маршрут"})


@role_required("Логист")
def route_edit(request, pk):
    route = get_object_or_404(Route, pk=pk)
    form = RouteForm(request.POST or None, instance=route)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Маршрут обновлён.")
        return redirect("/logistics/routes/")
    return render(request, "logistics/route_form.html", {"form": form, "title": "Редактирование маршрута"})


@role_required("Логист")
def route_detail(request, pk):
    route = get_object_or_404(Route, pk=pk)
    stops = RouteStop.objects.filter(route=route).select_related("delivery", "delivery__order")
    assignments = CourierAssignment.objects.filter(route=route).select_related("courier", "courier__user")

    stop_form = RouteStopForm(prefix="stop")
    stop_form.fields["delivery"].queryset = Delivery.objects.exclude(route_stops__route=route)
    assign_form = CourierAssignmentForm(prefix="assign")
    assign_form.fields["courier"].queryset = Courier.objects.exclude(assignments__route=route)

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "add_stop":
            stop_form = RouteStopForm(request.POST, prefix="stop")
            stop_form.fields["delivery"].queryset = Delivery.objects.exclude(route_stops__route=route)
            delivery_id = request.POST.get("stop-delivery")
            if delivery_id:
                delivery = get_object_or_404(Delivery, pk=delivery_id)
                delivery_date = delivery.delivery_date or (delivery.planned_at.date() if delivery.planned_at else None)
                if not delivery_date:
                    return HttpResponseBadRequest("У доставки не задана дата.")
                if delivery_date != route.planned_date:
                    return HttpResponseBadRequest("Нельзя добавить точку другой даты доставки.")
            if stop_form.is_valid():
                obj = stop_form.save(commit=False)
                obj.route = route
                last = RouteStop.objects.filter(route=route).order_by("-sequence_index").first()
                obj.sequence_index = (last.sequence_index + 1) if last else 1
                obj.save()
                _normalize_route_stop_sequence(route)
                _log_action(request.user, route, "stops", "", f"Добавлена остановка {obj.id}")
                messages.success(request, "Остановка добавлена.")
                return redirect(f"/logistics/routes/{route.id}/")
        if action == "assign_courier":
            assign_form = CourierAssignmentForm(request.POST, prefix="assign")
            assign_form.fields["courier"].queryset = Courier.objects.exclude(assignments__route=route)
            if assign_form.is_valid():
                obj = assign_form.save(commit=False)
                obj.route = route
                obj.save()
                _log_action(request.user, route, "courier", "", obj.courier_id)
                messages.success(request, "Курьер назначен.")
                return redirect(f"/logistics/routes/{route.id}/")
        if action in ["move_up", "move_down"]:
            stop_id = request.POST.get("stop_id")
            stop = get_object_or_404(RouteStop, pk=stop_id, route=route)
            delta = -1 if action == "move_up" else 1
            target = RouteStop.objects.filter(route=route, sequence_index=stop.sequence_index + delta).first()
            if target:
                RouteStop.objects.filter(pk=stop.pk).update(sequence_index=target.sequence_index)
                RouteStop.objects.filter(pk=target.pk).update(sequence_index=stop.sequence_index)
                _normalize_route_stop_sequence(route)
                _log_action(request.user, route, "sequence", "", "reorder")
                messages.success(request, "Порядок остановок обновлён.")
            return redirect(f"/logistics/routes/{route.id}/")
        if action == "remove_stop":
            stop_id = request.POST.get("stop_id")
            reason = request.POST.get("reason", "")
            stop = get_object_or_404(RouteStop, pk=stop_id, route=route)
            old_status = stop.status
            stop.status = RouteStop.StopStatus.CANCELLED
            stop.save(update_fields=["status"])
            _normalize_route_stop_sequence(route)
            _log_action(request.user, stop, "status", old_status, stop.status, reason or "Удалена из маршрута")
            messages.success(request, "Остановка удалена из маршрута.")
            return redirect(f"/logistics/routes/{route.id}/")
        if action == "publish_route":
            metrics, errors, warnings = _route_validation(route)
            if errors:
                return HttpResponseBadRequest("; ".join(errors))
            old_status = route.status
            route.status = RouteStatus.PUBLISHED
            route.save(update_fields=["status"])
            RouteStop.objects.filter(route=route, status__in=[RouteStop.StopStatus.DRAFT, RouteStop.StopStatus.CONFIRMED]).update(
                status=RouteStop.StopStatus.PLANNED
            )
            _log_action(request.user, route, "status", old_status, route.status, "Публикация маршрута")
            messages.success(request, "Маршрут опубликован.")
            return redirect(f"/logistics/routes/{route.id}/")

    stop_points = [
        {
            "id": None,
            "sequence": 0,
            "status": "Склад",
            "address": getattr(settings, "LOGISTICS_DEPOT_ADDRESS", "Склад"),
            "lat": float(getattr(settings, "LOGISTICS_DEPOT_LAT", 55.886)),
            "lng": float(getattr(settings, "LOGISTICS_DEPOT_LNG", 37.442)),
            "kind": "depot",
        }
    ]
    for s in stops:
        address = s.delivery.address or s.delivery.order.address
        stop_points.append(
            {
                "id": s.id,
                "sequence": s.sequence_index,
                "status": s.status,
                "address": address,
                "lat": float(s.latitude) if s.latitude is not None else None,
                "lng": float(s.longitude) if s.longitude is not None else None,
                "kind": "delivery",
            }
        )
    map_payload = {"route_id": route.id, "stops": stop_points}
    profile, _ = LogisticianProfile.objects.get_or_create(user=request.user)
    metrics, errors, warnings = _route_validation(route)
    if not errors and route.status == RouteStatus.DRAFT:
        old_status = route.status
        route.status = RouteStatus.PLANNED
        route.save(update_fields=["status"])
        _log_action(request.user, route, "status", old_status, route.status, "Авто-переход при валидности")

    context = {
        "route": route,
        "stops": stops,
        "assignments": assignments,
        "stop_form": stop_form,
        "assign_form": assign_form,
        "map_payload": map_payload,
        "map_prefs": profile,
        "total_points": metrics["total_stops"],
        "total_weight": metrics["total_weight"],
        "total_volume": metrics["total_volume"],
        "route_distance_km": metrics["distance_km"],
        "route_duration_minutes": metrics["duration_minutes"],
        "route_errors": errors,
        "route_warnings": warnings,
    }
    context.update(entity_comments_context(route))
    return render(request, "logistics/route_detail.html", context)

# Create your views here.


@role_required("Логист")
def logistic_profile(request):
    profile, _ = LogisticianProfile.objects.get_or_create(user=request.user)
    form = LogisticianProfileForm(request.POST or None, instance=profile)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Профиль логиста обновлён.")
        return redirect("/logistics/profile/")
    return render(
        request,
        "logistics/profile.html",
        {
            "form": form,
            "profile": profile,
        },
    )


@role_required("Курьер")
def courier_routes(request):
    courier, created = _get_or_create_courier_profile(request.user)
    if created:
        messages.info(request, "Профиль курьера создан автоматически. Заполните данные профиля.")
    date = request.GET.get("date")
    assignments = CourierAssignment.objects.filter(courier=courier).select_related("route")
    routes = [a.route for a in assignments]
    if date:
        routes = [r for r in routes if str(r.planned_date) == date]
    return render(request, "courier/routes.html", {"routes": routes})


@role_required("Курьер")
def courier_route_detail(request, pk):
    courier, _ = _get_or_create_courier_profile(request.user)
    route = get_object_or_404(Route, pk=pk)
    if not CourierAssignment.objects.filter(route=route, courier=courier).exists():
        return HttpResponseBadRequest("Маршрут недоступен.")
    stops = RouteStop.objects.filter(route=route).select_related("delivery", "delivery__order")
    stop_form = CourierStopStatusForm()
    proof_form = ProofUploadForm()
    return render(
        request,
        "courier/route_detail.html",
        {"route": route, "stops": stops, "stop_form": stop_form, "proof_form": proof_form},
    )


@role_required("Курьер")
def courier_stop_update(request, pk):
    courier, _ = _get_or_create_courier_profile(request.user)
    stop = get_object_or_404(RouteStop, pk=pk)
    if not CourierAssignment.objects.filter(route=stop.route, courier=courier).exists():
        return HttpResponseBadRequest("Остановка недоступна.")
    form = CourierStopStatusForm(request.POST, instance=stop)
    if request.method == "POST" and form.is_valid():
        new_status = form.cleaned_data["status"]
        if stop.status not in [RouteStop.StopStatus.IN_PROGRESS, RouteStop.StopStatus.PLANNED]:
            return HttpResponseBadRequest("Нельзя изменить статус этой остановки.")
        if new_status == RouteStop.StopStatus.IN_PROGRESS and stop.route.status not in [
            RouteStatus.PUBLISHED,
            RouteStatus.IN_PROGRESS,
        ]:
            return HttpResponseBadRequest("Маршрут ещё не опубликован.")
        if new_status == RouteStop.StopStatus.DONE:
            if not stop.proof_of_delivery:
                return HttpResponseBadRequest("Документ доставки обязателен.")
        if new_status == RouteStop.StopStatus.FAILED and not form.cleaned_data.get("failure_reason"):
            return HttpResponseBadRequest("Укажите причину недоставки.")
        old_status = stop.status
        stop = form.save(commit=False)
        if new_status in [RouteStop.StopStatus.DONE, RouteStop.StopStatus.FAILED]:
            stop.actual_time = timezone.now()
        stop.save()
        if new_status == RouteStop.StopStatus.IN_PROGRESS and stop.route.status == RouteStatus.PUBLISHED:
            stop.route.status = RouteStatus.IN_PROGRESS
            stop.route.save(update_fields=["status"])
        if new_status in [RouteStop.StopStatus.DONE, RouteStop.StopStatus.FAILED]:
            remaining = RouteStop.objects.filter(
                route=stop.route,
                status__in=[
                    RouteStop.StopStatus.DRAFT,
                    RouteStop.StopStatus.CONFIRMED,
                    RouteStop.StopStatus.PLANNED,
                    RouteStop.StopStatus.IN_PROGRESS,
                ],
            ).exists()
            if not remaining:
                stop.route.status = RouteStatus.DONE
                stop.route.save(update_fields=["status"])
        _log_action(request.user, stop, "status", old_status, new_status)
        messages.success(request, "Статус остановки обновлён.")
    return redirect(f"/courier/routes/{stop.route.id}/")


@role_required("Курьер")
def courier_upload_proof(request, pk):
    courier, _ = _get_or_create_courier_profile(request.user)
    stop = get_object_or_404(RouteStop, pk=pk)
    if not CourierAssignment.objects.filter(route=stop.route, courier=courier).exists():
        return HttpResponseBadRequest("Остановка недоступна.")
    form = ProofUploadForm(request.POST or None, request.FILES or None, instance=stop)
    if request.method == "POST" and form.is_valid():
        uploaded = request.FILES.get("proof_of_delivery")
        if uploaded:
            ext = f".{uploaded.name.split('.')[-1].lower()}" if "." in uploaded.name else ""
            allowed = getattr(settings, "LOGISTICS_ALLOWED_PROOF_EXT", [".pdf", ".jpg", ".jpeg", ".png"])
            if ext not in allowed:
                return HttpResponseBadRequest("Недопустимый формат файла.")
            max_size_mb = getattr(settings, "LOGISTICS_MAX_PROOF_SIZE_MB", 10)
            if uploaded.size > max_size_mb * 1024 * 1024:
                return HttpResponseBadRequest(f"Файл слишком большой. Максимальный размер — {max_size_mb} МБ.")
        else:
            return HttpResponseBadRequest("Документ доставки обязателен.")
        stop = form.save(commit=False)
        stop.proof_uploaded_at = timezone.now()
        stop.proof_uploaded_by = request.user
        stop.proof_review_status = RouteStop.ProofReviewStatus.PENDING
        if request.POST.get("status") == RouteStop.StopStatus.DONE:
            stop.status = RouteStop.StopStatus.DONE
            stop.actual_time = timezone.now()
        stop.save(
            update_fields=[
                "proof_of_delivery",
                "proof_uploaded_at",
                "proof_uploaded_by",
                "proof_review_status",
                "status",
                "actual_time",
            ]
        )
        _log_action(request.user, stop, "proof_of_delivery", "", stop.proof_of_delivery.name)
        messages.success(request, "Документ загружен.")
    return redirect(f"/courier/routes/{stop.route.id}/")


@role_required("Менеджер")
def proof_review_list(request):
    stops = RouteStop.objects.filter(proof_of_delivery__isnull=False).select_related("route", "delivery", "delivery__order")
    status = request.GET.get("status")
    if status:
        stops = stops.filter(proof_review_status=status)
    return render(request, "manager/proof_review_list.html", {"stops": stops})


@role_required("Менеджер")
def proof_review_update(request, pk):
    stop = get_object_or_404(RouteStop, pk=pk)
    action = request.POST.get("action")
    comment = request.POST.get("comment", "")
    if action not in ["approve", "reject"]:
        return HttpResponseBadRequest("Некорректное действие.")
    old_status = stop.proof_review_status
    stop.proof_review_status = (
        RouteStop.ProofReviewStatus.APPROVED if action == "approve" else RouteStop.ProofReviewStatus.REJECTED
    )
    stop.proof_review_comment = comment
    stop.proof_reviewed_at = timezone.now()
    stop.proof_reviewed_by = request.user
    stop.save(update_fields=["proof_review_status", "proof_review_comment", "proof_reviewed_at", "proof_reviewed_by"])
    _log_action(request.user, stop, "proof_review_status", old_status, stop.proof_review_status, comment)
    messages.success(request, "Проверка обновлена.")
    return redirect("/logistics/manager/proofs/")


@role_required("Курьер")
def courier_profile(request):
    courier, _ = _get_or_create_courier_profile(request.user)
    form = CourierProfileForm(request.POST or None, instance=courier)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Профиль курьера обновлён.")
        return redirect("/logistics/courier/profile/")
    return render(
        request,
        "courier/profile.html",
        {
            "form": form,
            "courier": courier,
        },
    )
