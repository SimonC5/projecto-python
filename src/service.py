
from typing import Any

from storage import load_records, save_records
from validate import (
    validate_id,
    validate_name,
    validate_email,
    validate_age,
    validate_status,
)


class RegisterService:
    """CRUD service for person records backed by a JSON file."""

    def __init__(self) -> None:
        self._records: list[dict[str, Any]] = load_records()
        # Build uniqueness indexes from persisted data
        self._ids: set[str] = {r["id"] for r in self._records}
        self._emails: set[str] = {r["email"] for r in self._records}

    def create_record(
        self,
        *,
        id: str,
        name: str,
        email: str,
        age: int,
        status: str,
    ) -> dict[str, Any]:
        """Validate and create a new record, then persist to disk.
        Parameters
        ----------
        id:     Unique string identifier.
        name:   Full name (letters and spaces only).
        email:  Valid, unique e-mail address.
        age:    Integer between 0 and 120.
        status: One of single | married | widowed | divorced.

        Returns
        -------
        The normalised record dict that was saved.

        Raises
        ------
        ValueError
            If any field fails validation or a uniqueness constraint is violated.
        """
        errors = self._collect_errors(id, name, email, age, status)
        if errors:
            raise ValueError("Validation errors:\n  - " + "\n  - ".join(errors))

        record = self._build_record(id, name, email, age, status)
        self._records.append(record)
        self._ids.add(record["id"])
        self._emails.add(record["email"])
        save_records(self._records)
        return record

    def list_records(self) -> list[dict[str, Any]]:
        """Return a shallow copy of all stored records."""
        return list(self._records)

    def count(self) -> int:
        """Return the total number of stored records."""
        return len(self._records)


    def _collect_errors(
        self, id: str, name: str, email: str, age: int, status: str
    ) -> list[str]:
        """Run all validators and return a list of error messages (empty = OK)."""
        checks = [
            validate_id(id),
            validate_name(name),
            validate_email(email),
            validate_age(age),
            validate_status(status),
        ]
        errors: list[str] = [msg for ok, msg in checks if not ok]

        if not errors:
            if id in self._ids:
                errors.append(f"ID '{id}' already exists.")
            normalised_email = email.strip().lower()
            if normalised_email in self._emails:
                errors.append(f"Email '{email}' is already registered.")

        return errors

    @staticmethod
    def _build_record(
        id: str, name: str, email: str, age: int, status: str
    ) -> dict[str, Any]:
        """Return a normalised record dict ready for storage."""
        return {
            "id": id.strip(),
            "name": name.strip(),
            "email": email.strip().lower(),
            "age": age,
            "status": status.strip().lower(),
        }