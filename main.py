from flask import Flask, request, render_template, jsonify
from Habit import Habit
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("serviceAccountKey.json")
align = firebase_admin.initialize_app(cred, name="ALIGN")
db = firestore.client(app=align)
app = Flask(__name__)

# This code had no AI use on it
@app.route("/add-habit", methods = ["POST"])
def add_habit():
    data = request.json
    habit = Habit(data.get("id"),
            data.get("user_id"),
            data.get("name"),
            data.get("category_id"),
            data.get("goal_time"),
            data.get("recurrence"),
            data.get("alerts", []),
            data.get("current_streak", 0))
    db.collection(habit.user_id).document(habit.name).set(habit.getHabit())
    return {"message": "Habit added successfully"}
    
@app.route("/remove-habit", methods = ["POST"])
def remove_habit():
    data = request.json
    habit = Habit.from_dict(data)
    db.collection(habit.user_id).document(habit.name).delete()
    return {"message": "Habit removed successfully"}

    
    


