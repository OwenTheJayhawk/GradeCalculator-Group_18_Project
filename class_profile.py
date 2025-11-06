from __future__ import annotations

from category import Category


class ClassProfile:
    
    def __init__(self, name: str):
        
        self.name = name
        self.categories = {} # Dictionary: {category_name: Category_object}

        
        # Keys: 'A','B','C','D','F' -> minimum percentage required for that letter
        self.grade_thresholds = {
            "A": 90.0,
            "B": 80.0,
            "C": 70.0,
            "D": 60.0,
            "F": 0.0
        }

    def add_category(self, category: Category):
        
        self.categories[category.name] = category

    def calculate_current_grade(self) -> float:
        
        if not self.categories:
            return 0.0

        total_contribution = 0.0
        total_weight_used = 0.0

        for category_name, category in self.categories.items():
            
            if category.assignments:
                total_contribution += category.get_weighted_contribution()
                total_weight_used += category.weight

        
        if total_weight_used == 0:
            return 0.0 # No assignments or weights were provided

        
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

        
        thr = {k: float(v) for k, v in thresholds.items()}
        for k, v in thr.items():
            if not (0.0 <= v <= 100.0):
                raise ValueError(f"Threshold for '{k}' must be between 0 and 100.")

        
        if not (thr["A"] > thr["B"] > thr["C"] > thr["D"] >= thr["F"]):
            raise ValueError("Thresholds must satisfy A > B > C > D >= F (and values within 0-100).")

        self.grade_thresholds = thr

    def get_grade_thresholds(self) -> dict:
        
        return dict(self.grade_thresholds)

    def get_letter_grade(self, percentage: float | None = None) -> str:
        
        if percentage is None:
            percentage = self.calculate_current_grade()

        
        for letter in ["A", "B", "C", "D", "F"]:
            if percentage >= self.grade_thresholds[letter]:
                return letter
        return "F"

    def to_dict(self) -> dict:
        
        return {
            "name": self.name,
            "grade_thresholds": dict(self.grade_thresholds),
            "categories": [c.to_dict() for c in self.categories.values()],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ClassProfile":
        
        name = data.get("name", "")
        cp = cls(name)
        thr = data.get("grade_thresholds")
        if isinstance(thr, dict):
            try:
                cp.set_grade_thresholds(thr)
            except Exception:
                # If thresholds are malformed, keep defaults. GUI will show defaults.
                pass

        for c in data.get("categories", []):
            cat = Category.from_dict(c)
            cp.add_category(cat)

        return cp
