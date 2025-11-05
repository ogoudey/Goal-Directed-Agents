from typing import List

from modes import Mode
from morphologies import Morphology
from environments import Environment

class Knowledge:
    """
    Class describing the content that gets injected into agent context.
    
    Distillation is used for minimizing hyperspecificity higher in the orchestration.
    """
    def __init__(self, modes: List[Mode], morph: Morphology, env: Environment):
        self.modes = modes
        self.morphology = morph
        self.environment = env

    def distill(self, level: int=0):
        return {
            0: f"Given that you are {self.morphology} in {self.environment}",
            1: f"Given that you are {self.morphology} in {self.environment}",
            2: f"Given that you are {self.morphology}",
            3: f"",
        }[level]

    def __repr__(self):
        return self.distill(0)
