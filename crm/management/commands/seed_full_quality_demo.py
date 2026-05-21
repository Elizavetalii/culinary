import random
from collections import defaultdict
from datetime import time
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from crm.models import (
    Client,
    ClientAllowedTechCard,
    ClientContact,
    ClientStageHistory,
    ClientType,
    CooperationStage,
    Courier,
    CourierAssignment,
    CourierStatus,
    Delivery,
    Dish,
    DishEquipmentRequirement,
    Equipment,
    EquipmentReservation,
    Ingredient,
    IngredientReservation,
    IngredientStock,
    Interaction,
    InteractionType,
    LogisticianProfile,
    Order,
    OrderItem,
    OrderStatus,
    PickingSession,
    ProductionReservation,
    Role,
    Route,
    RouteStatus,
    RouteStop,
    TechCard,
    TechCardComponent,
    TechCardVariant,
    UserRole,
)
from reports.models import Report


class Command(BaseCommand):
    help = "Создаёт полноценную качественную демо-БД: клиенты, блюда, заказы, позиции, производство и логистика."

    def add_arguments(self, parser):
        parser.add_argument(
            "--fresh",
            action="store_true",
            help="Очистить бизнес-данные и демо-пользователей перед наполнением. Суперпользователи сохраняются.",
        )
        parser.add_argument("--orders", type=int, default=80, help="Количество заказов для создания.")
        parser.add_argument("--clients", type=int, default=24, help="Количество клиентов для создания.")

    @transaction.atomic
    def handle(self, *args, **options):
        random.seed(42)
        today = timezone.localdate()
        order_count = max(1, options["orders"])
        client_count = max(4, options["clients"])

        if options["fresh"]:
            self._clear_demo_data()

        roles = self._create_roles()
        users = self._create_users(roles)
        stages = self._create_stages()
        ingredients = self._create_ingredients()
        dishes = self._create_dishes(ingredients, users["manager"])
        equipment = self._create_equipment(dishes)
        clients = self._create_clients(client_count, stages, users["manager"])
        self._allow_client_tech_cards(clients, dishes)
        orders = self._create_orders(order_count, clients, dishes, users, today)
        deliveries = self._create_deliveries(orders, users["couriers"], today)
        self._create_routes(deliveries, users["logistician"], today)
        self._create_reservations(orders, ingredients, equipment, today)
        self._create_reports(users["manager"], today)

        self.stdout.write(
            self.style.SUCCESS(
                "Готово: создана полноценная демо-БД "
                f"({Client.objects.count()} клиентов, {Dish.objects.count()} блюд, "
                f"{Order.objects.count()} заказов, {OrderItem.objects.count()} позиций)."
            )
        )

    def _clear_demo_data(self):
        RouteStop.objects.all().delete()
        CourierAssignment.objects.all().delete()
        Delivery.objects.all().delete()
        PickingSession.objects.all().delete()
        OrderItem.objects.all().delete()
        IngredientReservation.objects.all().delete()
        EquipmentReservation.objects.all().delete()
        ProductionReservation.objects.all().delete()
        Order.objects.all().delete()
        Report.objects.all().delete()
        Interaction.objects.all().delete()
        ClientStageHistory.objects.all().delete()
        ClientContact.objects.all().delete()
        ClientAllowedTechCard.objects.all().delete()
        Client.objects.all().delete()
        Route.objects.all().delete()
        Courier.objects.all().delete()
        LogisticianProfile.objects.all().delete()
        TechCardComponent.objects.all().delete()
        TechCardVariant.objects.all().delete()
        TechCard.objects.all().delete()
        DishEquipmentRequirement.objects.all().delete()
        Equipment.objects.all().delete()
        IngredientStock.objects.all().delete()
        Dish.objects.all().delete()
        Ingredient.objects.all().delete()
        UserRole.objects.all().delete()
        get_user_model().objects.filter(is_superuser=False).delete()

    def _create_roles(self):
        role_names = {
            "manager": "Менеджер",
            "logistician": "Логист",
            "picker": "Сборщик заказов",
            "admin": "Администратор системы",
            "courier": "Курьер",
        }
        return {key: Role.objects.get_or_create(name=name)[0] for key, name in role_names.items()}

    def _create_users(self, roles):
        User = get_user_model()
        specs = [
            ("manager_quality", "Елена Морозова", "manager@artculinary.local", "ManagerDemo123!", roles["manager"]),
            ("logistic_quality", "Антон Соколов", "logistic@artculinary.local", "LogisticDemo123!", roles["logistician"]),
            ("picker_quality", "Наталья Орлова", "picker@artculinary.local", "PickerDemo123!", roles["picker"]),
            ("admin_quality", "Ирина Кузнецова", "admin.demo@artculinary.local", "AdminDemo123!", roles["admin"]),
        ]
        users = {}
        for username, full_name, email, password, role in specs:
            user, _ = User.objects.update_or_create(
                username=username,
                defaults={
                    "email": email,
                    "full_name": full_name,
                    "is_active": True,
                    "is_staff": role == roles["admin"],
                    "is_superuser": False,
                },
            )
            user.set_password(password)
            user.save()
            UserRole.objects.get_or_create(user=user, role=role)
            users[username.split("_")[0]] = user

        LogisticianProfile.objects.update_or_create(
            user=users["logistic"],
            defaults={
                "region": "Москва и МО",
                "city": "Москва",
                "transport_types": ["car", "van", "refrigerated"],
                "timezone": "Europe/Moscow",
                "map_show_traffic": True,
            },
        )

        courier_specs = [
            ("courier_quality_01", "Алексей Смирнов", "Авто", "Центр", 450, 4),
            ("courier_quality_02", "Мария Волкова", "Фургон", "Север", 900, 9),
            ("courier_quality_03", "Дмитрий Орлов", "Рефрижератор", "Запад", 1200, 12),
            ("courier_quality_04", "Ольга Белова", "Фургон", "Юг", 800, 8),
            ("courier_quality_05", "Павел Егоров", "Авто", "Восток", 500, 5),
        ]
        couriers = []
        for index, (username, full_name, transport, zone, weight, volume) in enumerate(courier_specs, start=1):
            user, _ = User.objects.update_or_create(
                username=username,
                defaults={
                    "email": f"{username}@artculinary.local",
                    "full_name": full_name,
                    "is_active": True,
                },
            )
            user.set_password("CourierDemo123!")
            user.save()
            UserRole.objects.get_or_create(user=user, role=roles["courier"])
            courier, _ = Courier.objects.update_or_create(
                user=user,
                defaults={
                    "transport_type": transport,
                    "experience_years": 2 + index,
                    "zone": zone,
                    "status": [CourierStatus.FREE, CourierStatus.BUSY, CourierStatus.ON_ROUTE][index % 3],
                    "payload_capacity_kg": Decimal(weight),
                    "cargo_volume_m3": Decimal(volume),
                    "cargo_length_cm": Decimal("260"),
                    "cargo_width_cm": Decimal("160"),
                    "cargo_height_cm": Decimal("150"),
                    "max_weight": Decimal(weight),
                    "max_volume": Decimal(volume),
                    "current_lat": Decimal("55.75") + Decimal(index) / Decimal("1000"),
                    "current_lng": Decimal("37.60") + Decimal(index) / Decimal("1000"),
                    "current_latitude": Decimal("55.75") + Decimal(index) / Decimal("1000"),
                    "current_longitude": Decimal("37.60") + Decimal(index) / Decimal("1000"),
                    "location_updated_at": timezone.now(),
                },
            )
            couriers.append(courier)
        users["couriers"] = couriers
        users["manager"] = users["manager"]
        users["logistician"] = users["logistic"]
        users["picker"] = users["picker"]
        return users

    def _create_stages(self):
        specs = [
            ("Первичный контакт", 1),
            ("Дегустация", 2),
            ("Коммерческое предложение", 3),
            ("Договор", 4),
            ("Регулярные поставки", 5),
        ]
        return [CooperationStage.objects.update_or_create(name=name, defaults={"order": order, "is_active": True})[0] for name, order in specs]

    def _create_ingredients(self):
        names = [
            "Куриное филе",
            "Говядина",
            "Лосось",
            "Креветки",
            "Рис",
            "Паста",
            "Картофель",
            "Морковь",
            "Томаты",
            "Огурцы",
            "Салат ромэн",
            "Шампиньоны",
            "Творог",
            "Мука",
            "Молоко",
            "Яйцо",
            "Сливки",
            "Пармезан",
            "Оливковое масло",
            "Соус фирменный",
            "Булгур",
            "Индейка",
            "Свекла",
            "Тыква",
            "Зелень",
        ]
        ingredients = {}
        for index, name in enumerate(names, start=1):
            ingredient, _ = Ingredient.objects.update_or_create(name=name, defaults={"is_active": True})
            IngredientStock.objects.update_or_create(
                ingredient=ingredient,
                defaults={"quantity": Decimal("1200.000") + Decimal(index * 37)},
            )
            ingredients[name] = ingredient
        return ingredients

    def _create_dishes(self, ingredients, manager):
        dish_specs = [
            ("Цезарь с курицей", "порция", "pcs", "0.280", "480.00", [("Куриное филе", "0.100"), ("Салат ромэн", "0.070"), ("Пармезан", "0.020"), ("Соус фирменный", "0.040")]),
            ("Паста болоньезе", "порция", "pcs", "0.360", "540.00", [("Паста", "0.180"), ("Говядина", "0.110"), ("Томаты", "0.060"), ("Пармезан", "0.010")]),
            ("Ризотто с грибами", "порция", "pcs", "0.340", "510.00", [("Рис", "0.130"), ("Шампиньоны", "0.100"), ("Сливки", "0.050"), ("Пармезан", "0.020")]),
            ("Лосось с булгуром", "порция", "pcs", "0.330", "920.00", [("Лосось", "0.180"), ("Булгур", "0.110"), ("Оливковое масло", "0.020"), ("Зелень", "0.010")]),
            ("Индейка с овощами", "порция", "pcs", "0.370", "620.00", [("Индейка", "0.190"), ("Морковь", "0.070"), ("Огурцы", "0.050"), ("Зелень", "0.010")]),
            ("Том Ям с креветками", "порция", "pcs", "0.420", "690.00", [("Креветки", "0.090"), ("Томаты", "0.060"), ("Шампиньоны", "0.060"), ("Сливки", "0.050")]),
            ("Оливье премиум", "кг", "kg", "1.000", "980.00", [("Картофель", "0.260"), ("Морковь", "0.120"), ("Яйцо", "0.080"), ("Соус фирменный", "0.120")]),
            ("Винегрет печеный", "кг", "kg", "1.000", "620.00", [("Свекла", "0.320"), ("Картофель", "0.220"), ("Морковь", "0.140"), ("Оливковое масло", "0.040")]),
            ("Тыквенный крем-суп", "порция", "pcs", "0.380", "360.00", [("Тыква", "0.240"), ("Сливки", "0.060"), ("Морковь", "0.030"), ("Зелень", "0.010")]),
            ("Куриные котлеты", "кг", "kg", "1.000", "840.00", [("Куриное филе", "0.700"), ("Яйцо", "0.060"), ("Мука", "0.080"), ("Молоко", "0.050")]),
            ("Сырники ванильные", "порция", "pcs", "0.240", "310.00", [("Творог", "0.160"), ("Мука", "0.030"), ("Яйцо", "0.030"), ("Молоко", "0.020")]),
            ("Боул с лососем", "порция", "pcs", "0.390", "790.00", [("Лосось", "0.120"), ("Рис", "0.140"), ("Огурцы", "0.060"), ("Соус фирменный", "0.030")]),
            ("Боул с индейкой", "порция", "pcs", "0.400", "650.00", [("Индейка", "0.150"), ("Рис", "0.130"), ("Томаты", "0.060"), ("Огурцы", "0.050")]),
            ("Плов с курицей", "кг", "kg", "1.000", "790.00", [("Куриное филе", "0.300"), ("Рис", "0.520"), ("Морковь", "0.120"), ("Оливковое масло", "0.040")]),
            ("Салат греческий", "кг", "kg", "1.000", "760.00", [("Огурцы", "0.280"), ("Томаты", "0.280"), ("Зелень", "0.050"), ("Оливковое масло", "0.050")]),
            ("Ланч офисный куриный", "порция", "pcs", "0.520", "580.00", [("Куриное филе", "0.160"), ("Рис", "0.160"), ("Огурцы", "0.060"), ("Томаты", "0.060")]),
            ("Ланч офисный рыбный", "порция", "pcs", "0.500", "720.00", [("Лосось", "0.150"), ("Булгур", "0.150"), ("Огурцы", "0.060"), ("Соус фирменный", "0.030")]),
            ("Паста с креветками", "порция", "pcs", "0.350", "740.00", [("Паста", "0.170"), ("Креветки", "0.100"), ("Сливки", "0.050"), ("Пармезан", "0.020")]),
        ]
        dishes = []
        for index, (name, unit, base_uom, weight, price, components) in enumerate(dish_specs, start=1):
            dish, _ = Dish.objects.update_or_create(
                name=name,
                defaults={
                    "unit": unit,
                    "base_uom": base_uom,
                    "quantity_scale": 3 if base_uom == "kg" else 0,
                    "is_active": True,
                    "created_by": manager,
                    "unit_weight_kg": Decimal(weight),
                    "min_batch_qty": Decimal("3.000") if base_uom == "kg" else Decimal("10.000"),
                    "batch_multiple_qty": Decimal("1.000"),
                    "daily_capacity": Decimal("80.000") + Decimal(index * 12),
                    "default_price": Decimal(price),
                },
            )
            tech_card, _ = TechCard.objects.update_or_create(
                dish=dish,
                version_label="1.0",
                defaults={
                    "description": f"Стандартизированная техкарта Art Culinary для позиции «{name}».",
                    "is_active": True,
                    "approved_by": manager,
                },
            )
            TechCardVariant.objects.update_or_create(
                tech_card=tech_card,
                quantity=Decimal("1.000"),
                defaults={"note": "Основной выход готового продукта"},
            )
            for ingredient_name, qty in components:
                TechCardComponent.objects.update_or_create(
                    tech_card=tech_card,
                    ingredient=ingredients[ingredient_name],
                    defaults={"quantity": Decimal(qty), "note": "Норма на единицу выпуска"},
                )
            dishes.append(dish)
        return dishes

    def _create_equipment(self, dishes):
        specs = [
            ("Пароконвектомат Rational", "85.00", "14.00"),
            ("Котёл варочный 150 л", "110.00", "12.00"),
            ("Шоковый охладитель", "70.00", "10.00"),
            ("Линия фасовки", "160.00", "16.00"),
        ]
        equipment = []
        for name, capacity, hours in specs:
            item, _ = Equipment.objects.update_or_create(
                name=name,
                defaults={"capacity_per_hour": Decimal(capacity), "available_hours": Decimal(hours)},
            )
            equipment.append(item)
        for index, dish in enumerate(dishes):
            DishEquipmentRequirement.objects.update_or_create(
                dish=dish,
                equipment=equipment[index % len(equipment)],
                defaults={"minutes_per_unit": Decimal("2.50") + Decimal(index % 4)},
            )
        return equipment

    def _create_clients(self, client_count, stages, manager):
        names = [
            "Ресторан Красная Площадь",
            "Кафе Тверская 7",
            "Гастробар Новый Арбат",
            "Бистро Кутузовский",
            "Маркет Ленинградский",
            "Кулинария Большая Дмитровка",
            "Кафе Мясницкая 24",
            "Ресторан Пятницкая",
            "Магазин Земляной Вал",
            "Офисный центр Пресня",
            "Столовая БЦ Савёловский",
            "Ресторан Сретенка",
            "Кафе Покровка",
            "Маркет Даниловский",
            "Корнер Арбат Фудхолл",
            "Кафе Хамовники",
            "Ресторан Замоскворечье",
            "Мини-маркет Бауманский",
            "БЦ Павелецкий Плаза",
            "Кейтеринг Сити",
            "Кафе Аэропорт",
            "Маркет Хорошёвский",
            "Ресторан Раменки",
            "Столовая Технопарк",
        ]
        addresses = [
            "Москва, Красная площадь, 1",
            "Москва, Тверская улица, 7",
            "Москва, Новый Арбат, 15",
            "Москва, Кутузовский проспект, 2/1",
            "Москва, Ленинградский проспект, 36",
            "Москва, Большая Дмитровка, 11",
            "Москва, Мясницкая улица, 24",
            "Москва, Пятницкая улица, 25",
            "Москва, Земляной Вал, 33",
            "Москва, Пресненская набережная, 12",
        ]
        type_cycle = [ClientType.RESTAURANT, ClientType.CAFE, ClientType.STORE, ClientType.OTHER]
        clients = []
        for index in range(client_count):
            name = names[index % len(names)]
            client, _ = Client.objects.update_or_create(
                name=name,
                defaults={
                    "client_type": type_cycle[index % len(type_cycle)],
                    "inn": f"7701{index + 1:06d}",
                    "kpp": f"7701{index + 1:05d}",
                    "default_delivery_address": addresses[index % len(addresses)],
                    "email": f"client{index + 1:02d}@artculinary.local",
                    "phone": f"+7 495 10{index + 1:02d}-{20 + index:02d}-{30 + index:02d}",
                    "status": "active" if index % 5 else "prospect",
                    "current_stage": stages[min(index % len(stages), len(stages) - 1)],
                    "responsible_manager": manager,
                    "daily_max_weight_kg": Decimal("80.00") + Decimal(index * 8),
                    "daily_min_qty": Decimal("10.00") + Decimal(index % 6),
                    "guaranteed_volume_kg": Decimal("120.00") + Decimal(index * 10),
                },
            )
            ClientContact.objects.update_or_create(
                client=client,
                email=f"buyer{index + 1:02d}@artculinary.local",
                defaults={
                    "full_name": f"{['Анна', 'Ирина', 'Олег', 'Мария'][index % 4]} {['Петрова', 'Соколова', 'Ильин', 'Ким'][index % 4]}",
                    "position": "Руководитель закупок",
                    "phone": f"+7 916 20{index + 1:02d}-{40 + index:02d}-{50 + index:02d}",
                    "is_primary": True,
                },
            )
            ClientStageHistory.objects.update_or_create(
                client=client,
                stage=client.current_stage,
                defaults={"changed_by": manager, "comment": "Качественная демо-БД: актуальный этап сотрудничества"},
            )
            Interaction.objects.update_or_create(
                client=client,
                manager=manager,
                interaction_type=InteractionType.CALL,
                defaults={"note": "Согласованы ассортимент, график поставок и условия оплаты."},
            )
            clients.append(client)
        return clients

    def _allow_client_tech_cards(self, clients, dishes):
        tech_cards = list(TechCard.objects.filter(dish__in=dishes))
        for client in clients:
            for tech_card in tech_cards[:12]:
                ClientAllowedTechCard.objects.get_or_create(client=client, tech_card=tech_card)

    def _create_orders(self, order_count, clients, dishes, users, today):
        orders = []
        statuses = [
            OrderStatus.REVIEW,
            OrderStatus.CONFIRMED,
            OrderStatus.IN_PRODUCTION,
            OrderStatus.READY_TO_SHIP,
            OrderStatus.SHIPPED,
        ]
        supply_types = ["Основная поставка", "Добор", "Регулярный контракт", "Срочная заявка"]
        for index in range(order_count):
            client = clients[index % len(clients)]
            delivery_date = today + timezone.timedelta(days=index % 14)
            production_date = delivery_date - timezone.timedelta(days=1)
            order, _ = Order.objects.update_or_create(
                order_number=f"AC-{today.strftime('%Y%m')}-{index + 1:04d}",
                defaults={
                    "client": client,
                    "manager": users["manager"],
                    "address": client.default_delivery_address,
                    "status": statuses[index % len(statuses)],
                    "delivery_date": delivery_date,
                    "delivery_time": time(hour=8 + (index % 8), minute=(index * 10) % 60),
                    "delivery_type": ["Регулярная", "Разовая", "Срочная"][index % 3],
                    "production_date": production_date,
                    "production_shift": "День" if index % 3 else "Ночь",
                    "production_window_start": time(hour=6 if index % 3 else 22, minute=0),
                    "production_window_end": time(hour=14 if index % 3 else 6, minute=0),
                    "comments": "Полноценная демо-БД: заказ содержит блюда, производство и доставку.",
                },
            )
            OrderItem.objects.filter(order=order).delete()
            chosen_dishes = [dishes[(index + offset) % len(dishes)] for offset in range(2 + index % 5)]
            for item_index, dish in enumerate(chosen_dishes, start=1):
                if dish.base_uom == "kg":
                    qty = Decimal(5 + ((index + item_index) % 9))
                else:
                    qty = Decimal(12 + ((index * 3 + item_index) % 35))
                item_status = [
                    OrderItem.ItemStatus.NOT_STARTED,
                    OrderItem.ItemStatus.IN_PROGRESS,
                    OrderItem.ItemStatus.DONE,
                ][index % 3]
                OrderItem.objects.create(
                    order=order,
                    dish=dish,
                    custom_tech_card=dish.tech_cards.filter(is_active=True).first(),
                    quantity=qty,
                    unit_price=dish.default_price or Decimal("0.00"),
                    supply_type=supply_types[(index + item_index) % len(supply_types)],
                    picked_quantity=qty if item_status == OrderItem.ItemStatus.DONE else Decimal("0.000"),
                    item_status=item_status,
                    item_comment="Плановая позиция заказа",
                )
            PickingSession.objects.update_or_create(
                order=order,
                defaults={
                    "picker": users["picker"],
                    "note": "Сборка по маршрутному листу",
                    "started_at": timezone.now() if index % 3 else None,
                    "finished_at": timezone.now() if index % 5 == 0 else None,
                },
            )
            order.refresh_from_db()
            orders.append(order)
        return orders

    def _create_deliveries(self, orders, couriers, today):
        deliveries = []
        statuses = [
            Delivery.DeliveryStatus.PLANNED,
            Delivery.DeliveryStatus.ON_ROUTE,
            Delivery.DeliveryStatus.DELIVERED,
            Delivery.DeliveryStatus.UNASSIGNED,
        ]
        for index, order in enumerate(orders):
            weight = sum(
                (item.quantity * (item.dish.unit_weight_kg or Decimal("0.300")) for item in order.items.select_related("dish")),
                Decimal("0"),
            )
            planned_at = timezone.make_aware(
                timezone.datetime.combine(
                    order.delivery_date or today,
                    order.delivery_time or time(hour=10, minute=0),
                )
            )
            delivery, _ = Delivery.objects.update_or_create(
                order=order,
                defaults={
                    "courier": couriers[index % len(couriers)],
                    "status": statuses[index % len(statuses)],
                    "planned_at": planned_at,
                    "departure_time": planned_at - timezone.timedelta(minutes=45) if index % 4 else None,
                    "delivered_at": planned_at + timezone.timedelta(minutes=30) if statuses[index % len(statuses)] == Delivery.DeliveryStatus.DELIVERED else None,
                    "delivery_date": order.delivery_date,
                    "address": order.address,
                    "note": "Доставка сформирована из полного демо-заказа",
                    "is_sent": index % 4 != 3,
                    "cargo_weight_kg": weight.quantize(Decimal("0.01")),
                    "cargo_volume_m3": (weight / Decimal("180")).quantize(Decimal("0.01")),
                    "cargo_length_cm": Decimal("60"),
                    "cargo_width_cm": Decimal("40"),
                    "cargo_height_cm": Decimal("35"),
                },
            )
            deliveries.append(delivery)
        return deliveries

    def _create_routes(self, deliveries, logistician, today):
        grouped = defaultdict(list)
        for delivery in deliveries:
            grouped[delivery.delivery_date or today].append(delivery)

        coordinates = [
            (Decimal("55.753930"), Decimal("37.620795")),
            (Decimal("55.760186"), Decimal("37.609543")),
            (Decimal("55.752815"), Decimal("37.592934")),
            (Decimal("55.749806"), Decimal("37.566734")),
            (Decimal("55.789742"), Decimal("37.557214")),
            (Decimal("55.762484"), Decimal("37.612799")),
            (Decimal("55.764799"), Decimal("37.637010")),
            (Decimal("55.740821"), Decimal("37.627093")),
        ]
        for date, date_deliveries in grouped.items():
            for route_index, chunk_start in enumerate(range(0, len(date_deliveries), 8), start=1):
                chunk = date_deliveries[chunk_start : chunk_start + 8]
                route = Route.objects.create(
                    logistician=logistician,
                    planned_date=date,
                    status=[RouteStatus.PLANNED, RouteStatus.PUBLISHED, RouteStatus.IN_PROGRESS][route_index % 3],
                    max_duration_minutes=420,
                    soft_limit_stops=8,
                    strict_mode=False,
                    notes=f"Качественный демо-маршрут {date} #{route_index}",
                )
                if chunk and chunk[0].courier:
                    CourierAssignment.objects.get_or_create(route=route, courier=chunk[0].courier)
                for stop_index, delivery in enumerate(chunk, start=1):
                    delivery.route = route
                    delivery.save(update_fields=["route"])
                    lat, lng = coordinates[(chunk_start + stop_index) % len(coordinates)]
                    RouteStop.objects.create(
                        route=route,
                        delivery=delivery,
                        sequence_index=stop_index,
                        planned_time=delivery.planned_at,
                        actual_time=delivery.delivered_at,
                        service_time_minutes=12 + stop_index,
                        note=f"Точка {stop_index}: {delivery.address}",
                        status=RouteStop.StopStatus.DONE if delivery.delivered_at else RouteStop.StopStatus.PLANNED,
                        delivery_date=delivery.delivery_date,
                        latitude=lat,
                        longitude=lng,
                    )

    def _create_reservations(self, orders, ingredients, equipment, today):
        ingredient_list = list(ingredients.values())
        for order in orders:
            weight = sum(
                (item.quantity * (item.dish.unit_weight_kg or Decimal("0.300")) for item in order.items.select_related("dish")),
                Decimal("0"),
            )
            ProductionReservation.objects.update_or_create(
                order=order,
                production_date=order.production_date or today,
                defaults={"weight_kg": weight.quantize(Decimal("0.001"))},
            )
            for ingredient in ingredient_list[:6]:
                IngredientReservation.objects.update_or_create(
                    order=order,
                    ingredient=ingredient,
                    production_date=order.production_date or today,
                    defaults={"quantity": (weight / Decimal("20")).quantize(Decimal("0.001"))},
                )
            for item in equipment[:2]:
                EquipmentReservation.objects.update_or_create(
                    order=order,
                    equipment=item,
                    production_date=order.production_date or today,
                    defaults={"hours": (weight / Decimal("120")).quantize(Decimal("0.01"))},
                )

    def _create_reports(self, manager, today):
        specs = [
            ("Продажи по клиентам за месяц", "ready"),
            ("Загрузка производства на неделю", "ready"),
            ("Логистика: маршруты и SLA", "draft"),
        ]
        for index, (title, status) in enumerate(specs):
            Report.objects.update_or_create(
                title=title,
                defaults={
                    "period_from": today - timezone.timedelta(days=30 - index * 5),
                    "period_to": today + timezone.timedelta(days=index * 3),
                    "status": status,
                    "created_by": manager,
                },
            )
