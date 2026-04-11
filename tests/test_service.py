
import pytest


VALID = dict(id="1", name="Alice Doe", email="alice@example.com", age=30, status="single")

class TestCreateRecord:
    def test_creates_and_returns_record(self, service):
        record = service.create_record(**VALID)
        assert record["id"] == "1"
        assert record["name"] == "Alice Doe"
        assert record["email"] == "alice@example.com"

    def test_normalises_email_to_lowercase(self, service):
        record = service.create_record(
            id="2", name="Bob Smith", email="Bob@Example.COM", age=25, status="married"
        )
        assert record["email"] == "bob@example.com"

    def test_normalises_status_to_lowercase(self, service):
        record = service.create_record(**{**VALID, "status": "WIDOWED"})
        assert record["status"] == "widowed"

    def test_list_records_returns_all(self, service):
        service.create_record(**VALID)
        service.create_record(id="2", name="Bob Smith", email="bob@example.com", age=25, status="married")
        assert service.count() == 2

    def test_count_increments(self, service):
        assert service.count() == 0
        service.create_record(**VALID)
        assert service.count() == 1

class TestUniqueness:
    def test_duplicate_id_raises(self, service):
        service.create_record(**VALID)
        with pytest.raises(ValueError, match="already exists"):
            service.create_record(**{**VALID, "email": "other@example.com"})

    def test_duplicate_email_raises(self, service):
        service.create_record(**VALID)
        with pytest.raises(ValueError, match="already registered"):
            service.create_record(**{**VALID, "id": "99"})

    def test_email_uniqueness_is_case_insensitive(self, service):
        service.create_record(**VALID)
        with pytest.raises(ValueError):
            service.create_record(id="2", name="Carol Lee", email="ALICE@EXAMPLE.COM", age=40, status="divorced")

class TestValidationErrors:
    def test_invalid_name_raises(self, service):
        with pytest.raises(ValueError):
            service.create_record(id="x", name="R2D2", email="r2@test.com", age=5, status="single")

    def test_invalid_email_raises(self, service):
        with pytest.raises(ValueError):
            service.create_record(id="x", name="Valid Name", email="not-an-email", age=20, status="single")

    def test_age_out_of_range_raises(self, service):
        with pytest.raises(ValueError):
            service.create_record(id="x", name="Valid Name", email="v@test.com", age=999, status="single")

    def test_invalid_status_raises(self, service):
        with pytest.raises(ValueError):
            service.create_record(id="x", name="Valid Name", email="v@test.com", age=30, status="complicated")

    def test_multiple_errors_reported_together(self, service):
        with pytest.raises(ValueError) as exc_info:
            service.create_record(id="", name="123", email="bad", age=-1, status="???")
        message = str(exc_info.value)
        # All four problems should surface in a single exception
        assert message.count("\n  - ") >= 3

class TestPersistence:
    def test_record_survives_reload(self, monkeypatch, tmp_path):
        """Creating a record and reloading the service should show the same data."""
        import storage
        tmp_file = tmp_path / "records.json"
        monkeypatch.setattr(storage, "DATA_PATH", str(tmp_file))

        from service import RegisterService
        svc1 = RegisterService()
        svc1.create_record(**VALID)

        svc2 = RegisterService()
        assert svc2.count() == 1
        assert svc2.list_records()[0]["id"] == "1"