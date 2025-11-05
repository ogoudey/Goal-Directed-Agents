# Goal-Directed Agents

This repo contains a scheme for an LLM-based architecture for robotic behavior.

It turns high-level decision making into a problem of finetuning.

Assumptions are that the robot is given:
** A ultimate goal/motive
** A minimal texttual description of a morphology
** A minimal textual description of an environment
** A list of "modes" that resemble the robot's capabilities (e.g. path plan, use a policy, say something outloud)

```
python3 main.py
```

runs a demo:
```
Ultimate goal: to fill all cardboard boxes      # (hard-coded)

Discrepancy detected: The assigned tasks require identifying cardboard boxes, determining appropriate filler material, fully filling them, and verifying the fill level. However, my available tool is limited to executing a specific instruction ('Put the colored blocks in the cardboard box'), and does not support these multi-step tasks. I'm unable to fully complete the tasks requested.

🔥 VLA performing Put the colored blocks in the cardboard box 🔥

Discrepancy: The assigned tasks include identifying all cardboard boxes, collecting enough colored blocks, and filling each box completely. However, I can only execute the task 'Put the colored blocks in the cardboard box.' Thus, I was only able to partially complete the task.
```
where the last output information is all volunteered by the agent.
