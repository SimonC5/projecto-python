from validate import (
    validate_id,
    validate_name,
    validate_email,
    validate_age,
    validate_status,
    REGISTERED_IDS,
    REGISTERED_EMAILS,
)
from file import load_data, save_data

class RegisterService:
    def __init__(self):
         self._registers = load_data()
         self._ids = REGISTERED_IDS
         self._emails = REGISTERED_EMAILS


for r in self._registers:
            self._ids.add(r["id"])
            self._emails.add(r["email"])

    def __create_record(self, id, name, email, age, status):
        errors = []

        ok, msg = validate_id(id)
        if not ok:
            errors.append(msg)

        ok, msg = validate_name(name)
        if not ok:
            errors.append(msg)

        ok, msg = validate_email(email)
        if not ok:
            errors.append(msg)

        ok, msg = validate_age(age)
        if not ok:
            errors.append(msg)

        ok, msg = validate_status(status)
        if not ok:
            errors.append(msg)

        if errors:
            raise ValueError("Validation errors:\n  - " + "\n  - ".join(errors))

        record = {
            "id": id,
            "name": name.strip(),
            "email": email.strip().lower(),
            "age": age,
            "status": status.strip().lower(),
        }

        self._registers.append(record)
        self._ids.add(id)
        self._emails.add(email.strip().lower())

        save_data(self._registers)

        return record

    def list_records(self):
        return list(self._registers)