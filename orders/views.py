from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from accounts.utils import roles_required, role_required
from django.utils import timezone
from django.conf import settings
from django.db.models import Q, Sum
from django.db import transaction
from django.http import JsonResponse, HttpResponseBadRequest
from communications.services import entity_comments_context
from crm.models import (
    Order,
    OrderStatus,
    Client,
    Delivery,
    OrderItem,
    PickingSession,
    Dish,
    TechCard,
    TechCardComponent,
    ClientAllowedTechCard,
    ProductionReservation,
    IngredientReservation,
    EquipmentReservation,
    IngredientStock,
    DishEquipmentRequirement,
    Ingredient,
)
from .forms import OrderForm, PickingSessionForm, OrderItemPickFormSet, OrderItemFormSet


def _apply_production_fields(order):
    if not order.delivery_date or not order.delivery_time:
        return
    morning_cutoff = timezone.datetime.strptime(
        getattr(settings, "ORDER_MORNING_CUTOFF_TIME", "10:00"), "%H:%M"
    ).time()
    if order.delivery_time <= morning_cutoff:
        order.production_date = order.delivery_date - timezone.timedelta(days=1)
        order.production_shift = "Ночная"
        order.production_window_start = timezone.datetime.strptime(
            getattr(settings, "PRODUCTION_WINDOW_NIGHT_START", "22:00"), "%H:%M"
        ).time()
        order.production_window_end = timezone.datetime.strptime(
            getattr(settings, "PRODUCTION_WINDOW_NIGHT_END", "06:00"), "%H:%M"
        ).time()
    else:
        order.production_date = order.delivery_date
        order.production_shift = "Дневная"
        order.production_window_start = timezone.datetime.strptime(
            getattr(settings, "PRODUCTION_WINDOW_DAY_START", "06:00"), "%H:%M"
        ).time()
        order.production_window_end = timezone.datetime.strptime(
            getattr(settings, "PRODUCTION_WINDOW_DAY_END", "18:00"), "%H:%M"
        ).time()


def _order_item_weight(item):
    if not item.dish:
        return item.quantity or 0
    if item.dish.base_uom == Dish.BaseUom.KG:
        return item.quantity or 0
    if item.dish.base_uom == Dish.BaseUom.PCS:
        if item.dish.unit_weight_kg:
            return (item.quantity or 0) * item.dish.unit_weight_kg
        return 0
    return item.quantity or 0


def _attach_tech_card(order, item):
    if not item.dish:
        return
    allowed = ClientAllowedTechCard.objects.filter(client=order.client, tech_card__dish=item.dish, tech_card__is_active=True)
    if allowed.exists():
        item.custom_tech_card = allowed.first().tech_card
        return
    active = TechCard.objects.filter(dish=item.dish, is_active=True).order_by("-id")
    if active.count() == 1:
        item.custom_tech_card = active.first()
        return
    raise ValueError("Для блюда нет активной техкарты или их несколько без разрешения клиента.")


def _ensure_order_number(order):
    if order.pk and order.order_number:
        return
    order.order_number = Order.generate_order_number()


RESERVED_STATUSES = {
    OrderStatus.CONFIRMED,
    OrderStatus.IN_PRODUCTION,
    OrderStatus.READY_TO_SHIP,
    OrderStatus.SHIPPED,
}


def _get_reserved_qty_map(production_date, exclude_order_id=None):
    if not production_date:
        return {}
    qs = OrderItem.objects.filter(
        order__status__in=RESERVED_STATUSES,
        dish__isnull=False,
    ).filter(
        Q(order__production_date=production_date)
        | Q(order__production_date__isnull=True, order__delivery_date=production_date)
    )
    if exclude_order_id:
        qs = qs.exclude(order_id=exclude_order_id)
    data = qs.values("dish_id").annotate(total=Sum("quantity"))
    return {row["dish_id"]: row["total"] for row in data}


