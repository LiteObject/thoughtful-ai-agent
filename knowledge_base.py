"""
Knowledge base for Thoughtful AI customer support agent.

Contains predefined Q&A pairs about Thoughtful AI's products and services,
along with fuzzy-matching logic to find the best answer for a user query.
"""

import re
from difflib import SequenceMatcher

# Common English stop words to ignore during keyword matching
_STOP_WORDS = frozenset(
    "a an the is are was were do does did has have had be been being "
    "i me my we our you your he she it its they them their what which "
    "who whom how when where why that this these those of in to for on "
    "with at by from about into through during before after above below "
    "between and but or nor not so yet if then else can could will would "
    "shall should may might must tell".split()
)

# Predefined dataset of questions and answers about Thoughtful AI
QUESTIONS_AND_ANSWERS = [
    {
        "question": "What does the eligibility verification agent (EVA) do?",
        "answer": (
            "EVA automates the process of verifying a patient's eligibility "
            "and benefits information in real-time, eliminating manual data "
            "entry errors and reducing claim rejections."
        ),
    },
    {
        "question": "What does the claims processing agent (CAM) do?",
        "answer": (
            "CAM streamlines the submission and management of claims, "
            "improving accuracy, reducing manual intervention, and "
            "accelerating reimbursements."
        ),
    },
    {
        "question": "How does the payment posting agent (PHIL) work?",
        "answer": (
            "PHIL automates the posting of payments to patient accounts, "
            "ensuring fast, accurate reconciliation of payments and "
            "reducing administrative burden."
        ),
    },
    {
        "question": "Tell me about Thoughtful AI's Agents.",
        "answer": (
            "Thoughtful AI provides a suite of AI-powered automation agents "
            "designed to streamline healthcare processes. These include "
            "Eligibility Verification (EVA), Claims Processing (CAM), and "
            "Payment Posting (PHIL), among others."
        ),
    },
    {
        "question": "What are the benefits of using Thoughtful AI's agents?",
        "answer": (
            "Using Thoughtful AI's Agents can significantly reduce "
            "administrative costs, improve operational efficiency, and "
            "reduce errors in critical processes like claims management "
            "and payment posting."
        ),
    },
]

# Minimum similarity score (0.0–1.0) required to consider a match valid
SIMILARITY_THRESHOLD = 0.35


def _normalize(text: str) -> str:
    """Lowercase, strip punctuation, and collapse whitespace."""
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)  # remove punctuation
    return " ".join(text.split())


def _content_keywords(text: str) -> set[str]:
    """Return the set of meaningful (non-stop) words in *text*."""
    return {w for w in _normalize(text).split() if w not in _STOP_WORDS}


def _similarity(a: str, b: str) -> float:
    """Return a similarity ratio between two strings (0.0–1.0)."""
    return SequenceMatcher(None, a, b).ratio()


def find_best_match(user_query: str) -> str | None:
    """
    Compare *user_query* against every predefined question using
    fuzzy string matching combined with keyword overlap scoring,
    and return the best answer, or ``None`` if nothing exceeds the
    similarity threshold.
    """
    if not user_query or not user_query.strip():
        return None

    normalized_query = _normalize(user_query)
    query_kw = _content_keywords(user_query)

    best_score = 0.0
    best_answer: str | None = None

    for item in QUESTIONS_AND_ANSWERS:
        normalized_question = _normalize(item["question"])
        question_kw = _content_keywords(item["question"])

        # Fuzzy string similarity
        seq_score = _similarity(normalized_query, normalized_question)

        # Keyword overlap (ignoring stop words) — check both directions
        # and average them so short queries with distinctive terms like
        # "EVA" still score highly against the matching question.
        kw_score = 0.0
        common_kw = query_kw & question_kw
        if question_kw and query_kw:
            forward = len(common_kw) / len(question_kw)  # coverage of question
            reverse = len(common_kw) / len(query_kw)  # coverage of query
            kw_score = (forward + reverse) / 2

        # Combined score — keyword overlap is weighted more to reward
        # queries that mention distinctive terms like EVA, CAM, PHIL.
        score = 0.4 * seq_score + 0.6 * kw_score

        if score > best_score:
            best_score = score
            best_answer = item["answer"]

    if best_score >= SIMILARITY_THRESHOLD:
        return best_answer

    return None
