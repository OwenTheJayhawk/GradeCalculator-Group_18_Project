class Category:
    #Represents a weighted grading category (e.g., Homework).
    def __init__(self, name: str, weight: float):
        # Requirement: Weighted Grades (Assign a percentage weight)
        self.name = name
        self.weight = self._validate_weight(weight)
        self.assignments = [] # Holds a list of Assignment objects

    def _validate_weight(self, weight: float) -> float:
        #Helper to ensure weights are valid percentages. Part of Requirement 5.
        if not (0.0 <= weight <= 100.0):
            raise ValueError(f"Weight for '{self.name}' must be between 0 and 100.")
        return weight / 100.0 # Store as a decimal (0.40 for 40%)

    def add_assignment(self, assignment: Assignment):
        #Adds an assignment to this category.
        # Requirement: Core Functionality (Input assignment data into categories)
        self.assignments.append(assignment)

    def get_category_score(self) -> dict:
        #Calculates the total points and percentage for the category.
        total_earned = sum(a.points_earned for a in self.assignments)
        total_possible = sum(a.points_possible for a in self.assignments)

        if total_possible == 0:
            return {"earned": 0, "possible": 0, "percentage": 0.0}

        percentage = (total_earned / total_possible) * 100
        return {
            "earned": total_earned,
            "possible": total_possible,
            "percentage": percentage
        }

    def get_weighted_contribution(self) -> float:
        #Calculates how many points this category contributes to the final grade.
        category_score = self.get_category_score()
        # weighted_contribution = Category_Percentage * Category_Weight
        return (category_score["percentage"] / 100.0) * self.weight