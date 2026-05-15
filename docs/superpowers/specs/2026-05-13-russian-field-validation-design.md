# Russian Field Validation Design

## Goal

Unify field validation across the project for Russian phone numbers and related client fields. Server-side Django forms remain the source of truth; browser masks are only a usability layer.

## Scope

- Accept only Russian phone numbers.
- Store phone numbers in normalized E.164-like form: `+79991234567`.
- Display phone numbers in forms as `+7 (999) 123-45-67`.
- Keep existing client validations for name, INN, KPP, email, and structured address behavior.
- Add the same core client validation to the portal client form, which currently has weaker validation.

## Phone Rules

Accepted user input:

- `+7 (999) 123-45-67`
- `8 (999) 123-45-67`
- `89991234567`
- `9991234567`

Rejected input:

- Any non-Russian country code.
- Too few or too many digits.
- Values that cannot be normalized to an 11-digit number starting with `7`.

## Architecture

Create a small shared validation module in `crm/validators.py` with pure functions for phone normalization/display and reusable INN/KPP/email validation. Use these helpers from `clients/forms.py` and `portal/forms.py`. Keep form-level business rules inside each form.

## Testing

Add unit tests for shared validation helpers and form-level behavior. Tests must first fail before implementation, then pass after the shared helpers and form integrations are added.
