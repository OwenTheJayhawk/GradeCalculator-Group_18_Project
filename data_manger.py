import json
import os
from typing import List, Optional
from class_profile import ClassProfile

DATA_FILE = "local_grade_data.json"


def save_class_data(classes: List[ClassProfile], path: Optional[str] = None):
    """Saves a list of ClassProfile objects to a local JSON file (overwrites).

    If `path` is provided, write to that path instead of the default DATA_FILE.
    """
    target = path or DATA_FILE
    data = [c.to_dict() for c in classes]
    try:
        with open(target, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Data successfully saved to {target}")
    except Exception as e:
        print(f"Error saving data: {e}")


def load_class_data(path: Optional[str] = None) -> List[ClassProfile]:
    """Loads a list of ClassProfile objects from a JSON file.

    If `path` is provided, read from that path instead of the default DATA_FILE.
    """
    target = path or DATA_FILE
    if not os.path.exists(target):
        print(f"No existing data file found at {target}. Starting fresh.")
        return []

    try:
        with open(target, 'r') as f:
            data = json.load(f)
            classes = [ClassProfile.from_dict(d) for d in data]
            print(f"Data successfully loaded from {target}")
            return classes
    except Exception as e:
        print(f"Error loading data: {e}")
        return []


# Convenience helpers for multi-class management

def upsert_class(profile: ClassProfile):
    """Add or update a class profile in the persistent store (by name).

    If a class with the same name exists, it is replaced. Otherwise appended.
    """
    classes = load_class_data()
    replaced = False
    for idx, c in enumerate(classes):
        if c.name == profile.name:
            classes[idx] = profile
            replaced = True
            break
    if not replaced:
        classes.append(profile)
    save_class_data(classes)


def delete_class(name: str) -> bool:
    """Delete a class by name. Returns True if deleted, False if not found."""
    classes = load_class_data()
    new = [c for c in classes if c.name != name]
    if len(new) == len(classes):
        return False
    save_class_data(new)
    return True


def list_class_names() -> List[str]:
    """Return the list of saved class names."""
    return [c.name for c in load_class_data()]


def import_from_file(path: str) -> List[ClassProfile]:
    """Load classes from an arbitrary JSON file path and return ClassProfile objects."""
    return load_class_data(path)


def export_class_to_file(profile: ClassProfile, path: str):
    """Export a single ClassProfile to a JSON file (writes a one-item list)."""
    save_class_data([profile], path)
