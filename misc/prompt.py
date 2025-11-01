from pydantic import BaseModel
from datetime import datetime 
from typing import Optional, Dict, Any 
class Prompt(BaseModel):
    model_name: str 
    prompt_text:str
    application:str 
    creator: str 
    date_created: datetime 
    temperature: Optional[float] = 0.3

ENTITY_EXTRACTION_PROMPT_V1 = Prompt(
    model_name="gemini-2.5-flash-lite",
    prompt_text=(
        "You are an expert entity extraction system. "
        "Your task is to analyze the user's text and extract all named entities, "
        "such as people, places, organizations, and dates. "
        "Respond ONLY with a JSON object."
    ),
    application= "Data-Process-Pipeline",
    creator= "Ujjwal-AI-Team",
    date_created=datetime(2025, 1, 15))