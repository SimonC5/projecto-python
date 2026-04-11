
from integration import build_record, generate_fake_records, VALID_STATUSES


class TestBuildRecord:
    def test_returns_all_expected_keys(self):
        record = build_record(id="1", name="Alice", email="a@b.com", age=25, status="single")
        assert set(record.keys()) == {"id", "name", "email", "age", "status"}

    def test_id_coerced_to_string(self):
        record = build_record(id=42)
        assert isinstance(record["id"], str)
        assert record["id"] == "42"

    def test_defaults_for_missing_fields(self):
        record = build_record()
        assert record["id"] == ""
        assert record["age"] == 0
        assert record["status"] == "single"


class TestGenerateFakeRecords:
    def test_returns_requested_count(self):
        records = generate_fake_records(5)
        assert len(records) == 5

    def test_default_count_is_ten(self):
        records = generate_fake_records()
        assert len(records) == 10

    def test_emails_are_unique(self):
        records = generate_fake_records(20)
        emails = [r["email"] for r in records]
        assert len(emails) == len(set(emails))

    def test_ids_follow_fake_prefix(self):
        records = generate_fake_records(3)
        for i, record in enumerate(records, start=1):
            assert record["id"] == f"fake-{i}"

    def test_status_is_valid(self):
        for record in generate_fake_records(10):
            assert record["status"] in VALID_STATUSES

    def test_age_within_range(self):
        for record in generate_fake_records(20):
            assert 18 <= record["age"] <= 80