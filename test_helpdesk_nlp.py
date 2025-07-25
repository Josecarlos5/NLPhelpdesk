import pytest
from unittest.mock import patch

# Mock database or external service call
def mock_fetch_user_data(user_id):
    # Simulated database call
    user_data = {
        "123": {"name": "Alice", "account_status": "active"},
        "456": {"name": "Bob", "account_status": "inactive"}
    }
    return user_data.get(user_id, None)

# Example NLP function with state/context handling
class HelpdeskNLP:
    
    def __init__(self):
        self.context = {}

    def process_query(self, query: str, user_id: str) -> str:
        user_data = mock_fetch_user_data(user_id)
        if not user_data:
            return "User not found. Please provide a valid user ID."
        
        self.context['user_name'] = user_data['name']
        
        # Simulated responses based on query type
        if "reset my password" in query:
            return f"Hello {self.context['user_name']}, to reset your password, click on 'Forgot Password'."
        elif "hours of operation" in query:
            return "We are open from 9 AM to 5 PM, Monday through Friday."
        elif "account status" in query:
            return f"{self.context['user_name']}, your account status is {user_data['account_status']}."
        else:
            return "I'm sorry, I didn't understand your question."

@pytest.fixture
def helpdesk_nlp():
    return HelpdeskNLP()

@pytest.mark.parametrize("query, user_id, expected_response", [
    ("How can I reset my password?", "123", 
     "Hello Alice, to reset your password, click on 'Forgot Password'."),
    ("What are your hours of operation?", "123", 
     "We are open from 9 AM to 5 PM, Monday through Friday."),
    ("What is my account status?", "456", 
     "Bob, your account status is inactive."),
    ("Can you help me with something else?", "123", 
     "I'm sorry, I didn't understand your question."),
    ("", "789", 
     "User not found. Please provide a valid user ID.")
])
def test_queries(helpdesk_nlp, query, user_id, expected_response):
    with patch('__main__.mock_fetch_user_data', side_effect=mock_fetch_user_data):
        response = helpdesk_nlp.process_query(query, user_id)
    assert response == expected_response

def test_state_management(helpdesk_nlp):
    with patch('__main__.mock_fetch_user_data', side_effect=mock_fetch_user_data):
        helpdesk_nlp.process_query("How can I reset my password?", "123")
    assert 'user_name' in helpdesk_nlp.context
    assert helpdesk_nlp.context['user_name'] == "Alice"

