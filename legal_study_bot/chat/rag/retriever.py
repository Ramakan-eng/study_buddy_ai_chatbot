from chat.chroma_store import collection

TOP_K = 5

def retrieve_case_chunks(
    query: str,
    case_id: str,
    top_k: int = TOP_K
):
    """
    Retrieve top-k relevant chunks for a given case from ChromaDB
    """

    results = collection.query(
        query_texts=[query],
        n_results=top_k,
        where={"case_id": case_id}
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    chunks = []
    for doc, meta in zip(documents, metadatas):
        chunks.append({
            "text": doc,
            "metadata": meta
        })

    return chunks
