from flask import Flask, request, render_template, jsonify
from Habit import Habit


# This code had no AI use on it
def add_habit():
    habit = Habit(data.get("id"),
            data.get("user_id"),
            data.get("name"),
            data.get("category_id"),
            data.get("goal_time", "any"),
            data.get("recurrence", "daily"),
            data.get("alerts", []),
            data.get("current_streak", 0))
    
def remove_habit(data):
    return None

