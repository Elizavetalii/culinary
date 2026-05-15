from django import forms
from django.conf import settings
from crm.forms import BootstrapFormMixin
from crm.models import Delivery, Route, RouteStop, CourierAssignment, LogisticianProfile, Courier


class DeliveryForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Delivery
        fields = [
            "courier",
            "route",
            "status",
            "planned_at",
            "departure_time",
            "delivered_at",
            "address",
            "cargo_weight_kg",
            "cargo_volume_m3",
            "cargo_length_cm",
            "cargo_width_cm",
            "cargo_height_cm",
            "note",
        ]
        labels = {
            "courier": "Курьер",
            "route": "Маршрут",
            "status": "Статус доставки",
            "planned_at": "Плановая дата/время",
            "departure_time": "Время выезда",
            "delivered_at": "Время доставки",
            "address": "Адрес",
            "cargo_weight_kg": "Вес груза (кг)",
            "cargo_volume_m3": "Объём груза (м³)",
            "cargo_length_cm": "Длина груза (см)",
            "cargo_width_cm": "Ширина груза (см)",
            "cargo_height_cm": "Высота груза (см)",
            "note": "Примечание",
        }
        widgets = {
            "planned_at": forms.DateTimeInput(attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
            "departure_time": forms.DateTimeInput(attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
            "delivered_at": forms.DateTimeInput(attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap()
        for name in ("planned_at", "departure_time", "delivered_at"):
            if name in self.fields:
                self.fields[name].input_formats = ["%Y-%m-%dT%H:%M"]

    def clean(self):
        cleaned = super().clean()
        status = cleaned.get("status")
        courier = cleaned.get("courier")
        route = cleaned.get("route")
        planned_at = cleaned.get("planned_at")
        departure_time = cleaned.get("departure_time")
        delivered_at = cleaned.get("delivered_at")
        note = cleaned.get("note")

        if status in ["Запланировано", "В пути", "Доставлено"] and not courier:
            self.add_error("courier", "Нужно назначить курьера.")
        if status in ["Запланировано", "В пути", "Доставлено"] and not planned_at:
            self.add_error("planned_at", "Нужно указать плановую дату/время.")
        if status in ["В пути", "Доставлено"] and not route:
            self.add_error("route", "Для статуса «В пути/Доставлено» нужен маршрут.")
        if status == "В пути" and not departure_time:
            self.add_error("departure_time", "Нужно указать время выезда.")
        if status == "Доставлено" and not delivered_at:
            self.add_error("delivered_at", "Нужно указать время доставки.")
        if status == "Доставлено" and route and route.status != "Завершён":
            self.add_error("status", "Нельзя отметить «Доставлено», пока маршрут не завершён.")
        if status == "Отменено" and not note:
            self.add_error("note", "Укажите причину отмены.")
        return cleaned


class RouteForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Route
        fields = ["planned_date", "status", "max_duration_minutes", "soft_limit_stops", "strict_mode", "notes"]
        labels = {
            "planned_date": "Дата маршрута",
            "status": "Статус",
            "max_duration_minutes": "Макс. длительность (мин)",
            "soft_limit_stops": "Мягкий лимит точек",
            "strict_mode": "Строгий режим лимита",
            "notes": "Заметки",
        }
        widgets = {
            "planned_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap()


class RouteStopForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = RouteStop
        fields = ["delivery", "planned_time", "note", "status", "service_time_minutes"]
        labels = {
            "delivery": "Доставка",
            "planned_time": "Плановое время",
            "note": "Примечание",
            "status": "Статус",
            "service_time_minutes": "Время обслуживания (мин)",
        }
        widgets = {
            "planned_time": forms.DateTimeInput(attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap()
        if "planned_time" in self.fields:
            self.fields["planned_time"].input_formats = ["%Y-%m-%dT%H:%M"]
        if "service_time_minutes" in self.fields and not self.instance.pk:
            self.fields["service_time_minutes"].initial = getattr(settings, "LOGISTICS_SERVICE_TIME_MINUTES", 15)
        if "status" in self.fields:
            allowed = ["Черновик", "Подтверждена", "Запланирована"]
            self.fields["status"].choices = [
                (value, label)
                for value, label in self.fields["status"].choices
                if value in allowed
            ]


class CourierStopStatusForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = RouteStop
        fields = ["status", "failure_reason", "note"]
        labels = {
            "status": "Статус",
            "failure_reason": "Причина",
            "note": "Комментарий",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap()
        if "status" in self.fields:
            allowed = ["В пути", "Не доставлено"]
            self.fields["status"].choices = [
                (value, label)
                for value, label in self.fields["status"].choices
                if value in allowed
            ]


class ProofUploadForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = RouteStop
        fields = ["proof_of_delivery"]
        labels = {"proof_of_delivery": "Документ доставки"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap()


class CourierAssignmentForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = CourierAssignment
        fields = ["courier"]
        labels = {"courier": "Курьер"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap()


class LogisticianProfileForm(BootstrapFormMixin, forms.ModelForm):
    transport_types = forms.MultipleChoiceField(
        label="Доступные типы транспорта",
        required=False,
        choices=[
            ("car", "Авто"),
            ("van", "Фургон"),
            ("refrigerated", "Рефрижератор"),
        ],
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = LogisticianProfile
        fields = [
            "region",
            "city",
            "transport_types",
            "timezone",
            "map_show_traffic",
            "preferred_route_type",
        ]
        labels = {
            "region": "Регион",
            "city": "Город",
            "timezone": "Часовой пояс",
            "map_show_traffic": "Пробки на карте",
            "preferred_route_type": "Тип маршрута",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap()
        self.fields["transport_types"].initial = self.instance.transport_types or []

    def clean_transport_types(self):
        return self.cleaned_data.get("transport_types") or []


class CourierProfileForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Courier
        fields = [
            "transport_type",
            "payload_capacity_kg",
            "cargo_volume_m3",
            "cargo_length_cm",
            "cargo_width_cm",
            "cargo_height_cm",
            "zone",
            "experience_years",
        ]
        labels = {
            "transport_type": "Тип транспорта",
            "payload_capacity_kg": "Грузоподъёмность (кг)",
            "cargo_volume_m3": "Объём кузова (м³)",
            "cargo_length_cm": "Длина кузова (см)",
            "cargo_width_cm": "Ширина кузова (см)",
            "cargo_height_cm": "Высота кузова (см)",
            "zone": "Зона",
            "experience_years": "Опыт (лет)",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap()
