### file: resilient_chain.py

import logging
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from retry import  RetryWrapper 
from config import settings
from tenacity import RetryError
from pydantic import BaseModel , Field
from langchain_core.messages import AIMessage

# ------- Setup Logging -------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
# ------------- setup Logging -----------------
logger= logging.getLogger(__name__)


# --------- Define Models with Different Characteristics ---------
primary_llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    api_key=settings.GEMINAI_API_KEY
)
# fallback llm , cheaper model
fallback_llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0.7,
    api_key=settings.GEMINAI_API_KEY
)


# build the resilient llm core with retries and fallbacks 

# wrap the primary model in retry retry logic for transient errors
primary_with_retry= RetryWrapper(
    func= primary_llm.invoke , 
    max_attempts= 4 , )

## fallback
def execute_resilient_chain(prompt:str):
    try : 
        logger.info("calling primary LLm...")
        return primary_with_retry(prompt)
        logger.info("primary LLm Suceeded")
    except RetryError as e : 
        logger.warning(f"Primary llm failed after retries : {e} usingg fallback  ")
        response= fallback_llm.invoke(prompt)
        logger.info("fallback llm suceeded")
        return response
    
    except Exception as e : 
        logger.error(f"unexpected error occour {e}")
        return AIMessage(content= "system error")


# classifier 
class Intent(BaseModel):
    intent:str= Field(description= "classify the user as 'greeting' or 'question'. ")

## use smaller , faster model for the classification task 
llm= ChatGoogleGenerativeAI(model= "gemini-2.5-flash-lite", temperature=0, api_key= settings.GEMINAI_API_KEY)

# prompt 
classifier_prompt = ChatPromptTemplate.from_messages([
    ("system", "Classify the user input."),
    ("human", "{input}"),
])


# output parser
classifier = llm.with_structured_output(Intent)
classifier_chain = classifier_prompt | classifier

qa_prompt= ChatPromptTemplate.from_messages([
    ("system", "Answer the question helpfully"),
    ('human' , "{input}"),
])

def run_chain(user_input: str):
    classfication= classifier_chain.invoke({'input': user_input})
    intent= classfication.intent.lower()

    if intent == "greeting":
        return "hi! how can i assissit your with your question today"
    
    elif intent =='question':
        chain_input= qa_prompt.invoke({'input': user_input})
        response= execute_resilient_chain(chain_input)
        print(response)
        return response.content
    
    else : 
        return "i am not sure how to help with that"

# Example Usage 
if __name__ == "__main__":
    # Test 1: Greeting
    print(f"\n--- Response: {run_chain('Hi there')} ---\n")
    
    # Test 2: Question (Runs the resilient logic)
    print(f"\n--- Response: {run_chain('ronald vs messi which is goat?.')} ---\n")