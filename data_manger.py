#import statements
import json
import os
from typing import List, Optional
from class_profile import ClassProfile # Import ClassProfile

# FIX: Use absolute path relative to the data_manger.py file's location
file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "grade_data.json") 

def save_data(classes: List[ClassProfile], path: Optional[str] = None): #Save Class data
    target = path or file #location to save to
    try:
        data = [_.SaveClass() for _ in classes] # Use the aliased SaveClass
        with open(target, 'w') as F:
            json.dump(data, F, indent=4)
        print(f"Data saved successfully to {target}")
    except Exception as E: #Error handling
        print(f"Error saving data: {E}")

def load_data(path: Optional[str] = None) -> List[ClassProfile]: #load data from file
    target = path or file #file to load from
    if not os.path.exists(target): #if no file found
        # Changed print message to match your original output
        print(f"no data found at {target}")
        return []
    try: #Open file to read data
        with open(target, 'r') as f:
            data = json.load(f)
            # Use the aliased LoadClass
            classes = [ClassProfile.LoadClass(_) for _ in data] 
            print(f"Data loaded from {target}")
            return classes
    except Exception as E: #If open fails
        print(f"Error loading: {E}")
        return []
    
def ClassOp(profile: ClassProfile): #Update class information (Save/Overwrite)
    classes = load_data() #get all classes
    rep = False #track if data has been updated
    for x, y in enumerate(classes):#check for duplicate classes
        # Use class_name attribute
        if y.class_name == profile.class_name:
            classes[x] = profile # Overwrite the existing class
            rep = True
            break
    if not rep:
        classes.append(profile) #add new class
    save_data(classes) #Save all data back

def deleteClass(name: str) -> bool: #delete a class
    classes = load_data()
    # Use class_name attribute
    add = [_ for _ in classes if _.class_name != name]
    if len(add) == len(classes):
        return False # Class not found
    save_data(add)
    return True

def listClasses() -> List[str]: #list all classes
    # Use class_name attribute
    return [_.class_name for _ in load_data()]
def import_data(path: str) -> List[ClassProfile]:
    return load_data(path)

def export_data(profile: ClassProfile, path: str):
    save_data([profile], path)