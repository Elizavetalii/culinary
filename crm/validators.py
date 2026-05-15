import re

from django.core.exceptions import ValidationError
from django.core.validators import validate_email as django_validate_email


DIGITS_RE = re.compile(r"\D+")
DEFAULT_PHONE_ERROR = "Введите российский номер в формате +7 (999) 123-45-67."


def normalize_russian_phone(value, error_message=DEFAULT_PHONE_ERROR):
    phone = (value or "").strip()
    if not phone:
        return phone

    digits = DIGITS_RE.sub("", phone)
    if len(digits) == 11 and digits[0] == "8":
        digits = "7" + digits[1:]
    elif len(digits) == 10:
        digits = "7" + digits

    if len(digits) != 11 or not digits.startswith("7"):
        raise ValidationError(error_message)
    return f"+{digits}"


def format_russian_phone_for_display(value):
    digits = DIGITS_RE.sub("", value or "")
    if len(digits) == 11 and digits.startswith("7"):
        return f"+7 ({digits[1:4]}) {digits[4:7]}-{digits[7:9]}-{digits[9:11]}"
    return value


def validate_inn(value, digits_message, length_message):
    inn = (value or "").strip()
    if not inn:
        return inn
    if not inn.isdigit():
        raise ValidationError(digits_message)
    if len(inn) not in (10, 12):
        raise ValidationError(length_message)
    return inn


def validate_kpp(value, digits_message, length_message):
    kpp = (value or "").strip()
    if not kpp:
        return kpp
    if not kpp.isdigit():
        raise ValidationError(digits_message)
    if len(kpp) != 9:
        raise ValidationError(length_message)
    return kpp


def validate_optional_email(value, error_message):
    email = (value or "").strip()
    if not email:
        return email
    try:
        django_validate_email(email)
    except ValidationError as exc:
        raise ValidationError(error_message) from exc
    return email