def _validate_dish_capacity(order, items):
    production_date = order.production_date or order.delivery_date
    reserved_map = _get_reserved_qty_map(production_date, exclude_order_id=order.id)
    requested_map = {}
    for item in items:
        if not item.dish_id:
            continue
        requested_map[item.dish_id] = requested_map.get(item.dish_id, 0) + (item.quantity or 0)

    errors = []
    for dish_id, requested_qty in requested_map.items():
        dish = Dish.objects.filter(pk=dish_id).only("id", "name", "daily_capacity").first()
        if not dish or dish.daily_capacity is None:
            continue
        reserved_qty = reserved_map.get(dish_id, 0) or 0
        available_qty = max(dish.daily_capacity - reserved_qty, 0)
        if requested_qty > available_qty:
            errors.append(
                f"Недостаточная мощность для «{dish.name}»: доступно {available_qty}, запрошено {requested_qty}."
            )
    return errors


def _validate_order_capacity(order, items):
    errors = []
    warnings = []
    info = {}

    if order.delivery_date:
        cutoff = timezone.datetime.strptime(getattr(settings, "ORDER_CUTOFF_TIME", "16:00"), "%H:%M").time()
        if order.delivery_date == timezone.now().date() and timezone.now().time() > cutoff:
            errors.append("Заказ после допустимого времени. Перенесите дату доставки.")

    total_weight = sum([_order_item_weight(i) for i in items])
    info["order_weight"] = total_weight
    if order.client.daily_max_weight_kg and order.delivery_date:
        existing = Order.objects.filter(client=order.client, delivery_date=order.delivery_date).exclude(pk=order.pk)
        existing_weight = sum([sum([_order_item_weight(i) for i in o.items.all()]) for o in existing])
        info["client_daily_limit"] = order.client.daily_max_weight_kg
        info["client_reserved"] = existing_weight
        if existing_weight + total_weight > order.client.daily_max_weight_kg:
            errors.append("Превышен лимит клиента по весу на день.")
    if order.client.daily_min_qty and total_weight < order.client.daily_min_qty:
        warnings.append("Минимальный объём клиента не достигнут.")

    max_capacity = getattr(settings, "PRODUCTION_MAX_WEIGHT_KG", None)
    if max_capacity is not None and order.production_date:
        reserved = ProductionReservation.objects.filter(production_date=order.production_date).exclude(order=order).aggregate(
            total=Sum("weight_kg")
        )["total"] or 0
        info["production_capacity"] = max_capacity
        info["production_reserved"] = reserved
        if reserved + total_weight > max_capacity:
            excess = (reserved + total_weight) - max_capacity
            errors.append(
                f"Превышена производственная мощность на {order.production_date}. "
                f"Доступно: {max_capacity} кг, ваш заказ: {total_weight} кг, превышение: {excess} кг."
            )
    elif max_capacity is not None:
        info["production_capacity"] = max_capacity
        info["production_reserved"] = 0

    equipment_requirements = {}
    for item in items:
        if not item.dish:
            continue
        for req in DishEquipmentRequirement.objects.filter(dish=item.dish).select_related("equipment"):
            minutes = (req.minutes_per_unit or 0) * (item.quantity or 0)
            equipment_requirements[req.equipment_id] = equipment_requirements.get(req.equipment_id, 0) + minutes

    for eq_id, minutes in equipment_requirements.items():
        eq = DishEquipmentRequirement.objects.filter(equipment_id=eq_id).select_related("equipment").first().equipment
        available_hours = float(eq.available_hours or 0)
        reserved_hours = EquipmentReservation.objects.filter(equipment=eq, production_date=order.production_date).exclude(
            order=order
        ).aggregate(total=Sum("hours"))["total"] or 0
        required_hours = minutes / 60
        if available_hours and reserved_hours + required_hours > available_hours:
            errors.append(f"Превышен лимит оборудования: {eq.name}")

    ingredients_need = {}
    for item in items:
        if not item.custom_tech_card and item.dish:
            active = TechCard.objects.filter(dish=item.dish, is_active=True).order_by("-id").first()
            if active:
                item.custom_tech_card = active
        if not item.custom_tech_card:
            continue
        for comp in TechCardComponent.objects.filter(tech_card=item.custom_tech_card):
            qty = (comp.quantity or 0) * (item.quantity or 0)
            ingredients_need[comp.ingredient_id] = ingredients_need.get(comp.ingredient_id, 0) + qty

    ingredient_warnings = []
    ingredients_map = Ingredient.objects.in_bulk(list(ingredients_need.keys()))
    for ingredient_id, qty in ingredients_need.items():
        stock = IngredientStock.objects.filter(ingredient_id=ingredient_id).first()
        available = stock.quantity if stock else 0
        reserved = IngredientReservation.objects.filter(ingredient_id=ingredient_id, production_date=order.production_date).exclude(
            order=order
        ).aggregate(total=Sum("quantity"))["total"] or 0
        missing = qty - (available - reserved)
        if missing > 0:
            ingredient = ingredients_map.get(ingredient_id)
            ingredient_warnings.append(
                {
                    "id": ingredient_id,
                    "name": ingredient.name if ingredient else f"ID {ingredient_id}",
                    "required": float(qty),
                    "available": float(available),
                    "reserved": float(reserved),
                    "missing": float(missing),
                }
            )
    if ingredient_warnings:
        errors.append("Недостаточно ингредиентов для заказа. Проверьте список ниже.")
        info["ingredient_warnings"] = ingredient_warnings

    for item in items:
        if not item.dish:
            continue
        if item.dish.min_batch_qty and (item.quantity or 0) < item.dish.min_batch_qty:
            errors.append(f"Минимальная партия для {item.dish.name} — {item.dish.min_batch_qty}")
        if item.dish.batch_multiple_qty and (item.quantity or 0) % item.dish.batch_multiple_qty != 0:
            errors.append(f"Количество для {item.dish.name} должно быть кратно {item.dish.batch_multiple_qty}")

    return errors, warnings, info


