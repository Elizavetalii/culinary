from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

from crm.validators import format_russian_phone_for_display, normalize_russian_phone


class RussianPhoneValidatorTests(SimpleTestCase):
    def test_normalizes_common_russian_phone_inputs(self):
        valid_inputs = [
            "+7 (999) 123-45-67",
            "8 (999) 123-45-67",
            "89991234567",
            "9991234567",
        ]

        for value in valid_inputs:
            with self.subTest(value=value):
                self.assertEqual(normalize_russian_phone(value), "+79991234567")

    def test_rejects_non_russian_or_incomplete_phone_inputs(self):
        invalid_inputs = [
            "+1 999 123-45-67",
            "+7 (999) 123-45",
            "799912345678",
            "phone",
        ]

        for value in invalid_inputs:
            with self.subTest(value=value):
                with self.assertRaises(ValidationError):
                    normalize_russian_phone(value)

    def test_formats_normalized_phone_for_display(self):
        self.assertEqual(
            format_russian_phone_for_display("+79991234567"),
            "+7 (999) 123-45-67",
        )
