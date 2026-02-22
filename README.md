# Thoughtful AI – Customer Support Agent

A conversational AI agent that answers common questions about **Thoughtful AI's** healthcare automation products (EVA, CAM, PHIL) using a predefined knowledge base and fuzzy string matching.

## Quick Start

```bash
# 1. Clone the repository
git clone <repo-url>
cd thoughtful-ai-agent

# 2. Create a virtual environment (recommended)
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. (Optional) Set OpenAI API key for generic LLM fallback
# Copy the example env file and add your key
cp .env.example .env               # macOS / Linux (or Git Bash)
# Copy-Item .env.example .env      # Windows PowerShell
# copy .env.example .env           # Windows CMD
# Or set it directly in your terminal:
# export OPENAI_API_KEY="your-api-key-here"  # macOS / Linux
# set OPENAI_API_KEY="your-api-key-here"     # Windows

# 5. Run the app
chainlit run app.py
```

The Chainlit UI will open automatically at **http://localhost:8000**.

## Project Structure

| File | Purpose |
|---|---|
| `knowledge_base.py` | Predefined Q&A dataset and fuzzy-match retrieval logic |
| `agent.py` | Agent routing – knowledge base lookup with static fallback |
| `app.py` | Chainlit chat UI entry point |
| `requirements.txt` | Python dependencies |

## How It Works

1. The user types a question in the Chainlit chat interface.
2. `agent.py` delegates to `knowledge_base.py`, which compares the query against predefined questions using **fuzzy string matching** (`difflib.SequenceMatcher`) and keyword overlap scoring.
3. If a match exceeds the similarity threshold, the corresponding answer is returned.
4. If no match is found, the agent falls back to a generic LLM response using OpenAI (if `OPENAI_API_KEY` is set).
5. If no API key is configured, a friendly static fallback message is shown suggesting the user rephrase or ask about a known topic.

## Sample Questions

- *What does the eligibility verification agent (EVA) do?*
- *What does the claims processing agent (CAM) do?*
- *How does the payment posting agent (PHIL) work?*
- *Tell me about Thoughtful AI's Agents.*
- *What are the benefits of using Thoughtful AI's agents?*
