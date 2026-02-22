"""
Conversational agent for Thoughtful AI customer support.

Routes user queries to the knowledge base for predefined answers
and falls back to an LLM or a friendly static response when no match is found.
"""

import os
from openai import AsyncOpenAI
from knowledge_base import find_best_match

# Friendly fallback when the knowledge base has no relevant answer
_FALLBACK_RESPONSE = (
    "I'm sorry, I don't have specific information about that. "
    "Could you try rephrasing your question, or ask me about "
    "Thoughtful AI's agents such as EVA, CAM, or PHIL?"
)

# Prompt shown when the user sends empty / whitespace-only input
_EMPTY_INPUT_RESPONSE = (
    "It looks like you didn't type anything. "
    "Go ahead and ask me a question about Thoughtful AI!"
)


async def get_response(user_input: str) -> str:
    """
    Return a conversational response for the given *user_input*.

    1. Reject empty / blank input with a friendly nudge.
    2. Search the knowledge base for a matching predefined answer.
    3. Fall back to an LLM response if OPENAI_API_KEY is set.
    4. Fall back to a static "I don't know" message if no key is set.
    """
    if not user_input or not user_input.strip():
        return _EMPTY_INPUT_RESPONSE

    try:
        answer = find_best_match(user_input)
        if answer:
            return answer

        # Fallback to LLM if API key is available
        api_key = os.environ.get("OPENAI_API_KEY")
        if api_key:
            client = AsyncOpenAI(api_key=api_key)
            response = await client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a helpful customer support assistant for Thoughtful AI. "
                            "Answer the user's question generally."
                        ),
                    },
                    {"role": "user", "content": user_input},
                ],
                max_tokens=250,
            )
            return response.choices[0].message.content or _FALLBACK_RESPONSE

        return _FALLBACK_RESPONSE
    except Exception:  # pylint: disable=broad-exception-caught
        return (
            "Oops — something went wrong while processing your question. "
            "Please try again in a moment."
        )
