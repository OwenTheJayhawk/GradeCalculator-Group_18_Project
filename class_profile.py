class ClassProfile:
    ##Represents a single course the student is taking.
    def __init__(self, name: str):
        # Requirement: Core Functionality (Input class name)
        self.name = name
        self.categories = {} # Dictionary: {category_name: Category_object}

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