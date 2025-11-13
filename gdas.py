from typing import List
import threading
import asyncio
asyncio.get_event_loop().set_debug(True)
from agents import Agent, Runner, function_tool

from knowledge import Knowledge

from logger import log

import time

"""
These agents compute according to their set up within a Goal-Directed Agent

"""

class GDA(Agent):
    parent: "GDA"
    options: List

    prior_prompt: str
    prompt: str
    last_output: str | None

    def __init__(self, name: str, instructions: str, child_agents: List = []):
        self.name = name
        self.instructions = instructions
        self.child_agents = child_agents
        super().__init__(
            name=name,
            instructions=instructions,
            tools=[],
            model="o3-mini"
        )

        self.options = [] # a list of functions that can be used by parent agent

        self.cycle_period = 60 # 1bpm

        self.on = False
        self.prior_prompt = ""
        self.last_output = None
        self.running_threads = []
        

    def run_thread(self):
        log(f"Async task started for {self.name}.", f"THREAD_{self.name}")
        thread_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(thread_loop)

        while self.on:
            if self.prompt == self.prior_prompt:
                # unless timer?
                continue
            for agent in self.child_agents:
                child_options = [function_tool(option) for option in agent.options]
                if len(child_options) == len(self.tools): 
                    # assuming there's no change in tools given child options are the same length of current tools
                    break
                log(f"Extending {self.name}'s tools with options of {agent.name}.", f"THREAD_{self.name}")
                log(f"These options are: {child_options}.", f"THREAD_{self.name}")
                self.tools = []
                self.tools.extend(child_options)
                agent.parent = self
            self.show_disposition(self.prompt)
            log(f"{self.name}'s thread self-prompting with {self.prompt}.", f"THREAD_{self.name}")
            
            result = Runner.run_sync(self, self.prompt)
            self.prior_prompt = self.prompt
            #time.sleep(5)
            log(f"{self.name}'s thread setting last_output to {self.last_output}.", f"THREAD_{self.name}")
            
            self.last_output = result.final_output
            self.show_response(self.prompt, result.final_output)

    async def run(self):
        #run = asyncio.create_task(self.run_thread())
        run = threading.Thread(target=self.run_thread)
        self.running_threads.append(run)
        run.start()
        log(f"{self.name} is now running {len(self.running_threads)} async tasks.", f"DEBUG_{self.name}")
        #await asyncio.sleep(0)
        return f"{self.name} is now running."


    def show_disposition(self, prompt: str):
        log(f"""\n\n\n\n\n\n\n\n\n
============================{self.name}===================================
{prompt}
--------------------------------------------------------------------------                     
{self.instructions}


{[child.name for child in self.child_agents]}:{[tool.name for tool in self.tools]}
                                ...   
        """, self.name)
        
    def show_response(self, prompt, response):
        log(f"""
{prompt}
--------------------------------------------------------------------------                     
{self.instructions}


{[child.name for child in self.child_agents]}:{[tool.name for tool in self.tools]}
--------------------------------------------------------------------------

{response}
==========================end {self.name}=================================
        """, self.name)



class UnTask2Goal(GDA):
    def __init__(self, knowledge: Knowledge, child_agents: List["Goal2Task"]=[]):
        instructions = f"{knowledge.distill(2)}, translate the goal into an actionable goal. Do not include the steps to reach that goal. You are an LLM in a network of Agents. You must call the next agent with something."
        super().__init__(
            name="untask2goaler",
            instructions=instructions,
            child_agents = child_agents,
        )
        self.options.append(self.loop)

    async def loop(self, prompt: str):
        log(f"{self.name} was just poked with prompt {prompt}", f"DEBUG_{self.name}")
        self.prompt = prompt
        if self.on:
            if not self.last_output:
                log(f"{self.name} is on, but not output yet.", f"DEBUG_{self.name}")
                return f"Called before any output."
            log(f"{self.name} is on, returning {self.last_output}", f"DEBUG_{self.name}")
            return self.last_output
        else:
            log(f"{self.name} was off, turning on.", f"DEBUG_{self.name}")
            self.on = True
            return await self.run()

    def stop_me(self):
        for running_thread in self.running_threads:
            running_thread.join()
            log(f"A thread of {self.name} was stopped.", f"DEBUG_{self.name}")
        self.on = False
        return f"{self.name} is stopped. Most recent output: {self.last_output}"











