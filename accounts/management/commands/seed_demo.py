from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from decimal import Decimal
from crm.models import (
    Role,
    UserRole,
    Client,
    CooperationStage,
    ClientStageHistory,
    Interaction,
    Order,
    Delivery,
    Courier,
    CourierAssignment,
    CourierStatus,
    LogisticianProfile,
    OrderStatus,
    InteractionType,
    Route,
    RouteStatus,
    RouteStop,
)
from reports.models import Report


class Command(BaseCommand):
    help = "Создаёт демо-данные для CRM"

    def handle(self, *args, **options):
        User = get_user_model()
        today = timezone.localdate()
        base_dt = timezone.now().replace(hour=10, minute=0, second=0, microsecond=0)

        roles = [
            "Менеджер",
            "Логист",
            "Сборщик заказов",
            "Администратор системы",
            "Курьер",
        ]
        role_map = {}
        for name in roles:
            role, _ = Role.objects.get_or_create(name=name)
            role_map[name] = role

        users_data = [
            ("manager_demo", "Менеджер", "ManagerDemo123!", "manager@art.com"),
            ("logistic_demo", "Логист", "LogisticDemo123!", "logistic@art.com"),
            ("picker_demo", "Сборщик заказов", "PickerDemo123!", "picker@art.com"),
            ("admin_demo", "Администратор системы", "AdminDemo123!", "admin@art.com"),
        ]
        users = {}
        for username, role_name, password, email in users_data:
            user, _ = User.objects.get_or_create(
                username=username,
                defaults={"email": email, "full_name": role_name, "is_active": True},
            )
            user.set_password(password)
            user.save()
            UserRole.objects.get_or_create(user=user, role=role_map[role_name])
            users[role_name] = user

        LogisticianProfile.objects.update_or_create(
            user=users["Логист"],
            defaults={
                "region": "Москва",
                "city": "Москва",
                "transport_types": ["car", "van", "refrigerated"],
                "timezone": "Europe/Moscow",
            },
        )

        stages = [
            ("Лид", 1),
            ("Переговоры", 2),
            ("Контракт", 3),
            ("Сделка", 4),
        ]
        stage_objs = []
        for name, order in stages:
            s, _ = CooperationStage.objects.get_or_create(name=name, defaults={"order": order, "is_active": True})
            stage_objs.append(s)

        demo_points = [
            {
                "client": "Ресторан «Красная Площадь»",
                "type": "restaurant",
                "address": "Москва, Красная площадь, 1",
                "street": "Красная площадь",
                "house": "1",
                "lat": "55.753930",
                "lng": "37.620795",
            },
            {
                "client": "Кафе «Тверская 7»",
                "type": "cafe",
                "address": "Москва, Тверская улица, 7",
                "street": "Тверская улица",
                "house": "7",
                "lat": "55.760186",
                "lng": "37.609543",
            },
            {
                "client": "Гастробар «Новый Арбат»",
                "type": "restaurant",
                "address": "Москва, Новый Арбат, 15",
                "street": "Новый Арбат",
                "house": "15",
                "lat": "55.752815",
                "lng": "37.592934",
            },
            {
                "client": "Бистро «Кутузовский»",
                "type": "cafe",
                "address": "Москва, Кутузовский проспект, 2/1",
                "street": "Кутузовский проспект",
                "house": "2/1",
                "lat": "55.749806",
                "lng": "37.566734",
            },
            {
                "client": "Маркет «Ленинградский»",
                "type": "store",
                "address": "Москва, Ленинградский проспект, 36",
                "street": "Ленинградский проспект",
                "house": "36",
                "lat": "55.789742",
                "lng": "37.557214",
            },
            {
                "client": "Кулинария «Большая Дмитровка»",
                "type": "store",
                "address": "Москва, Большая Дмитровка, 11",
                "street": "Большая Дмитровка",
                "house": "11",
                "lat": "55.762484",
                "lng": "37.612799",
            },
            {
                "client": "Кафе «Мясницкая 24»",
                "type": "cafe",
                "address": "Москва, Мясницкая улица, 24",
                "street": "Мясницкая улица",
                "house": "24",
                "lat": "55.764799",
                "lng": "37.637010",
            },
            {
                "client": "Ресторан «Пятницкая»",
                "type": "restaurant",
                "address": "Москва, Пятницкая улица, 25",
                "street": "Пятницкая улица",
                "house": "25",
                "lat": "55.740821",
                "lng": "37.627093",
            },
            {
                "client": "Магазин «Земляной Вал»",
                "type": "store",
                "address": "Москва, Земляной Вал, 33",
                "street": "Земляной Вал",
                "house": "33",
                "lat": "55.757557",
                "lng": "37.659548",
            },
            {
                "client": "Офисный центр «Пресня»",
                "type": "other",
                "address": "Москва, Пресненская набережная, 12",
                "street": "Пресненская набережная",
                "house": "12",
                "lat": "55.749451",
                "lng": "37.536924",
            },
        ]
        clients = []
        for i, point in enumerate(demo_points, start=1):
            c, _ = Client.objects.update_or_create(
                name=point["client"],
                defaults={
                    "client_type": point["type"],
                    "inn": f"77010000{i:02d}",
                    "kpp": f"77010{i:04d}",
                    "default_delivery_address": point["address"],
                    "phone": f"+799900010{i:02d}",
                    "email": f"demo-client-{i}@artculinary.local",
                    "status": "active" if i % 3 else "prospect",
                    "responsible_manager": users["Менеджер"],
                    "current_stage": stage_objs[min(i - 1, len(stage_objs) - 1)],
                },
            )
            clients.append(c)
            ClientStageHistory.objects.update_or_create(
                client=c,
                stage=c.current_stage,
                defaults={"changed_by": users["Менеджер"], "comment": "Демо-клиент: московская точка доставки"},
            )

        for c in clients:
            Interaction.objects.update_or_create(
                client=c,
                manager=users["Менеджер"],
                interaction_type=InteractionType.CALL,
                defaults={"note": "Демо: согласование регулярных поставок", "happened_at": timezone.now()},
            )

        orders = []
        statuses = [
            OrderStatus.REVIEW,
            OrderStatus.CONFIRMED,
            OrderStatus.IN_PRODUCTION,
            OrderStatus.READY_TO_SHIP,
            OrderStatus.SHIPPED,
        ]
        for idx, (client, point) in enumerate(zip(clients, demo_points), start=1):
            order, _ = Order.objects.update_or_create(
                order_number=f"ORD-DEMO-MSK-{idx:02d}",
                defaults={
                    "client": client,
                    "manager": users["Менеджер"],
                    "status": statuses[(idx - 1) % len(statuses)],
                    "address": point["address"],
                    "delivery_date": today,
                    "delivery_time": (base_dt + timezone.timedelta(minutes=idx * 25)).time(),
                    "delivery_type": "Разовая" if idx % 2 else "Регулярная",
                    "total_amount": Decimal("18000.00") + Decimal(idx * 1750),
                    "comments": "DEMO_MOSCOW_LOGISTICS",
                },
            )
            orders.append(order)

        courier_data = [
            {
                "username": "courier_demo",
                "email": "courier@art.com",
                "full_name": "Алексей Смирнов",
                "transport_type": "Авто",
                "status": CourierStatus.ON_ROUTE,
                "payload": "450",
                "volume": "4.5",
                "lat": "55.755864",
                "lng": "37.617698",
                "zone": "Центр",
            },
            {
                "username": "courier_demo_van",
                "email": "courier.van@art.com",
                "full_name": "Мария Волкова",
                "transport_type": "Фургон",
                "status": CourierStatus.FREE,
                "payload": "900",
                "volume": "9.0",
                "lat": "55.751244",
                "lng": "37.618423",
                "zone": "Центр-Север",
            },
            {
                "username": "courier_demo_ref",
                "email": "courier.ref@art.com",
                "full_name": "Дмитрий Орлов",
                "transport_type": "Рефрижератор",
                "status": CourierStatus.BUSY,
                "payload": "1200",
                "volume": "12.0",
                "lat": "55.760186",
                "lng": "37.609543",
                "zone": "Центр",
            },
        ]
        couriers = []
        User.objects.filter(username="courier_demo_walk").delete()
        Courier.objects.filter(transport_type__iregex=r"bike|velo|вело|велосипед|пеш|самокат").update(
            transport_type="Авто",
            payload_capacity_kg=Decimal("450"),
            cargo_volume_m3=Decimal("4.5"),
            max_weight=Decimal("450"),
            max_volume=Decimal("4.5"),
        )
        for data in courier_data:
            courier_user, _ = User.objects.update_or_create(
                username=data["username"],
                defaults={"email": data["email"], "full_name": data["full_name"], "is_active": True},
            )
            courier_user.set_password("CourierDemo123!")
            courier_user.save()
            UserRole.objects.get_or_create(user=courier_user, role=role_map["Курьер"])
            courier, _ = Courier.objects.update_or_create(
                user=courier_user,
                defaults={
                    "transport_type": data["transport_type"],
                    "experience_years": 3,
                    "zone": data["zone"],
                    "status": data["status"],
                    "payload_capacity_kg": Decimal(data["payload"]),
                    "cargo_volume_m3": Decimal(data["volume"]),
                    "cargo_length_cm": Decimal("220"),
                    "cargo_width_cm": Decimal("140"),
                    "cargo_height_cm": Decimal("140"),
                    "max_weight": Decimal(data["payload"]),
                    "max_volume": Decimal(data["volume"]),
                    "current_lat": Decimal(data["lat"]),
                    "current_lng": Decimal(data["lng"]),
                    "current_latitude": Decimal(data["lat"]),
                    "current_longitude": Decimal(data["lng"]),
                    "location_updated_at": timezone.now(),
                },
            )
            couriers.append(courier)

        delivery_statuses = [
            Delivery.DeliveryStatus.PLANNED,
            Delivery.DeliveryStatus.ON_ROUTE,
            Delivery.DeliveryStatus.PLANNED,
            Delivery.DeliveryStatus.DELIVERED,
            Delivery.DeliveryStatus.PLANNED,
            Delivery.DeliveryStatus.ON_ROUTE,
            Delivery.DeliveryStatus.PLANNED,
            Delivery.DeliveryStatus.PLANNED,
            Delivery.DeliveryStatus.DELIVERED,
            Delivery.DeliveryStatus.PLANNED,
        ]
        deliveries = []
        for idx, (order, point) in enumerate(zip(orders, demo_points), start=1):
            delivery, _ = Delivery.objects.update_or_create(
                order=order,
                defaults={
                    "courier": couriers[(idx - 1) % len(couriers)],
                    "planned_at": base_dt + timezone.timedelta(minutes=idx * 25),
                    "delivery_date": today,
                    "address": point["address"],
                    "status": delivery_statuses[idx - 1],
                    "cargo_weight_kg": Decimal("18.0") + Decimal(idx * 3),
                    "cargo_volume_m3": Decimal("0.40") + Decimal(idx) / Decimal("10"),
                    "cargo_length_cm": Decimal("60"),
                    "cargo_width_cm": Decimal("40"),
                    "cargo_height_cm": Decimal("35"),
                    "note": "DEMO_MOSCOW_LOGISTICS",
                },
            )
            deliveries.append(delivery)

        stop_statuses = [
            RouteStop.StopStatus.PLANNED,
            RouteStop.StopStatus.IN_PROGRESS,
            RouteStop.StopStatus.PLANNED,
            RouteStop.StopStatus.DONE,
            RouteStop.StopStatus.PLANNED,
            RouteStop.StopStatus.IN_PROGRESS,
            RouteStop.StopStatus.PLANNED,
            RouteStop.StopStatus.PLANNED,
            RouteStop.StopStatus.DONE,
            RouteStop.StopStatus.PLANNED,
        ]
        Route.objects.filter(notes__startswith="DEMO_MOSCOW_ROUTE").delete()
        route_specs = [
            {
                "notes": "DEMO_MOSCOW_ROUTE_CENTER",
                "title": "Центр Москвы",
                "indexes": [0, 1, 5],
                "courier": couriers[0],
                "status": RouteStatus.IN_PROGRESS,
                "start_minutes": 20,
            },
            {
                "notes": "DEMO_MOSCOW_ROUTE_NORTH",
                "title": "Северный маршрут",
                "indexes": [4, 6, 8],
                "courier": couriers[1],
                "status": RouteStatus.PUBLISHED,
                "start_minutes": 35,
            },
            {
                "notes": "DEMO_MOSCOW_ROUTE_WEST",
                "title": "Запад и деловой центр",
                "indexes": [2, 3, 7, 9],
                "courier": couriers[2],
                "status": RouteStatus.PUBLISHED,
                "start_minutes": 50,
            },
        ]
        for route_spec in route_specs:
            route = Route.objects.create(
                planned_date=today,
                logistician=users["Логист"],
                status=route_spec["status"],
                max_duration_minutes=360,
                soft_limit_stops=5,
                strict_mode=False,
                notes=route_spec["notes"],
            )
            CourierAssignment.objects.get_or_create(route=route, courier=route_spec["courier"])
            for sequence, point_idx in enumerate(route_spec["indexes"], start=1):
                delivery = deliveries[point_idx]
                point = demo_points[point_idx]
                delivery.route = route
                delivery.courier = route_spec["courier"]
                delivery.planned_at = base_dt + timezone.timedelta(minutes=route_spec["start_minutes"] + sequence * 25)
                delivery.delivery_date = today
                delivery.save(update_fields=["route", "courier", "planned_at", "delivery_date"])
                RouteStop.objects.create(
                    route=route,
                    delivery=delivery,
                    sequence_index=sequence,
                    planned_time=base_dt + timezone.timedelta(minutes=route_spec["start_minutes"] + sequence * 25),
                    status=stop_statuses[point_idx],
                    delivery_date=today,
                    service_time_minutes=12,
                    note=f"{route_spec['title']}: {point['street']}, дом {point['house']}",
                    latitude=Decimal(point["lat"]),
                    longitude=Decimal(point["lng"]),
                )

        Report.objects.get_or_create(
            title="Отчёт по продажам",
            defaults={
                "period_from": timezone.now().date(),
                "period_to": timezone.now().date(),
                "status": "ready",
                "created_by": users["Менеджер"],
            },
        )

        self.stdout.write(self.style.SUCCESS("Демо-данные созданы: 3 маршрута от склада по Москве готовы."))
