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
        
        print(f"""
============================{self.name}===================================
{prompt}
--------------------------------------------------------------------------                     
{self.instructions}


{self.tools}
----------------------------   ...   -------------------------------------
        """)
        
    def show_response(self, prompt, response):
        print(f"""
============================{self.name}===================================
{prompt}
--------------------------------------------------------------------------                     
{self.instructions}


{self.tools}
--------------------------------------------------------------------------

{response}
==========================end {self.name}=================================
        """)
class UnTask2Goal(GDA):
    def __init__(self, knowledge: Knowledge, child_agents: List["Goal2Task"]=[]):
        tools = tools = [function_tool(agent.forward) for agent in child_agents]
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
        self.knowledge = knowledge
        instructions = f"{knowledge.distill(2)}, translate the goal into a task. Keep them informal, brief, and abstract. In your final response (and not as the argument of your tool calls), give a brief description of the status of the progress towards your assigned goal. Do not decompose the task. You are merely performing a slight shift of goal -> task."
        super().__init__(
            name="goal2tasker",
            instructions=instructions,
            tools=tools
        )
    
    async def forward(self, prompt: str) -> str:
        """Turns the goal into tasks. Give your goal to this agent."""
        result = await self.run(prompt)
        return result.final_output

class Task2Task(GDA):
    def __init__(self, knowledge: Knowledge):
        tools = [function_tool(mode) for mode in knowledge.modes]
        self.knowledge = knowledge
        instructions = f"{knowledge.distill(0)}, call your tools to fulfill the tasks the best you can. ONLY use your tools. If there's any discrepency between what you're 'assigned' to do and what you can do, return that. Otherwise return something simple, like 'Success' - but don't return 'Success' if you have not sufficiently completed the tasks requested of you. Be clever, but don't lie. Get creative, and don't be a perfectionist."
        super().__init__(
            name="task2tasker",
            instructions=instructions,
            tools=tools
        )

    async def forward(self, prompt: str) -> str:
        """Turns the task into actual actions that the system is capable of doing. Call this agent with your outputs tasks."""
        result = await self.run(prompt)
        return result.final_output
