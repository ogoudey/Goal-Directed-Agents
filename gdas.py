from typing import List

from agents import Agent, Runner, function_tool

from knowledge import Knowledge

from logger import log

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
    parent: "GDA"
    def __init__(self, name: str, instructions: str, tools: List = []):
        self.name = name
        self.instructions = instructions
        self.tools = tools
        super().__init__(
            name=name,
            instructions=instructions,
            tools=tools,
            model="o3-mini"
        )
    
    async def run(self, prompt:str):
        self.show_disposition(prompt)
        result = await Runner.run(self, prompt)
        self.show_response(prompt, result.final_output)
        return result
        
        
    def show_disposition(self, prompt: str):
        log(f"""\n\n\n\n\n\n\n\n\n
============================{self.name}===================================
{prompt}
--------------------------------------------------------------------------                     
{self.instructions}


{[tool.name for tool in self.tools]}
                                ...   
        """, self.name)
        
    def show_response(self, prompt, response):
        log(f"""
{prompt}
--------------------------------------------------------------------------                     
{self.instructions}


{[tool.name for tool in self.tools]}
--------------------------------------------------------------------------

{response}
==========================end {self.name}=================================
        """, self.name)
class UnTask2Goal(GDA):
    def __init__(self, knowledge: Knowledge, child_agents: List["Goal2Task"]=[]):
        tools = [function_tool(agent.forward) for agent in child_agents]
        for agent in child_agents:
            agent.parent = self
        instructions = f"{knowledge.distill(2)}, translate the goal into an actionable goal. Do not include the steps to reach that goal. You are an LLM in a network of Agents. You must call the next agent with something."
        super().__init__(
            name="untask2goaler",
            instructions=instructions,
            tools=tools
        )
    
    async def forward(self, prompt: str) -> str:
        result = await self.run(prompt)
        return result.final_output

class Goal2Task(GDA):
    def __init__(self, knowledge: Knowledge, child_agents: List["Task2Task"]=[]):
        tools = [function_tool(agent.forward) for agent in child_agents]
        for agent in child_agents:
            agent.parent = self
        self.knowledge = knowledge
        instructions = f"{knowledge.distill(2)}, translate the goal into a task and give it to the next Agent. You are an LLM in a network of Agents. Keep the tasks informal, brief, and abstract. In your final response (and not as the argument of your tool calls), give a brief description of the status of the progress towards your assigned goal. Do not decompose the task. You are merely performing a slight shift of goal -> task."
        super().__init__(
            name="goal2tasker",
            instructions=instructions,
            tools=tools
        )
    
    async def forward(self, prompt: str) -> str:
        """Turns the goal into tasks. Give your goal to this agent."""
        log(f"{self.name}({prompt})", self.parent.name)
        result = await self.run(prompt)
        log(f"{self.name}({prompt}) => {result.final_output}", self.parent.name)
        return result.final_output

class Task2Task(GDA):
    def __init__(self, knowledge: Knowledge):
        tools = [function_tool(mode) for mode in knowledge.modes]
        self.knowledge = knowledge
        instructions = f"{knowledge.distill(0)}, call your tools to fulfill the tasks the best you can. Turn the abstract task into something you can do. ONLY use your tools. If there's any discrepency between what you're 'assigned' to do and what you can do, return that. Otherwise return something simple, like 'Success' - but don't return 'Success' if you have not sufficiently completed the tasks requested of you. Be clever, but don't lie. Get creative, and don't be a perfectionist."
        super().__init__(
            name="task2tasker",
            instructions=instructions,
            tools=tools
        )

    async def forward(self, prompt: str) -> str:
        """Turns the task into actual actions that the system is capable of doing. Call this agent with your outputs tasks."""
        log(f"{self.name}({prompt})", self.parent.name)
        result = await self.run(prompt)
        log(f"{self.name}({prompt}) => {result.final_output}", self.parent.name)
        return result.final_output
