def build_case_prompt(question, chunks, summary=""):
    """
    chunks: list of dicts
      {
        "text": "...",
        "metadata": {...}
      }
    """

    context = "\n\n".join(
        chunk["text"] for chunk in chunks if "text" in chunk
    )

    return f"""
You are a legal assistant.

Conversation summary (context only):
{summary if summary else "No prior conversation."}

Authoritative case material:
{context}

Rules:
- Answer ONLY from the case material


Question:
{question}
"""

# - If the answer is not found, say "Not available in this case"





