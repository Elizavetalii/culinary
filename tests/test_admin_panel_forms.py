from django.test import TestCase

from admin_panel.forms import UserUpdateForm
from admin_panel.views import _entity_form_class
from crm.models import Client, Role


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
