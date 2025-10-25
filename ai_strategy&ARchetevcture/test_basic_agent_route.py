# test_agent.py
import pytest
from basic_agent_router import get_router, RouteQuery # Import your function and schema

# Use @pytest.mark.parametrize to test many cases at once
@pytest.mark.parametrize("query, expected_destination", [
    ("how do i file an expense report?", "finance"),
    ("Where is my invoice?", "finance"),
    ("I need to submit a budget proposal.", "finance"),
    ("How many vacation days do I have left?", "hr"),
    ("What are our company benefits?", "hr"),
    ("I need to update my personal information.", "hr"),
    ("My laptop screen is flickering.", "general_support"),
    ("What's the wifi password?", "general_support"),
    ("How do I book a meeting room?", "general_support"),
])
def test_router(query, expected_destination):
    """
    Tests that the router function correctly classifies various queries.
    """
    # Note: This test makes a live API call, which is an "integration test".
    # For a true "unit test", you would "mock" the router_chain.
    
    result = get_router(query)
    
    assert result is not None, f"Router failed to process query: {query}"
    assert isinstance(result, RouteQuery)
    assert result.destination == expected_destination

# run [pytest] in terminal to run this test   :