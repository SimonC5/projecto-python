
import json
import os
from typing import Any

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH: str = os.path.join(_BASE_DIR, "data", "records.json")


def load_records() -> list[dict[str, Any]]:
    if not os.path.exists(DATA_PATH):
        return []
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except json.JSONDecodeError:
        print("⚠ Warning: data file is corrupted. Starting with empty list.")
        return []
    except OSError as exc:
        print(f"⚠ Could not read data file: {exc}")
        return []


def save_records(records: list[dict[str, Any]]) -> None:
    try:
        os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
        with open(DATA_PATH, "w", encoding="utf-8") as fh:
            json.dump(records, fh, indent=4, ensure_ascii=False)
    except OSError as exc:
        print(f"⚠ Error saving data: {exc}")