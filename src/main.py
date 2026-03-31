from service import RegisterService

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "records.json")


def print_record(r, i):
    print(
        f"[{i}] ID: {r['id']:<6} | "
        f"Name: {r['name']:<20} | "
        f"Email: {r['email']:<25} | "
        f"Age: {r['age']:<4} | "
        f"Status: {r['status']}"
    )


def try_create(service, **kwargs):
    try:
        service.create_record(**kwargs)
        print(f"  ✓ Record created → ID='{kwargs.get('id')}'")
    except ValueError as e:
        print(f"  ✗ Rejected → ID='{kwargs.get('id')}'\n    {e}")

        
def main():
    service = RegisterService()


    print("\n──── Creating records ────────────────────────────────")
    try_create(service, id="1", name="Liam Nakamura",   email="liam.nakamura@gmail.com",  age=38, status="married")
    try_create(service, id="2", name="Valentina Cruz",  email="val.cruz@gmail.com", age=51, status="widowed")
    try_create(service, id="3", name="Omar Fitzgerald",   email="omar.fitz@gmail.com",  age=23, status="single")


    print("\n──── Attempting duplicate ID ─────────────────────────")
    try_create(service, id="1", name="Priya Okonkwo", email="priya.ok@gmail.com", age=45, status="single")

    print("\n──── Invalid fields ──────────────────────────────────")
    try_create(service, id="4", name="Zoe",  email="not-an-email",  age=25,  status="single")
    try_create(service, id="5", name="Kwame", email="kwame@gmail.com", age=200, status="married")

    print("\n──── Records in memory & file ────────────────────────")
    records = service.list_records()
    for i, r in enumerate(records, start=1):
        print_record(r, i)

    print(f"\n  Total: {len(records)} record(s)")
    print(f"\n   Registered IDs (set): {service._ids}")
    print("  Data saved to → data/records.json")


if __name__ == "__main__":
    main()