from typing import List

from agents import Agent, Runner, function_tool

from knowledge import Knowledge

"""
These agents compute according to their set up within a Goal-Directed Agent

UnTask2Goal
    V
Goal2Task
    V
Task2Task
    V
Mode calls
"""

class GDA(Agent):
    def __init__(self, name: str, instructions: str, tools: List = []):
        super().__init__(
            name=name,
            instructions=instructions,
            tools=tools,
            model="o3-mini"
        )

class UnTask2Goal(GDA):
    def __init__(self, knowledge: Knowledge, child_agents: List["Goal2Task"]=[]):
        tools = [agent.as_tool(tool_name="goal2tasker", tool_description="Turns the goal into tasks. Give your goal to this agent.") for agent in child_agents]
        super().__init__(
            name="untask2goaler",
            instructions=f"{knowledge.distill(3)}, translate the goal into an actionable goal. Do not include the steps to reach that goal. You are an LLM in a network of Agents. Assume that some other Agent will find steps to get to the goal.",
            tools=tools
        )
    
    async def forward(self, prompt: str):
        result = await Runner.run(self, f"{prompt}")
        return result.final_output

class Goal2Task(GDA):
    def __init__(self, knowledge: Knowledge, child_agents: List["Task2Task"]=[]):
        tools = [agent.as_tool(tool_name="task2tasker", tool_description="Turns the task into actual actions that the system is capable of doing. Call this agent with your outputs tasks.") for agent in child_agents]
        super().__init__(
            name="goal2tasker",
            instructions=f"{knowledge.distill(3)}, translate the goal into one or more tasks. Keep them simple, brief, and abstract. In your final response (and not as the argument of your tool calls), give a brief description of the status of the progress towards your assigned goal.",
            tools=tools
        )

    async def forward(self, prompt: str):
        result = await Runner.run(self, f"{prompt}")
        return result.final_output

class Task2Task(GDA):
    def __init__(self, knowledge: Knowledge):
        tools = [function_tool(mode) for mode in knowledge.modes]
        super().__init__(
            name="task2tasker",
            instructions=f"{knowledge.distill(0)}, call your tools to fulfill the tasks the best you can. ONLY use your tools. If there's any discrepency between what you're 'assigned' to do and what you can do, return that. Otherwise return something simple, like 'Success' - but don't return 'Success' if you have not sufficiently completed the tasks requested of you. Be clever, but don't lie. Get creative, and don't be a perfectionist.",
            tools=tools
        )

    async def forward(self, prompt: str):
        result = await Runner.run(self, f"{prompt}")
        return result.final_output