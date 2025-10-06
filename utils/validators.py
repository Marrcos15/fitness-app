import re
from datetime import date
from wtforms.validators import ValidationError


def validate_email(email: str) -> bool:
    """
    Valida que el email tenga un formato correcto.
    """
    if not email:
        return False
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))


def validate_password(password: str, min_length: int = 8) -> bool:
    """
    Valida que la contraseña cumpla una longitud mínima y tenga letras y números.
    """
    if not password or len(password) < min_length:
        return False
    has_letter = any(c.isalpha() for c in password)
    has_digit = any(c.isdigit() for c in password)
    return has_letter and has_digit


def validate_future_date(input_date: date) -> bool:
    """
    Valida que la fecha no esté en el futuro.
    """
    if not input_date:
        return False
    return input_date <= date.today()


def validate_required(field_value: str) -> bool:
    """
    Valida que el campo no esté vacío o solo con espacios.
    """
    return bool(field_value and field_value.strip())


def validate_positive_number(value, allow_zero: bool = False) -> bool:
    """
    Valida que un número sea positivo (y opcionalmente que pueda ser 0).
    """
    try:
        val = float(value)
        if allow_zero:
            return val >= 0
        return val > 0
    except (TypeError, ValueError):
        return False


# =====================
# Wrappers para WTForms
# =====================

class EmailValidator:
    def __call__(self, form, field):
        if not validate_email(field.data):
            raise ValidationError("Introduce un email válido.")


class PasswordValidator:
    def __init__(self, min_length: int = 8):
        self.min_length = min_length

    def __call__(self, form, field):
        if not validate_password(field.data, self.min_length):
            raise ValidationError(
                f"La contraseña debe tener al menos {self.min_length} caracteres, incluir una letra y un número."
            )


class NoFutureDateValidator:
    def __call__(self, form, field):
        if not validate_future_date(field.data):
            raise ValidationError("La fecha no puede estar en el futuro.")


class RequiredValidator:
    def __call__(self, form, field):
        if not validate_required(field.data):
            raise ValidationError("Este campo es obligatorio.")


class PositiveNumberValidator:
    def __init__(self, allow_zero: bool = False):
        self.allow_zero = allow_zero

    def __call__(self, form, field):
        if not validate_positive_number(field.data, self.allow_zero):
            if self.allow_zero:
                raise ValidationError("El valor debe ser mayor o igual a 0.")
            else:
                raise ValidationError("El valor debe ser mayor que 0.")