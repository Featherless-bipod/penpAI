# Code Autocorrection Agent
This project is a leanring prototype for the PenpAI start-up idea. This repository implements an AI agent that is able to enter folders within a specified workspace repository to read, write, and run python code. 

## ⚠️ WARNING ⚠️
This code is not ready to be used commerically as low boundaries have been set for agent actions. It could be dangerous if agent were to bypass these boundaries and conduct unwanted actions. Use at your own discretion.

## How To Run: 
To run the agent, simply locate yourself to the base repository, and enter `uv run main.py "prompt"` with prompt being any request that you want the agent to do.

To test out the capabilities of the agent, go into the `calculator/main.py` file and mess something up—have fun with it. I usually like to mess up the priority of the order of operations just so I can produce some wacky numbers. After that run `uv run calculator/main.py "3 + 5 *2"` (or any calculation you would like to do) to see if the code is broken. If it is broken, good, now we can get the agent to fix it. 

Using the prompt call of `uv run main.py "blah blah blah fix my calculator"` (replace blah blah blah with prompt of course) and watch the code fix itself!