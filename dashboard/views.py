from urllib.parse import quote

from django.conf import settings
from django.shortcuts import render, redirect
from django.utils import timezone
from accounts.utils import role_required
from crm.models import Client, Order, Delivery, Route, RouteStatus, LogisticianProfile, Courier, CourierStatus
from reports.models import Report


@role_required("Менеджер")
def manager_dashboard(request):
    today = timezone.localdate()
    stats = {
        "clients": Client.objects.count(),
        "orders": Order.objects.count(),
        "active_orders": Order.objects.filter(
            status__in=["На проверке", "Подтвержден производством", "В производстве"]
        ).count(),
    }
    demo_stats = {
        "clients_today": Client.objects.filter(created_at__date=today).count(),
        "orders_today": Order.objects.filter(created_at__date=today).count(),
        "deliveries_today": Delivery.objects.filter(delivery_date=today).count(),
    }
    recent_clients = Client.objects.order_by("-id")[:5]
    recent_orders = Order.objects.select_related("client").order_by("-created_at")[:5]
    return render(
        request,
        "dashboard/manager.html",
        {
            "stats": stats,
            "demo_stats": demo_stats,
            "recent_clients": recent_clients,
            "recent_orders": recent_orders,
        },
    )


@role_required("Логист")
def logistic_dashboard(request):
    stats = {
        "deliveries": Delivery.objects.count(),
        "pending": Delivery.objects.filter(is_sent=False).count(),
        "couriers_total": Courier.objects.count(),
        "couriers_free": Courier.objects.filter(status=CourierStatus.FREE).count(),
        "active_cargo": Delivery.objects.exclude(
            status__in=[Delivery.DeliveryStatus.DELIVERED, Delivery.DeliveryStatus.CANCELLED]
        ).count(),
    }
    recent_deliveries = Delivery.objects.select_related("order").order_by("-id")[:5]
    active_routes = (
        Route.objects.filter(status__in=[RouteStatus.PLANNED, RouteStatus.PUBLISHED, RouteStatus.IN_PROGRESS])
        .prefetch_related("stops__delivery__order")
        .select_related("logistician")
        .order_by("planned_date")
    )
    routes_payload = []
    for route in active_routes:
        stops = sorted(route.stops.all(), key=lambda s: s.sequence_index)
        stop_points = [
            {
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
                    "address": address,
                    "lat": float(s.latitude) if s.latitude is not None else None,
                    "lng": float(s.longitude) if s.longitude is not None else None,
                    "kind": "delivery",
                }
            )
        routes_payload.append(
            {
                "id": route.id,
                "title": f"Маршрут {route.planned_date}",
                "status": route.get_status_display(),
                "stops": stop_points,
            }
        )
    profile, _ = LogisticianProfile.objects.get_or_create(user=request.user)
    return render(
        request,
        "dashboard/logistic.html",
        {
            "stats": stats,
            "recent_deliveries": recent_deliveries,
            "routes_payload": routes_payload,
            "map_prefs": profile,
        },
    )


@role_required("Сборщик заказов")
def picker_dashboard(request):
    stats = {
        "orders": Order.objects.count(),
        "in_progress": Order.objects.filter(status="В производстве").count(),
    }
    recent_orders = Order.objects.select_related("client").order_by("-created_at")[:5]
    return render(request, "dashboard/picker.html", {"stats": stats, "recent_orders": recent_orders})


@role_required("Администратор системы")
def admin_dashboard(request):
    stats = {
        "clients": Client.objects.count(),
        "orders": Order.objects.count(),
        "reports": Report.objects.count(),
    }
    return render(request, "dashboard/admin.html", {"stats": stats})

# Create your views here.
