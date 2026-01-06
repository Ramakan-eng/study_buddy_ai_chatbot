def validate_answer(answer: str, chunks: list):
    """
    Basic safety checks to prevent hallucinations
    """

    if not answer:
        return False, "Empty answer"

    if "not found in the provided case materials" in answer.lower():
        return True, answer

    # Simple keyword grounding check
    combined_text = " ".join(chunk["text"] for chunk in chunks).lower()

    key_terms = answer.lower().split()[:10]

    if not any(term in combined_text for term in key_terms):
        return False, "Answer not grounded in case text"

    return True, answer
