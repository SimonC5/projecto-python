
import re

VALID_STATUSES: frozenset[str] = frozenset({"single", "married", "widowed", "divorced"})


def validate_id(value: str) -> tuple[bool, str]:
    """Return (True, '') if *value* is a non-empty string, else (False, msg)."""
    if not isinstance(value, str) or not value.strip():
        return False, "ID cannot be empty."
    return True, ""


def validate_name(value: str) -> tuple[bool, str]:
    """Return (True, '') if *value* contains only letters and spaces."""
    if not isinstance(value, str) or not value.strip():
        return False, "Name cannot be empty."
    if not re.fullmatch(r"[A-Za-záéíóúÁÉÍÓÚüÜñÑ\s]+", value.strip()):
        return False, "Name can only contain letters and spaces."
    return True, ""


def validate_email(value: str) -> tuple[bool, str]:
    """Return (True, '') if *value* matches a basic e-mail pattern."""
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
    if not isinstance(value, str) or not value.strip():
        return False, "Email cannot be empty."
    if not re.match(pattern, value.strip()):
        return False, f"'{value}' is not a valid email address."
    return True, ""


def validate_age(value: int) -> tuple[bool, str]:
    """Return (True, '') if *value* is an integer between 0 and 120."""
    if not isinstance(value, int):
        return False, "Age must be an integer."
    if not (0 <= value <= 120):
        return False, f"Age {value} must be between 0 and 120."
    return True, ""


def validate_status(value: str) -> tuple[bool, str]:
    """Return (True, '') if *value* is one of the accepted marital statuses."""
    if not isinstance(value, str) or value.strip().lower() not in VALID_STATUSES:
        return False, f"Invalid status. Accepted values: {', '.join(sorted(VALID_STATUSES))}."
    return True, ""