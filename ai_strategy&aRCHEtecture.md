## Enterprise Enviroment Setup And Configuration 
code -> [`ai_strategy&ARchetevcture/config.py`](ai_strategy&ARchetevcture/config.py)


In enterprise deployment:

Code goes inside container (Docker image).and 

Configuration stays outside — passed in via environment variables, .env files, or secrets manager (Vault, AWS SSM, etc.). so that 


which  lets us to  run the same container in different environments with different behavior 


# Simple Multi Agent Architecture Router 
code -> [`ai_strategy&ARchetevcture/test_basic_agent_route.py`](ai_strategy&ARchetevcture/test_basic_agent_route.py)

Big companies usually use multiple specialized agents — each focused on a specific task.
In this architecture, every user request enters the system through a Router.
The router inspects the query and, based on predefined rules or LLM classification, directs it to the most appropriate agent.

We typically use a lightweight, low-cost LLM for routing.

# Wrapping LangchainOn Fastapi Endpoint 
