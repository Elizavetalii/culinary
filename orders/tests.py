from datetime import date, timedelta

from django.test import TestCase
from django.utils import timezone

from crm.models import Client, Dish, Order, OrderItem, OrderStatus, User
from orders.forms import OrderForm, OrderItemForm
from orders.views import _get_reserved_qty_map


class OrderFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="manager1",
            email="manager1@example.com",
            password="pass12345",
            full_name="Manager One",
        )
        self.client_obj = Client.objects.create(name="Test Client")

    def test_order_number_not_required(self):
        future_day = date.today() + timedelta(days=7)
        form = OrderForm(
            data={
                "order_number": "",
                "client": self.client_obj.id,
                "status": OrderStatus.DRAFT,
                "address": "Test address",
                "delivery_date": future_day.isoformat(),
                "delivery_time": "10:00",
                "delivery_type": "Разовая",
                "comments": "",
                "total_amount": "0.00",
            }
        )
        self.assertTrue(form.is_valid())

    def test_delivery_date_time_required(self):
        form = OrderForm(
            data={
                "order_number": "",
                "client": self.client_obj.id,
                "status": OrderStatus.DRAFT,
                "address": "Test address",
                "delivery_date": "",
                "delivery_time": "",
                "delivery_type": "Разовая",
                "comments": "",
                "total_amount": "0.00",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("delivery_date", form.errors)
        self.assertIn("delivery_time", form.errors)

    def test_delivery_date_cannot_be_in_past(self):
        past_day = date.today() - timedelta(days=1)
        form = OrderForm(
            data={
                "order_number": "",
                "client": self.client_obj.id,
                "status": OrderStatus.DRAFT,
                "address": "Test address",
                "delivery_date": past_day.isoformat(),
                "delivery_time": "10:00",
                "delivery_type": "Разовая",
                "comments": "",
                "total_amount": "0.00",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("delivery_date", form.errors)


class OrderItemFormTests(TestCase):
    def setUp(self):
        self.dish = Dish.objects.create(name="Тест блюдо", unit="шт", daily_capacity=100, default_price=10)

    def test_quantity_must_be_integer(self):
        form = OrderItemForm(data={"dish": self.dish.id, "quantity": 0, "unit_price": "10.00"})
        self.assertFalse(form.is_valid())
        form = OrderItemForm(data={"dish": self.dish.id, "quantity": 1.5, "unit_price": "10.00"})
        self.assertFalse(form.is_valid())
        form = OrderItemForm(data={"dish": self.dish.id, "quantity": 2, "unit_price": "10.00"})
        self.assertTrue(form.is_valid())


class ReservedQtyTests(TestCase):
    def setUp(self):
        self.client_obj = Client.objects.create(name="Test Client")
        self.dish = Dish.objects.create(name="Котлета", unit="шт", daily_capacity=100, default_price=50)

    def test_reserved_qty_excludes_statuses_and_order(self):
        day = timezone.localdate() + timedelta(days=7)
        order1 = Order.objects.create(
            order_number="ORD-001",
            client=self.client_obj,
            status=OrderStatus.CONFIRMED,
            delivery_date=day,
        )
        OrderItem.objects.create(order=order1, dish=self.dish, quantity=5, unit_price=50)

        order2 = Order.objects.create(
            order_number="ORD-002",
            client=self.client_obj,
            status=OrderStatus.CANCELLED,
            delivery_date=day,
        )
        OrderItem.objects.create(order=order2, dish=self.dish, quantity=7, unit_price=50)

        order3 = Order.objects.create(
            order_number="ORD-003",
            client=self.client_obj,
            status=OrderStatus.IN_PRODUCTION,
            delivery_date=day,
        )
        OrderItem.objects.create(order=order3, dish=self.dish, quantity=9, unit_price=50)

        reserved = _get_reserved_qty_map(day)
        self.assertEqual(reserved.get(self.dish.id), 14)

        reserved_excluding = _get_reserved_qty_map(day, exclude_order_id=order3.id)
        self.assertEqual(reserved_excluding.get(self.dish.id), 5)

    def test_reserved_qty_uses_production_date_when_it_differs_from_delivery_date(self):
        production_day = timezone.localdate() + timedelta(days=7)
        delivery_day = production_day + timedelta(days=1)
        order = Order.objects.create(
            order_number="ORD-004",
            client=self.client_obj,
            status=OrderStatus.CONFIRMED,
            delivery_date=delivery_day,
            production_date=production_day,
        )
        OrderItem.objects.create(order=order, dish=self.dish, quantity=6, unit_price=50)

        reserved = _get_reserved_qty_map(production_day)

        self.assertEqual(reserved.get(self.dish.id), 6)
