from typing import List

"""
Modes are the actionable interfaces of the GDA.

They bare an execute function that should link to their respective libraries etc.

These functions are also turned into tools for the lowest Agent in the orchestration. 
"""

class Mode:
    def __init__(self):
        pass

class VLA(Mode):
    for_real = False
    def __init__(self):
        super().__init__()
        self.execute.__func__.__name__ = self.__class__.__name__

        if self.for_real:
            import sys
            import importlib.util
            from pathlib import Path

            module_path = Path("/home/olin/Robotics/Projects/LeRobot/lerobot/custom_brains/test.py")
            lerobot_root = module_path.parent.parent  # -> /home/olin/Robotics/Projects/LeRobot/lerobot

            # Add the parent *of* lerobot (so "lerobot" is importable as a package)
            sys.path.insert(0, str(lerobot_root.parent))

            spec = importlib.util.spec_from_file_location("custom_brains.test", module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            from lerobot.custom_brains import test
            self.run = test.test_policy

            self.policy_location = lerobot_root / "outputs" / "stationary_env_7k"
            self.camera_streams = ["rtsp://10.243.112.170:8080/h264_ulaw.sdp", "rtsp://10.243.63.69:8080/h264_ulaw.sdp"]

    def execute(self, instruction: str):
        """docstring here"""
        if self.for_real:
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

        At this point, the VLA has severe limitations. Here is what it can do (only use one of them as an argument):
        
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