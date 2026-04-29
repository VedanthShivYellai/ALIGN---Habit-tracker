from flask import Flask, request, render_template, jsonify
from Habit import Habit
import firebase_admin
from firebase_admin import credentials, firestore


cred = credentials.Certificate("serviceAccountKey.json")
align = firebase_admin.initialize_app(cred, name="ALIGN")
db = firestore.client(app=align)
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/add-habit", methods=["POST"])
def add_habit():
    data = request.json or {}
    try:
        habit = Habit(
            name=data.get("name"),
            category_id=data.get("category_id"),
            description=data.get("description"),
            goal_time=data.get("goal_time", "any"),
            recurrence=data.get("recurrence", "daily"),
            alerts=data.get("alerts", []),
            icon=data.get("icon", "🎯"),
            color=data.get("color", "#534ab7"),
        )
    except ValueError as e:
        return jsonify({"ok": False, "error": str(e)}), 400

    # Doc ID = habit name (uppercased by the model).
    # Note: saving a habit with an existing name will overwrite the old one.
    db.collection("Habits").document(habit.name).set(habit.getHabit())
    return jsonify({"ok": True, "habit": habit.getHabit()}), 201


@app.route("/remove-habit", methods=["POST"])
def remove_habit():
    data = request.json or {}
    name = data.get("name")
    if not name:
        return jsonify({"ok": False, "error": "Missing habit name"})
    # Match the same uppercasing the model does on save
    doc_id = str(name).strip().upper()
    db.collection("Habits").document(doc_id).delete()
    return jsonify({"ok": True}), 200


@app.route("/get-habits", methods=["GET"])
def get_habits():
    docs = db.collection("Habits").stream()
    habitList = []
    for doc in docs:
        habitList.append(doc.to_dict())
    return jsonify({"habits": habitList}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5019)