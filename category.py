class Category:
    #Represents a weighted grading category (e.g., Homework).
    def __init__(self, name: str, weight: float):
        # Requirement: Weighted Grades (Assign a percentage weight)
        self.name = name
        self.weight = self._validate_weight(weight)
        self.assignments = [] # Holds a list of Assignment objects

    def to_dict(self) -> dict:
        #Converts the Category object to a dictionary for JSON serialization.
        return {
            "name": self.name,
            "weight": self.weight * 100, # Store as percentage for readability
            "assignments": [a.to_dict() for a in self.assignments]
        }

    @classmethod
    def from_dict(cls, data: dict):
        #Creates a Category object from a dictionary, recreating assignments.
        # Use the stored percentage for weight to initialize
        category = cls(name=data["name"], weight=data["weight"]) 
        # Recreate nested Assignment objects
        for a_data in data["assignments"]:
            # NOTE: Assignment class must be imported here
            from assignment import Assignment 
            category.add_assignment(Assignment.from_dict(a_data))
        return category

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