from datetime import date, time, timedelta

from django.test import TestCase
from django.utils import timezone

from crm.models import (
    Client,
    Dish,
    Ingredient,
    IngredientReservation,
    IngredientStock,
    Order,
    OrderItem,
    OrderStatus,
    ProductionReservation,
    Role,
    TechCard,
    TechCardComponent,
    User,
    UserRole,
)
from orders.forms import OrderForm, OrderItemForm
from orders.views import _apply_production_fields, _get_reserved_qty_map, _reserve_resources, _validate_order_capacity


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


class OrderReservationTests(TestCase):
    def setUp(self):
        self.client_obj = Client.objects.create(name="Test Client")
        self.dish = Dish.objects.create(
            name="Котлета",
            unit="шт",
            daily_capacity=100,
            default_price=50,
            unit_weight_kg=1,
        )
        self.ingredient = Ingredient.objects.create(name="Фарш")
        IngredientStock.objects.create(ingredient=self.ingredient, quantity=100)
        self.tech_card = TechCard.objects.create(dish=self.dish, version_label="1", is_active=True)
        TechCardComponent.objects.create(
            tech_card=self.tech_card,
            ingredient=self.ingredient,
            quantity=2,
        )

    def test_review_order_does_not_create_resource_reservations(self):
        day = timezone.localdate() + timedelta(days=2)
        order = Order.objects.create(
            order_number="ORD-REVIEW",
            client=self.client_obj,
            status=OrderStatus.REVIEW,
            delivery_date=day,
            delivery_time=time(12, 0),
        )
        _apply_production_fields(order)
        order.save()
        OrderItem.objects.create(
            order=order,
            dish=self.dish,
            custom_tech_card=self.tech_card,
            quantity=3,
            unit_price=50,
        )

        _reserve_resources(order)

        self.assertFalse(ProductionReservation.objects.filter(order=order).exists())
        self.assertFalse(IngredientReservation.objects.filter(order=order).exists())

    def test_confirmed_order_creates_resource_reservations(self):
        day = timezone.localdate() + timedelta(days=2)
        order = Order.objects.create(
            order_number="ORD-CONFIRMED",
            client=self.client_obj,
            status=OrderStatus.CONFIRMED,
            delivery_date=day,
            delivery_time=time(12, 0),
        )
        _apply_production_fields(order)
        order.save()
        OrderItem.objects.create(
            order=order,
            dish=self.dish,
            custom_tech_card=self.tech_card,
            quantity=3,
            unit_price=50,
        )

        _reserve_resources(order)

        self.assertEqual(ProductionReservation.objects.filter(order=order).count(), 1)
        reservation = IngredientReservation.objects.get(order=order, ingredient=self.ingredient)
        self.assertEqual(reservation.quantity, 6)

    def test_morning_delivery_today_is_rejected_instead_of_saving_past_production_date(self):
        today = timezone.localdate()
        form = OrderForm(
            data={
                "order_number": "",
                "client": self.client_obj.id,
                "status": OrderStatus.DRAFT,
                "address": "Test address",
                "delivery_date": today.isoformat(),
                "delivery_time": "09:00",
                "delivery_type": "Разовая",
                "comments": "",
                "total_amount": "0.00",
            }
        )
        self.assertTrue(form.is_valid())
        order = form.save(commit=False)
        _apply_production_fields(order)
        errors, warnings, info = _validate_order_capacity(order, [])

        self.assertLess(order.production_date, today)
        self.assertTrue(any("Дата производства" in err for err in errors))


