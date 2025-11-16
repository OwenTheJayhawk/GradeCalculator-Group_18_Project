#import commands
from __future__ import annotations
from category import Category

class ClassProfile: #dataclass for acadmeic classes
    def __init__(self, name: str):
        self.class_name = name #name of class
        self.class_categories = {} #Categories in class
        self.gradeBoundaries = {"A": 90.0, "B": 80.0, "C": 70.0, "D": 60.0, "F": 0.0} #grade thresholds assigned to class

    def AddCategory(self, category: Category): #Adds category to class
        self.class_categories[category.cat_name] = category

    def get_cur_grade(self) -> float: #calculate final percent grade for class
        if not self.class_categories: #return 0 if no categories
            return 0.0
        Div = 0.0 #Division of grades added
        weight = 0.0 #track how much weight has been used
        for cat_name, category in self.class_categories.items(): #iterate through categories
            if category.cat_assignments:
                Div += category.findWeightDiv()
                weight += category.cat_weight
        if weight == 0: #if weight is zero, omit
            return 0.0
        finalPerc = (Div / weight) * 100 #calculate final percentage grade
        return round(finalPerc, 2) #round grade for simplicity
    
    def weightSum(self) -> float: #Check sum of category weights
        return sum(_.cat_weight for _ in self.class_categories.values()) * 100
    
    def CreateThresholds(self, thresholds: dict): #Set percentage thresholds for each letter grade
        LetterGrades = {"A", "B", "C", "D", "F"} #letter grades
        if set(thresholds.keys()) != LetterGrades: #Make sure all letter grades are present
            raise ValueError("Letter grades not present")
        temp = {x: float(y) for x, y in thresholds.items()} #convert values to float and check validity
        for x, y in temp.items():
            if not (0.0 <= y <= 100.0): #Throw error if value not in feasible range
                raise ValueError("Threshold should be between 0 and 100")
        if not (temp["A"] > temp["B"] > temp["C"] > temp["D"] >= temp["F"]): #throw error if thresholds overlap with each other
            raise ValueError("Thresholds must fit A > B > C > D >= F")
        self.gradeBoundaries = temp

    def get_Boundaries(self) -> dict: #return current grade thresholds for loading classes
        return dict(self.gradeBoundaries)
    
    def LetterGrade(self, percentage: float | None = None) -> str: #Calculate letter grade
        if percentage is None: #unchanging grade
            percentage = self.get_cur_grade()
        for _ in ["A", "B", "C", "D", "F"]: #iterate through thresholds to find correct letter grade
            if percentage >= self.gradeBoundaries[_]:
                return _
        return "F"
    
    def SaveClass(self) -> dict: #Save class data
        return {
            "name": self.class_name,
            "grade_thresholds": dict(self.gradeBoundaries),
            "categories": [_.SaveCat() for _ in self.class_categories.values()]
        }
    
    @classmethod
    def LoadClass(cls, data: dict) -> "ClassProfile": #load class data
        className = data.get("name", "")
        Class_Profile = cls(className)
        thresholds = data.get("grade_thresholds")
        if isinstance(thresholds, dict):
            try:
                Class_Profile.CreateThresholds(thresholds)
            except Exception:
                pass
        for _ in data.get("categories", []):
            categories = Category.LoadCat(_)
            Class_Profile.AddCategory(categories)

        return Class_Profile