def _reserve_resources(order):
    ProductionReservation.objects.filter(order=order).delete()
    IngredientReservation.objects.filter(order=order).delete()
    EquipmentReservation.objects.filter(order=order).delete()

    items = list(order.items.select_related("dish"))
    total_weight = sum([_order_item_weight(i) for i in items])
    if order.production_date:
        ProductionReservation.objects.create(order=order, production_date=order.production_date, weight_kg=total_weight)

    ingredients_need = {}
    for item in items:
        if item.custom_tech_card:
            for comp in TechCardComponent.objects.filter(tech_card=item.custom_tech_card):
                qty = (comp.quantity or 0) * (item.quantity or 0)
                ingredients_need[comp.ingredient_id] = ingredients_need.get(comp.ingredient_id, 0) + qty
    for ingredient_id, qty in ingredients_need.items():
        IngredientReservation.objects.create(
            order=order,
            ingredient_id=ingredient_id,
            production_date=order.production_date,
            quantity=qty,
        )

    equipment_requirements = {}
    for item in items:
        if not item.dish:
            continue
        for req in DishEquipmentRequirement.objects.filter(dish=item.dish).select_related("equipment"):
            minutes = (req.minutes_per_unit or 0) * (item.quantity or 0)
            equipment_requirements[req.equipment_id] = equipment_requirements.get(req.equipment_id, 0) + minutes
    for eq_id, minutes in equipment_requirements.items():
        EquipmentReservation.objects.create(
            order=order,
            equipment_id=eq_id,
            production_date=order.production_date,
            hours=minutes / 60,
        )


