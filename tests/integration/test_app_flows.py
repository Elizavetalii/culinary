from datetime import timedelta
from decimal import Decimal

from django.test import TestCase
from django.utils import timezone

from crm.models import (
    Client,
    CooperationStage,
    Courier,
    CourierAssignment,
    Delivery,
    Dish,
    Ingredient,
    IngredientStock,
    InteractionType,
    Order,
    OrderItem,
    OrderStatus,
    Role,
    Route,
    RouteStatus,
    RouteStop,
    TechCard,
    TechCardComponent,
    User,
)


class AppIntegrationTests(TestCase):
    """Сквозные интеграционные проверки для основных модулей Art Culinary CRM."""

    @classmethod
    def setUpTestData(cls):
        cls.role_manager = Role.objects.create(name="Менеджер")
        cls.role_logist = Role.objects.create(name="Логист")
        cls.role_admin = Role.objects.create(name="Администратор системы")
        cls.role_picker = Role.objects.create(name="Сборщик заказов")
        cls.role_courier = Role.objects.create(name="Курьер")

        cls.manager = User.objects.create_user(
            username="manager",
            email="manager@test.local",
            password="Pass12345!",
            full_name="Manager Test",
        )
        cls.manager.roles.add(cls.role_manager)

        cls.logist = User.objects.create_user(
            username="logist",
            email="logist@test.local",
            password="Pass12345!",
            full_name="Logist Test",
        )
        cls.logist.roles.add(cls.role_logist)

        cls.admin = User.objects.create_user(
            username="admin",
            email="admin@test.local",
            password="Pass12345!",
            full_name="Admin Test",
        )
        cls.admin.roles.add(cls.role_admin)

        cls.picker = User.objects.create_user(
            username="picker",
            email="picker@test.local",
            password="Pass12345!",
            full_name="Picker Test",
        )
        cls.picker.roles.add(cls.role_picker)

        cls.courier_user = User.objects.create_user(
            username="courier",
            email="courier@test.local",
            password="Pass12345!",
            full_name="Courier Test",
        )
        cls.courier_user.roles.add(cls.role_courier)

        cls.stage = CooperationStage.objects.create(name="Переговоры", order=1, is_active=True)
        cls.client_obj = Client.objects.create(
            name="ООО Тест Клиент",
            client_type="store",
            status="active",
            current_stage=cls.stage,
            responsible_manager=cls.manager,
            default_delivery_address="Санкт-Петербург, Невский 1",
            email="client@test.local",
            phone="+79990000000",
        )

        cls.ingredient = Ingredient.objects.create(name="Картофель", is_active=True)
        IngredientStock.objects.create(ingredient=cls.ingredient, quantity=Decimal("500.000"))
        cls.dish = Dish.objects.create(
            name="Оливье",
            unit="кг",
            base_uom=Dish.BaseUom.KG,
            quantity_scale=3,
            default_price=Decimal("900.00"),
            is_active=True,
            created_by=cls.manager,
        )
        tech = TechCard.objects.create(
            dish=cls.dish,
            version_label="v1",
            is_active=True,
            approved_by=cls.manager,
        )
        TechCardComponent.objects.create(
            tech_card=tech,
            ingredient=cls.ingredient,
            quantity=Decimal("1.000"),
        )

    def _make_order(self, qty=Decimal("10.000")):
        order = Order.objects.create(
            order_number=Order.generate_order_number(),
            client=self.client_obj,
            manager=self.manager,
            address=self.client_obj.default_delivery_address,
            status=OrderStatus.REVIEW,
            delivery_date=timezone.localdate() + timedelta(days=1),
            delivery_time=timezone.localtime().time().replace(microsecond=0),
            delivery_type="Разовая",
        )
        OrderItem.objects.create(
            order=order,
            dish=self.dish,
            quantity=qty,
            unit_price=Decimal("900.00"),
        )
        order.refresh_from_db()
        return order

    def test_login_redirect_by_role(self):
        response = self.client.post(
            "/login/",
            {"username": "manager", "password": "Pass12345!"},
            follow=False,
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/dashboard/manager/")

    def test_manager_clients_pages_and_create(self):
        self.client.force_login(self.manager)
        self.assertEqual(self.client.get("/clients/").status_code, 200)
        create_resp = self.client.post(
            "/clients/create/",
            {
                "name": "ООО Новый клиент",
                "client_type": "store",
                "inn": "1234567890",
                "kpp": "123456789",
                "default_delivery_address": "",
                "address_city": "Санкт-Петербург",
                "address_street": "Литейный проспект",
                "address_house": "10",
                "address_building": "к. 2",
                "address_unit": "офис 305",
                "address_comment": "Вход со двора",
                "email": "new-client@test.local",
                "phone": "8 (999) 111-22-33",
                "status": "prospect",
                "current_stage": str(self.stage.id),
            },
            follow=False,
        )
        self.assertEqual(create_resp.status_code, 302)
        created = Client.objects.get(email="new-client@test.local")
        self.assertEqual(created.phone, "+79991112233")
        self.assertEqual(created.responsible_manager, self.manager)
        self.assertEqual(
            created.default_delivery_address,
            "Санкт-Петербург, Литейный проспект, д. 10, к. 2, офис 305. Комментарий курьеру: Вход со двора",
        )

    def test_client_create_validation_errors_keep_form_data(self):
        self.client.force_login(self.manager)
        response = self.client.post(
            "/clients/create/",
            {
                "name": "О",
                "client_type": "",
                "inn": "123abc",
                "kpp": "456",
                "default_delivery_address": "",
                "address_city": "",
                "address_street": "",
                "address_house": "",
                "address_building": "к. 1",
                "address_unit": "офис 2",
                "address_comment": "Позвонить заранее",
                "email": "bad-email",
                "phone": "+7 (999) 111-22",
                "status": "",
                "current_stage": "",
            },
            follow=False,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Название должно быть не короче 2 символов.")
        self.assertContains(response, "Выберите тип клиента.")
        self.assertContains(response, "ИНН должен содержать только цифры.")
        self.assertContains(response, "КПП должен состоять из 9 цифр.")
        self.assertContains(response, "Укажите город или населённый пункт.")
        self.assertContains(response, "Укажите улицу.")
        self.assertContains(response, "Укажите дом.")
        self.assertContains(response, "Позвонить заранее")
        self.assertContains(response, "Введите корректный email.")
        self.assertContains(response, "Введите российский номер")
        self.assertContains(response, "Выберите статус клиента.")
        self.assertContains(response, "Выберите текущий этап.")
        self.assertContains(response, "bad-email")
        self.assertFalse(Client.objects.filter(email="bad-email").exists())

    def test_client_create_rejects_numeric_address_parts(self):
        self.client.force_login(self.manager)
        response = self.client.post(
            "/clients/create/",
            {
                "name": "ООО Адрес Тест",
                "client_type": "store",
                "inn": "1234567890",
                "kpp": "123456789",
                "default_delivery_address": "",
                "address_city": "4234324",
                "address_street": "432423423",
                "address_house": "abc",
                "address_building": "!!!",
                "address_unit": "@@@",
                "address_comment": "Проверка",
                "email": "address-test@test.local",
                "phone": "+79991112233",
                "status": "prospect",
                "current_stage": str(self.stage.id),
            },
            follow=False,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Город не может состоять только из цифр")
        self.assertContains(response, "Улица не может состоять только из цифр")
        self.assertContains(response, "Дом должен содержать номер")
        self.assertContains(response, "Укажите корпус или строение")
        self.assertContains(response, "Укажите квартиру или офис")
        self.assertContains(response, "4234324")
        self.assertFalse(Client.objects.filter(email="address-test@test.local").exists())

    def test_client_create_accepts_real_address_formats(self):
        self.client.force_login(self.manager)
        response = self.client.post(
            "/clients/create/",
            {
                "name": "ООО Валидный Адрес",
                "client_type": "store",
                "inn": "1234567890",
                "kpp": "123456789",
                "default_delivery_address": "",
                "address_city": "посёлок Новинки",
                "address_street": "ул. 1905 года",
                "address_house": "12 стр 1",
                "address_building": "корп. 2",
                "address_unit": "кв. 7Б",
                "address_comment": "Позвонить за 10 минут",
                "email": "valid-address@test.local",
                "phone": "+79991112233",
                "status": "prospect",
                "current_stage": str(self.stage.id),
            },
            follow=False,
        )
        self.assertEqual(response.status_code, 302)
        created = Client.objects.get(email="valid-address@test.local")
        self.assertEqual(
            created.default_delivery_address,
            "посёлок Новинки, ул. 1905 года, д. 12 стр 1, корп. 2, кв. 7Б. Комментарий курьеру: Позвонить за 10 минут",
        )

    def test_client_create_validates_client_name_letters(self):
        self.client.force_login(self.manager)
        invalid_response = self.client.post(
            "/clients/create/",
            {
                "name": "4234324",
                "client_type": "store",
                "inn": "1234567890",
                "kpp": "123456789",
                "default_delivery_address": "",
                "address_city": "Москва",
                "address_street": "Ленина",
                "address_house": "12",
                "email": "numeric-name@test.local",
                "phone": "+79991112233",
                "status": "prospect",
                "current_stage": str(self.stage.id),
            },
            follow=False,
        )
        self.assertEqual(invalid_response.status_code, 200)
        self.assertContains(invalid_response, "Название должно содержать хотя бы одну букву.")
        self.assertFalse(Client.objects.filter(email="numeric-name@test.local").exists())

        valid_response = self.client.post(
            "/clients/create/",
            {
                "name": "Точка №5",
                "client_type": "store",
                "inn": "1234567890",
                "kpp": "123456789",
                "default_delivery_address": "",
                "address_city": "Москва",
                "address_street": "Ленина",
                "address_house": "12",
                "email": "valid-name@test.local",
                "phone": "+79991112233",
                "status": "prospect",
                "current_stage": str(self.stage.id),
            },
            follow=False,
        )
        self.assertEqual(valid_response.status_code, 302)
        self.assertTrue(Client.objects.filter(email="valid-name@test.local", name="Точка №5").exists())

    def test_client_detail_interaction_and_stage_history(self):
        self.client.force_login(self.manager)
        detail_url = f"/clients/{self.client_obj.id}/"
        response = self.client.post(
            detail_url,
            {
                "action": "add_interaction",
                "interaction-interaction_type": InteractionType.CALL,
                "interaction-note": "Созвон",
                "interaction-happened_at": timezone.localtime().strftime("%Y-%m-%dT%H:%M"),
            },
            follow=False,
        )
        self.assertEqual(response.status_code, 302)
        response2 = self.client.post(
            detail_url,
            {
                "action": "change_stage",
                "stage-stage": str(self.stage.id),
                "stage-comment": "Оставили на текущем этапе",
            },
            follow=False,
        )
        self.assertEqual(response2.status_code, 302)
        self.client_obj.refresh_from_db()
        self.assertEqual(self.client_obj.current_stage_id, self.stage.id)

    def test_order_status_flow_creates_delivery(self):
        self.client.force_login(self.manager)
        order = self._make_order()
        response = self.client.post(
            f"/orders/{order.id}/status/",
            {"status": OrderStatus.SHIPPED},
            follow=False,
        )
        self.assertEqual(response.status_code, 302)
        order.refresh_from_db()
        self.assertEqual(order.status, OrderStatus.SHIPPED)
        self.assertTrue(Delivery.objects.filter(order=order).exists())

    def test_order_archive_toggle_and_bulk_delete(self):
        self.client.force_login(self.manager)
        order1 = self._make_order()
        order2 = self._make_order()
        response = self.client.post(f"/orders/{order1.id}/archive-toggle/", follow=False)
        self.assertEqual(response.status_code, 302)
        order1.refresh_from_db()
        self.assertTrue(order1.is_archived)

        bulk = self.client.post(
            "/orders/bulk-delete/",
            {"order_ids": [str(order1.id), str(order2.id)]},
            follow=False,
        )
        self.assertEqual(bulk.status_code, 302)
        self.assertFalse(Order.objects.filter(id__in=[order1.id, order2.id]).exists())

    def test_order_item_recalculates_order_total(self):
        order = self._make_order(qty=Decimal("5.000"))
        self.assertEqual(order.total_amount, Decimal("4500.00"))
        item = order.items.first()
        item.quantity = Decimal("7.000")
        item.save()
        order.refresh_from_db()
        self.assertEqual(order.total_amount, Decimal("6300.00"))

    def test_logistics_routes_and_assignments_model_integration(self):
        order = self._make_order()
        delivery = Delivery.objects.create(
            order=order,
            address=order.address,
            status=Delivery.DeliveryStatus.PLANNED,
        )
        route = Route.objects.create(
            logistician=self.logist,
            planned_date=timezone.localdate() + timedelta(days=1),
            status=RouteStatus.PLANNED,
        )
        courier = Courier.objects.create(
            user=self.courier_user,
            transport_type="car",
            experience_years=2,
            status="Свободен",
            zone="СПб",
        )
        CourierAssignment.objects.create(courier=courier, route=route)
        RouteStop.objects.create(
            route=route,
            delivery=delivery,
            sequence_index=1,
            status=RouteStop.StopStatus.PLANNED,
        )
        delivery.route = route
        delivery.courier = courier
        delivery.save()

        self.assertEqual(route.assignments.count(), 1)
        self.assertEqual(route.stops.count(), 1)
        self.assertEqual(delivery.route_id, route.id)

    def test_logistics_pages_access_by_roles(self):
        self.client.force_login(self.logist)
        self.assertEqual(self.client.get("/logistics/").status_code, 200)
        self.assertEqual(self.client.get("/logistics/routes/").status_code, 200)
        self.assertEqual(self.client.get("/logistics/couriers/").status_code, 200)

        self.client.force_login(self.courier_user)
        self.assertEqual(self.client.get("/logistics/courier/profile/").status_code, 200)
        self.assertEqual(self.client.get("/logistics/courier/routes/").status_code, 200)

    def test_reports_pages(self):
        self.client.force_login(self.manager)
        self.assertEqual(self.client.get("/reports/").status_code, 200)
        self.assertEqual(self.client.get("/reports/analytics/").status_code, 200)

    def test_admin_panel_pages(self):
        self.client.force_login(self.admin)
        self.assertEqual(self.client.get("/admin-panel/").status_code, 200)
        self.assertEqual(self.client.get("/admin-panel/users/").status_code, 200)
        self.assertEqual(self.client.get("/admin-panel/roles/").status_code, 200)
        self.assertEqual(self.client.get("/admin-panel/access/").status_code, 200)
        self.assertEqual(self.client.get("/admin-panel/data-check/").status_code, 200)

    def test_api_endpoints_require_auth(self):
        self.assertEqual(self.client.get("/api/clients/").status_code, 401)
        self.client.force_login(self.manager)
        authed = self.client.get("/api/clients/")
        self.assertEqual(authed.status_code, 200)
