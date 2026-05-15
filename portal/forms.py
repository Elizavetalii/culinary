from django import forms
from crm.models import Client, Order, Delivery, Courier
from crm.validators import (
    format_russian_phone_for_display,
    normalize_russian_phone,
    validate_inn,
    validate_kpp,
    validate_optional_email,
)


class ClientForm(forms.ModelForm):
    error_messages = {
        "inn_digits": "ИНН должен содержать только цифры.",
        "inn_length": "ИНН должен состоять из 10 или 12 цифр.",
        "kpp_digits": "КПП должен содержать только цифры.",
        "kpp_length": "КПП должен состоять из 9 цифр.",
        "email_invalid": "Введите корректный email.",
        "phone_invalid": "Введите российский номер в формате +7 (999) 123-45-67.",
    }

    class Meta:
        model = Client
        fields = [
            "name",
            "client_type",
            "inn",
            "kpp",
            "default_delivery_address",
            "email",
            "phone",
            "status",
        ]
        labels = {
            "name": "Название / ФИО",
            "client_type": "Тип клиента",
            "inn": "ИНН",
            "kpp": "КПП",
            "default_delivery_address": "Адрес доставки",
            "email": "Электронная почта",
            "phone": "Телефон",
            "status": "Статус",
        }
        widgets = {
            "inn": forms.TextInput(attrs={"inputmode": "numeric", "maxlength": "12", "pattern": r"\d{10}|\d{12}"}),
            "kpp": forms.TextInput(attrs={"inputmode": "numeric", "maxlength": "9", "pattern": r"\d{9}"}),
            "email": forms.EmailInput(attrs={"autocomplete": "email"}),
            "phone": forms.TextInput(
                attrs={
                    "placeholder": "+7 (___) ___-__-__",
                    "autocomplete": "tel",
                    "inputmode": "tel",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].error_messages["invalid"] = self.error_messages["email_invalid"]
        self.fields["phone"].help_text = "Можно ввести через 8 или +7."
        if not self.is_bound and self.instance and self.instance.phone:
            self.initial["phone"] = format_russian_phone_for_display(self.instance.phone)

    def clean_inn(self):
        return validate_inn(
            self.cleaned_data.get("inn"),
            self.error_messages["inn_digits"],
            self.error_messages["inn_length"],
        )

    def clean_kpp(self):
        return validate_kpp(
            self.cleaned_data.get("kpp"),
            self.error_messages["kpp_digits"],
            self.error_messages["kpp_length"],
        )

    def clean_email(self):
        return validate_optional_email(self.cleaned_data.get("email"), self.error_messages["email_invalid"])

    def clean_phone(self):
        return normalize_russian_phone(self.cleaned_data.get("phone"), self.error_messages["phone_invalid"])


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "order_number",
            "client",
            "status",
            "address",
            "comments",
            "total_amount",
        ]
        labels = {
            "order_number": "Номер заказа",
            "client": "Клиент",
            "status": "Статус",
            "address": "Адрес доставки",
            "comments": "Комментарии",
            "total_amount": "Сумма",
        }


class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["status", "comments"]
        labels = {"status": "Статус", "comments": "Комментарий"}


class DeliveryPlanForm(forms.ModelForm):
    courier = forms.ModelChoiceField(queryset=Courier.objects.all(), required=False, label="Курьер")

    class Meta:
        model = Delivery
        fields = ["courier", "departure_time", "delivered_at", "address", "note", "is_sent"]
        labels = {
            "departure_time": "Время выезда",
            "delivered_at": "Доставлено",
            "address": "Адрес",
            "note": "Примечание",
            "is_sent": "Отправлен",
        }