@roles_required(["Менеджер", "Администратор системы"])
def order_list(request):
    qs = Order.objects.select_related("client").filter(is_archived=False)
    q = request.GET.get("q")
    status = request.GET.get("status")
    date_from = request.GET.get("from")
    date_to = request.GET.get("to")
    client_id = request.GET.get("client")
    sort = request.GET.get("sort")
    if q:
        qs = qs.filter(order_number__icontains=q)
    if status:
        qs = qs.filter(status=status)
    if client_id:
        qs = qs.filter(client_id=client_id)
    if date_from:
        qs = qs.filter(created_at__date__gte=date_from)
    if date_to:
        qs = qs.filter(created_at__date__lte=date_to)
    if sort in ["created_at", "-created_at", "order_number", "-order_number"]:
        qs = qs.order_by(sort)
    clients = Client.objects.all()
    return render(
        request,
        "orders/list.html",
        {"orders": qs, "statuses": OrderStatus.choices, "clients": clients},
    )


def _order_form_context(form, formset, title, **extra):
    context = {
        "form": form,
        "formset": formset,
        "title": title,
        "clients": Client.objects.all(),
        "dish_prices": {
            d.id: float(d.default_price)
            for d in Dish.objects.filter(is_active=True, default_price__isnull=False)
        },
    }
    context.update(extra)
    if form.instance and form.instance.pk:
        context.update(entity_comments_context(form.instance))
    return context


def _active_formset_items(formset):
    items = []
    for item_form in formset.forms:
        if not item_form.cleaned_data:
            continue
        if item_form.cleaned_data.get("DELETE"):
            continue
        item = item_form.save(commit=False)
        if item.dish:
            items.append(item)
    return items


def _deleted_formset_items(formset):
    deleted = []
    for item_form in formset.forms:
        if item_form.cleaned_data.get("DELETE") and item_form.instance.pk:
            deleted.append(item_form.instance)
    return deleted


def _prepare_order_items(order, items):
    errors = []
    for item in items:
        item.order = order
        try:
            _attach_tech_card(order, item)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if item.unit_price is None and item.dish and item.dish.default_price is not None:
            item.unit_price = item.dish.default_price
        if item.unit_price is None:
            errors.append(f"Цена не задана для блюда «{item.dish}».")
    return errors


def _save_order_with_items(request, form, formset, title, success_message, redirect_url, existing_order=None):
    order = form.save(commit=False)
    if existing_order is None and request.user.roles.filter(name__iexact="Менеджер").exists():
        order.manager = request.user
    action = request.POST.get("action", "save")
    order.status = OrderStatus.DRAFT if action == "draft" else OrderStatus.REVIEW
    _apply_production_fields(order)
    _ensure_order_number(order)

    items = _active_formset_items(formset)
    if not items:
        messages.error(request, "Добавьте хотя бы одну позицию заказа.")
        return render(request, "orders/form.html", _order_form_context(form, formset, title))

    item_errors = _prepare_order_items(order, items)
    if item_errors:
        for err in item_errors:
            messages.error(request, err)
        return render(request, "orders/form.html", _order_form_context(form, formset, title))

    errors, warnings, info = _validate_order_capacity(order, items)
    capacity_errors = _validate_dish_capacity(order, items)
    errors.extend(capacity_errors)
    if errors:
        for err in errors:
            messages.error(request, err)
        return render(
            request,
            "orders/form.html",
            _order_form_context(form, formset, title, warnings=warnings, info=info),
        )

    with transaction.atomic():
        order.save()
        for deleted in _deleted_formset_items(formset):
            deleted.delete()
        for item in items:
            item.order = order
            item.save()
        order.recalc_total()
        _reserve_resources(order)
        if order.status in [OrderStatus.CONFIRMED, OrderStatus.READY_TO_SHIP, OrderStatus.SHIPPED] and not order.deliveries.exists():
            Delivery.objects.create(
                order=order,
                address=order.address,
                status=Delivery.DeliveryStatus.UNASSIGNED,
            )
    messages.success(request, success_message)
    return redirect(redirect_url)


@roles_required(["Менеджер", "Администратор системы"])
def order_create(request):
    form = OrderForm(request.POST or None)
    formset = OrderItemFormSet(request.POST or None, queryset=OrderItem.objects.none())
    if request.method == "POST" and form.is_valid() and formset.is_valid():
        return _save_order_with_items(request, form, formset, "Новый заказ", "Заказ создан.", "/orders/")
    return render(
        request,
        "orders/form.html",
        _order_form_context(form, formset, "Новый заказ"),
    )


