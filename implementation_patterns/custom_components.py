import httpx 
from typing import Dict, Any , Optional
from langchain_core.runnables import chain , RunnableConfig, RunnableLambda
from langchain_google_genai import ChatGoogleGenerativeAI 
from pydantic import BaseModel 
from config  import settings 
from langchain_core.prompts import ChatPromptTemplate
import logging
import asyncio

class UserContext(BaseModel):
    user_id:str 
    query:str 
    user_name: Optional[str]= None
    department: Optional[str] = None
    
async def fetch_user_profile_async(user_id:str) -> dict:
    """Simulates a non-blocking async API call."""
    logging.info(f"Fetching profile asynchronously for: {user_id}")
    await asyncio.sleep(0.1)

    if user_id =='user123':
        return {'name': 'ujjwal' , 'department': 'Risk Management'}
    
    elif user_id == 'user456':
        return {'name': 'rakesh', 'department': 'Quantitative Analysis'}
    
    else : 
        raise httpx.HTTPStatusError("user not found" , response= None, request= None)
    
@chain 
async def user_enricher(input_data: UserContext , config: RunnableConfig= None) -> UserContext:
    try: 
        profile = await fetch_user_profile_async(input_data.user_id)
        input_data.user_name= profile['name']
        input_data.department= profile['department']

    except httpx.HTTPStatusError:
        logging.warning(f"User {input_data.user_id} not found procedding with defults")
        input_data.user_name= "unknown user "
        input_data.department= "general staff"

    return input_data 


# .model_dump() is the modern Pydantic v2 method for dictionary conversion.
convert_to_dict = RunnableLambda(lambda x: x.model_dump())


# prompt and chaining
prompt = ChatPromptTemplate.from_template(
    "user {user_name} from {department} asked : {query}. provide a concise answer" ) 

llm = ChatGoogleGenerativeAI(model= settings.DEFAULT_MODEL_NAME , api_key= settings.GEMINAI_API_KEY)

full_chain= user_enricher | convert_to_dict |  prompt | llm 



### execute 

# --- Execution ---
async def main():
    input_obj = UserContext(user_id="user_123", query="What are the risks?")
    
    # We pass the configuration here. 
    # These tags/metadata will flow into `user_enricher` via the `config` argument we added above.
    config_options = {
        "tags": ["env:production", "team:risk"],
        "metadata": {"source": "slack_bot", "request_id": "req_999"}
    }

    print("--- Invoking Chain with Config ---")
    response = await full_chain.ainvoke(input_obj, config=config_options)
    print(f"Result: {response.content}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())