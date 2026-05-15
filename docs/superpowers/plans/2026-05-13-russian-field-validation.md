# Russian Field Validation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add consistent Russian phone validation and shared client-field validation across Django forms.

**Architecture:** Create `crm/validators.py` with pure reusable helpers, then wire those helpers into `clients/forms.py` and `portal/forms.py`. Keep browser-side phone masks aligned with the server contract and verify through Django tests.

**Tech Stack:** Django forms, Django test runner, Python standard library regular expressions.

---

### Task 1: Shared Validators

**Files:**
- Create: `crm/validators.py`
- Test: `tests/test_field_validators.py`

- [ ] **Step 1: Write failing tests for phone normalization and display**

```python
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
        invalid_inputs = ["+1 999 123-45-67", "+7 (999) 123-45", "799912345678", "phone"]

        for value in invalid_inputs:
            with self.subTest(value=value):
                with self.assertRaises(ValidationError):
                    normalize_russian_phone(value)

    def test_formats_normalized_phone_for_display(self):
        self.assertEqual(format_russian_phone_for_display("+79991234567"), "+7 (999) 123-45-67")
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python manage.py test tests.test_field_validators -v 2`

Expected: FAIL because `crm.validators` does not exist.

- [ ] **Step 3: Implement minimal shared validators**

Create `crm/validators.py` with `normalize_russian_phone`, `format_russian_phone_for_display`, and reusable `validate_inn`, `validate_kpp`, `validate_optional_email` helpers.

- [ ] **Step 4: Run validator tests to verify they pass**

Run: `python manage.py test tests.test_field_validators -v 2`

Expected: PASS.

### Task 2: Clients Form Integration

**Files:**
- Modify: `clients/forms.py`
- Test: `tests/integration/test_app_flows.py`

- [ ] **Step 1: Add or reuse form tests for client phone normalization**

Use existing integration coverage that posts `8 (999) 111-22-33` and expects `+79991112233`.

- [ ] **Step 2: Run the existing client validation test**

Run: `python manage.py test tests.integration.test_app_flows.ClientManagerFlowTests -v 2`

Expected: current behavior should pass before refactor; rerun after refactor to catch regressions.

- [ ] **Step 3: Replace duplicated phone/email/INN/KPP logic with shared helpers**

Import helpers from `crm.validators`, remove duplicate phone formatter logic, and keep the existing error message strings.

- [ ] **Step 4: Run client flow tests**

Run: `python manage.py test tests.integration.test_app_flows.ClientManagerFlowTests -v 2`

Expected: PASS.

### Task 3: Portal Form Integration

**Files:**
- Modify: `portal/forms.py`
- Test: `tests/test_portal_forms.py`

- [ ] **Step 1: Write failing tests for portal client validation**

Test that portal client form normalizes `8 (999) 111-22-33`, rejects invalid phone numbers, rejects malformed INN/KPP, and rejects malformed email.

- [ ] **Step 2: Run test to verify it fails**

Run: `python manage.py test tests.test_portal_forms -v 2`

Expected: FAIL because portal form does not yet apply the shared validation.

- [ ] **Step 3: Add shared validation to `portal.forms.ClientForm`**

Add widgets and `clean_phone`, `clean_inn`, `clean_kpp`, `clean_email` methods using `crm.validators`.

- [ ] **Step 4: Run portal form tests**

Run: `python manage.py test tests.test_portal_forms -v 2`

Expected: PASS.

### Task 4: Final Verification

**Files:**
- Verify all changed files.

- [ ] **Step 1: Run focused tests**

Run: `python manage.py test tests.test_field_validators tests.test_portal_forms tests.integration.test_app_flows.ClientManagerFlowTests -v 2`

Expected: PASS.

- [ ] **Step 2: Check git diff**

Run: `git diff -- clients/forms.py portal/forms.py crm/validators.py tests/test_field_validators.py tests/test_portal_forms.py templates/clients/form.html`

Expected: Diff only contains shared validation and phone-mask related changes.