class Goal2Task(GDA):
    def __init__(self, knowledge: Knowledge, child_agents: List["Task2Task"]=[]):
        for agent in child_agents:
            agent.parent = self
        self.knowledge = knowledge
        instructions = f"{knowledge.distill(2)}, translate the goal into a task and give it to the next Agent. You are an LLM in a network of Agents. Keep the tasks informal, brief, and abstract. In your final response (and not as the argument of your tool calls), give a brief description of the status of the progress towards your assigned goal. Do not decompose the task. You are merely performing a slight shift of goal -> task."
        super().__init__(
            name="goal2tasker",
            instructions=instructions,
            child_agents=child_agents,
        )
        self.options.append(self.loop)
        self.cycle_period = 30
        
    
    async def loop(self, prompt: str) -> str:
        """Turns the goal into tasks. Give your goal to this agent. Only call this once."""
        log(f"{self.name} was just poked with prompt {prompt}", f"DEBUG_{self.name}")
        self.prompt = prompt
        if self.on:
            log(f"{self.name} is on, returning {self.last_output}", f"DEBUG_{self.name}")
            return self.last_output
        else:
            log(f"{self.name} was off, turning on.", f"DEBUG_{self.name}")
            self.on = True
            self.options.append(self.stop_me)
            return await self.run()
        
    def stop_me(self):
        for running_thread in self.running_threads:
            running_thread.join()
            log(f"A thread of {self.name} was stopped.", f"DEBUG_{self.name}")
        self.on = False
        return f"{self.name} is stopped. Most recent output: {self.last_output}"



class Task2Task(GDA):
    def __init__(self, knowledge: Knowledge):
        self.knowledge = knowledge
        instructions = f"{knowledge.distill(0)}, call your tools to fulfill the tasks the best you can. Turn the abstract task into something you can do. ONLY use your tools. If there's any discrepency between what you're 'assigned' to do and what you can do, return that. Otherwise return something simple, like 'Success' - but don't return 'Success' if you have not sufficiently completed the tasks requested of you. Be clever, but don't lie. Get creative, and don't be a perfectionist."
        super().__init__(
            name="task2tasker",
            instructions=instructions,
        )

        self.options.append(self.loop)
        self.cycle_period = 5

    async def loop(self, prompt: str) -> str:
        """Turns the goal into tasks. Give your goal to this agent. Only call this once."""
        log(f"{self.name} was just poked with prompt {prompt}", f"DEBUG_{self.name}")
        self.prompt = prompt
        if self.on:
            log(f"{self.name} is on, returning {self.last_output}", f"DEBUG_{self.name}")
            return self.last_output
        else:
            log(f"{self.name} was off, turning on.", f"DEBUG_{self.name}")
            self.on = True
            self.options.append(self.stop_me)
            return await self.run()

    def stop_me(self):
        for running_thread in self.running_threads:
            running_thread.join()
            log(f"A thread of {self.name} was stopped.", f"DEBUG_{self.name}")
        self.on = False
        return f"{self.name} is stopped. Most recent output: {self.last_output}"

    def run_thread(self):
        log(f"Async task started for {self.name}.", f"THREAD_{self.name}")
        thread_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(thread_loop)

        while self.on:
            if self.prompt == self.prior_prompt:
                # unless timer?
                continue
            for agent in self.child_agents:
                log(f"Modes: {len(self.knowledge.modes)}. Tools: {self.tools}.", f"THREAD_{self.name}")
                if len(self.knowledge.modes) == len(self.tools): 
                    # assuming there's no change in tools given child options are the same length of current tools
                    break
                self.tools = [function_tool(mode) for mode in self.knowledge.modes]
                log(f"Updating {self.name}'s tools to {self.tools}.", f"THREAD_{self.name}")
                agent.parent = self
            self.show_disposition(self.prompt)
            log(f"{self.name}'s thread self-prompting with {self.prompt}.", f"THREAD_{self.name}")
            
            result = Runner.run_sync(self, self.prompt)
            self.prior_prompt = self.prompt
            #time.sleep(5)
            log(f"{self.name}'s thread setting last_output to {self.last_output}.", f"THREAD_{self.name}")
            
            self.last_output = result.final_output
            self.show_response(self.prompt, result.final_output)
    
    async def forward(self, prompt: str) -> str:
        """Turns the task into actual actions that the system is capable of doing. Call this agent with your outputs tasks."""
        log(f"{self.name}({prompt})", self.parent.name)
        result = await self.run(prompt)
        log(f"{self.name}({prompt}) => {result.final_output}", self.parent.name)
        return result.final_output
