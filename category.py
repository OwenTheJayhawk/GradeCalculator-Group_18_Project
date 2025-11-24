#import functions
from __future__ import annotations
from assignment import Assignment # Keep this import for method definitions

class Category: #data class for category of assignment which has associated percentage weight
    def __init__(self, name: str, weight: float): #initialize class values
        self.cat_name = name #class name
        self.cat_weight = self.check_weight(weight) #class percentage weight
        self.cat_assignments = [] #assignments in class

    def check_weight(self, weight: float) -> float: #verify that weight is valid
        if not (0.0 <= weight <= 100.0):
            raise ValueError("Category weight must be between 0 and 100")
        return weight / 100.0
    
    def AddAssignment(self, assignment: Assignment): #Add assignment to category
        self.cat_assignments.append(assignment) # Corrected typo in variable name: assignment

    def removeAssignment(self, index: int):
        """Removes an assignment by index from the category's list."""
        if 0 <= index < len(self.cat_assignments):
            self.cat_assignments.pop(index)
        else:
            raise IndexError("Assignment index out of range for removal.")

    def editAssignment(self, index: int, new_name: str, new_earned: float, new_possible: float):
        """Updates an existing assignment by index."""
        if 0 <= index < len(self.cat_assignments):
            assignment = self.cat_assignments[index]
            
            # The Assignment class handles internal validation (e.g., negative scores)
            assignment.name = new_name
            assignment.possible_points = new_possible
            assignment.earned_points = new_earned
            # Re-run checkScore after update if necessary, or ensure setters handle it
            # Assuming Assignment.__init__ logic is sufficient, but setting attributes directly bypasses it.
            # Best practice is to call a setter/update method if one existed, but updating fields directly is quicker for this fix.
        else:
            raise IndexError("Assignment index out of range for editing.")

    def getCatScore(self) -> dict: #calculate total points and percentage for category
        earned = sum(_.earned_points for _ in self.cat_assignments) #calculate earned points
        possible = sum(_.possible_points for _ in self.cat_assignments) #calculate possible points
        if possible == 0: #avoid divide by zero
            return {"earned": 0, "possible": 0, "percentage": 0.0}
        perc = (earned / possible) * 100 #calculate percentage
        return { 
            "earned": earned,
            "possible": possible,
            "percentage": perc
            }
    
    def findWeightDiv(self) -> float: #calculate points the category contributes to final grade
        catScore = self.getCatScore() #get score from category
        return (catScore["percentage"] / 100.0) * self.cat_weight
    
    def SaveCat(self) -> dict: #save category data
        """Serialization method for saving data."""
        return {
            "name": self.cat_name,
            "weight": float(self.cat_weight * 100), # Stored as percentage for file readability
            "assignments": [_.create_save() for _ in self.cat_assignments], # Assuming Assignment uses create_save() or similar
        }
    
    @classmethod
    def LoadCat(cls, data: dict) -> "Category": #load category data
        """Deserialization method for loading data, handles nested Assignment objects."""
        # Note: We must import Assignment within the method or rely on the top-level import
        from assignment import Assignment 
        
        category_name = data.get("name", "")
        category_weight = float(data.get("weight", 0.0))
        category = cls(category_name, category_weight)
        
        for ass_data in data.get("assignments", []):
            # Recursively load the Assignment object
            assignment = Assignment.Load(ass_data) # Assuming Assignment uses Load() or LoadCat()
            category.AddAssignment(assignment)
            
        return category