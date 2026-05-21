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

    def test_admin_order_create_generates_order_number_when_blank(self):
        self.client.force_login(self.admin)
        delivery_day = timezone.localdate() + timedelta(days=2)

        response = self.client.post(
            "/admin-panel/entities/orders/create/",
            {
                "order_number": "",
                "client": self.client_obj.pk,
                "manager": "",
                "address": "Москва, Тверская, 1",
                "status": OrderStatus.DRAFT,
                "delivery_date": delivery_day.isoformat(),
                "delivery_time": "12:00",
                "delivery_type": "Разовая",
                "production_date": "",
                "production_shift": "",
                "production_window_start": "",
                "production_window_end": "",
                "comments": "",
                "total_amount": "0.00",
            },
        )

        self.assertEqual(response.status_code, 302)
        order = Order.objects.get(client=self.client_obj)
        self.assertRegex(order.order_number, r"^ORD-\d{8}-\d{3}$")

    def test_admin_order_form_uses_order_creation_input_masks(self):
        form_class = _entity_form_class(Order)
        form = form_class()

        self.assertFalse(form.fields["order_number"].required)
        self.assertEqual(form.fields["order_number"].widget.attrs["readonly"], True)
        self.assertEqual(form.fields["delivery_date"].widget.attrs["type"], "date")
        self.assertEqual(form.fields["production_date"].widget.attrs["type"], "date")
        self.assertEqual(form.fields["delivery_time"].widget.attrs["type"], "time")
        self.assertEqual(form.fields["production_window_start"].widget.attrs["type"], "time")
        self.assertEqual(form.fields["production_window_end"].widget.attrs["type"], "time")
        self.assertEqual(form.fields["total_amount"].widget.attrs["readonly"], True)
        self.assertEqual(form.fields["total_amount"].widget.attrs["inputmode"], "decimal")
