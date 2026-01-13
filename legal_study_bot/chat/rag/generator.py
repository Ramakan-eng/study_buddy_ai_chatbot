import os
from openai import OpenAI
from dotenv import load_dotenv
from django.conf import settings
# load_dotenv()
# client = OpenAI(api_key="OPENAI_API_KEY")
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))
# client = OpenAI(api_key="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")

def generate_answer(prompt: str):
    """
    Generate answer from LLM using RAG prompt
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a legal assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0  # IMPORTANT: no creativity
    )
    # print(response.choices[0].message.content.strip())
    return response.choices[0].message.content.strip()
