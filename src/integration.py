
from faker import Faker
import random

fake = Faker()

VALID_STATUSES = ["single", "married", "widowed", "divorced"]


def build_record(*args, **kwargs):
    """
    Función genérica que construye un registro a partir de kwargs.
    *args  → ignorados (flexibilidad futura)
    **kwargs → campos del registro (id, name, email, age, status)
    """
    return {
        "id":     str(kwargs.get("id", "")),
        "name":   kwargs.get("name", ""),
        "email":  kwargs.get("email", ""),
        "age":    kwargs.get("age", 0),
        "status": kwargs.get("status", "single"),
    }


def generate_fake_records(n=10):
    """
    Genera n registros falsos usando Faker.
    Devuelve una lista de dicts listos para pasar a RegisterService.
    """
    records = []
    used_emails = set()

    for i in range(n):
        # Garantizar email único dentro del lote
        email = fake.email()
        while email in used_emails:
            email = fake.email()
        used_emails.add(email)

        record = build_record(
            id=f"fake-{i+1}",
            name=fake.name(),
            email=email,
            age=random.randint(18, 80),
            status=random.choice(VALID_STATUSES),
        )
        records.append(record)

    return records