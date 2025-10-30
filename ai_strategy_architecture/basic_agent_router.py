import logging
from typing import Literal
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.exceptions import OutputParserException
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from config import settings

# --- Setup Logging ---
# Set up a structured logger. In a real app, this might be configured in a central file.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- LLM and Schema Definition ---
try:
    router_llm = ChatGoogleGenerativeAI(
        model=settings.DEFAULT_MODEL_NAME,
        temperature=0,
        api_key=settings.GEMINAI_API_KEY
    )
except AttributeError as e:
    logger.critical(f"Failed to load settings from config. Make sure settings are correct. Error: {e}")
    raise SystemExit(f"Configuration error: {e}")


class RouteQuery(BaseModel):
    """Route a user query to the relevant agent."""
    destination: Literal["finance", "hr", "general_support"] = Field(
        ...,
        description=(
            "'finance' → for questions about invoices, budgets, and expenses. "
            "'hr' → for questions about company policy, vacation, and benefits. "
            "'general_support' → for all other inquiries."
        ),
    )

structured_llm_router = router_llm.with_structured_output(RouteQuery)

# --- Prompt Template (with typos fixed) ---
system_prompt = """You are an expert at routing a user's request to the correct department.
Based on the user's query, select one of the following destinations: 'finance', 'hr', or 'general_support'.
Do not attempt to answer the question yourself; only select the destination.
"""

prompt = ChatPromptTemplate.from_messages(
    [("system", system_prompt),
     ('human', "{query}"),
     ]
)

router_chain = prompt | structured_llm_router

# --- Core Function with Error Handling ---

def get_router(query: str) -> RouteQuery | None:
    """
    Determines the route for the given query with error handling.

    Args:
        query: The user's input string.

    Returns:
        A RouteQuery object if successful, else None.
    """
    logger.info(f"Routing query: '{query}'")
    try:
        # Note: LangChain maps the single string `query` to the {"query": query} dict
        result = router_chain.invoke(query)
        logger.info(f"Successfully routed to: '{result.destination}'")
        return result

    except OutputParserException as e:
        # This is critical: happens if the LLM output doesn't match the Pydantic schema
        logger.error(f"Failed to parse LLM output for query: '{query}'. Error: {e}")
        return None
    except Exception as e:
        # Catch-all for other errors (API, network, etc.)
        logger.error(f"An unexpected error occurred while routing query: '{query}'. Error: {e}")
        return None

# --- Main execution block ---
# This code only runs when you execute `python agent.py` directly.
# It will NOT run when this file is imported by another module.
if __name__ == "__main__":
    
    # --- Example Test Cases ---
    test_queries = [
        "how do i file an expense report for my recent trip", # Should be finance
        "what's the company policy on remote work?",          # Should be hr
        "My printer is broken",                               # Should be general_support
        "where can I see my last paycheck stub?",             # Should be finance or hr (good test case)
    ]

    for q in test_queries:
        route = get_router(q)
        if route:
            print(f"Query:   '{q}'\nRouted:  '{route.destination}'")
        else:
            print(f"Query:   '{q}'\nFailed to route.")
        print("-" * 20)