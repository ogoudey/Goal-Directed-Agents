class Morphology:
    def __init__(self):
        pass

class SO101(Morphology):
    def __init__(self):
        super().__init__()

    def __repr__(self):
        return f"An SO-101 robot from Huggingface's Lerobot"
    
class AutonomousBoat(Morphology):
    def __init__(self):
        super().__init__()

    def __repr__(self):
        return f"An autonomous sailboat"

class Combination(Morphology):
    def __init__(self, morph1: Morphology, morph2: Morphology, relationAB: str="on"):
        super().__init__()
        self.morphology1 = morph1
        self.morphology2 = morph2
        self.relation = relationAB
    
    def __repr__(self):
        return f"{self.morphology1} {self.relation} {self.morphology2}"

