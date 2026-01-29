from chat.models import CachedResponse
import sqlite3


def cache_response(case_name: str, query: str) -> None:
    data = CachedResponse.objects.filter(case_name=case_name, query=query).first()
    if data:
       return data.response
    return None

def store_in_sql_cache(case_name: str, query: str, response: str) -> None:
    CachedResponse.objects.update_or_create(
        case_name=case_name,
        query=query,
        defaults={'response': response}
    )