from django import forms
from django.contrib.auth import get_user_model
from crm.forms import BootstrapFormMixin
from crm.models import Role
from crm.validators import format_russian_phone_for_display, normalize_russian_phone
from .models import BackupSchedule


User = get_user_model()


class UserPhoneValidationMixin:
    phone_error_message = "Введите российский номер в формате +7 (999) 123-45-67."

    def _init_phone_validation(self):
        self.fields["phone"].widget.attrs.update(
            {
                "placeholder": "+7 (___) ___-__-__",
                "autocomplete": "tel",
                "inputmode": "tel",
            }
        )
        self.fields["phone"].help_text = "Можно ввести через 8 или +7."
        if not self.is_bound and self.instance and self.instance.phone:
            self.initial["phone"] = format_russian_phone_for_display(self.instance.phone)

    def clean_phone(self):
        return normalize_russian_phone(self.cleaned_data.get("phone"), self.phone_error_message)


class UserCreateForm(UserPhoneValidationMixin, BootstrapFormMixin, forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    roles = forms.ModelMultipleChoiceField(queryset=Role.objects.all(), label="Роли")

    class Meta:
        model = User
        fields = ["username", "email", "full_name", "phone", "is_active"]
        labels = {
            "username": "Логин",
            "email": "Электронная почта",
            "full_name": "ФИО",
            "phone": "Телефон",
            "is_active": "Активен",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap()
        self._init_phone_validation()
        self.fields["password"].widget.attrs.setdefault("class", "form-control")
        self.fields["roles"].widget.attrs.setdefault("class", "form-select")


class UserUpdateForm(UserPhoneValidationMixin, BootstrapFormMixin, forms.ModelForm):
    roles = forms.ModelMultipleChoiceField(queryset=Role.objects.all(), label="Роли", required=False)

    class Meta:
        model = User
        fields = ["email", "full_name", "phone", "is_active"]
        labels = {
            "email": "Электронная почта",
            "full_name": "ФИО",
            "phone": "Телефон",
            "is_active": "Активен",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap()
        self._init_phone_validation()
        self.fields["roles"].widget.attrs.setdefault("class", "form-select")


class UserPasswordForm(BootstrapFormMixin, forms.Form):
    password = forms.CharField(label="Новый пароль", widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput)

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("password") != cleaned.get("password_confirm"):
            self.add_error("password_confirm", "Пароли не совпадают.")
        return cleaned


class RoleForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Role
        fields = ["name"]
        labels = {"name": "Название роли"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap()


class BackupScheduleForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = BackupSchedule
        fields = ["frequency", "is_active"]
        labels = {"frequency": "Частота", "is_active": "Активные задания"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap()


class BackupCreateForm(BootstrapFormMixin, forms.Form):
    destination_dir = forms.CharField(
        label="Каталог для бэкапа",
        required=False,
        max_length=500,
        help_text="Пусто: media/backups. Можно указать абсолютный путь на сервере или путь внутри media.",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap()
        self.fields["destination_dir"].widget.attrs.update(
            {
                "placeholder": "backups или /var/backups/artculinary",
                "autocomplete": "off",
            }
        )

    def clean_destination_dir(self):
        return (self.cleaned_data.get("destination_dir") or "").strip()
