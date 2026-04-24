# AI GENERATED - Prompt: "Generate a test file for the test main based on the blackbox testing pdf"
# This prompt was used here as I did not know how to actually create tests for file that required 
# json data without a parameter
# And I did not know how to use the firebase database for testing

import pytest
import json
from unittest.mock import MagicMock, patch


# ── App setup ─────────────────────────────────────────────────────────────────
# We mock Firebase entirely so tests run without a real serviceAccountKey.json
# or a live Firestore connection.

@pytest.fixture(autouse=True)
def mock_firebase():
    """Patches Firebase init and Firestore client before main.py is imported."""
    with patch("firebase_admin.credentials.Certificate") as mock_cert, \
         patch("firebase_admin.initialize_app") as mock_init, \
         patch("firebase_admin.firestore.client") as mock_firestore:

        # Fake Firestore chain: db.collection().document().set() / .delete()
        mock_doc = MagicMock()
        mock_collection = MagicMock()
        mock_collection.document.return_value = mock_doc
        mock_firestore.return_value.collection.return_value = mock_collection

        yield {
            "db": mock_firestore.return_value,
            "collection": mock_collection,
            "document": mock_doc,
        }


@pytest.fixture
def client(mock_firebase):
    """Creates a Flask test client with Firebase already mocked."""
    import importlib
    import main
    importlib.reload(main)
    main.app.config["TESTING"] = True
    with main.app.test_client() as c:
        yield c


# ── /add-habit ────────────────────────────────────────────────────────────────

class TestAddHabit:
    def _payload(self, **overrides):
        base = {
            "user_id": "u1",
            "name": "Exercise",
            "category_id": "cat1",
            "goal_time": "morning",
            "recurrence": "daily",
            "alerts": [],
            "current_streak": 0,
        }
        base.update(overrides)
        return base

    def test_returns_200_on_valid_payload(self, client):
        resp = client.post(
            "/add-habit",
            data=json.dumps(self._payload()),
            content_type="application/json",
        )
        assert resp.status_code == 200

    def test_returns_success_message(self, client):
        resp = client.post(
            "/add-habit",
            data=json.dumps(self._payload()),
            content_type="application/json",
        )
        body = resp.get_json()
        assert body["message"] == "Habit added successfully"

    def test_writes_to_firestore(self, client, mock_firebase):
        client.post(
            "/add-habit",
            data=json.dumps(self._payload()),
            content_type="application/json",
        )
        mock_firebase["document"].set.assert_called_once()

    def test_uses_user_id_as_collection(self, client, mock_firebase):
        client.post(
            "/add-habit",
            data=json.dumps(self._payload(user_id="user_abc")),
            content_type="application/json",
        )
        mock_firebase["db"].collection.assert_called_with("user_abc")

    def test_uses_habit_name_as_document(self, client, mock_firebase):
        client.post(
            "/add-habit",
            data=json.dumps(self._payload(name="Meditate")),
            content_type="application/json",
        )
        # Habit.__init__ uppercases the name
        mock_firebase["collection"].document.assert_called_with("MEDITATE")

    def test_optional_fields_default_gracefully(self, client):
        minimal = {"user_id": "u1", "name": "Sleep"}
        resp = client.post(
            "/add-habit",
            data=json.dumps(minimal),
            content_type="application/json",
        )
        assert resp.status_code == 200


# ── /remove-habit ─────────────────────────────────────────────────────────────

class TestRemoveHabit:
    def _payload(self, **overrides):
        base = {
            "user_id": "u1",
            "name": "Exercise",
            "recurrence": "daily",
        }
        base.update(overrides)
        return base

    def test_returns_200_on_valid_payload(self, client):
        resp = client.post(
            "/remove-habit",
            data=json.dumps(self._payload()),
            content_type="application/json",
        )
        assert resp.status_code == 200

    def test_returns_success_message(self, client):
        resp = client.post(
            "/remove-habit",
            data=json.dumps(self._payload()),
            content_type="application/json",
        )
        body = resp.get_json()
        assert body["message"] == "Habit removed successfully"

    def test_deletes_from_firestore(self, client, mock_firebase):
        client.post(
            "/remove-habit",
            data=json.dumps(self._payload()),
            content_type="application/json",
        )
        mock_firebase["document"].delete.assert_called_once()

    def test_uses_user_id_as_collection(self, client, mock_firebase):
        client.post(
            "/remove-habit",
            data=json.dumps(self._payload(user_id="user_xyz")),
            content_type="application/json",
        )
        mock_firebase["db"].collection.assert_called_with("user_xyz")

    def test_uses_habit_name_as_document(self, client, mock_firebase):
        client.post(
            "/remove-habit",
            data=json.dumps(self._payload(name="Run")),
            content_type="application/json",
        )
        mock_firebase["collection"].document.assert_called_with("RUN")


# ── Integration Test ──────────────────────────────────────────────────────────
# AI GENERATED - Prompt: "based on this requirement, in the main test file,
# add one integration test incorporating multiple functions working together"
#
# This test verifies the full add -> remove lifecycle using both routes
# together, confirming that add-habit and remove-habit work as a pair and
# that Firestore receives the correct calls in the correct order.

class TestAddThenRemoveIntegration:
    def test_add_then_remove_habit(self, client, mock_firebase):
        """
        Integration test: adds a habit then immediately removes it.
        Verifies both routes work together and Firestore receives
        a set() call followed by a delete() call for the same habit.
        """
        payload = {
            "user_id": "u1",
            "name": "Yoga",
            "recurrence": "daily",
        }

        # Step 1 — add the habit
        add_resp = client.post(
            "/add-habit",
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert add_resp.status_code == 200
        assert add_resp.get_json()["message"] == "Habit added successfully"

        # Step 2 — remove the same habit
        remove_resp = client.post(
            "/remove-habit",
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert remove_resp.status_code == 200
        assert remove_resp.get_json()["message"] == "Habit removed successfully"

        # Step 3 — verify Firestore received both calls for the correct habit
        mock_firebase["document"].set.assert_called_once()
        mock_firebase["document"].delete.assert_called_once()
        mock_firebase["collection"].document.assert_called_with("YOGA")