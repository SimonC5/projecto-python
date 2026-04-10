
from service import RegisterService
from integration import generate_fake_records

def print_header(title):
    bar = "─" * 56
    print(f"\n{bar}")
    print(f"  {title}")
    print(bar)


def print_record(r, i):
    print(
        f"  [{i}] ID: {r['id']:<10} | "
        f"Name: {r['name']:<22} | "
        f"Age: {r['age']:<4} | "
        f"Status: {r['status']:<10} | "
        f"Email: {r['email']}"
    )


def print_menu():
    print_header("GESTIÓN DE REGISTROS — MENÚ PRINCIPAL")
    print("  1. Crear registro")
    print("  2. Listar registros")
    print("  3. Generar 10 registros falsos (Faker)")
    print("  0. Salir")
    print()


def action_create(service):
    print_header("CREAR REGISTRO")
    id_val  = input("  ID     : ").strip()
    name    = input("  Nombre : ").strip()
    email   = input("  Email  : ").strip()
    age_raw = input("  Edad   : ").strip()
    status  = input("  Estado (single/married/widowed/divorced): ").strip()

    try:
        age = int(age_raw)
    except ValueError:
        print("  ✗ La edad debe ser un número entero.")
        return

    try:
        service.create_record(id=id_val, name=name, email=email, age=age, status=status)
        print(f"  ✓ Registro creado → ID='{id_val}'")
    except ValueError as e:
        print(f"  ✗ Error de validación:\n  {e}")


def action_list(service):
    print_header("LISTADO DE REGISTROS")
    records = service.list_records()
    if not records:
        print("  (No hay registros guardados)")
        return
    for i, r in enumerate(records, start=1):
        print_record(r, i)
    print(f"\n  Total: {len(records)} registro(s)")


def action_generate_fake(service):
    print_header("GENERAR REGISTROS FALSOS CON FAKER")
    print("  Generando 10 registros…\n")

    fake_records = generate_fake_records(10)
    created = 0
    skipped = 0

    for r in fake_records:
        try:
            service.create_record(**r)
            print(f"  ✓ {r['name']} — {r['email']}")
            created += 1
        except ValueError as e:
            # Puede ocurrir si el ID o email ya existe entre corridas
            print(f"  ✗ Omitido ({r['id']}): {e}")
            skipped += 1

    print(f"\n  Resultado: {created} creados, {skipped} omitidos.")
    print("  Datos guardados en data/records.json")

def run():
    service = RegisterService()

    while True:
        print_menu()
        choice = input("  Selecciona una opción: ").strip()

        if choice == "1":
            action_create(service)
        elif choice == "2":
            action_list(service)
        elif choice == "3":
            action_generate_fake(service)
        elif choice == "0":
            print("\n  Hasta luego 👋\n")
            break
        else:
            print("  ✗ Opción inválida. Intenta de nuevo.")


if __name__ == "__main__":
    run()