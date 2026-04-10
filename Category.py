import uuid
from datetime import datetime

# Will require an array in main of all existing categories. This array will be fetched when a user
# tries to assign a category to a habit and be displayed as a dropdown. The selected category will
# retrive the category id

class Category:
    def __init__(self, name, user_id, color="#800080", icon="default"):
        self.id = str(uuid.uuid4())
        self.name = str(name)
        self.user_id = user_id
        self.color = color
        self.icon = icon
        self.created_at = datetime.now().isoformat()

    def to_dict(self):
        """Prepares the object for when you eventually plug the database back in."""
        return {
            "id": self.id,
            "name": self.name,
            "color": self.color,
            "icon": self.icon,
            "created_at": self.created_at
        }
    
    def __str__(self):
        # Just to make printing the object look clean in the terminal
        return f"Category(name='{self.name}', id='{self.id}')"