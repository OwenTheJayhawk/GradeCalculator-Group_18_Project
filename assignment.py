class Assignment: #data class for adding assignment to class
    def __init__(self, name: str, earned: float, possible: float): #initalize values
        self.name = name #name of assignment
        self.possible_points = self.checkScore(possible, checkPoss = True) #points possible to earn on an assingment
        self.earned_points = self.checkScore(earned) #points earned on assingment

    def checkScore(self, score: float, checkPoss: bool = False) -> float: #check if score is possible
        if score < 0: #check for negative score
            raise ValueError("Cannot have negative score")
        if not checkPoss and hasattr(self, "possible_points") and score > self.possible_points: #check for invalid case of more points earned than possible
            print("Earned points greater that points possible")
        return score #return valid score
    
    def calcPerc_(self) -> float: #calculate percentage grade
        if self.possible_points == 0: #avoid divide by zero
            return 0.0
        return (self.earned_points / self.possible_points) * 100 #return percentage grade
    
    def create_save(self) -> dict: #save assignment data
        return {
            "name": self.name, 
            "points_earned": float(self.earned_points),
            "points_possible": float(self.possible_points),
        }
    
    @classmethod
    def Load(cls, data: dict) -> "Assignment": #load previous assingment data
        name = data.get("name", "")
        earned = float(data.get("points_earned", 0.0))
        possible = float(data.get("points_possible", 0.0))
        return cls(name, earned, possible)
