def add_habit(data):
    habit = Habit(data.get("id"),
            data.get("user_id"),
            data.get("name"),
            data.get("category_id"),
            data.get("goal_time", "any"),
            data.get("recurrence", "daily"),
            data.get("alerts", []),
            data.get("current_streak", 0))
