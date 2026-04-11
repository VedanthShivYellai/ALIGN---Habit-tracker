import uuid
from datetime import datetime

class Habit:
    # use keyword arguments for the optional fields with sensible defaults
    # defaults make habit creation easier for user
    def __init__(self, user_id, name, goal_time="any", recurrence="daily", alerts=None, id=None, created_at=None, current_streak=0):
        
        # make sure there is a name
        # Gemini AI helped add the .strip() stuff
        if not name or not str(name).strip():
            raise ValueError("Habit name cannot be empty.")
        if not user_id:
            raise ValueError("Habit must be tied to a user_id.")

        self.id = id if id else str(uuid.uuid4())
        self.user_id = user_id
        self.name = str(name).strip()
        self.goal_time = goal_time
        self.recurrence = recurrence
        self.alerts = alerts if alerts is not None else []
        self.current_streak = current_streak
        # Gemini helped with datetime.now(), originally I did datetime.now.isoformat() but we found
        # issues with the created_at timestamp being changed as it was passed to the database
        # and so we had AI help us fix the issue of unncessary updates to timestamps
        self.created_at = created_at if created_at else datetime.now().isoformat()

    def to_dict(self):
        #Prepares the object to be saved to the database.
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "goal_time": self.goal_time,
            "recurrence": self.recurrence,
            "alerts": self.alerts,
            "current_streak": self.current_streak,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data):
        #Rebuilds a Habit object from a raw dictionary.
        return cls(
            id=data.get("id"),
            user_id=data.get("user_id"),
            name=data.get("name"),
            goal_time=data.get("goal_time", "any"),
            recurrence=data.get("recurrence", "daily"),
            alerts=data.get("alerts", []),
            current_streak=data.get("current_streak", 0),
            created_at=data.get("created_at")
        )

    def __str__(self):
        return f"Habit(name='{self.name}', streak={self.current_streak})"
        