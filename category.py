from __future__ import annotations

from assignment import Assignment


class Category:
    
    def __init__(self, name: str, weight: float):
        
        self.name = name
        self.weight = self._validate_weight(weight)
        self.assignments = [] 

    def _validate_weight(self, weight: float) -> float:
       
        if not (0.0 <= weight <= 100.0):
            raise ValueError(f"Weight for '{self.name}' must be between 0 and 100.")
        return weight / 100.0 # Store as a decimal (0.40 for 40%)

    def add_assignment(self, assignment: Assignment):
        
        self.assignments.append(assignment)

    def get_category_score(self) -> dict:
        
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
        
        category_score = self.get_category_score()
        return (category_score["percentage"] / 100.0) * self.weight

    def to_dict(self) -> dict:
        """Serialize category to a plain dict. Weight is stored as percentage (0-100) to match UI."""
        return {
            "name": self.name,
            "weight": float(self.weight * 100.0),
            "assignments": [a.to_dict() for a in self.assignments],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Category":
        
        name = data.get("name", "")
        weight = float(data.get("weight", 0.0))
        cat = cls(name, weight)
        for a in data.get("assignments", []):
            
            cat.add_assignment(Assignment.from_dict(a))
        return cat
