class UnTaskable:
    """
    Input to a GDA Orchestra. A wrapper around a goal (string) intended to suggest the distinction of certain goals from tasks.
    """
    goal: str
    def __init__(self, goal: str):
        self.goal = goal

    def __repr__(self):
        return f"{self.goal}"