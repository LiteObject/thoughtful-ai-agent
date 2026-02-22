"""
Chainlit chat application for the Thoughtful AI customer support agent.

Run with:
    chainlit run app.py
"""

from dotenv import load_dotenv

load_dotenv()

import chainlit as cl
from agent import get_response


WELCOME_MESSAGE = (
    "👋 **Welcome to Thoughtful AI Support!**\n\n"
    "I can help you learn about our AI-powered healthcare automation agents:\n\n"
    "• **EVA** – Eligibility Verification\n"
    "• **CAM** – Claims Processing\n"
    "• **PHIL** – Payment Posting\n\n"
    "Ask me anything about Thoughtful AI's agents!"
)


@cl.on_chat_start
async def on_chat_start():
    """Send a welcome message when a new chat session begins."""
    await cl.Message(content=WELCOME_MESSAGE).send()


@cl.on_message
async def on_message(message: cl.Message):
    """Handle each incoming user message."""
    response = await get_response(message.content)
    await cl.Message(content=response).send()
