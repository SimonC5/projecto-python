
import random
from typing import Any

from faker import Faker

VALID_STATUSES: list[str] = ["single", "married", "widowed", "divorced"]

_faker = Faker()


def build_record(**kwargs: Any) -> dict[str, Any]:
    """Build a record dict from keyword arguments.

    Unknown keys are passed through; missing keys fall back to safe defaults.
    This allows callers to supply only the fields they care about.
    """
    return {
        "id":     str(kwargs.get("id", "")),
        "name":   kwargs.get("name", ""),
        "email":  kwargs.get("email", ""),
        "age":    kwargs.get("age", 0),
        "status": kwargs.get("status", "single"),
    }


def generate_fake_records(n: int = 10) -> list[dict[str, Any]]:
    """Return a list of *n* random person records using Faker.

    E-mail uniqueness is guaranteed within the returned batch.
    IDs are ``fake-1`` … ``fake-n``.
    """
    used_emails: set[str] = set()
    records: list[dict[str, Any]] = []

    for i in range(1, n + 1):
        email = _faker.email()
        while email in used_emails:
            email = _faker.email()
        used_emails.add(email)

        records.append(
            build_record(
                id=f"fake-{i}",
                name=_faker.name(),
                email=email,
                age=random.randint(18, 80),
                status=random.choice(VALID_STATUSES),
            )
        )

    return records