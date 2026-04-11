
from service import RegisterService
from integration import generate_fake_records


def _header(title: str) -> None:
    bar = "─" * 56
    print(f"\n{bar}\n  {title}\n{bar}")


def _fmt_record(record: dict, index: int) -> str:
    return (
        f"  [{index}] ID: {record['id']:<10} | "
        f"Name: {record['name']:<22} | "
        f"Age: {record['age']:<4} | "
        f"Status: {record['status']:<10} | "
        f"Email: {record['email']}"
    )

def _print_menu() -> None:
    _header("GESTIÓN DE REGISTROS — MENÚ PRINCIPAL")
    options = [
        ("1", "Crear registro"),
        ("2", "Listar registros"),
        ("3", "Generar 10 registros falsos (Faker)"),
        ("0", "Salir"),
    ]
    for key, label in options:
        print(f"  {key}. {label}")
    print()

def _action_create(service: RegisterService) -> None:
    _header("CREAR REGISTRO")
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
    except ValueError as exc:
        print(f"  ✗ Error de validación:\n  {exc}")


def _action_list(service: RegisterService) -> None:
    _header("LISTADO DE REGISTROS")
    records = service.list_records()
    if not records:
        print("  (No hay registros guardados)")
        return
    for i, record in enumerate(records, start=1):
        print(_fmt_record(record, i))
    print(f"\n  Total: {len(records)} registro(s)")


def _action_generate_fake(service: RegisterService) -> None:
    _header("GENERAR REGISTROS FALSOS CON FAKER")
    print("  Generando 10 registros…\n")
    created = skipped = 0

    for record in generate_fake_records(10):
        try:
            service.create_record(**record)
            print(f"  ✓  {record['name']} — {record['email']}")
            created += 1
        except ValueError as exc:
            print(f"  ✗  Omitido ({record['id']}): {exc}")
            skipped += 1

    print(f"\n  Resultado: {created} creados, {skipped} omitidos.")
    print("  Datos guardados en data/records.json")

_ACTIONS = {
    "1": _action_create,
    "2": _action_list,
    "3": _action_generate_fake,
}


def run() -> None:
    """Start the interactive console loop."""
    service = RegisterService()

    while True:
        _print_menu()
        choice = input("  Selecciona una opción: ").strip()

        if choice == "0":
            print("\n  Hasta luego 👋\n")
            break
        elif choice in _ACTIONS:
            _ACTIONS[choice](service)
        else:
            print("  ✗ Opción inválida. Intenta de nuevo.")


if __name__ == "__main__":
    run()