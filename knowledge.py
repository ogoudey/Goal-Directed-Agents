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

        self.updates_from_child = ""
        self.is_fresh = False

    def distill(self, level: int=0):
        return {
            0: f"Given that you are {self.morphology} in the phsycal location of (continent, nation,... building, room #): {self.environment}",
            1: f"Given that you are {self.morphology} in {self.environment}",
            2: f"Given that you are {self.morphology}",
            3: f"",
        }[level] + \
        f"{self.updates_from_child}"

    def update(self, last_command: str, updates: str):
        self.updates_from_child = f"Last time you called \"{last_command}\", garnering this response: \"{updates}\""
        self.is_fresh = True
        return self.updates_from_child

    def __repr__(self):
        return self.distill(0)
