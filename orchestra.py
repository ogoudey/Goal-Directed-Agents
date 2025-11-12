from knowledge import Knowledge
from motives import UnTaskable

from gdas import Task2Task, Goal2Task, UnTask2Goal

from time import sleep

from logger import log
class GDAO:
    """
    Initializes the architecture of the orchestration
    """
    def __init__(self, knowledge: Knowledge):
        self.knowledge = knowledge

    async def orchestrate(self, untaskable: "UnTaskable"):
        task2tasker = Task2Task(self.knowledge)
        goal2tasker = Goal2Task(self.knowledge, [task2tasker])
        untask2goaler = UnTask2Goal(self.knowledge, [goal2tasker])

        print(f"Ultimate goal: {untaskable}")
        
        done = await untask2goaler.forward(f"{untaskable}")
        
    async def loop(self, untaskable: UnTaskable):
        task2tasker = Task2Task(self.knowledge)
        goal2tasker = Goal2Task(self.knowledge, [task2tasker])
        untask2goaler = UnTask2Goal(self.knowledge, [goal2tasker])

        while True:
            print(f"Poking untasker with {untaskable}")
            done = await untask2goaler.loop(f"{untaskable}")
            print(f"Waiting {untask2goaler.cycle_period} seconds...")
            sleep(untask2goaler.cycle_period)
  

    async def execute(self, untaskable: "UnTaskable"):
        print(f"Untaskable: {untaskable}")
        goal = await UnTask2Goal(self.knowledge).forward(f"{untaskable}")
        print(f"Goal: {goal}")
        task = await Goal2Task(self.knowledge).forward(goal)
        print(f"Task: {task}")
        executable = await Task2Task(self.knowledge).forward(task)
        print(f"Executable: {executable}")