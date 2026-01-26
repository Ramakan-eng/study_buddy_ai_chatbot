from collections import OrderedDict


class InMemoryCache:
    def __init__(self, max_size=100):
        self.cache = OrderedDict()
        self.max_size = max_size

    def get_cached_response(self, case_id: str, query: str) -> str | None:
        key = (case_id, query)
        
        if key in self.cache:
            self.cache.move_to_end(key)  
            return self.cache[key]
        return None

    def store_cache(self, case_id: str, query: str, response: str) -> None:
        key = (case_id, query)
        if key in self.cache:
            self.cache.move_to_end(key)
        else:
            if len(self.cache) >= self.max_size:
                self.cache.popitem(last=False)  
        self.cache[key] = response

   