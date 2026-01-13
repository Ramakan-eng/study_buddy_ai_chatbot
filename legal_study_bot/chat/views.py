import os
import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from chat.chroma_store import collection, store_case_in_chroma,normalize_case_id
#build_case_promp,build_prompt,classify_query,
from chat.rag.prompt import build_case_prompt
from chat.rag import retrieve_case_chunks, generate_answer, validate_answer,detect_intent 
from chat.memory import get_summary, update_summary
from chat.models import ConversationSummary

# CourtListener setup


COURTLISTENER_BASE = "https://www.courtlistener.com/api/rest/v4"
_TOKEN = os.environ.get("COURTLISTENER_TOKEN") or getattr(settings, "COURTLISTENER_TOKEN", "")
_TOKEN =  "8801d9c790ffe652460d0a24d6bd41b22ffa19b0"
HEADERS = {"Authorization": f"Token {_TOKEN}"} if _TOKEN else {}

# Helpers


def clean_text(html_or_text):
    if html_or_text and html_or_text.strip().startswith("<"):
        soup = BeautifulSoup(html_or_text, "html.parser")
        return soup.get_text(separator="\n", strip=True)
    return html_or_text or ""


def  case_exists_in_chroma(case_id: str) -> bool:
    """
    Check whether any chunk exists for this case_id
    """
    try:
        # case_id = normalize_case_id(case_id)
        results = collection.query(
                    query_texts=["privacy"],
                    n_results=3,
                    where={"case_id": case_id}
                )
        return len(results.get("documents", [[]])[0]) > 0
    except Exception:
        return False


def fetch_case_from_courtlistener(case_name: str, citation: str | None):
    """
    Fetch case + opinions from CourtListener
    """
    search_url = f"{COURTLISTENER_BASE}/search/"
    params = {"q": case_name, "type": "o"}

    try:
        search_res = requests.get(
            search_url, headers=HEADERS, params=params, timeout=15
        ).json()
    except Exception:
        return None, "CourtListener request failed"

    results = search_res.get("results", [])
    if not results:
        return None, "No cases found"

    cluster_id = None

    # If citation provided → strict match
    if citation:
        for r in results:
            for cite in r.get("citation", []):
                if citation.lower() in cite.lower():
                    cluster_id = r.get("cluster_id")
                    break
            if cluster_id:
                break

        if not cluster_id:
            return None, "Citation did not match any case"

    # No citation → accept only single confident result
    else:
        if len(results)  >= 1:
            cluster_id = results[0].get("cluster_id")
        else:
            return None, "Multiple cases found. Please provide citation."

    # Fetch cluster
    try:
        cluster = requests.get(
            f"{COURTLISTENER_BASE}/clusters/{cluster_id}/",
            headers=HEADERS,
            timeout=15
        ).json()
    except Exception:
        return None, "Failed to fetch case cluster"

    opinions = []
    for op_url in cluster.get("sub_opinions", []):
        try:
            op = requests.get(op_url, headers=HEADERS, timeout=15).json()
            text = clean_text(
                op.get("html_with_citations") or op.get("plain_text", "")
            )
            opinions.append({
                "author": op.get("author_str", ""),
                "opinion_type": op.get("type"),
                "text": text
            })
        except Exception:
            continue

    return {
        "case_id": cluster.get("case_id"),     
        "case_name": cluster.get("case_name"),
        "citations": cluster.get("citations"),
        "court": cluster.get("court"),
        "date_filed": cluster.get("date_filed"),
        "opinions": opinions
    }, None


# MAIN ENDPOINT (DB FIRST)


@csrf_exempt
def ask_case(request):
    """
    Single unified endpoint

    Required:
      - case_id (case name for now)
      - query   (user question)

    Optional:
      - citation
    """

    case_id = (request.GET.get("case_id") or request.POST.get("case_id"))
    query = request.GET.get("query") or request.POST.get("query")
    citation = request.GET.get("citation") or request.POST.get("citation")
    session_id = request.GET.get("session_id", "default_session")
    print(case_id, query, citation, session_id)
    if not case_id:
        return JsonResponse({"error": "case_id is required"}, status=400)

    if not query:
        return JsonResponse({"error": "query is required"}, status=400)

    if not HEADERS:
        return JsonResponse(
            {"error": "CourtListener token not configured"},
            status=500
        )

    intent = detect_intent(query)
    if intent == 0:
        # return JsonResponse({"answer": "This question is currently not supported in StudyBuddyPro Phase 1."})
        ans = "This question is currently not supported in StudyBuddyPro Phase 1."
        safe_answer = generate_answer(ans)
        return JsonResponse({
            "case_id": case_id,
            "answer": safe_answer})
    else:

        print("Intent detected as supported question.")
 #   DB FIRST

        if not case_exists_in_chroma(case_id):
            case_data, error = fetch_case_from_courtlistener(case_id, citation)

            if error:
                return JsonResponse({"error": error}, status=404)

            try:
                store_case_in_chroma(case_data)
            except Exception as e:
                return JsonResponse(
                    {"error": "Failed to store case in vector DB", "detail": str(e)},
                    status=500
                )

            source = "courtlistener_then_vector_db"
        else:
            source = "vector_db"


        #  RAG
        chunks = retrieve_case_chunks(query, case_id)

        if not chunks:
            return JsonResponse(
                {"error": "No relevant content found for this case"},
                status=404
            )


 
        prompt = build_case_prompt(query, chunks)
        # prompt = build_prompt(category, query, chunks)
        # print("Generated prompt:", prompt)
        answer = generate_answer(prompt)


        ok, safe_answer = validate_answer(answer, chunks)
        if not ok:
            return JsonResponse(
                {"error": "Answer failed safety checks", "detail": safe_answer},
                status=422
            )


        return JsonResponse({
            "case_id": case_id,
            "question": query,
            "answer": safe_answer,
            # "chunks_used": len(chunks),
            "source": source
        })
