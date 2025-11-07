from typing import List

import sys
import os
from pathlib import Path
"""
Modes are the actionable interfaces of the GDA.

They bare an execute function that should link to their respective libraries etc.

These functions are also turned into tools for the lowest Agent in the orchestration. 
"""

low_level = True

class Mode:
    def __init__(self):
        pass

class VLA(Mode):
    
    def __init__(self, policy_location="outputs/blocks_box/checkpoints/021000/pretrained_model"):
        super().__init__()
        self.execute.__func__.__name__ = self.__class__.__name__
        global low_level
        if low_level:
        
            sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
            import vla_test
            # Now you can safely import from lerobot

            self.run = vla_test.test_policy

            self.policy_location = policy_location
            #print(Path(self.policy_location).exists())
            self.camera_streams = ["rtsp://10.243.51.52:8080/h264_ulaw.sdp", "rtsp://10.243.115.110:8080/h264_ulaw.sdp"]

    def execute(self, instruction: str):
        """docstring here"""
        global low_level
        if low_level:
            print(f"\033[1;31m VLA performing {instruction} \033[0m")
            self.run(self.policy_location, self.camera_streams)
            return "OK"
        else:
            print(f"\033[1;31m🔥 VLA performing {instruction} 🔥\033[0m")
            return f"Successfully executed {instruction} by the VLA."

    def restrict_to_capabilities(self, capabilities: List[str]):
        func = type(self).execute
        func.__doc__ = \
        f"""
        Performs the vision-language-action policy given the language instruction input.

        At this point, the VLA has severe limitations. Here are the recommended language prompts (suggested that we use one of them as an argument):
        
        {capabilities}

        instruction: Language instruction to VLA. 

        """

class BostonHarbor2BackBay(Mode):
    def __init__(self):
        super().__init__()
        self.execute.__func__.__name__ = self.__class__.__name__ # Names the function (which will be converted to a tool) to te class name.

    def execute(self):
        """Performs a search and discovers a plan (if there is one) to Back Bay from Boston Harbor."""
        print(f"\033[1;31m🔥 Path planner planning from Boston Harbor to Back Bay 🔥\033[0m")
        return f"Successfully executed path from Boston Harbor to Back Bay"

class SayToProgrammer(Mode):
    def __init__(self):
        super().__init__()
        self.execute.__func__.__name__ = self.__class__.__name__ # Names the function (which will be converted to a tool) to te class name.

    def execute(self, text: str):
        """Prints text to the terminal, for a programmer to maybe see while he/she is debugging you. In doing this, nothing will be performed in the real world except the printing of the message. Don't provide any task analysis or refere to anything that hasn't been performed. Rather, use this function mostly to communicate error.
        
        text: A line of pure text to send to the programmer.
        """
        print(f"{text}")
        return f"Successfully sent {text} to the programmer. (Though we don't know if he/she saw it.)"