@roles_required(["Менеджер", "Администратор системы"])
def order_edit(request, pk):
    obj = get_object_or_404(Order, pk=pk)
    form = OrderForm(request.POST or None, instance=obj)
    formset = OrderItemFormSet(request.POST or None, queryset=obj.items.all())
    if request.method == "POST" and form.is_valid() and formset.is_valid():
        return _save_order_with_items(
            request,
            form,
            formset,
            "Редактирование заказа",
            "Заказ обновлён.",
            "/orders/",
            existing_order=obj,
        )
    return render(
        request,
        "orders/form.html",
        _order_form_context(form, formset, "Редактирование заказа"),
    )


@roles_required(["Менеджер", "Администратор системы"])
def order_availability(request):
    delivery_date = request.GET.get("delivery_date")
    client_id = request.GET.get("client_id")
    order_id = request.GET.get("order_id")
    if not delivery_date:
        return HttpResponseBadRequest("delivery_date обязателен")
    max_capacity = getattr(settings, "PRODUCTION_MAX_WEIGHT_KG", None)
    reserved_map = _get_reserved_qty_map(delivery_date, exclude_order_id=order_id)
    reserved_capacity = ProductionReservation.objects.filter(production_date=delivery_date).aggregate(
        total=Sum("weight_kg")
    )["total"] or 0
    dishes = []
    for dish in Dish.objects.filter(is_active=True).order_by("name"):
        daily_capacity = float(dish.daily_capacity) if dish.daily_capacity is not None else None
        reserved_qty = float(reserved_map.get(dish.id, 0) or 0)
        available_qty = None
        if daily_capacity is not None:
            available_qty = max(daily_capacity - reserved_qty, 0)
        weight_per_unit = float(dish.unit_weight_kg) if dish.unit_weight_kg is not None else None
        max_by_capacity = None
        if max_capacity is not None:
            if dish.base_uom == Dish.BaseUom.KG:
                max_by_capacity = max_capacity - reserved_capacity
            elif dish.base_uom == Dish.BaseUom.PCS and weight_per_unit:
                max_by_capacity = (max_capacity - reserved_capacity) / weight_per_unit
        dishes.append(
            {
                "dish_id": dish.id,
                "dish_name": dish.name,
                "unit": dish.unit,
                "base_uom": dish.base_uom,
                "quantity_scale": dish.quantity_scale,
                "weight_per_unit_kg": weight_per_unit,
                "daily_capacity": daily_capacity,
                "reserved_qty": round(reserved_qty, 3),
                "available_qty": round(available_qty, 3) if available_qty is not None else None,
                "max_by_capacity": round(max_by_capacity, 3) if max_by_capacity is not None else None,
                "min_batch": float(dish.min_batch_qty) if dish.min_batch_qty else None,
                "step": float(dish.batch_multiple_qty) if dish.batch_multiple_qty else None,
                "price": float(dish.default_price) if dish.default_price is not None else None,
            }
        )
    return JsonResponse(
        {
            "production_date": delivery_date,
            "capacity_total": max_capacity if max_capacity is not None else 0,
            "capacity_reserved": reserved_capacity,
            "capacity_available": max_capacity - reserved_capacity if max_capacity is not None else 0,
            "dishes": dishes,
        }
    )


@roles_required(["Менеджер", "Администратор системы"])
def order_delete(request, pk):
    obj = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Заказ удалён.")
        return redirect("/orders/")
    return render(request, "orders/delete.html", {"object": obj})

@roles_required(["Менеджер", "Администратор системы"])
def order_archive(request):
    qs = Order.objects.select_related("client").filter(is_archived=True)
    return render(request, "orders/archive.html", {"orders": qs, "statuses": OrderStatus.choices})


