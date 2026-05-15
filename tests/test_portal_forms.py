from django.test import SimpleTestCase

from portal.forms import ClientForm


class PortalClientFormValidationTests(SimpleTestCase):
    def valid_data(self, **overrides):
        data = {
            "name": "ООО Портал",
            "client_type": "store",
            "inn": "7701000001",
            "kpp": "770101001",
            "default_delivery_address": "Москва, Тверская, д. 1",
            "email": "portal@example.com",
            "phone": "8 (999) 111-22-33",
            "status": "prospect",
        }
        data.update(overrides)
        return data

    def test_normalizes_russian_phone(self):
        form = ClientForm(data=self.valid_data(phone="8 (999) 111-22-33"))

        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["phone"], "+79991112233")

    def test_rejects_invalid_phone(self):
        form = ClientForm(data=self.valid_data(phone="+1 999 111-22-33"))

        self.assertFalse(form.is_valid())
        self.assertIn("phone", form.errors)
        self.assertIn("Введите российский номер", str(form.errors["phone"]))

    def test_rejects_invalid_inn_and_kpp(self):
        form = ClientForm(data=self.valid_data(inn="123abc", kpp="123"))

        self.assertFalse(form.is_valid())
        self.assertIn("ИНН должен содержать только цифры.", form.errors["inn"])
        self.assertIn("КПП должен состоять из 9 цифр.", form.errors["kpp"])

    def test_rejects_invalid_email_with_project_message(self):
        form = ClientForm(data=self.valid_data(email="bad-email"))

        self.assertFalse(form.is_valid())
        self.assertIn("Введите корректный email.", form.errors["email"])

    def test_formats_existing_phone_for_display(self):
        form = ClientForm(instance=ClientForm.Meta.model(phone="+79991112233"))

        self.assertEqual(form.initial["phone"], "+7 (999) 111-22-33")
