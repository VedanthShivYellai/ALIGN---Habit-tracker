import pytest
from unittest.mock import patch
from datetime import datetime
from Habit import Habit


# ── Fixtures ────────────────────────────────────────────────────────────────

@pytest.fixture
def valid_habit():
    """A basic valid Habit object used as a baseline across tests."""
    return Habit(user_id="u1", name="Exercise")


# ── testGetHabit ─────────────────────────────────────────────────────────────
# From black-box doc: call getHabit(), expect dict with required keys.

class TestGetHabit:
    def test_returns_dict(self, valid_habit):
        result = valid_habit.getHabit()
        assert isinstance(result, dict)

    def test_contains_required_keys(self, valid_habit):
        result = valid_habit.getHabit()
        for key in ("id", "name", "user_id", "recurrence", "current_streak"):
            assert key in result, f"Missing key: {key}"

    def test_values_match_object(self, valid_habit):
        result = valid_habit.getHabit()
        assert result["name"] == valid_habit.name
        assert result["user_id"] == valid_habit.user_id
        assert result["recurrence"] == valid_habit.recurrence
        assert result["current_streak"] == valid_habit.current_streak

    def test_contains_optional_keys(self, valid_habit):
        result = valid_habit.getHabit()
        for key in ("category_id", "goal_time", "alerts", "created_at"):
            assert key in result, f"Missing optional key: {key}"


# ── testEmptyHabitName ────────────────────────────────────────────────────────

class TestEmptyHabitName:
    def test_empty_string_raises(self):
        with pytest.raises(ValueError, match="Habit name cannot be empty"):
            Habit(user_id="u1", name="")

    def test_whitespace_only_raises(self):
        with pytest.raises(ValueError, match="Habit name cannot be empty"):
            Habit(user_id="u1", name="   ")

    def test_none_name_raises(self):
        with pytest.raises(ValueError):
            Habit(user_id="u1", name=None)


# ── testMissingUserId ─────────────────────────────────────────────────────────
class TestMissingUserId:
    def test_none_user_id_raises(self):
        with pytest.raises(ValueError, match="Habit must be tied to a user_id"):
            Habit(user_id=None, name="Journal")

    def test_empty_user_id_raises(self):
        # Empty string is also an invalid user_id
        with pytest.raises(ValueError):
            Habit(user_id="", name="Journal")


# ── testBuildHabit (from_dict) ────────────────────────────────────────────────

class TestBuildHabit:
    def test_returns_habit_object(self):
        data = {"user_id": "u1", "name": "Read", "recurrence": "weekly"}
        result = Habit.from_dict(data)
        assert isinstance(result, Habit)

    def test_name_matches_input(self):
        data = {"user_id": "u1", "name": "Read", "recurrence": "weekly"}
        result = Habit.from_dict(data)
        assert result.name == "READ"  # __init__ uppercases the name

    def test_recurrence_matches_input(self):
        data = {"user_id": "u1", "name": "Read", "recurrence": "weekly"}
        result = Habit.from_dict(data)
        assert result.recurrence == "weekly"

    def test_defaults_applied_when_keys_missing(self):
        data = {"user_id": "u1", "name": "Meditate"}
        result = Habit.from_dict(data)
        assert result.recurrence == "daily"
        assert result.goal_time == "any"
        assert result.alerts == []
        assert result.current_streak == 0

    def test_preserves_id_from_dict(self):
        data = {"user_id": "u1", "name": "Run", "id": "existing-id-123"}
        result = Habit.from_dict(data)
        assert result.id == "existing-id-123"

    def test_preserves_created_at(self):
        ts = "2024-01-01T00:00:00"
        data = {"user_id": "u1", "name": "Run", "created_at": ts}
        result = Habit.from_dict(data)
        assert result.created_at == ts


# ── Additional edge-case tests ────────────────────────────────────────────────

class TestHabitDefaults:
    def test_id_is_generated_if_not_provided(self):
        h = Habit(user_id="u1", name="Sleep")
        assert h.id is not None
        assert len(h.id) > 0

    def test_name_is_uppercased(self):
        h = Habit(user_id="u1", name="exercise")
        assert h.name == "EXERCISE"

    def test_created_at_is_set_automatically(self):
        h = Habit(user_id="u1", name="Walk")
        assert h.created_at is not None
        # Should be a valid ISO format string
        datetime.fromisoformat(h.created_at)

    def test_created_at_not_overwritten_if_provided(self):
        ts = "2023-06-15T10:00:00"
        h = Habit(user_id="u1", name="Walk", created_at=ts)
        assert h.created_at == ts

    def test_str_representation(self):
        h = Habit(user_id="u1", name="Run")
        assert "RUN" in str(h)
        assert "0" in str(h)  # default streak