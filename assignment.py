class Assignment:
   
    def __init__(self, name: str, earned: float, possible: float):
        
        self.name = name
        self.points_possible = self._validate_score(possible, is_possible=True)
        self.points_earned = self._validate_score(earned)

    def _validate_score(self, score: float, is_possible: bool = False) -> float:
        if score < 0:
            raise ValueError(f"Score for '{self.name}' cannot be negative.")
        
        if not is_possible and hasattr(self, "points_possible") and score > self.points_possible:
             print(f"Warning: Earned points ({score}) exceed possible points ({self.points_possible}) for {self.name}.")
        return score

    def get_percentage(self) -> float:
        
        if self.points_possible == 0:
            return 0.0  # Avoids division by zero
        return (self.points_earned / self.points_possible) * 100

    def to_dict(self) -> dict:
       
        return {
            "name": self.name,
            "points_earned": float(self.points_earned),
            "points_possible": float(self.points_possible),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Assignment":
        name = data.get("name", "")
        earned = float(data.get("points_earned", 0.0))
        possible = float(data.get("points_possible", 0.0))
        return cls(name, earned, possible)
