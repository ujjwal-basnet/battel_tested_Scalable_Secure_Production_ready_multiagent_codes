## file: cost tracking_example.py
from config import settings ## first always run config
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.exceptions import OutputParserException
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.callbacks import StdOutCallbackHandler


##  initialize llm 
llm= ChatGoogleGenerativeAI(model= settings.DEFAULT_MODEL_NAME , 
                            api_key=settings.GEMINAI_API_KEY)

prompt = ChatPromptTemplate.from_template("Write a short poem , very short")
chain= prompt | llm 

def process_request_with_tracking(user_id:str, department:str , topic:str):
    ##
    print(f"\n Processing {user_id} in {department}")
    
    #langshmit 
    response= chain.invoke(
        {"topic": topic},
        config={
            "callbacks":[StdOutCallbackHandler()],
            "metadata": {
                "user_id": user_id,
                "department":department,
            },
            "tags": ["poem_generator" , f"dept_{department}"]
        }
    )
    print("\n--- Request complete ---")
    return response

process_request_with_tracking(user_id="user_123" , department="marketing", topic="sell me pen")
process_request_with_tracking(user_id="ujjwal", department="ai" , topic= "ai vs human")