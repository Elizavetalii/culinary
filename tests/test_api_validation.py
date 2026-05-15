from django.test import TestCase

from crm.api import ClientContactSerializer, ClientSerializer, UserSerializer
from crm.models import Client, User


class ApiValidationTests(TestCase):
    def test_client_serializer_rejects_invalid_shared_fields(self):
        serializer = ClientSerializer(
            data={
                "name": "ООО API",
                "client_type": "store",
                "inn": "123abc",
                "kpp": "123",
                "default_delivery_address": "Москва, Тверская, д. 1",
                "email": "bad-email",
                "phone": "+1 999 111-22-33",
                "status": "prospect",
            }
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("inn", serializer.errors)
        self.assertIn("kpp", serializer.errors)
        self.assertIn("email", serializer.errors)
        self.assertIn("phone", serializer.errors)

    def test_client_serializer_normalizes_russian_phone(self):
        serializer = ClientSerializer(
            data={
                "name": "ООО API",
                "client_type": "store",
                "inn": "7701000001",
                "kpp": "770101001",
                "default_delivery_address": "Москва, Тверская, д. 1",
                "email": "api-client@example.com",
                "phone": "8 (999) 111-22-33",
                "status": "prospect",
            }
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)
        client = serializer.save()
        self.assertEqual(client.phone, "+79991112233")

    def test_user_serializer_normalizes_russian_phone(self):
        serializer = UserSerializer(
            data={
                "username": "api-user",
                "full_name": "API User",
                "email": "api-user@example.com",
                "phone": "8 (999) 111-22-33",
                "is_active": True,
                "is_staff": False,
            }
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertEqual(user.phone, "+79991112233")

    def test_client_contact_serializer_rejects_invalid_phone(self):
        client = Client.objects.create(name="ООО API", client_type="store")
        serializer = ClientContactSerializer(
            data={
                "client": client.pk,
                "full_name": "Иван",
                "position": "",
                "phone": "+1 999 111-22-33",
                "email": "contact@example.com",
                "is_primary": True,
            }
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("phone", serializer.errors)
