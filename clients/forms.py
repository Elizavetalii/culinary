import re

from django import forms
from crm.forms import BootstrapFormMixin
from crm.models import Client, Interaction, ClientStageHistory, CooperationStage
from crm.validators import (
    format_russian_phone_for_display,
    normalize_russian_phone,
    validate_inn,
    validate_kpp,
    validate_optional_email,
)


HAS_LETTER_RE = re.compile(r"[A-Za-zА-Яа-яЁё]")
CLIENT_NAME_RE = re.compile(r"^[A-Za-zА-Яа-яЁё0-9\s\"'«»„“”\-\.№]+$")
CITY_RE = re.compile(r"^[A-Za-zА-Яа-яЁё\s-]+$")
STREET_RE = re.compile(r"^[A-Za-zА-Яа-яЁё0-9\s.-]+$")
HOUSE_RE = re.compile(r"^[0-9]+[A-Za-zА-Яа-яЁё]?(?:/[0-9]+)?(?:\s*(?:к|корп|корп\.|стр|стр\.|строение)\s*[0-9A-Za-zА-Яа-яЁё]+)?$", re.IGNORECASE)
BUILDING_RE = re.compile(r"^(?:к\.?|корп\.?|корпус|стр\.?|строение)\s*[0-9A-Za-zА-Яа-яЁё-]+$", re.IGNORECASE)
UNIT_RE = re.compile(r"^(?:[0-9A-Za-zА-Яа-яЁё-]+|(?:кв\.?|квартира|офис|пом\.?|помещение)\s*[0-9A-Za-zА-Яа-яЁё-]+)$", re.IGNORECASE)
ADDRESS_STRUCTURED_FIELDS = (
    "address_city",
    "address_street",
    "address_house",
    "address_building",
    "address_unit",
    "address_comment",
)


