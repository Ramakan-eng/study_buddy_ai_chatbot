from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class SemanticCache:
    def __init__(self, embedding_model_name='all-MiniLM-L6-v2', dimension=384, similarity_threshold=0.8):
        self.embedding_model = SentenceTransformer(embedding_model_name)
        self.dimension = dimension
        self.cache = {}  
        self.case_indices = {} 
        self.case_embeddings = {} 
        self.case_queries = {}  
        self.similarity_threshold = similarity_threshold

    def _embed(self, text: str) -> np.ndarray:
        """Convert text to embedding vector"""
        embedding = self.embedding_model.encode([text])
        return np.array(embedding).astype('float32')
    
    def _calculate_similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        
        # Normalize embeddings
        emb1_norm = embedding1 / (np.linalg.norm(embedding1) + 1e-10)
        emb2_norm = embedding2 / (np.linalg.norm(embedding2) + 1e-10)
        # Cosine similarity
        similarity = np.dot(emb1_norm, emb2_norm.T)[0][0]
        return float(similarity)
    
    def semantic_cache_response(self, case_name: str, query: str) -> str | None:
     
        # If case not in index, return None
        if case_name not in self.case_indices:
            return None
        
        # Get embedding of incoming query
        query_embedding = self._embed(query)
        
        # Search in case-specific FAISS index
        # Returns top 1 result and its L2 distance
        index = self.case_indices[case_name]
        distances, indices = index.search(query_embedding, k=1)
        
        if len(indices[0]) == 0 or indices[0][0] == -1:
            return None
        
        # Convert L2 distance to similarity score (0 to 1)
        # L2 distance: lower = more similar
        # similarity = 1 / (1 + distance)
        l2_distance = distances[0][0]
        similarity_score = 1 / (1 + l2_distance)
        
        # If similarity meets threshold, return cached response
        if similarity_score >= self.similarity_threshold:
            matched_query = self.case_queries[case_name][indices[0][0]]
            cache_key = (case_name, matched_query)
            return self.cache.get(cache_key)
        
        return None
    
    def store_in_semantic_cache(self, case_name: str, query: str, response: str) -> None:
        """Store response in semantic cache"""
        cache_key = (case_name, query)
        
        # Skip if already cached (exact match)
        if cache_key in self.cache:
            return
        
        # Store in cache
        self.cache[cache_key] = response
        
        # Initialize case index if needed
        if case_name not in self.case_indices:
            self.case_indices[case_name] = faiss.IndexFlatL2(self.dimension)
            self.case_embeddings[case_name] = []
            self.case_queries[case_name] = []
        
        # Embed the query (not the response)
        query_embedding = self._embed(query)
        
        # Add to case-specific index
        self.case_indices[case_name].add(query_embedding)
        self.case_embeddings[case_name].append(query_embedding)
        self.case_queries[case_name].append(query)
    
    def clear_case_cache(self, case_name: str) -> None:
        """Clear cache for a specific case"""
        # Remove all entries for this case
        keys_to_remove = [key for key in self.cache.keys() if key[0] == case_name]
        for key in keys_to_remove:
            del self.cache[key]
        
        # Clear indices
        if case_name in self.case_indices:
            del self.case_indices[case_name]
            del self.case_embeddings[case_name]
            del self.case_queries[case_name]
    
    def get_cache_stats(self, case_name: str = None) -> dict:
        """Get cache statistics"""
        if case_name:
            count = len([key for key in self.cache.keys() if key[0] == case_name])
            return {
                'case_name': case_name,
                'cached_queries': count
            }
        else:
            return {
                'total_cached_queries': len(self.cache),
                'cases_count': len(self.case_indices)
            }

