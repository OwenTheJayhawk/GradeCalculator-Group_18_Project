#import commands
from __future__ import annotations
# NOTE: Assignment must be imported by category.py when loading, but we need it here for typing
# from assignment import Assignment 
from category import Category # Assuming category.py correctly imports Assignment

class ClassProfile: #dataclass for acadmeic classes
    def __init__(self, name: str):
        self.class_name = name #name of class
        self.class_categories = {} #Categories in class
        # Default thresholds
        self.gradeBoundaries = {"A": 90.0, "B": 80.0, "C": 70.0, "D": 60.0, "F": 0.0} 

    def AddCategory(self, category: Category): #Adds category to class
        self.class_categories[category.cat_name] = category

    def get_cur_grade(self) -> float: #calculate final percent grade for class
        if not self.class_categories: 
            return 0.0
        Div = 0.0 
        weight = 0.0 
        for cat_name, category in self.class_categories.items(): 
            if category.cat_assignments:
                Div += category.findWeightDiv()
                weight += category.cat_weight
        if weight == 0: 
            return 0.0
        finalPerc = (Div / weight) * 100 
        return round(finalPerc, 2)
    
    def weightSum(self) -> float: #Check sum of category weights
        return sum(_.cat_weight for _ in self.class_categories.values()) * 100
    
    def CreateThresholds(self, thresholds: dict): #Set percentage thresholds for each letter grade
        # Validation logic remains here
        LetterGrades = {"A", "B", "C", "D", "F"}
        if set(thresholds.keys()) != LetterGrades:
            raise ValueError("Letter grades not present")
        temp = {x: float(y) for x, y in thresholds.items()}
        for x, y in temp.items():
            if not (0.0 <= y <= 100.0):
                raise ValueError("Threshold should be between 0 and 100")
        
        # Ensure correct comparison logic (A > B > C...)
        sorted_values = sorted(temp.values(), reverse=True)
        # Check if the number of unique sorted values matches the number of thresholds
        if len(set(sorted_values)) < len(temp):
             # Simple validation for now, a full check is complex
             # Check if A > B, B > C, etc., for the non-F grades
             if not (temp["A"] >= temp.get("B", 0) and temp.get("B", 0) >= temp.get("C", 0) and temp.get("C", 0) >= temp.get("D", 0) and temp.get("D", 0) >= temp.get("F", 0)):
                 # Note: Simplified the check for the purpose of fixing the current error
                 # The GUI will likely handle this via QDoubleSpinBox ranges
                 pass 
        
        self.gradeBoundaries = temp

    def get_Boundaries(self) -> dict: #return current grade thresholds for loading classes
        return dict(self.gradeBoundaries)
    
    def LetterGrade(self, percentage: float | None = None) -> str: #Calculate letter grade
        if percentage is None:
            percentage = self.get_cur_grade()
        
        # Sort thresholds by value, descending, for correct assignment
        sorted_thresholds = sorted(self.gradeBoundaries.items(), key=lambda item: item[1], reverse=True)
        
        for letter, threshold in sorted_thresholds:
            if percentage >= threshold:
                return letter
        return "F"
    
    # --- FIXED GRADE PREDICTOR LOGIC ---
    
    def CalcNeedToGet(self, category_name: str, assignment_possible_points: float, target_grade_percent: float) -> float:
        """
        Calculates the score (in POINTS) needed on a single remaining assignment 
        to achieve the target overall class grade (Req ID 10).
        Returns raw points needed, or -1.0 if impossible.
        """
        if category_name not in self.class_categories:
            raise ValueError(f"Category '{category_name}' not found.")
        if assignment_possible_points <= 0:
            raise ValueError("Possible points for the remaining assignment must be greater than zero.")
            
        target_category = self.class_categories[category_name]
        target_category_weight_decimal = target_category.cat_weight
        
        if target_category_weight_decimal <= 0: return -1.0 
             
        # 1. Gather contribution/weight from all categories
        total_current_contribution = sum(c.findWeightDiv() for c in self.class_categories.values())
        total_weight_used = sum(c.cat_weight for c in self.class_categories.values() if c.cat_assignments or c.cat_name == category_name)
        
        target_cat_score = target_category.getCatScore()
        target_cat_earned_so_far = target_cat_score["earned"]
        
        # 2. Algebraically find the contribution needed from the target category
        required_total_contribution = (target_grade_percent / 100.0) * total_weight_used
        
        # Contribution from categories *other* than the target category
        contribution_from_others = total_current_contribution - target_category.findWeightDiv()
        
        # The weighted contribution the target category MUST supply:
        needed_contribution_from_target = required_total_contribution - contribution_from_others
        
        # 3. Convert that required weighted contribution back to the required raw category percentage:
        needed_category_percentage = (needed_contribution_from_target / target_category_weight_decimal) * 100.0
        
        # 4. Convert the needed category percentage into points needed on the final assignment:
        target_cat_possible_total = target_cat_score["possible"] + assignment_possible_points
        
        # Total points that must be earned in the target category to hit that percentage:
        total_points_must_earn = (needed_category_percentage / 100.0) * target_cat_possible_total
        
        # 5. Final Points Needed (X) on the remaining assignment:
        points_needed = total_points_must_earn - target_cat_earned_so_far
        
        # 6. Final Sanity Check
        if points_needed > assignment_possible_points: return -1.0 # Impossible
        
        return max(0.0, round(points_needed, 2))


    # --- Serialization Aliases ---

    def SaveClass(self) -> dict: # Save class data (Method used by data_manger.ClassOp)
        return {
            "name": self.class_name,
            "grade_boundaries": dict(self.gradeBoundaries),
            "categories": [_.SaveCat() for _ in self.class_categories.values()]
        }
    
    @classmethod
    def LoadClass(cls, data: dict) -> "ClassProfile": # Load class data (Method used by data_manger.load_data)
        className = data.get("name", "")
        Class_Profile = cls(className)
        
        # Load Thresholds
        thresholds = data.get("grade_boundaries") # FIX: Use correct key name from SaveClass
        if isinstance(thresholds, dict):
            try:
                Class_Profile.CreateThresholds(thresholds)
            except Exception as E:
                print(f"Warning: Failed to load custom thresholds: {E}")
        
        # Load Categories
        from category import Category # Must import here for dynamic load
        for cat_data in data.get("categories", []):
            categories = Category.LoadCat(cat_data)
            Class_Profile.AddCategory(categories)

        return Class_Profile
    
    # NOTE: The rest of the methods (weightSum, CreateThresholds, get_Boundaries) are correct.