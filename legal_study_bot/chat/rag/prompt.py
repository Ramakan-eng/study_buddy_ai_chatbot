import os
from langchain_openai import ChatOpenAI

from langchain_core.messages import SystemMessage, HumanMessage

from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  

llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.0, openai_api_key=OPENAI_API_KEY)

def detect_intent(query: str) -> int:
    """
    Returns:
      0 -> unsupported (Cross-case comparisons, Hypotheticals, Essay evaluation, External updates)
      1 -> supported (other intents)
    """
    system = SystemMessage(
        content=(
            "You are an intent detection model for a legal study assistant. "
            "If the user query belongs to any of these categories: "
            "1) Cross-case comparisons, 2) Hypotheticals, 3) Essay evaluation, "
            "4) External case updates not in DB, respond with exactly '0'. "
            "Otherwise respond with exactly '1'. Respond with nothing else."
        )
    )
    human = HumanMessage(content=f"User query: {query}")
    resp = llm.invoke([system, human])


    
    text = resp.content.strip()
    if text.startswith("0"):
        return 0
    if text.startswith("1"):
        return 1
    raise ValueError(f"Unexpected model response: {text}")





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





if __name__ == "__main__":
    def detect_intent(query):
        return detect_intent(query)
    