import uuid
from datetime import datetime

# Will require an array in main of all existing categories. This array will be fetched when a user
# tries to assign a category to a habit and be displayed as a dropdown. The selected category will
# retrive the category id

class Category:
    def __init__(self, name, user_id, color="#800080", icon="default", created_at=None):
        if not name or not str(name).strip():
            raise ValueError("Category name cannot be empty.")
        self.id = str(uuid.uuid4())
        self.name = str(name).strip()
        self.user_id = user_id
        self.color = color
        self.icon = icon
        self.created_at = created_at if created_at else datetime.now().isoformat()

    #methods

    def update_name(self, new_name):
        if not new_name or not str(new_name).strip():
            raise ValueError("Category name cannot be empty.")
        self.name = str(new_name).strip()

    def update_icon(self, new_icon):
        self.icon = new_icon

    # Gemini AI was used to aid in the logic and code for to_dict and from_dict as we lack database and frontend integration knowledge
    #passes class object as dictionary for frontend use
    def to_dict(self):
        #Prepares the object for when you eventually plug the database back in.
        return {
            "id": self.id,
            "name": self.name,
            "user_id": self.user_id,
            "color": self.color,
            "icon": self.icon,
            "created_at": self.created_at
        }
    
    #turns dic back into obj for frontend use, requires functionality on both back and front end

    @classmethod
    def from_dict(cls, data):
        """Rebuilds a Category object from a dictionary (e.g., data fetched from a database)."""
        return cls(
            name=data.get("name"),
            user_id=data.get("user_id"),
            color=data.get("color", "#800080"),
            icon=data.get("icon", "default"),
            id=data.get("id"),
            created_at=data.get("created_at")
        )
    
    def __str__(self):
        # Just to make printing the object look clean in the terminal
        return f"Category(name='{self.name}', id='{self.id}')"