class ClientForm(BootstrapFormMixin, forms.ModelForm):
    address_city = forms.CharField(label="Город/населённый пункт", required=False, max_length=80)
    address_street = forms.CharField(label="Улица", required=False, max_length=120)
    address_house = forms.CharField(label="Дом", required=False, max_length=20)
    address_building = forms.CharField(label="Корпус/строение", required=False, max_length=40)
    address_unit = forms.CharField(label="Квартира/офис", required=False, max_length=40)
    address_comment = forms.CharField(
        label="Комментарий для курьера",
        required=False,
        max_length=300,
        widget=forms.Textarea(attrs={"rows": "2"}),
    )

    error_messages = {
        "name_required": "Укажите название клиента.",
        "name_min_length": "Название должно быть не короче 2 символов.",
        "name_letter_required": "Название должно содержать хотя бы одну букву.",
        "name_invalid": "Используйте буквы, цифры, пробелы, кавычки, дефис, точку и №.",
        "client_type_required": "Выберите тип клиента.",
        "inn_digits": "ИНН должен содержать только цифры.",
        "inn_length": "ИНН должен состоять из 10 или 12 цифр.",
        "kpp_digits": "КПП должен содержать только цифры.",
        "kpp_length": "КПП должен состоять из 9 цифр.",
        "address_min_length": "Адрес доставки должен быть не короче 5 символов.",
        "address_city_required": "Укажите город или населённый пункт.",
        "address_street_required": "Укажите улицу.",
        "address_house_required": "Укажите дом.",
        "address_too_short": "Слишком короткое значение.",
        "address_city_digits_only": "Город не может состоять только из цифр.",
        "address_city_letter_required": "Город должен содержать хотя бы одну букву.",
        "address_city_invalid": "Используйте буквы, пробелы и дефис.",
        "address_street_digits_only": "Улица не может состоять только из цифр.",
        "address_street_letter_required": "Улица должна содержать хотя бы одну букву.",
        "address_street_invalid": "Используйте буквы, цифры, пробелы, дефис и точку.",
        "address_house_number_required": "Дом должен содержать номер.",
        "address_house_invalid": "Укажите дом в формате 12, 12А, 12/1, 12к2 или 12 стр 1.",
        "address_building_invalid": "Укажите корпус или строение в формате к. 2, корп. 2, стр. 1.",
        "address_unit_invalid": "Укажите квартиру или офис в формате 15, офис 204 или кв. 7Б.",
        "address_full_too_long": "Полный адрес не должен быть длиннее 255 символов.",
        "email_invalid": "Введите корректный email.",
        "phone_invalid": "Введите российский номер в формате +7 (999) 123-45-67.",
        "status_required": "Выберите статус клиента.",
        "stage_required": "Выберите текущий этап.",
    }

    class Meta:
        model = Client
        fields = [
            "name",
            "client_type",
            "inn",
            "kpp",
            "default_delivery_address",
            "address_city",
            "address_street",
            "address_house",
            "address_building",
            "address_unit",
            "address_comment",
            "email",
            "phone",
            "status",
            "current_stage",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"minlength": "2", "required": "required"}),
            "client_type": forms.Select(attrs={"required": "required"}),
            "inn": forms.TextInput(attrs={"inputmode": "numeric", "maxlength": "12", "pattern": r"\d{10}|\d{12}"}),
            "kpp": forms.TextInput(attrs={"inputmode": "numeric", "maxlength": "9", "pattern": r"\d{9}"}),
            "default_delivery_address": forms.HiddenInput(),
            "email": forms.EmailInput(attrs={"autocomplete": "email"}),
            "phone": forms.TextInput(
                attrs={
                    "placeholder": "+7 (___) ___-__-__",
                    "autocomplete": "tel",
                    "inputmode": "tel",
                }
            ),
            "status": forms.Select(attrs={"required": "required"}),
            "current_stage": forms.Select(attrs={"required": "required"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].required = True
        self.fields["client_type"].required = True
        self.fields["status"].required = True
        self.fields["current_stage"].required = True
        self.fields["inn"].widget.attrs["maxlength"] = "12"
        self.fields["kpp"].widget.attrs["maxlength"] = "9"
        self.fields["phone"].help_text = "Можно ввести через 8 или +7."
        if not self.is_bound and self.instance and self.instance.phone:
            self.initial["phone"] = format_russian_phone_for_display(self.instance.phone)
        if not self.is_bound and self.instance and self.instance.default_delivery_address:
            self.initial["default_delivery_address"] = self.instance.default_delivery_address
        self.fields["address_city"].widget.attrs.update(
            {
                "autocomplete": "address-level2",
                "data-address-part": "city",
                "placeholder": "Например, Москва",
            }
        )
        self.fields["address_street"].widget.attrs.update(
            {
                "autocomplete": "address-line1",
                "data-address-part": "street",
                "placeholder": "Например, Тверская",
            }
        )
        self.fields["address_house"].widget.attrs.update(
            {
                "autocomplete": "address-line2",
                "data-address-part": "house",
                "placeholder": "12",
            }
        )
        self.fields["address_building"].widget.attrs.update(
            {
                "data-address-part": "building",
                "placeholder": "к. 2, стр. 1",
            }
        )
        self.fields["address_unit"].widget.attrs.update(
            {
                "data-address-part": "unit",
                "placeholder": "офис 305",
            }
        )
        self.fields["address_comment"].widget.attrs.update(
            {
                "data-address-part": "comment",
                "placeholder": "Код домофона, вход со двора, время разгрузки",
                "maxlength": "300",
            }
        )
        self._init_bootstrap()

    def _validate_city(self, value):
        if not value:
            raise forms.ValidationError(self.error_messages["address_city_required"])
        if len(value) < 2:
            raise forms.ValidationError(self.error_messages["address_too_short"])
        if value.isdigit():
            raise forms.ValidationError(self.error_messages["address_city_digits_only"])
        if not HAS_LETTER_RE.search(value):
            raise forms.ValidationError(self.error_messages["address_city_letter_required"])
        if not CITY_RE.fullmatch(value):
            raise forms.ValidationError(self.error_messages["address_city_invalid"])

    def _validate_street(self, value):
        if not value:
            raise forms.ValidationError(self.error_messages["address_street_required"])
        if len(value) < 2:
            raise forms.ValidationError(self.error_messages["address_too_short"])
        if value.isdigit():
            raise forms.ValidationError(self.error_messages["address_street_digits_only"])
        if not HAS_LETTER_RE.search(value):
            raise forms.ValidationError(self.error_messages["address_street_letter_required"])
        if not STREET_RE.fullmatch(value):
            raise forms.ValidationError(self.error_messages["address_street_invalid"])

    def _validate_house(self, value):
        if not value:
            raise forms.ValidationError(self.error_messages["address_house_required"])
        if not any(char.isdigit() for char in value):
            raise forms.ValidationError(self.error_messages["address_house_number_required"])
        if not HOUSE_RE.fullmatch(value):
            raise forms.ValidationError(self.error_messages["address_house_invalid"])

    def _validate_building(self, value):
        if value and not BUILDING_RE.fullmatch(value):
            raise forms.ValidationError(self.error_messages["address_building_invalid"])

    def _validate_unit(self, value):
        if value and not UNIT_RE.fullmatch(value):
            raise forms.ValidationError(self.error_messages["address_unit_invalid"])

    def _address_parts(self):
        return {
            field: (self.cleaned_data.get(field) or "").strip()
            for field in ADDRESS_STRUCTURED_FIELDS
        }

    def _build_full_address(self, parts):
        chunks = [
            parts["address_city"],
            parts["address_street"],
            f"д. {parts['address_house']}" if parts["address_house"] else "",
            parts["address_building"],
            parts["address_unit"],
        ]
        full_address = ", ".join(chunk for chunk in chunks if chunk)
        if parts["address_comment"]:
            full_address = f"{full_address}. Комментарий курьеру: {parts['address_comment']}" if full_address else parts["address_comment"]
        return full_address

    def clean_name(self):
        name = (self.cleaned_data.get("name") or "").strip()
        if not name:
            raise forms.ValidationError(self.error_messages["name_required"])
        if len(name) < 2:
            raise forms.ValidationError(self.error_messages["name_min_length"])
        if not HAS_LETTER_RE.search(name):
            raise forms.ValidationError(self.error_messages["name_letter_required"])
        if not CLIENT_NAME_RE.fullmatch(name):
            raise forms.ValidationError(self.error_messages["name_invalid"])
        return name

    def clean_client_type(self):
        client_type = self.cleaned_data.get("client_type")
        if not client_type:
            raise forms.ValidationError(self.error_messages["client_type_required"])
        return client_type

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

    def clean_default_delivery_address(self):
        address = (self.cleaned_data.get("default_delivery_address") or "").strip()
        if address and len(address) < 5:
            raise forms.ValidationError(self.error_messages["address_min_length"])
        return address

    def clean(self):
        cleaned_data = super().clean()
        parts = self._address_parts()
        has_structured_address = any(parts.values())
        existing_address = (cleaned_data.get("default_delivery_address") or "").strip()

        if has_structured_address or not existing_address:
            validators = {
                "address_city": self._validate_city,
                "address_street": self._validate_street,
                "address_house": self._validate_house,
                "address_building": self._validate_building,
                "address_unit": self._validate_unit,
            }
            for field, validator in validators.items():
                try:
                    validator(parts[field])
                except forms.ValidationError as exc:
                    self.add_error(field, exc)

        if (
            parts["address_city"]
            and parts["address_street"]
            and parts["address_house"]
            and not self.errors.get("address_city")
            and not self.errors.get("address_street")
            and not self.errors.get("address_house")
            and not self.errors.get("address_building")
            and not self.errors.get("address_unit")
        ):
            full_address = self._build_full_address(parts)
            if len(full_address) > Client._meta.get_field("default_delivery_address").max_length:
                self.add_error("address_comment", self.error_messages["address_full_too_long"])
            else:
                cleaned_data["default_delivery_address"] = full_address
        elif existing_address:
            cleaned_data["default_delivery_address"] = existing_address

        return cleaned_data

    def clean_email(self):
        return validate_optional_email(self.cleaned_data.get("email"), self.error_messages["email_invalid"])

    def clean_phone(self):
        return normalize_russian_phone(self.cleaned_data.get("phone"), self.error_messages["phone_invalid"])

    def clean_status(self):
        status = self.cleaned_data.get("status")
        if not status:
            raise forms.ValidationError(self.error_messages["status_required"])
        return status

    def clean_current_stage(self):
        stage = self.cleaned_data.get("current_stage")
        if not stage:
            raise forms.ValidationError(self.error_messages["stage_required"])
        return stage


class InteractionForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Interaction
        fields = ["interaction_type", "note", "happened_at"]
        labels = {
            "interaction_type": "Тип взаимодействия",
            "note": "Заметка",
            "happened_at": "Дата и время",
        }
        widgets = {
            "happened_at": forms.DateTimeInput(attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap()
        self.fields["happened_at"].input_formats = ["%Y-%m-%dT%H:%M"]


class StageChangeForm(BootstrapFormMixin, forms.ModelForm):
    stage = forms.ModelChoiceField(
        queryset=CooperationStage.objects.none(),
        label="Этап сотрудничества",
        required=True,
    )

    class Meta:
        model = ClientStageHistory
        fields = ["stage", "comment"]
        labels = {"comment": "Комментарий"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["stage"].queryset = CooperationStage.objects.filter(is_active=True)
        self._init_bootstrap()
