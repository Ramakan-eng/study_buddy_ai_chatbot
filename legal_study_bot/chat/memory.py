# from chat.models import ConversationSummary
# from chat.rag.generator import generate_answer


# MAX_MEMORY_CHARS = 1200   


# def get_summary(session_id: str, case_id: str) -> str:
#     try:
#         obj = ConversationSummary.objects.get(
#             session_id=session_id,
#             case_id=case_id
#         )
#         return obj.summary
#     except ConversationSummary.DoesNotExist:
#         return ""


# def compress_summary(long_text: str) -> str:
#     """
#     Uses LLM to compress conversation history safely
#     """
#     prompt = f"""
# Summarize the following conversation context.
# Keep it factual and concise.
# Do NOT add new information.

# Conversation:
# {long_text}

# Summary:
# """
#     return generate_answer(prompt)


# def update_summary(session_id: str, case_id: str, new_turn: str):
#     obj, _ = ConversationSummary.objects.get_or_create(
#         session_id=session_id,
#         case_id=case_id,
#         defaults={"summary": ""}
#     )

#     combined = (obj.summary + "\n" + new_turn).strip()

#     if len(combined) > MAX_MEMORY_CHARS:
#         combined = compress_summary(combined)

#     obj.summary = combined
#     obj.save()
