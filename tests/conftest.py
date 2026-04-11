
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


@pytest.fixture()
def service(monkeypatch, tmp_path):
    """Return a fresh RegisterService backed by a temporary directory."""
    import storage

    tmp_file = tmp_path / "records.json"
    monkeypatch.setattr(storage, "DATA_PATH", str(tmp_file))

    from service import RegisterService
    return RegisterService()