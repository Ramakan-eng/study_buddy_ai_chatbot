# Legal RAG Chatbot

## Overview

**Legal RAG Chatbot** is a Retrieval-Augmented Generation (RAG) system designed to answer questions about judicial cases using primary legal sources.

The system retrieves case law from the **CourtListener API**, stores it in a vector database, and uses a controlled LLM pipeline to generate grounded answers.

The goal of this project is to build a system that answers case-specific legal questions while **minimizing hallucination**, ensuring responses are derived only from retrieved legal documents.

The application follows a **DB-first retrieval strategy**, meaning the system always checks the local vector database before fetching data from external sources.

> This project was developed as part of an AI/ML internship and focuses on building a production-oriented RAG pipeline.

---

## Core Features

### Legal RAG Pipeline
Implements a Retrieval-Augmented Generation workflow where answers are generated using retrieved legal case documents instead of relying solely on the LLM's internal knowledge.

### DB-First Retrieval Strategy
The system first checks whether the requested case exists in the vector database.
- **If available** → retrieval happens locally
- **If not available** → the case is fetched from the CourtListener API and stored

### CourtListener Integration
The system integrates with the CourtListener API to retrieve:
- Judicial opinions
- Case citations
- Judge information
- Legal metadata

### Semantic Search
Legal case opinions are chunked and stored in **ChromaDB** using embeddings. User queries are matched against embeddings to retrieve the most relevant sections of a legal case.

### Query Classification
The system restricts queries to supported legal categories.

**Supported Query Types:**
- Case Brief
- Rule of Law
- Legal Issue
- Case Summary
- Majority Reasoning

> Queries such as cross-case comparisons or hypothetical legal scenarios are rejected.

### Deterministic Response via Caching
To ensure consistent responses, the system implements an **in-memory LRU cache**. If the same case + question is asked again, the cached answer is returned without calling the LLM again.

### Safety Validation
Generated responses are validated against retrieved document chunks to ensure answers remain grounded in the original legal sources.

---

## System Architecture

The system follows a modular architecture separating:
- Retrieval
- Prompting
- Answer generation
- Safety validation

### High-Level Workflow

1. User submits a case question
2. Query classification validates the request
3. System checks in-memory cache
4. System checks vector database
5. If case not found → fetch from CourtListener API
6. Store case data in ChromaDB
7. Retrieve relevant chunks
8. Build prompt for LLM
9. Generate answer
10. Validate response
11. Store response in cache
12. Return final answer

---

## User Flow

### Request Pipeline
```
User Request
→ Django API Endpoint
→ Query Classification
→ Cache Check
→ Vector Database Retrieval
→ CourtListener Fetch (if needed)
→ Chunking and Embedding
→ RAG Pipeline
→ LLM Generation
→ Safety Validation
→ Cache Storage
→ Final Response
```

---

## Project Structure
```
legal_study_bot/
├── chat/
│   ├── views.py
│   ├── urls.py
│   ├── chroma_store.py
│   ├── rag/
│   │   ├── retriever.py
│   │   ├── prompt.py
│   │   ├── generator.py
│   │   └── safety.py
│   ├── memory/
│   │   ├── in_memory_cache.py
│   │   └── memory.py
│   ├── models.py
│   └── utils/
├── chroma_db/
├── manage.py
├── requirements.txt
└── README.md
```

---

## Key Components

### `views.py`
Handles API requests and orchestrates the pipeline including caching, retrieval, and response generation.

### `chroma_store.py`
Responsible for storing case data in the vector database, including chunking judicial opinions and attaching metadata.

### `retriever.py`
Handles semantic search queries against ChromaDB using embedding similarity.

### `prompt.py`
Defines prompt templates used to structure LLM input for different legal query categories.

### `generator.py`
Handles interaction with the language model and generates the final response.

### `safety.py`
Validates generated responses to ensure they remain grounded in retrieved legal content.

### `in_memory_cache.py`
Implements an LRU cache to store previously generated answers for repeated queries.

---

## Data Processing Pipeline

When a case is fetched from the CourtListener API:

1. Case metadata is extracted
2. Judicial opinions are cleaned
3. Text is split into smaller chunks
4. Embeddings are generated
5. Embeddings are stored in ChromaDB with metadata

### Metadata Stored with Each Chunk

| Field | Description |
|---|---|
| `case_name` | Name of the legal case |
| `case_id` | Unique case identifier |
| `citation_key` | Legal citation reference |
| `opinion_type` | Type of judicial opinion |
| `author` | Author of the opinion |
| `chunk_index` | Index of the text chunk |

---

## Query Processing

When a user asks a question:

1. System validates the query category
2. Cache is checked for `(case_id + query)`
3. **If cached** → response returned immediately
4. **If not cached:**
   - Retrieve relevant chunks from ChromaDB
   - If case missing → fetch from CourtListener
   - Generate answer using retrieved context
   - Store answer in cache

---

## Caching Strategy

The system uses an **in-memory LRU cache**.

**Cache Key Format:** `case_id + query`

**Benefits:**
- Prevents repeated LLM calls
- Reduces response latency
- Ensures consistent answers
- Controls memory usage with LRU eviction

---

## Example API Request
```
GET /chat/ask/question/
```

**Parameters:**

| Parameter | Value |
|---|---|
| `case_id` | Roe v. Wade |
| `citation` | 410 U.S. 113 |
| `query` | what was the legal issue in this case |

**Example Response:**
```json
{
  "case_id": "Roe v. Wade",
  "question": "what was the legal issue in this case",
  "answer": "...",
  "chunks_used": 4,
  "source": "vector_db"
}
```

---

## Technologies Used

- **Python**
- **Django**
- **ChromaDB**
- **SentenceTransformers**
- **CourtListener API**
- REST APIs
- Vector Databases
- Retrieval Augmented Generation (RAG)
- Prompt Engineering

---

## Running the Project

### Clone the Repository
```bash
git clone <repo_url>
cd legal_study_bot
```

### Create Virtual Environment
```bash
python -m venv venv
```

### Activate Environment

**Linux / Mac:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run the Server
```bash
python manage.py runserver
```

### Environment Variables

Create a `.env` file and add:
```env
COURTLISTENER_TOKEN=your_api_token
OPENAI_API_KEY=your_api_key
```

---

## Future Improvements

- Redis-based distributed caching
- Streaming responses for long answers
- Case comparison support
- Multi-case reasoning
- Docker deployment
- Persistent memory storage
- Query intent classification using ML

---

## Motivation

Legal documents are long and complex, making them difficult to analyze quickly. This project aims to allow users to ask **natural language questions** about judicial cases while ensuring responses remain **accurate and grounded** in real legal sources.

Instead of relying purely on LLM knowledge, the system prioritizes **document retrieval and structured reasoning**.
