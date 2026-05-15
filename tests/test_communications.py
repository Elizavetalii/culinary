from django.test import TestCase
from django.urls import reverse

from crm.models import Client, Role, User


class CommunicationsTests(TestCase):
    def setUp(self):
        self.manager_role = Role.objects.create(name="Менеджер")
        self.sender = User.objects.create_user(
            username="sender",
            email="sender@example.com",
            password="Pass123!",
            full_name="Sender User",
        )
        self.sender.roles.add(self.manager_role)
        self.recipient = User.objects.create_user(
            username="recipient",
            email="recipient@example.com",
            password="Pass123!",
            full_name="Recipient User",
        )
        self.recipient.roles.add(self.manager_role)

    def test_direct_message_creates_unread_for_recipient(self):
        self.client.force_login(self.sender)

        response = self.client.post(
            reverse("communications-thread", args=[self.recipient.pk]),
            {"body": "Нужна сверка по заказу."},
        )

        self.assertEqual(response.status_code, 302)
        self.client.force_login(self.recipient)
        response = self.client.get(reverse("communications-unread-count"))
        self.assertEqual(response.json()["unread_count"], 1)

    def test_opening_thread_marks_incoming_messages_as_read(self):
        self.client.force_login(self.sender)
        self.client.post(
            reverse("communications-thread", args=[self.recipient.pk]),
            {"body": "Проверь доставку."},
        )

        self.client.force_login(self.recipient)
        response = self.client.get(reverse("communications-thread", args=[self.sender.pk]))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse("communications-unread-count"))
        self.assertEqual(response.json()["unread_count"], 0)

    def test_entity_comment_is_saved_for_client_card(self):
        client_obj = Client.objects.create(name="ООО Комментарии", client_type="store")
        self.client.force_login(self.sender)

        response = self.client.post(
            reverse("communications-comment-create", args=["crm", "client", client_obj.pk]),
            {"body": "Клиент просит позвонить утром."},
        )

        self.assertEqual(response.status_code, 302)
        response = self.client.get(f"/clients/{client_obj.pk}/")
        self.assertContains(response, "Клиент просит позвонить утром.")
