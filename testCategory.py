import pytest
from datetime import datetime
from Category import Category


# ── Fixtures ─────────────────────────────────────────────────────────────────

@pytest.fixture
def valid_category():
    """A basic valid Category object used as a baseline across tests."""
    return Category(name="Fitness", user_id="u1")


# ── testCategoryUpdateName ────────────────────────────────────────────────────

class TestCategoryUpdateName:
    def test_name_updates_to_new_value(self, valid_category):
        valid_category.update_name("Wellness")
        assert valid_category.name == "Wellness"

    def test_no_other_fields_change(self, valid_category):
        original_id = valid_category.id
        original_user_id = valid_category.user_id
        original_color = valid_category.color
        original_icon = valid_category.icon
        original_created_at = valid_category.created_at

        valid_category.update_name("Wellness")

        assert valid_category.id == original_id
        assert valid_category.user_id == original_user_id
        assert valid_category.color == original_color
        assert valid_category.icon == original_icon
        assert valid_category.created_at == original_created_at

    def test_whitespace_is_stripped(self, valid_category):
        valid_category.update_name("  Health  ")
        assert valid_category.name == "Health"


# ── testCategoryEmptyName ─────────────────────────────────────────────────────

class TestCategoryEmptyName:
    def test_empty_string_raises(self, valid_category):
        with pytest.raises(ValueError, match="Category name cannot be empty"):
            valid_category.update_name("")

    def test_whitespace_only_raises(self, valid_category):
        with pytest.raises(ValueError, match="Category name cannot be empty"):
            valid_category.update_name("   ")

    def test_none_raises(self, valid_category):
        with pytest.raises(ValueError):
            valid_category.update_name(None)

    def test_empty_name_on_creation_raises(self):
        with pytest.raises(ValueError, match="Category name cannot be empty"):
            Category(name="", user_id="u1")

    def test_whitespace_name_on_creation_raises(self):
        with pytest.raises(ValueError):
            Category(name="   ", user_id="u1")


# ── testCategoryToDict ────────────────────────────────────────────────────────

class TestCategoryToDict:
    def test_returns_dict(self, valid_category):
        result = valid_category.to_dict()
        assert isinstance(result, dict)

    def test_contains_all_required_keys(self, valid_category):
        result = valid_category.to_dict()
        for key in ("id", "name", "user_id", "color", "icon", "created_at"):
            assert key in result, f"Missing key: {key}"

    def test_values_match_object(self, valid_category):
        result = valid_category.to_dict()
        assert result["id"] == valid_category.id
        assert result["name"] == valid_category.name
        assert result["user_id"] == valid_category.user_id
        assert result["color"] == valid_category.color
        assert result["icon"] == valid_category.icon
        assert result["created_at"] == valid_category.created_at


# ── TestCategoryFromDict ──────────────────────────────────────────────────────

class TestCategoryFromDict:
    def test_returns_category_object(self):
        data = {"name": "Work", "user_id": "u2"}
        result = Category.from_dict(data)
        assert isinstance(result, Category)

    def test_name_matches_input(self):
        data = {"name": "Work", "user_id": "u2"}
        result = Category.from_dict(data)
        assert result.name == "Work"

    def test_defaults_applied_when_keys_missing(self):
        data = {"name": "Work", "user_id": "u2"}
        result = Category.from_dict(data)
        assert result.color == "#800080"
        assert result.icon == "default"

    def test_preserves_existing_id(self):
        data = {"name": "Work", "user_id": "u2", "id": "existing-id-456"}
        result = Category.from_dict(data)
        assert result.id == "existing-id-456"

    def test_generates_id_when_not_provided(self):
        data = {"name": "Work", "user_id": "u2"}
        result = Category.from_dict(data)
        assert result.id is not None
        assert len(result.id) > 0


# ── Additional edge-case tests ────────────────────────────────────────────────

class TestCategoryDefaults:
    def test_default_color_is_purple(self):
        c = Category(name="Health", user_id="u1")
        assert c.color == "#800080"

    def test_default_icon_is_default(self):
        c = Category(name="Health", user_id="u1")
        assert c.icon == "default"

    def test_id_is_generated(self):
        c = Category(name="Health", user_id="u1")
        assert c.id is not None and len(c.id) > 0

    def test_created_at_set_automatically(self):
        c = Category(name="Health", user_id="u1")
        assert c.created_at is not None
        datetime.fromisoformat(c.created_at)

    def test_update_icon(self):
        c = Category(name="Health", user_id="u1")
        c.update_icon("🏃")
        assert c.icon == "🏃"

    def test_str_representation(self):
        c = Category(name="Health", user_id="u1")
        assert "Health" in str(c)