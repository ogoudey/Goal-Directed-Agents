import asyncio

from environments import Room, Geographic

from morphologies import SO101, AutonomousBoat
from morphologies import Combination

from modes import VLA, BostonHarbor2BackBay, SayToProgrammer

from knowledge import Knowledge

from motives import UnTaskable

from orchestra import GDAO

def vla_in_JCC():
    untaskable = UnTaskable(goal="for things to be in their proper place")

    vla = VLA()
    vla.restrict_to_capabilities(["Put the cube in the bowl"])
    say2prog = SayToProgrammer()
    modes = [
        vla.execute,
        say2prog.execute,
    ]
    knowledge = Knowledge(modes, SO101(), Room("", "North America", "USA", "MA", "Medford", "", "JCC", "474"))
    gda = GDAO(knowledge=knowledge)
    asyncio.run(gda.execute(untaskable))

def boat_in_boston():
    untaskable = UnTaskable(goal="to get home (Back Bay)")

    planner = BostonHarbor2BackBay()
    say2prog = SayToProgrammer()

    modes = [
        planner.execute,
        say2prog.execute,
    ]
    knowledge = Knowledge(modes, AutonomousBoat(), Geographic("Boston Harbor"))
    gda = GDAO(knowledge=knowledge)
    asyncio.run(gda.execute(untaskable))

def chimera_in_boston():
    untaskable = UnTaskable(goal="to have any cube that is in Boston Harbor moved to a bowl in Back Bay")

    vla = VLA()
    vla.restrict_to_capabilities(["Put the cube in the bowl"])
    
    planner = BostonHarbor2BackBay()
    say2prog = SayToProgrammer()
    modes = [
        vla.execute,
        planner.execute,
        say2prog.execute,
    ]

    morphology = Combination(SO101(), AutonomousBoat(), "on")

    knowledge = Knowledge(modes, morphology, Geographic("Boston Harbor"))
    gda = GDAO(knowledge=knowledge)
    asyncio.run(gda.execute(untaskable))

def orchestrate():
    untaskable = UnTaskable(goal="to get home (Back Bay)")

    planner = BostonHarbor2BackBay()
    say2prog = SayToProgrammer()
    modes = [
        planner.execute,
        say2prog.execute,
    ]
    knowledge = Knowledge(modes, AutonomousBoat(), Geographic("Boston Harbor"))
    gda = GDAO(knowledge=knowledge)

    asyncio.run(gda.orchestrate(untaskable))

def orchestrate_jcc():
    untaskable = UnTaskable(goal="to fill all cardboard boxes")

    vla = VLA()
    vla.restrict_to_capabilities(["Put the colored blocks in the cardboard box"])
    say2prog = SayToProgrammer()

    modes = [
        vla.execute,
        say2prog.execute,
    ]
    knowledge = Knowledge(modes, SO101(), Room("", "North America", "USA", "MA", "Medford", "", "JCC", "474"))
    gda = GDAO(knowledge=knowledge)

    asyncio.run(gda.orchestrate(untaskable))
    
def impress_jcc():
    untaskable = UnTaskable(goal="to impress the programmer with my physical capabilities")

    vla2 = VLA(policy_location="outputs/stationary_mug_pretrained_model")
    vla2.restrict_to_capabilities(["Put the stuffed animal in the mug"])

    vla1 = VLA(policy_location="outputs/stationary_mug_pretrained_model")
    vla1.restrict_to_capabilities(["Put the colored blocks in the cardboard box"])
    
    
    
    say2prog = SayToProgrammer()

    modes = [
        vla1.execute,
        vla2.execute,
        say2prog.execute,
    ]
    knowledge = Knowledge(modes, SO101(), Room("", "North America", "USA", "MA", "Medford", "", "JCC", "474"))
    gda = GDAO(knowledge=knowledge)

    asyncio.run(gda.orchestrate(untaskable))

def cycling_jcc():
    untaskable = UnTaskable(goal="to put all blocks in boxes")

    vla1 = VLA(policy_location="outputs/stationary_mug_pretrained_model")
    vla1.restrict_to_capabilities(["Put the colored blocks in the cardboard box"]) # affects docstring
    
    
    
    say2prog = SayToProgrammer()

    modes = [
        vla1.execute,
        say2prog.execute,
    ]
    knowledge = Knowledge(modes, SO101(), Room("", "North America", "USA", "MA", "Medford", "", "JCC", "474"))
    gda = GDAO(knowledge=knowledge)

    asyncio.run(gda.loop(untaskable))
