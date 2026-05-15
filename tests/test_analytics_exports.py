from datetime import date
from decimal import Decimal
from zipfile import ZipFile

from django.core.files.storage import default_storage
from django.test import TestCase
from django.urls import reverse

from crm.models import (
    Client,
    Delivery,
    Order,
    OrderStatus,
    Role,
    User,
    UserRole,
)
from reports.models import Report
from reports.services import build_analytics_report, create_analytics_report_file


class AnalyticsExportTests(TestCase):
    def setUp(self):
        self.admin_role = Role.objects.create(name="Администратор системы")
        self.manager_role = Role.objects.create(name="Менеджер")
        self.admin = User.objects.create_user(
            username="admin",
            email="admin@example.com",
            password="pass",
            full_name="Админ",
        )
        self.manager = User.objects.create_user(
            username="manager",
            email="manager@example.com",
            password="pass",
            full_name="Менеджер",
        )
        UserRole.objects.create(user=self.admin, role=self.admin_role)
        UserRole.objects.create(user=self.manager, role=self.manager_role)

        client = Client.objects.create(
            name="Кафе Тест",
            client_type="cafe",
            email="client@example.com",
            phone="+79991112233",
            status="active",
            responsible_manager=self.manager,
        )
        order = Order.objects.create(
            order_number="ORD-T-001",
            client=client,
            manager=self.manager,
            status=OrderStatus.SHIPPED,
            delivery_date=date(2026, 5, 13),
            total_amount=Decimal("1200.00"),
        )
        Delivery.objects.create(
            order=order,
            status=Delivery.DeliveryStatus.DELIVERED,
            delivery_date=date(2026, 5, 13),
            address="Москва, Тестовая, 1",
        )

    def test_build_admin_analytics_report_contains_sales_and_admin_sections(self):
        payload = build_analytics_report(
            scope="admin",
            period_from=date(2026, 5, 1),
            period_to=date(2026, 5, 31),
        )

        self.assertEqual(payload["summary"]["orders"], 1)
        self.assertEqual(payload["summary"]["revenue"], Decimal("1200.00"))
        self.assertEqual(payload["summary"]["users"], 2)
        self.assertEqual(payload["sections"]["orders_by_status"][0]["label"], "Отгружен")
        self.assertEqual(payload["sections"]["deliveries_by_status"][0]["value"], 1)

    def test_create_analytics_report_file_saves_all_supported_formats(self):
        for fmt in ["html", "csv", "xlsx", "pdf", "docx"]:
            with self.subTest(fmt=fmt):
                report = create_analytics_report_file(
                    scope="admin",
                    fmt=fmt,
                    period_from=date(2026, 5, 1),
                    period_to=date(2026, 5, 31),
                    user=self.admin,
                )

                self.assertEqual(report.status, "ready")
                self.assertTrue(report.file.name.endswith(f".{fmt}"))
                self.assertTrue(default_storage.exists(report.file.name))
                self.assertGreater(report.file.size, 20)

                if fmt in {"xlsx", "docx"}:
                    with report.file.open("rb") as fh:
                        with ZipFile(fh) as archive:
                            self.assertTrue(archive.namelist())

    def test_admin_analytics_export_view_creates_report_and_redirects_to_file(self):
        self.client.force_login(self.admin)

        response = self.client.get(
            reverse("admin-analytics-export"),
            {"format": "csv", "from": "2026-05-01", "to": "2026-05-31"},
        )

        self.assertEqual(response.status_code, 302)
        report = Report.objects.latest("created_at")
        self.assertIn("Административная аналитика", report.title)
        self.assertTrue(report.file.name.endswith(".csv"))

    def test_admin_analytics_page_renders(self):
        self.client.force_login(self.admin)

        response = self.client.get(reverse("admin-analytics"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Административная аналитика")
        self.assertContains(response, "Сформировать отчёт")

    def test_manager_analytics_export_view_creates_manager_report(self):
        self.client.force_login(self.manager)

        response = self.client.get(
            reverse("reports-analytics-export"),
            {"format": "html", "from": "2026-05-01", "to": "2026-05-31"},
        )

        self.assertEqual(response.status_code, 302)
        report = Report.objects.latest("created_at")
        self.assertIn("Менеджерская аналитика", report.title)
        self.assertTrue(report.file.name.endswith(".html"))

    def test_manager_analytics_page_renders_export_menu(self):
        self.client.force_login(self.manager)

        response = self.client.get(reverse("reports-analytics"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Сформировать отчёт")
        self.assertContains(response, "XLSX")