class OrderCreateFlowTests(TestCase):
    def setUp(self):
        self.role = Role.objects.create(name="Менеджер")
        self.user = User.objects.create_user(
            username="manager2",
            email="manager2@example.com",
            password="pass12345",
            full_name="Manager Two",
        )
        UserRole.objects.create(user=self.user, role=self.role)
        self.client_obj = Client.objects.create(name="Test Client")
        self.dish = Dish.objects.create(name="Котлета", unit="шт", daily_capacity=100, default_price=50)
        self.ingredient = Ingredient.objects.create(name="Фарш")
        IngredientStock.objects.create(ingredient=self.ingredient, quantity=100)
        self.tech_card = TechCard.objects.create(dish=self.dish, version_label="1", is_active=True)
        TechCardComponent.objects.create(
            tech_card=self.tech_card,
            ingredient=self.ingredient,
            quantity=2,
        )

    def test_create_order_saves_review_without_resource_reservations(self):
        self.client.force_login(self.user)
        day = timezone.localdate() + timedelta(days=2)

        response = self.client.post(
            "/orders/create/",
            {
                "order_number": "",
                "client": self.client_obj.id,
                "status": OrderStatus.DRAFT,
                "address": "Test address",
                "delivery_date": day.isoformat(),
                "delivery_time": "12:00",
                "delivery_type": "Разовая",
                "comments": "",
                "total_amount": "0.00",
                "form-TOTAL_FORMS": "1",
                "form-INITIAL_FORMS": "0",
                "form-MIN_NUM_FORMS": "0",
                "form-MAX_NUM_FORMS": "1000",
                "form-0-dish": self.dish.id,
                "form-0-quantity": "3",
                "form-0-unit_price": "50.00",
                "form-0-supply_type": "",
                "form-0-item_comment": "",
            },
        )

        self.assertEqual(response.status_code, 302)
        order = Order.objects.get(client=self.client_obj)
        self.assertEqual(order.status, OrderStatus.REVIEW)
        self.assertFalse(ProductionReservation.objects.filter(order=order).exists())
        self.assertFalse(IngredientReservation.objects.filter(order=order).exists())

    def test_create_order_rejects_quantity_above_available_max(self):
        self.client.force_login(self.user)
        day = timezone.localdate() + timedelta(days=2)

        response = self.client.post(
            "/orders/create/",
            {
                "order_number": "",
                "client": self.client_obj.id,
                "status": OrderStatus.DRAFT,
                "address": "Test address",
                "delivery_date": day.isoformat(),
                "delivery_time": "12:00",
                "delivery_type": "Разовая",
                "comments": "",
                "total_amount": "0.00",
                "form-TOTAL_FORMS": "1",
                "form-INITIAL_FORMS": "0",
                "form-MIN_NUM_FORMS": "0",
                "form-MAX_NUM_FORMS": "1000",
                "form-0-dish": self.dish.id,
                "form-0-quantity": "51",
                "form-0-unit_price": "50.00",
                "form-0-supply_type": "",
                "form-0-item_comment": "",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Order.objects.filter(client=self.client_obj).exists())
        self.assertContains(response, "максимально можно добавить")

    def test_availability_uses_previous_production_date_for_morning_delivery(self):
        self.client.force_login(self.user)
        production_day = timezone.localdate() + timedelta(days=2)
        delivery_day = production_day + timedelta(days=1)
        order = Order.objects.create(
            order_number="ORD-MORNING",
            client=self.client_obj,
            status=OrderStatus.CONFIRMED,
            delivery_date=delivery_day,
            delivery_time=time(9, 0),
            production_date=production_day,
        )
        OrderItem.objects.create(order=order, dish=self.dish, quantity=7, unit_price=50)

        response = self.client.get(
            "/api/orders/availability/",
            {"delivery_date": delivery_day.isoformat(), "delivery_time": "09:00"},
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["production_date"], production_day.isoformat())
        dish_payload = next(item for item in payload["dishes"] if item["dish_id"] == self.dish.id)
        self.assertEqual(dish_payload["reserved_qty"], 7)
        self.assertEqual(dish_payload["max_order_qty"], 50)
        self.assertEqual(dish_payload["max_by_ingredients"], 50)

    def test_edit_order_renders_existing_item_hidden_id(self):
        self.client.force_login(self.user)
        day = timezone.localdate() + timedelta(days=2)
        order = Order.objects.create(
            order_number=Order.generate_order_number(),
            client=self.client_obj,
            status=OrderStatus.REVIEW,
            delivery_date=day,
            delivery_time=time(12, 0),
        )
        item = OrderItem.objects.create(order=order, dish=self.dish, quantity=3, unit_price=50)

        response = self.client.get(f"/orders/{order.pk}/edit/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'name="form-0-id" value="{item.pk}"')

    def test_edit_order_updates_existing_item(self):
        self.client.force_login(self.user)
        day = timezone.localdate() + timedelta(days=2)
        order = Order.objects.create(
            order_number=Order.generate_order_number(),
            client=self.client_obj,
            status=OrderStatus.REVIEW,
            address="Old address",
            delivery_date=day,
            delivery_time=time(12, 0),
        )
        item = OrderItem.objects.create(order=order, dish=self.dish, quantity=3, unit_price=50)

        response = self.client.post(
            f"/orders/{order.pk}/edit/",
            {
                "order_number": order.order_number,
                "client": self.client_obj.id,
                "status": OrderStatus.REVIEW,
                "address": "Updated address",
                "delivery_date": day.isoformat(),
                "delivery_time": "13:30",
                "delivery_type": "Разовая",
                "comments": "Updated comment",
                "form-TOTAL_FORMS": "1",
                "form-INITIAL_FORMS": "1",
                "form-MIN_NUM_FORMS": "0",
                "form-MAX_NUM_FORMS": "1000",
                "form-0-id": item.pk,
                "form-0-dish": self.dish.id,
                "form-0-quantity": "5",
                "form-0-unit_price": "50.00",
                "form-0-supply_type": "",
                "form-0-item_comment": "",
            },
        )

        self.assertEqual(response.status_code, 302)
        order.refresh_from_db()
        item.refresh_from_db()
        self.assertEqual(order.address, "Updated address")
        self.assertEqual(order.delivery_time, time(13, 30))
        self.assertEqual(item.quantity, 5)
        self.assertEqual(order.items.count(), 1)

    def test_picker_order_detail_renders_existing_item_hidden_id(self):
        picker_role = Role.objects.create(name="Сборщик заказов")
        picker = User.objects.create_user(
            username="picker2",
            email="picker2@example.com",
            password="pass12345",
            full_name="Picker Two",
        )
        UserRole.objects.create(user=picker, role=picker_role)
        self.client.force_login(picker)
        day = timezone.localdate() + timedelta(days=2)
        order = Order.objects.create(
            order_number=Order.generate_order_number(),
            client=self.client_obj,
            status=OrderStatus.CONFIRMED,
            delivery_date=day,
            delivery_time=time(12, 0),
        )
        item = OrderItem.objects.create(order=order, dish=self.dish, quantity=3, unit_price=50)

        response = self.client.get(f"/orders/picker/{order.pk}/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'name="form-0-id" value="{item.pk}"')
