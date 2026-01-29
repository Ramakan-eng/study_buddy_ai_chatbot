# import chromadb
# from chromadb.utils import embedding_functions
# from pathlib import Path
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# import uuid

# BASE_DIR = Path(__file__).resolve().parent.parent
# CHROMA_DIR = BASE_DIR / "chroma_db"

# embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
#     model_name="all-MiniLM-L6-v2"
# )

# client = chromadb.PersistentClient(
#     path=str(CHROMA_DIR)
# )
# collection = client.get_or_create_collection(
#     name="legal_cases",
#     embedding_function=embedding_fn
# )