from config import settings
from prompt import ENTITY_EXTRACTION_PROMPT_V1
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI


system_prompt = ENTITY_EXTRACTION_PROMPT_V1.prompt_text
prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{user_input}")
])


llm = ChatGoogleGenerativeAI(model=ENTITY_EXTRACTION_PROMPT_V1.model_name , 
                             google_api_key=settings.GEMINAI_API_KEY,
                             temperature=ENTITY_EXTRACTION_PROMPT_V1.temperature
                             )

chain= prompt_template | llm 

text_to_analyze= "Ujjwal  Basnet from Ithari. is flying to Kathmandu tomorrow"

answer = chain.invoke({'user_input': text_to_analyze})
print(f"\n---  {answer.content}  ---\n")