@roles_required(["Менеджер", "Администратор системы"])
def order_bulk_delete(request):
    if request.method != "POST":
        return HttpResponseBadRequest("POST обязателен")
    ids = request.POST.getlist("order_ids")
    if not ids:
        messages.error(request, "Выберите заказы для удаления.")
        return redirect("/orders/")
    qs = Order.objects.filter(id__in=ids)
    count = qs.count()
    qs.delete()
    messages.success(request, f"Удалено заказов: {count}.")
    return redirect("/orders/")


@roles_required(["Менеджер", "Сборщик заказов"])
def order_status_update(request, pk):
    obj = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        status = request.POST.get("status")
        if status in dict(OrderStatus.choices):
            obj.status = status
            obj.save(update_fields=["status"])
            if status in [OrderStatus.CONFIRMED, OrderStatus.READY_TO_SHIP, OrderStatus.SHIPPED] and not obj.deliveries.exists():
                Delivery.objects.create(
                    order=obj,
                    address=obj.address,
                    status=Delivery.DeliveryStatus.UNASSIGNED,
                )
                messages.success(request, "Доставка создана автоматически.")
            messages.success(request, "Статус заказа обновлён.")
    return redirect(request.META.get("HTTP_REFERER", "/orders/"))


@roles_required(["Менеджер", "Администратор системы"])
def order_archive_toggle(request, pk):
    obj = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        obj.is_archived = not obj.is_archived
        obj.save(update_fields=["is_archived"])
        messages.success(request, "Статус архива обновлён.")
    return redirect(request.META.get("HTTP_REFERER", "/orders/"))


@role_required("Сборщик заказов")
def picker_orders(request):
    qs = Order.objects.select_related("client").filter(is_archived=False)
    status = request.GET.get("status")
    date_from = request.GET.get("from")
    date_to = request.GET.get("to")
    if status:
        qs = qs.filter(status=status)
    else:
        qs = qs.exclude(status__in=[OrderStatus.SHIPPED, OrderStatus.CANCELLED])
    if date_from:
        qs = qs.filter(created_at__date__gte=date_from)
    if date_to:
        qs = qs.filter(created_at__date__lte=date_to)
    return render(
        request,
        "orders/picker_list.html",
        {"orders": qs, "statuses": OrderStatus.choices},
    )


@role_required("Сборщик заказов")
def picker_order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    items_qs = order.items.all()
    session, _ = PickingSession.objects.get_or_create(order=order, defaults={"picker": request.user})
    if not session.started_at:
        session.started_at = timezone.now()
        session.picker = request.user
        session.save(update_fields=["started_at", "picker"])

    formset = OrderItemPickFormSet(request.POST or None, queryset=items_qs)
    session_form = PickingSessionForm(request.POST or None, instance=session, prefix="session")

    if request.method == "POST":
        action = request.POST.get("action", "save")
        if formset.is_valid() and session_form.is_valid():
            formset.save()
            session_form.save()

            if action == "finish":
                final_statuses = {
                    OrderItem.ItemStatus.DONE,
                    OrderItem.ItemStatus.OUT_OF_STOCK,
                    OrderItem.ItemStatus.REPLACED,
                }
                if items_qs.exclude(item_status__in=final_statuses).exists():
                    messages.error(request, "Не все позиции имеют итоговый статус.")
                else:
                    order.status = OrderStatus.SHIPPED
                    order.save(update_fields=["status"])
                    session.finished_at = timezone.now()
                    session.save(update_fields=["finished_at"])
                    if not order.deliveries.exists():
                        Delivery.objects.create(
                            order=order,
                            address=order.address,
                            status=Delivery.DeliveryStatus.UNASSIGNED,
                        )
                    messages.success(request, "Сборка завершена. Заказ передан в доставку.")
            else:
                messages.success(request, "Изменения сохранены.")
        else:
            messages.error(request, "Проверьте данные: есть ошибки в позициях.")

    context = {
        "order": order,
        "formset": formset,
        "session_form": session_form,
        "session": session,
    }
    context.update(entity_comments_context(order))
    return render(request, "orders/picker_detail.html", context)

# Create your views here.
