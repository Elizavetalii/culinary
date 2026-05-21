from django.test import TestCase, override_settings
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile

from crm.models import (
    Role,
    User,
    Client,
    Order,
    Delivery,
    Route,
    RouteStop,
    Courier,
    CourierAssignment,
    RouteStatus,
)
from logistics.forms import DeliveryForm


class LogisticsRulesTests(TestCase):
    def setUp(self):
        self.logist_role = Role.objects.create(name="Логист")
        self.courier_role = Role.objects.create(name="Курьер")
        self.logist = User.objects.create_user(
            username="logist",
            password="Pass123!",
            email="logist@test.com",
            full_name="Логист",
        )
        self.logist.roles.add(self.logist_role)
        self.courier_user = User.objects.create_user(
            username="courier",
            password="Pass123!",
            email="courier@test.com",
            full_name="Курьер",
        )
        self.courier_user.roles.add(self.courier_role)
        self.courier = Courier.objects.create(user=self.courier_user, status="Свободен")

        self.client_obj = Client.objects.create(name="Test", client_type="store")
        self.order = Order.objects.create(
            order_number="ORD-1",
            client=self.client_obj,
            status="confirmed",
            address="Москва",
            total_amount=1000,
        )

    def test_cannot_add_stop_with_different_date(self):
        route = Route.objects.create(planned_date=timezone.now().date(), logistician=self.logist)
        delivery = Delivery.objects.create(
            order=self.order,
            status="Запланировано",
            planned_at=timezone.now() + timezone.timedelta(days=1),
        )
        self.client.force_login(self.logist)
        response = self.client.post(
            f"/logistics/routes/{route.id}/",
            {"action": "add_stop", "stop-delivery": delivery.id, "stop-status": "Запланирована"},
        )
        self.assertEqual(response.status_code, 400)

    def test_publish_blocked_by_duration(self):
        route = Route.objects.create(
            planned_date=timezone.now().date(),
            logistician=self.logist,
            max_duration_minutes=10,
        )
        CourierAssignment.objects.create(route=route, courier=self.courier)
        delivery = Delivery.objects.create(
            order=self.order,
            status="Запланировано",
            planned_at=timezone.now(),
            cargo_weight_kg=10,
            cargo_volume_m3=1,
        )
        RouteStop.objects.create(
            route=route,
            delivery=delivery,
            sequence_index=1,
            service_time_minutes=30,
            status="Запланирована",
            latitude=55.8,
            longitude=37.6,
        )
        self.client.force_login(self.logist)
        response = self.client.post(f"/logistics/routes/{route.id}/", {"action": "publish_route"})
        self.assertEqual(response.status_code, 400)

    def test_courier_cannot_deliver_without_proof(self):
        route = Route.objects.create(
            planned_date=timezone.now().date(),
            logistician=self.logist,
            status=RouteStatus.PUBLISHED,
        )
        CourierAssignment.objects.create(route=route, courier=self.courier)
        delivery = Delivery.objects.create(
            order=self.order,
            status="Запланировано",
            planned_at=timezone.now(),
        )
        stop = RouteStop.objects.create(
            route=route,
            delivery=delivery,
            sequence_index=1,
            status="Запланирована",
        )
        self.client.force_login(self.courier_user)
        response = self.client.post(f"/logistics/courier/stops/{stop.id}/proof/", {"status": "Доставлено"})
        self.assertEqual(response.status_code, 400)

        file = SimpleUploadedFile("proof.pdf", b"test", content_type="application/pdf")
        response = self.client.post(
            f"/logistics/courier/stops/{stop.id}/proof/",
            {"proof_of_delivery": file, "status": "Доставлено"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], f"/logistics/courier/routes/{route.id}/")

    @override_settings(LOGISTICS_MAX_PROOF_SIZE_MB=1)
    def test_courier_proof_size_is_limited(self):
        route = Route.objects.create(
            planned_date=timezone.now().date(),
            logistician=self.logist,
            status=RouteStatus.PUBLISHED,
        )
        CourierAssignment.objects.create(route=route, courier=self.courier)
        delivery = Delivery.objects.create(
            order=self.order,
            status="Запланировано",
            planned_at=timezone.now(),
        )
        stop = RouteStop.objects.create(
            route=route,
            delivery=delivery,
            sequence_index=1,
            status="Запланирована",
        )
        self.client.force_login(self.courier_user)
        file = SimpleUploadedFile("proof.pdf", b"x" * (1024 * 1024 + 1), content_type="application/pdf")
        response = self.client.post(
            f"/logistics/courier/stops/{stop.id}/proof/",
            {"proof_of_delivery": file, "status": "Доставлено"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, "Файл слишком большой", status_code=400)

    def test_delivery_form_exposes_all_statuses_checked_by_clean(self):
        form = DeliveryForm()
        values = {value for value, _ in form.fields["status"].choices}

        self.assertIn("Не назначено", values)
        self.assertIn("Запланировано", values)
        self.assertIn("В пути", values)
        self.assertIn("Доставлено", values)
        self.assertIn("Отменено", values)
