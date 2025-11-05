from __future__ import annotations


class ClassProfile:
    ##Represents a single course the student is taking.
    def __init__(self, name: str):
        # Requirement: Core Functionality (Input class name)
        self.name = name
        self.categories = {} # Dictionary: {category_name: Category_object}

        # Grade thresholds in percent (default)
        # Keys: 'A','B','C','D','F' -> minimum percentage required for that letter
        self.grade_thresholds = {
            "A": 90.0,
            "B": 80.0,
            "C": 70.0,
            "D": 60.0,
            "F": 0.0
        }

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

    def set_grade_thresholds(self, thresholds: dict):
        """
        Replace grade thresholds. Expected keys: 'A','B','C','D','F' with numeric percentages 0-100.
        Validation ensures sensible ordering (A > B > C > D >= F) and values in range.
        """
        required_keys = {"A", "B", "C", "D", "F"}
        if set(thresholds.keys()) != required_keys:
            raise ValueError(f"Thresholds must include exactly these keys: {sorted(required_keys)}")

        # Convert values to float and validate range
        thr = {k: float(v) for k, v in thresholds.items()}
        for k, v in thr.items():
            if not (0.0 <= v <= 100.0):
                raise ValueError(f"Threshold for '{k}' must be between 0 and 100.")

        # Ensure descending order: A > B > C > D >= F and F == min (commonly 0)
        if not (thr["A"] > thr["B"] > thr["C"] > thr["D"] >= thr["F"]):
            raise ValueError("Thresholds must satisfy A > B > C > D >= F (and values within 0-100).")

        self.grade_thresholds = thr

    def get_grade_thresholds(self) -> dict:
        """Return a copy of current grade thresholds (percentages)."""
        return dict(self.grade_thresholds)

    def get_letter_grade(self, percentage: float | None = None) -> str:
        
        if percentage is None:
            percentage = self.calculate_current_grade()

        # Ensure checking from highest to lowest
        for letter in ["A", "B", "C", "D", "F"]:
            if percentage >= self.grade_thresholds[letter]:
                return letter
        return "F"
