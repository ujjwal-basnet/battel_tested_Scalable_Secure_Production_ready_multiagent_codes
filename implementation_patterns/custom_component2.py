### unlike @chain abstract this is 100% custom component 

import httpx
from typing import Dict  , Any ,Optional
from langchain_core.runnables import  RunnableConfig  , Runnable
import logging 
import asyncio
from langchain_core.prompts import ChatPromptTemplate
from config import settings 
from langchain_google_genai import  ChatGoogleGenerativeAI
import asyncio



class UserProfileEnricher(Runnable): 
    def __init__(self, user_id_key: str = "user_id", output_key:str = "profile"):
        self.user_id_key= user_id_key 
        self.output_key= output_key

    def fetch_profile_sync(self,user_id:str)-> Dict[str, Any]: 
        logging.info(f"Fetching profile for user id {user_id}")
        if user_id == "1":
            return {"name" : "ujjwal" , "department": "Risk Management" , "tenure_years": 10}
        
        elif user_id == "2":
            return {'name': 'ram', 'department': 'Backend' , 'tenure_years': 3}
        
        else : 
            raise httpx.HTTPStatusError("user not found", request= None , response= None )
        
    def invoke(self, input:Dict, config:Optional[RunnableConfig] = None, async_call= False)-> Dict:
        if async_call:
            logging.info(f"UserProfileEnricher ainvoked")

        else : 
            logging.info(f"UserProfileEnricher invoked") 

        
        
        user_id= input.get(self.user_id_key)
        if not user_id: 
            raise ValueError(f"Input must contains key '{self.user_id_key}'")
        
        try : 
            profile= self.fetch_profile_sync(user_id)

        except httpx.HTTPStatusError as e : 
            logging.warning(f"Profile fetch failed {e}")
            profile = {} 

        ## if yes return merged dict 
        return {
                    **input,
                    self.output_key: profile,  # optional, keep full profile if needed later
                    "user_name": profile.get("name", "Unknown User"),
                    "user_dept": profile.get("department", "Unknown Dept")
                }

    
    ## async invoke 
    async def ainvoke(self, input: Dict, config:Optional[RunnableConfig]= None) -> Dict:
            return await asyncio.to_thread(self.invoke, input, config, async_call=True)

## here async call parameter is just for logging 

    

############# example usages in chain 
def main():
    enricher= UserProfileEnricher() 
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant."),
        (
            "human",
            # Use flat variables instead of dictionary access
            "User {user_name} from {user_dept} asked: {query}\n" 
            "Provide the best concise answer."
        )
    ])
    llm = ChatGoogleGenerativeAI(model= settings.DEFAULT_MODEL_NAME , api_key= settings.GEMINAI_API_KEY)

    #chain 
    chain = enricher | prompt | llm 

    ## test 
    sync_result = chain.invoke({
        "user_id": "1",
        "query": "Explain credit default swaps."
    })
    print("SYNC result:\n", sync_result.content)

    async def async_test():
        async_result = await chain.ainvoke({
            "user_id": "2",
            "query": "Explain VaR."
        })
        print("ASYNC result:\n", async_result.content)

    asyncio.run(async_test())


if __name__ == "__main__":
     logging.basicConfig(level= logging.INFO)
     main()



    

