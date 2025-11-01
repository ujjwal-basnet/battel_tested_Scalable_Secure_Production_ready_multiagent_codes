## Enterprise Enviroment Setup And Configuration 
code -> [`ai_strategy_architecture/config.py`](ai_strategy_architecture/config.py)


In enterprise deployment:

Code goes inside container (Docker image).and 

Configuration stays outside — passed in via environment variables, .env files, or secrets manager (Vault, AWS SSM, etc.). so that 


which  lets us to  run the same container in different environments with different behavior 


## Simple Multi Agent Architecture Router 
code ->  [`ai_strategy_architecture/basic_agent_route.py`](ai_strategy_architecture/basic_agent_router.py)


code-> test function for our code [`ai_strategy_architecture/test_basic_agent_route.py`](ai_strategy_architecture/test_basic_agent_router.py)


Big companies usually use multiple specialized agents — each focused on a specific task.
In this architecture, every user request enters the system through a Router.
The router inspects the query and, based on predefined rules or LLM classification, directs it to the most appropriate agent.

We typically use a lightweight, low-cost LLM for routing.

## Wrapping LangchainOn Fastapi Endpoint
code-> test function for our code [`ai_strategy_architecture/wrapping_langchainOn_fastapi_endpoint.py`](ai_strategy_architecture/wrapping_langchainOn_fastapi_endpoint.py)


We need To Wrap the complex logic behind the apis ,  .... and present a user nice ..... so this code wraps the langchian logic behind a secure 
'POST' endpoint , using  pydantic for request validation ensuring data integrity 


code explain : 
'APIKeyQuery'  means FastAPI expects an API key in the query parameter of the request URL.

ps:(their are some compatibility , .venv files problme form my side i will so this is completed and might have some erros)

## Prompt versioing 
code-> test function for our code [`misc/prompt.py`](misc/prompt.py)

code-> test function for our code [`misc/extraction.py`](misc/extraction.py)

its good practice to seperate prompts from code because 

oftern some  application use same prompts and writing same 10 sentence long prompts  does not sound 

and versioing prompts  also helps on to  test code using different prompts 


## PII 
code-> test function for our code [`ai_strategy_architecture/pii_utils.py`](ai_strategy_architecture/pii_utils.py)


User can sometimes request query with  their personal Information


    my email is ujjwal@gmail.com and my bank password  is "bank13"  help me to login 


their is no-way as an organization you can trust thrid party api/llm for your user data
thus you usall have to scan ,  mask these information  to avoid data lekage 


previous text after masking 

    "my email is <email> password is <password> ... help me to login

now you send mask_text to llm 
llm.answer("my emial is <email> password is <password>.... help me to login)

after llm answer you  put real  values in those placeholder and send back to user 



