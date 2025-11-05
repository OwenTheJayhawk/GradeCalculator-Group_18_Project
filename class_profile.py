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
    
    def calculate_what_if_grade(self, category_name: str, new_earned: float, new_possible: float) -> float:
        
        #Calculates the projected grade if a hypothetical score is added 
        #to a specific category (Requirement 5 from the stack).
        
        if category_name not in self.categories:
            raise ValueError(f"Category '{category_name}' not found.")

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

    def add_category(self, category: Category):
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
