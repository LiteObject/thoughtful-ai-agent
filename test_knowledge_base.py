import pytest
from knowledge_base import find_best_match, QUESTIONS_AND_ANSWERS


def test_find_best_match_exact():
    """Test that an exact match returns the correct answer."""
    question = QUESTIONS_AND_ANSWERS[0]["question"]
    expected_answer = QUESTIONS_AND_ANSWERS[0]["answer"]
    assert find_best_match(question) == expected_answer


def test_find_best_match_fuzzy():
    """Test that a fuzzy match (slight typo/rephrasing) returns the correct answer."""
    # "What does the eligibility verification agent (EVA) do?"
    query = "what does the eligibility verification agent eva do?"
    expected_answer = QUESTIONS_AND_ANSWERS[0]["answer"]
    assert find_best_match(query) == expected_answer


def test_find_best_match_no_match():
    """Test that an unrelated query returns None."""
    query = "What is the weather like today?"
    assert find_best_match(query) is None


def test_find_best_match_empty():
    """Test that empty or whitespace-only queries return None."""
    assert find_best_match("") is None
    assert find_best_match("   ") is None
