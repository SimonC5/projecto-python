
import pytest
from validate import validate_id, validate_name, validate_email, validate_age, validate_status

class TestValidateId:
    def test_valid_id(self):
        ok, msg = validate_id("abc-123")
        assert ok is True
        assert msg == ""

    def test_empty_string(self):
        ok, msg = validate_id("")
        assert ok is False
        assert "empty" in msg.lower()

    def test_whitespace_only(self):
        ok, _ = validate_id("   ")
        assert ok is False

    def test_non_string(self):
        ok, _ = validate_id(None)  # type: ignore[arg-type]
        assert ok is False

class TestValidateName:
    def test_ascii_name(self):
        ok, _ = validate_name("John Doe")
        assert ok is True

    def test_accented_chars(self):
        ok, _ = validate_name("José María Ñoño")
        assert ok is True

    def test_digits_rejected(self):
        ok, msg = validate_name("R2D2")
        assert ok is False
        assert "letter" in msg.lower()

    def test_empty_name(self):
        ok, _ = validate_name("")
        assert ok is False

class TestValidateEmail:
    def test_valid_email(self):
        ok, _ = validate_email("user@example.com")
        assert ok is True

    def test_missing_at(self):
        ok, msg = validate_email("userexample.com")
        assert ok is False
        assert "valid" in msg.lower()

    def test_missing_domain(self):
        ok, _ = validate_email("user@")
        assert ok is False

    def test_empty_email(self):
        ok, _ = validate_email("")
        assert ok is False

class TestValidateAge:
    @pytest.mark.parametrize("age", [0, 1, 60, 120])
    def test_boundary_values(self, age):
        ok, _ = validate_age(age)
        assert ok is True

    @pytest.mark.parametrize("age", [-1, 121, 200])
    def test_out_of_range(self, age):
        ok, _ = validate_age(age)
        assert ok is False

    def test_float_rejected(self):
        ok, _ = validate_age(25.5)  # type: ignore[arg-type]
        assert ok is False

    def test_string_rejected(self):
        ok, _ = validate_age("30")  # type: ignore[arg-type]
        assert ok is False


class TestValidateStatus:
    @pytest.mark.parametrize("status", ["single", "married", "widowed", "divorced"])
    def test_all_valid_statuses(self, status):
        ok, _ = validate_status(status)
        assert ok is True

    def test_case_insensitive(self):
        ok, _ = validate_status("MARRIED")
        assert ok is True

    def test_invalid_status(self):
        ok, msg = validate_status("complicated")
        assert ok is False
        assert "invalid" in msg.lower()