from flask import Flask, request, render_template, jsonify
from Habit import Habit
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("serviceAccountKey.json")
align = firebase_admin.initialize_app(cred, name="ALIGN")
db = firestore.client(app=align)

# This code had no AI use on it
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
    db.collection("User_Habits").document(habit.name).set(habit.getHabit())
    

def remove_habit():
    data = request.json
    
    user_ID = data.get("user_id")

    
    


