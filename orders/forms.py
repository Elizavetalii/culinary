from django import forms
from django.utils import timezone
from decimal import Decimal, InvalidOperation
from crm.forms import BootstrapFormMixin
from django.forms import modelformset_factory
from crm.models import Order, OrderItem, PickingSession, Dish


class OrderForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "order_number",
            "client",
            "status",
            "address",
            "delivery_date",
            "delivery_time",
            "delivery_type",
            "comments",
        ]
        widgets = {
            "delivery_date": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "delivery_time": forms.TimeInput(attrs={"type": "time"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap()
        if "order_number" in self.fields:
            self.fields["order_number"].widget.attrs.setdefault("readonly", True)
            self.fields["order_number"].required = False
            self.fields["order_number"].widget.attrs.pop("required", None)
            if not self.instance.pk and not self.instance.order_number:
                self.fields["order_number"].initial = Order.generate_order_number()
        if "status" in self.fields:
            allowed = ["Черновик", "На проверке"]
            self.fields["status"].choices = [
                (value, label)
                for value, label in self.fields["status"].choices
                if value in allowed
            ]
        if "delivery_date" in self.fields:
            min_date = timezone.localdate()
            # Не ставим min, если редактируем заказ с датой в прошлом, чтобы дата отображалась
            if not self.instance.pk or not self.instance.delivery_date or self.instance.delivery_date >= min_date:
                self.fields["delivery_date"].widget.attrs["min"] = min_date.isoformat()
            else:
                self.fields["delivery_date"].widget.attrs.pop("min", None)
            # Явный формат для value, чтобы input type=date показывал значение
            self.fields["delivery_date"].input_formats = ["%Y-%m-%d"]

    def clean(self):
        cleaned = super().clean()
        if not cleaned.get("delivery_date"):
            self.add_error("delivery_date", "Укажите дату доставки.")
        else:
            if cleaned["delivery_date"] < timezone.localdate():
                self.add_error("delivery_date", "Дата доставки не может быть в прошедшем времени.")
        if not cleaned.get("delivery_time"):
            self.add_error("delivery_time", "Укажите время доставки.")
        return cleaned


class PickingSessionForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = PickingSession
        fields = ["note"]
        labels = {"note": "Примечание сборщика"}
        widgets = {"note": forms.Textarea(attrs={"rows": 3})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap()


class OrderItemPickForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ["picked_quantity", "item_status", "item_comment", "replacement_text"]
        labels = {
            "picked_quantity": "Собрано фактически",
            "item_status": "Статус позиции",
            "item_comment": "Комментарий",
            "replacement_text": "Замена",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap()

    def clean(self):
        cleaned = super().clean()
        status = cleaned.get("item_status")
        comment = cleaned.get("item_comment", "")
        replacement = cleaned.get("replacement_text", "")
        if status == OrderItem.ItemStatus.OUT_OF_STOCK and not comment:
            self.add_error("item_comment", "Укажите причину отсутствия.")
        if status == OrderItem.ItemStatus.REPLACED and not replacement:
            self.add_error("replacement_text", "Укажите текст замены.")
        return cleaned


class OrderItemForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = [
            "dish",
            "quantity",
            "unit_price",
            "supply_type",
            "item_comment",
        ]
        labels = {
            "dish": "Блюдо",
            "quantity": "Количество",
            "unit_price": "Цена",
            "supply_type": "Тип поставки",
            "item_comment": "Комментарий",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap()
        if "dish" in self.fields:
            self.fields["dish"].queryset = Dish.objects.filter(is_active=True).order_by("name")
        if "unit_price" in self.fields:
            self.fields["unit_price"].widget.attrs.setdefault("readonly", True)
            self.fields["unit_price"].widget.attrs.setdefault("inputmode", "decimal")
            self.fields["unit_price"].widget.attrs.setdefault("step", "0.01")
        if "quantity" in self.fields:
            self.fields["quantity"].widget.attrs.setdefault("min", "1")
            self.fields["quantity"].widget.attrs.setdefault("step", "1")

    def clean(self):
        cleaned = super().clean()
        dish = cleaned.get("dish")
        qty = cleaned.get("quantity")
        if not dish:
            self.add_error("dish", "Выберите блюдо.")
        if qty is not None:
            if qty <= 0:
                self.add_error("quantity", "Количество должно быть больше 0.")
            if dish:
                scale = dish.quantity_scale or 0
                quant = Decimal("1").scaleb(-scale)
                try:
                    quantized = Decimal(qty).quantize(quant)
                except (InvalidOperation, TypeError):
                    self.add_error("quantity", "Некорректный формат количества.")
                    return cleaned
                if quantized != Decimal(qty):
                    self.add_error("quantity", f"Количество должно иметь не более {scale} знаков после запятой.")
                if dish.base_uom == Dish.BaseUom.PCS and quantized != quantized.to_integral_value():
                    self.add_error("quantity", "Для штучных блюд количество должно быть целым.")
                if dish.min_batch_qty is not None and quantized < dish.min_batch_qty:
                    self.add_error("quantity", f"Минимальная партия: {dish.min_batch_qty}.")
                if dish.batch_multiple_qty:
                    step = dish.batch_multiple_qty
                    remainder = (quantized % step) if step else Decimal("0")
                    if remainder != 0:
                        self.add_error("quantity", f"Количество должно быть кратно {step}.")
        return cleaned


OrderItemPickFormSet = modelformset_factory(
    OrderItem,
    form=OrderItemPickForm,
    extra=0,
)


OrderItemFormSet = modelformset_factory(
    OrderItem,
    form=OrderItemForm,
    extra=1,
    can_delete=True,
)
