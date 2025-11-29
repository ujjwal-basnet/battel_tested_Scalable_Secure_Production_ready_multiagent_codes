# this is v0 of async chat services , we use chain here 
## but for better v1 we will use langgraph where we can track all the state not only chat msg 

import asyncio   #for async 
from config import settings 
from langchain_google_genai import ChatGoogleGenerativeAI
from fastapi import FastAPI 
from pydantic  import BaseModel 
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder 

#persitant memory 
from langchain_postgres import PostgresChatMessageHistory 
from langchain_core.runnables import RunnableWithMessageHistory


import psycopg2
import uuid



from config import config 
from custom_component2 import UserProfileEnricher 

app= FastAPI(title=  "Async Chat Service")

class ChatRequest(BaseModel):
    user_id: str 
    session_id:str
    message:str 

## build a core chat chain  , we will use our enricher to add user context to the conversation 
enricher= UserProfileEnricher() 

prompt= ChatPromptTemplate.from_messages([
    ("system", "you are helpful assistant"),    
    MessagesPlaceholder(variable_name= "history"),
("human", "{message}")
])


llm= ChatGoogleGenerativeAI(
    model= settings.DEFAULT_MODEL_NAME, 
    api= settings.GEMINAI_API_KEY) 


#chain 
base_chain= enricher | prompt   | llm 

###### wrap the chian with persistant memory 
