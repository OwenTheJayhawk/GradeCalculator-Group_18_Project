import json
import os
from class_profile import ClassProfile

DATA_FILE = "local_grade_data.json"

def save_class_data(classes: list[ClassProfile]):
    """Saves a list of ClassProfile objects to a local JSON file."""
    data = [c.to_dict() for c in classes]
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Data successfully saved to {DATA_FILE}")
    except Exception as e:
        print(f"Error saving data: {e}")

def load_class_data() -> list[ClassProfile]:
    """Loads a list of ClassProfile objects from a local JSON file."""
    if not os.path.exists(DATA_FILE):
        print(f"No existing data file found at {DATA_FILE}. Starting fresh.")
        return []
        
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
            # NOTE: ClassProfile class must be imported here
            classes = [ClassProfile.from_dict(d) for d in data]
            print(f"Data successfully loaded from {DATA_FILE}")
            return classes
    except Exception as e:
        print(f"Error loading data: {e}")
        return []