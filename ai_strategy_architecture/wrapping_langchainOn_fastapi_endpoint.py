## file:: main.py 
from fastapi import FastAPI, HTTPException , Security 
from fastapi.security import APIKeyHeader 
from pydantic import BaseModel 

### using our inbuilt-routing agent 
try:
    # prefer the real router when available
    from .basic_agent_router import get_router
except Exception:
    # Fallback simple router for development when langchain or dependencies are missing.
    def get_router(query: str):
        q = (query or "").lower()
        if any(w in q for w in ["invoice", "expense", "budget", "payroll", "payment", "invoice"]):
            return "finance"
        if any(w in q for w in ["vacation", "benefits", "policy", "hr", "human resources"]):
            return "hr"
        return "general_support"

from .config import settings


####### PII checker #######

# Local PII helpers (pii_utils provides a Presidio fallback)
from .pii_utils import analyze_pii, anonymize_with_placeholders, restore_placeholders


#### --- App Settings -- ### 
app = FastAPI(
    title= "AI Gateway",
    description= "provides intelligent routing agentic services  ",
    version='1.0.0'
)

## simple API key security for internal services (development)
# Hardcoded API key for initial testing as requested
API_KEY = "ujjwal"
API_KEY_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)


async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPException(status_code=403, detail="could not validate credentials")

### Api Models  ------- 

class QueryRequest(BaseModel):
    query: str 
    user_id: str | None = None 

class RouteResponse(BaseModel): 
    query_received: str 
    destination: str 

class PII_Response(BaseModel):
    analysis: str


def pii_analysis(raw_query: QueryRequest):
    """Deprecated helper kept for backward compatibility.

    Prefer using the functions in `pii_utils.py` (analyze_pii, anonymize_with_placeholders).
    """
    return PII_Response(analysis=str(analyze_pii(raw_query.query)))

        


#### APi endpoint 
@app.post("/route_query", response_model=RouteResponse)
async def route_query_endpoint(request: QueryRequest, api_key: str = Security(get_api_key)):
    """  Accepts user query and return a appropriate agente destination
    This endpoint is secured and requires a valid api """

    if not request.query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    # Detect PII
    matches = analyze_pii(request.query)
    pii_found = bool(matches)

    # If PII found, anonymize before routing to avoid leaking sensitive data to downstream services
    sanitized_query = request.query
    mapping = []
    if pii_found:
        sanitized_query, mapping = anonymize_with_placeholders(request.query, matches)

    # Route the (sanitized) query
    destination = get_router(sanitized_query)

    # Build a short PII summary
    pii_summary = None
    if pii_found:
        # simple summary: counts per entity
        counts = {}
        for m in matches:
            counts[m["entity_type"]] = counts.get(m["entity_type"], 0) + 1
        pii_summary = str(counts)

    # response payload
    return RouteResponse(
        destination=destination,
        query_received=request.query,
    )


## to run : uvicorn main:app --reload
    
    
    
    
    




    



