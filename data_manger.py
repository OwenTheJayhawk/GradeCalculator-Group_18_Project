#import statements
import json
import os
from typing import List, Optional
from class_profile import ClassProfile

file = "grade_data.json" #name of file to save data to

def save_data(classes: List[ClassProfile], path: Optional[str] = None): #Save Class data
    target = path or file #location to save to
    data = [_.SaveClass() for _ in classes] #data to be saved
    try: #open file to save to
        with open(target, 'w') as F:
            json.dump(data, F, indent=4)
        print(f"Data saved to {target}")
    except Exception as E: #Error handling
        print(f"Error saving: {E}")

def load_data(path: Optional[str] = None) -> List[ClassProfile]: #load data from file
    target = path or file #file to load from
    if not os.path.exists(target): #if no file found
        print(f"no data found at {target}")
        return []
    try: #Open file to read data
        with open(target, 'r') as f:
            data = json.load(f)
            classes = [ClassProfile.LoadClass(_) for _ in data]
            print("Data loaded")
            return classes
    except Exception as E: #If open fails
        print(f"Error loading: {E}")
        return []
    
def ClassOp(profile: ClassProfile): #Update class information
    classes = load_data() #get classes
    rep = False #track if data has been updated
    for x, y in enumerate(classes):#check for duplicate classes
        if y.class_name == profile.class_name:
            classes[x] = profile
            rep = True
            break
    if not rep:
        classes.append(profile) #add saved class
    save_data(classes) #Save data

def deleteClass(name: str) -> bool: #delete a class
    classes = load_data()
    add = [_ for _ in classes if _.class_name != name]
    if len(add) == len(classes):
        return False
    save_data(add)
    return True

def listClasses() -> List[str]: #list all classes
    return [_.name for _ in load_data()]

def import_data(path: str) -> List[ClassProfile]:
    return load_data(path)

def export_data(profile: ClassProfile, path: str):
    save_data([profile], path)
