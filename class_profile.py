from assignment import Assignment 

class ClassProfile:
    ##Represents a single course the student is taking.
    def __init__(self, name: str):
        # Requirement: Core Functionality (Input class name)
        self.name = name
        self.categories = {} # Dictionary: {category_name: Category_object}

    def to_dict(self) -> dict:
        #Converts the ClassProfile object to a dictionary for saving.
        return {
            "name": self.name,
            "categories": [c.to_dict() for c in self.categories.values()]
        }

    @classmethod
    def from_dict(cls, data: dict):
        #Creates a ClassProfile object from a dictionary, recreating all categories.
        class_profile = cls(name=data["name"])
        # NOTE: Category class must be imported here
        from category import Category
        for c_data in data["categories"]:
            class_profile.add_category(Category.from_dict(c_data))
        return class_profile
    
    # --- START UPDATED LOGIC ---

    def get_letter_grade(self, percentage: float) -> str:
        """Converts a numerical percentage to a letter grade (Req ID 3)."""
        # Kept the original thresholds based on previous discussion
        if percentage >= 93.0:
            return "A"
        elif percentage >= 90.0:
            return "A-"
        elif percentage >= 87.0:
            return "B+"
        elif percentage >= 83.0:
            return "B"
        elif percentage >= 80.0:
            return "B-"
        elif percentage >= 77.0:
            return "C+"
        elif percentage >= 73.0:
            return "C"
        elif percentage >= 70.0:
            return "C-"
        elif percentage >= 60.0:
            return "D"
        else:
            return "F"
            
    def calculate_score_needed(self, category_name: str, assignment_possible_points: float, target_grade_percent: float) -> float:
        """
        Calculates the score (in points) needed on a single remaining assignment 
        to achieve the target overall class grade (Requirement 10).
        """
        if category_name not in self.categories:
            raise ValueError(f"Category '{category_name}' not found.")
        if assignment_possible_points <= 0:
            raise ValueError("Possible points for the remaining assignment must be greater than zero.")
            
        target_category = self.categories[category_name]
        target_category_weight_decimal = target_category.weight
        
        # 1. Calculate total weighted contribution from all *currently graded* items (excluding the remaining assignment)
        completed_contribution = 0.0
        total_weight_used = 0.0

        for category in self.categories.values():
            contribution = category.get_weighted_contribution()
            completed_contribution += contribution
            if category.assignments:
                total_weight_used += category.weight
        
        # 2. Extract current score data for the target category
        target_cat_score = target_category.get_category_score()
        target_cat_earned_so_far = target_cat_score["earned"]
        target_cat_possible_so_far = target_cat_score["possible"]
        
        # 3. Algebraically solve for the points needed (X) in the target category.
        
        # Total Possible Points in target category *with* the new assignment
        target_cat_possible_total = target_cat_possible_so_far + assignment_possible_points
        
        # Target contribution needed from the final assignment itself to meet the goal:
        # The goal is: (Total Earned + X) / (Total Possible + Final Possible) * Target Weight = Needed Contribution
        
        # New Target Final Grade (as decimal)
        target_grade_decimal = target_grade_percent / 100.0
        
        # The equation we are solving for X (points needed on the final assignment):
        # (Completed Contribution - (Target Category's current weighted contribution)) 
        #   + (((Target Cat Earned + X) / Target Cat Possible Total) * Target Weight) = Target Grade Decimal * Total Weight Used
        
        # 3a. Calculate the portion of the target grade that MUST come from the target category:
        target_category_current_contribution = target_category.get_weighted_contribution()
        
        # This is the contribution we need from the target category, regardless of its current score:
        # (Target Grade Decimal * Total Weight Used) - (All Other Categories' Contribution)
        target_needed_contribution = (target_grade_decimal * total_weight_used) - (completed_contribution - target_category_current_contribution)
        
        if target_category_weight_decimal == 0:
             return -1.0 # Cannot solve if target category has zero weight
             
        # 3b. Convert that required weighted contribution back to the required raw category percentage:
        needed_category_percentage = (target_needed_contribution / target_category_weight_decimal) * 100.0
        
        if needed_category_percentage < 0:
            return 0.0 # Target grade is already achieved
        
        # 3c. Convert the needed category percentage into points needed on the final assignment:
        # Points Needed (X) = ((Needed Category % / 100) * Target Cat Possible Total) - Target Cat Earned So Far
        points_needed = ((needed_category_percentage / 100.0) * target_cat_possible_total) - target_cat_earned_so_far
        
        # 4. Final Sanity Check: return -1.0 if impossible, otherwise return needed points (min 0)
        if points_needed > assignment_possible_points:
            return -1.0 # Impossible
        
        return max(0.0, round(points_needed, 2))
        
    def calculate_what_if_grade(self, category_name: str, new_earned: float, new_possible: float) -> float:
        # ... (Existing What-If logic remains unchanged)
        
        if category_name not in self.categories:
            raise ValueError(f"Category '{category_name}' not found.")

        # NOTE: Assignment class must be imported here if this method is called independently
        from assignment import Assignment 

        # --- Setup the temporary hypothetical assignment list ---
        target_category = self.categories[category_name]
        
        # Create a list of assignments including the hypothetical one
        temp_assignments_list = target_category.assignments + [
            Assignment("Hypothetical", new_earned, new_possible)
        ]
        
        total_contribution = 0.0
        total_weight_used = 0.0

        for name, category in self.categories.items():
            current_category_weight = category.weight
            
            if name == category_name:
                # Calculate category score using the hypothetical data
                cat_earned = sum(a.points_earned for a in temp_assignments_list)
                cat_possible = sum(a.points_possible for a in temp_assignments_list)
                
                cat_percentage = (cat_earned / cat_possible) * 100 if cat_possible > 0 else 0.0
                
                total_contribution += (cat_percentage / 100.0) * current_category_weight
                total_weight_used += current_category_weight
            
            else:
                # Use the original (completed) category scores for all other categories
                contribution = category.get_weighted_contribution()
                total_contribution += contribution
                
                # Only include the category's weight if it has assignments (as per Sprint 1 logic)
                if category.assignments:
                    total_weight_used += current_category_weight

        # Final grade normalization
        if total_weight_used == 0:
            return 0.0
        
        return round((total_contribution / total_weight_used) * 100, 2)

    def add_category(self, category: 'Category'):
        #Adds a grading category to the class profile.
        self.categories[category.name] = category

    def calculate_current_grade(self) -> float:
        #Calculates the final weighted percentage for the entire class.
        if not self.categories:
            return 0.0

        total_contribution = 0.0
        total_weight_used = 0.0

        for category_name, category in self.categories.items():
            # Only count categories with assignments for weight normalization (common practice)
            if category.assignments:
                total_contribution += category.get_weighted_contribution()
                total_weight_used += category.weight

        # Normalize the grade based on weights of categories that HAVE assignments
        if total_weight_used == 0:
            return 0.0 # No assignments or weights were provided

        # Grade is the sum of weighted contributions divided by the total weight of *graded* categories.
        final_percentage = (total_contribution / total_weight_used) * 100
        return round(final_percentage, 2)

    def get_total_declared_weight(self) -> float:
        #Checks the sum of all category weights. 
        return sum(c.weight for c in self.categories.values()) * 100 