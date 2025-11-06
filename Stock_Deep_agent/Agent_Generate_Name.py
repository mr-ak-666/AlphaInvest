from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI
from langchain.agents.agent_types import AgentType
# import os
# from dotenv import load_dotenv

# load_dotenv()

# OPENAI_API_KEY = "sk..."
# if not os.getenv("OPENAI_API_KEY"):
#     raise ValueError("Please set the OPENAI_API_KEY environment variable.")

# Tool to generate fictional names
def generate_fictional_names(sector: str) -> str:
    # Simple logic to generate names (can be replaced with LLM call)
    suffixes = ["Corp", "Solutions", "Systems", "Dynamics", "Labs"]
    prefixes = ["Neo", "Quantum", "Zenith", "Astra", "Nimbus"]
    import random
    names = [f"{random.choice(prefixes)} {sector.capitalize()} {random.choice(suffixes)}" for _ in range(5)]
    return "\n".join(names)

# Wrap the tool
tools = [
    Tool(
        name="FictionalNameGenerator",
        func=generate_fictional_names,
        description="Generates fictional company names for a given sector"
    )
]

# Initialize agent
llm = OpenAI(temperature=0.7)
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

# Run agent
sector = input("Enter the Sector Name :- ")
response = agent.run(sector)
print(response)