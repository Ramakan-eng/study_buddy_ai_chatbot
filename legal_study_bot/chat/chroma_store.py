import chromadb
from chromadb.utils import embedding_functions
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
import uuid
# Project root & ChromaDB directory
BASE_DIR = Path(__file__).resolve().parent.parent
CHROMA_DIR = BASE_DIR / "chroma_db"

# Embedding function

embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# Persistent Chroma Client

client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)

collection = client.get_or_create_collection(
    name="legal_cases",
    embedding_function=embedding_fn
)

#  Recursive Text Splitter (legal-optimized)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150,
    separators=["\n\n", "\n", ".", " ", ""]
)

#  Case ID normalizer (consistent keys)

def normalize_case_id(case_name: str) -> str:
    return (
        case_name
        .lower()
        .strip()
        .replace(".", "")
        .replace(",", "")
        .replace(" v ", "_v_")
        .replace(" ", "_")
    )



#  Citation normalizer (clean + searchable)

def normalize_citation(citations) -> str:
    """
    Convert CourtListener citation list to a clean searchable string
    Example: '64 N.E.3d 231'
    """
    if not citations:
        return ""

    c = citations[0]
    return f"{c.get('volume')} {c.get('reporter')} {c.get('page')}".lower()

#  Store case in ChromaDB

def store_case_in_chroma(case_data: dict):
    """
    Chunk full case text and store in ChromaDB.
    case_id is stored EXACTLY as case_name (no normalization).
    """

    documents = []
    metadatas = []
    ids = []

    case_name = case_data.get("case_name")   
    case_id = case_name                      


    citation_key = normalize_citation(case_data.get("citations", []))

    for opinion in case_data.get("opinions", []):
        opinion_text = opinion.get("text", "")
        opinion_type = opinion.get("type", "unknown")
        author = opinion.get("author", "")

        chunks = text_splitter.split_text(opinion_text)

        for chunk_index, chunk in enumerate(chunks):
            if len(chunk.strip()) <0:
                continue

            documents.append(chunk)

            metadatas.append({
                "case_id": case_id,          # exact case name
                "case_name": case_name,
                "citation_key": citation_key,
                "opinion_type": opinion_type,
                "author": author,
                "chunk_index": chunk_index
            })

            # ids.append(f"{case_id}_{opinion_type}_{chunk_index}")
            ids.append(f"{case_id}_{uuid.uuid4().hex}")

    if documents:
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

        print("Stored vectors count:", collection.count())


































