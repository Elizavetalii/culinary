from decimal import Decimal

from django.core.management import call_command
from django.test import TestCase

from crm.models import (
    Client,
    Delivery,
    Dish,
    IngredientStock,
    Order,
    OrderItem,
    Route,
    RouteStop,
    TechCard,
)


class SeedFullQualityDemoTests(TestCase):
    def test_command_creates_connected_orders_with_dishes_and_logistics(self):
        call_command("seed_full_quality_demo", fresh=True, orders=12, verbosity=0)

        self.assertGreaterEqual(Client.objects.count(), 12)
        self.assertGreaterEqual(Dish.objects.count(), 15)
        self.assertEqual(Order.objects.count(), 12)
        self.assertGreaterEqual(TechCard.objects.count(), Dish.objects.count())
        self.assertGreater(IngredientStock.objects.count(), 0)

        for order in Order.objects.prefetch_related("items").all():
            self.assertGreaterEqual(order.items.count(), 2)
            expected_total = sum((item.line_total for item in order.items.all()), Decimal("0"))
            self.assertEqual(order.total_amount, expected_total)
            self.assertTrue(order.deliveries.exists())

        self.assertEqual(OrderItem.objects.filter(dish__isnull=False).count(), OrderItem.objects.count())
        self.assertGreaterEqual(Delivery.objects.count(), 12)
        self.assertGreaterEqual(Route.objects.count(), 2)
        self.assertGreaterEqual(RouteStop.objects.count(), 12)
