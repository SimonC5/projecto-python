
from service import RegisterService


def _print_record(record: dict, index: int) -> None:
    print(
        f"  [{index}] ID: {record['id']:<6} | "
        f"Name: {record['name']:<20} | "
        f"Email: {record['email']:<28} | "
        f"Age: {record['age']:<4} | "
        f"Status: {record['status']}"
    )


def _try_create(service: RegisterService, **kwargs) -> None:
    try:
        service.create_record(**kwargs)
        print(f"  ✓ Created → ID='{kwargs.get('id')}'")
    except ValueError as exc:
        print(f"  ✗ Rejected → ID='{kwargs.get('id')}'\n    {exc}")


def main() -> None:
    service = RegisterService()

    print("\n──── Creating records ────────────────────────────────")
    _try_create(service, id="1", name="Liam Nakamura",   email="liam.nakamura@gmail.com", age=38, status="married")
    _try_create(service, id="2", name="Valentina Cruz",  email="val.cruz@gmail.com",       age=51, status="widowed")
    _try_create(service, id="3", name="Omar Fitzgerald", email="omar.fitz@gmail.com",       age=23, status="single")

    print("\n──── Duplicate ID ────────────────────────────────────")
    _try_create(service, id="1", name="Priya Okonkwo",   email="priya.ok@gmail.com",        age=45, status="single")

    print("\n──── Invalid fields ──────────────────────────────────")
    _try_create(service, id="4", name="Zoe123",          email="not-an-email",              age=25, status="single")
    _try_create(service, id="5", name="Kwame",           email="kwame@gmail.com",            age=200, status="married")

    print("\n──── Current records ─────────────────────────────────")
    for i, record in enumerate(service.list_records(), start=1):
        _print_record(record, i)
    print(f"\n  Total: {service.count()} record(s)")


if __name__ == "__main__":
    main()