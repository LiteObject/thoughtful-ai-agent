import os
import pytest
from unittest.mock import patch, AsyncMock, MagicMock

from agent import get_response, _EMPTY_INPUT_RESPONSE, _FALLBACK_RESPONSE
from knowledge_base import QUESTIONS_AND_ANSWERS


@pytest.mark.asyncio
async def test_get_response_empty_input():
    """Test that empty input returns the empty input response."""
    response = await get_response("")
    assert response == _EMPTY_INPUT_RESPONSE

    response = await get_response("   ")
    assert response == _EMPTY_INPUT_RESPONSE


@pytest.mark.asyncio
async def test_get_response_knowledge_base_match():
    """Test that a known question returns the predefined answer."""
    question = QUESTIONS_AND_ANSWERS[0]["question"]
    expected_answer = QUESTIONS_AND_ANSWERS[0]["answer"]

    response = await get_response(question)
    assert response == expected_answer


@pytest.mark.asyncio
@patch.dict(os.environ, {}, clear=True)
async def test_get_response_no_match_no_api_key():
    """Test that an unknown question without an API key returns the static fallback."""
    response = await get_response("What is the meaning of life?")
    assert response == _FALLBACK_RESPONSE


@pytest.mark.asyncio
@patch.dict(os.environ, {"OPENAI_API_KEY": "fake-api-key"}, clear=True)
@patch("agent.AsyncOpenAI")
async def test_get_response_no_match_with_api_key(mock_async_openai):
    """Test that an unknown question with an API key calls the LLM."""
    # Setup the mock LLM response
    mock_client = AsyncMock()
    mock_async_openai.return_value = mock_client

    mock_message = MagicMock()
    mock_message.content = "This is a mocked LLM response."

    mock_choice = MagicMock()
    mock_choice.message = mock_message

    mock_response = MagicMock()
    mock_response.choices = [mock_choice]

    mock_client.chat.completions.create.return_value = mock_response

    # Call the agent
    response = await get_response("What is the meaning of life?")

    # Verify the LLM was called and the response was returned
    assert response == "This is a mocked LLM response."
    mock_client.chat.completions.create.assert_called_once()


@pytest.mark.asyncio
@patch("agent.find_best_match")
async def test_get_response_exception_handling(mock_find_best_match):
    """Test that an unexpected exception returns a friendly error message."""
    mock_find_best_match.side_effect = Exception("Something broke!")

    response = await get_response("Hello?")
    assert "Oops — something went wrong" in response
