class Assignment:
    #Represents a single graded item within a category.
    def __init__(self, name: str, earned: float, possible: float):
        # Requirement: Core Functionality (Input assignment names, points earned, and total points possible)
        self.name = name
        # validate/set possible first so earned validation can reference it
        self.points_possible = self._validate_score(possible, is_possible=True)
        self.points_earned = self._validate_score(earned)

    def _validate_score(self, score: float, is_possible: bool = False) -> float:
        #Helper to ensure scores are non-negative.
        if score < 0:
            raise ValueError(f"Score for '{self.name}' cannot be negative.")
        # Only compare against points_possible if it has already been set
        if not is_possible and hasattr(self, "points_possible") and score > self.points_possible:
             print(f"Warning: Earned points ({score}) exceed possible points ({self.points_possible}) for {self.name}.")
        return score

    def get_percentage(self) -> float:
        #Calculates the percentage score for this single assignment.
        if self.points_possible == 0:
            return 0.0  # Avoids division by zero
        return (self.points_earned / self.points_possible) * 100
