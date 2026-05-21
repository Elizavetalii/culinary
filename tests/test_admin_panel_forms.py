from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from admin_panel.forms import UserUpdateForm
from admin_panel.views import _entity_form_class
from crm.models import Client, Order, OrderStatus, Role, User, UserRole


class AdminPanelValidationTests(TestCase):
    def setUp(self):
        self.role = Role.objects.create(name="Менеджер")

    def test_user_update_form_normalizes_russian_phone(self):
        form = UserUpdateForm(
            data={
                "email": "manager@example.com",
                "full_name": "Иван Петров",
                "phone": "8 (999) 111-22-33",
                "is_active": "on",
                "roles": [self.role.pk],
            }
        )

        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["phone"], "+79991112233")

    def test_user_update_form_rejects_invalid_phone(self):
        form = UserUpdateForm(
            data={
                "email": "manager@example.com",
                "full_name": "Иван Петров",
                "phone": "+1 999 111-22-33",
                "is_active": "on",
                "roles": [self.role.pk],
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("Введите российский номер", str(form.errors["phone"]))

    def test_generic_client_form_validates_shared_fields(self):
        form_class = _entity_form_class(Client)
        form = form_class(
            data={
                "name": "ООО Админ",
                "client_type": "store",
                "inn": "123abc",
                "kpp": "123",
                "default_delivery_address": "Москва, Тверская, д. 1",
                "email": "bad-email",
                "phone": "+1 999 111-22-33",
                "status": "prospect",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("ИНН должен содержать только цифры.", form.errors["inn"])
        self.assertIn("КПП должен состоять из 9 цифр.", form.errors["kpp"])
        self.assertIn("Введите корректный email.", form.errors["email"])
        self.assertIn("Введите российский номер", str(form.errors["phone"]))

    def test_generic_client_form_normalizes_russian_phone(self):
        form_class = _entity_form_class(Client)
        form = form_class(
            data={
                "name": "ООО Админ",
                "client_type": "store",
                "inn": "7701000001",
                "kpp": "770101001",
                "default_delivery_address": "Москва, Тверская, д. 1",
                "email": "admin-client@example.com",
                "phone": "8 (999) 111-22-33",
                "status": "prospect",
            }
        )

        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["phone"], "+79991112233")


class AdminPanelOrderCreateTests(TestCase):
    def setUp(self):
        self.admin_role = Role.objects.create(name="Администратор системы")
        self.admin = User.objects.create_user(
            username="admin",
            email="admin@example.com",
            password="pass12345",
            full_name="Admin User",
        )
        UserRole.objects.create(user=self.admin, role=self.admin_role)
        self.client_obj = Client.objects.create(name="ООО Админский клиент")

    def test_admin_panel_order_create_uses_business_order_form(self):
        self.client.force_login(self.admin)

        response = self.client.get("/admin-panel/entities/orders/create/")

        self.assertRedirects(response, "/orders/create/")

    def test_admin_order_create_page_has_items_and_hides_internal_fields(self):
        self.client.force_login(self.admin)

        response = self.client.get("/admin-panel/entities/orders/create/", follow=True)

        self.assertContains(response, "Позиции заказа")
        self.assertContains(response, 'type="date"')
        self.assertContains(response, 'type="time"')
        self.assertNotContains(response, "Смена")
        self.assertNotContains(response, "Окно производства")
        self.assertNotContains(response, "Сумма итого")

    def test_admin_panel_order_edit_uses_business_order_form(self):
        self.client.force_login(self.admin)
        order = Order.objects.create(
            order_number=Order.generate_order_number(),
            client=self.client_obj,
            status=OrderStatus.DRAFT,
            delivery_date=timezone.localdate() + timedelta(days=2),
        )

        response = self.client.get(f"/admin-panel/entities/orders/{order.pk}/edit/")

        self.assertRedirects(response, f"/orders/{order.pk}/edit/")
