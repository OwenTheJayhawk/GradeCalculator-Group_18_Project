#import functions
from __future__ import annotations
from assignment import Assignment

class Category: #data class for category of assignment which has associated percentage weight
    def __init__(self, name: str, weight: float): #initialize class values
        self.cat_name = name #class name
        self.cat_weight = self.check_weight(weight) #class percentage weight
        self.cat_assignments = [] #assignments in class

    def check_weight(self, weight: float) -> float: #verify that weight is valid
        if not (0.0 <= weight <= 100.0):
            raise ValueError("Category weight must be between 0 and 100")
        return weight / 100.0
    
    def AddAssignment(self, assingment: Assignment): #Add assignment to category
        self.cat_assignments.append(assingment)

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
        return {
            "name": self.cat_name,
            "weight": float(self.cat_weight * 100),
            "assignments": [_.SaveCat() for _ in self.cat_assignments],
        }
    
    @classmethod
    def LoadCat(cls, data: dict) -> "Category": #load category data
        category_name = data.get("name", "")
        category_weight = float(data.get("weight", 0.0))
        category = cls(category_name, category_weight)
        for _ in data.get("assignments", []):
            category.AddAssignment(Assignment.LoadCat(_))
        return category
