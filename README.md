## StudyBuddy Legal RAG Chatbot
Overview
CourtListener Integration
This project is a Legal Retrieval-Augmented Generation (RAG) system designed to answer questions about judicial cases using primary legal sources. The system retrieves case law from the CourtListener API, stores it in a vector database, and uses a controlled LLM pipeline to generate grounded answers.

The goal of the project is to build a system that answers case-specific questions while minimizing hallucination and ensuring that answers are derived only from the retrieved legal documents.

The system follows a DB-first retrieval strategy, meaning the application always checks the local vector database before fetching data from external sources.

This project was developed as part of an AI/ML internship and focuses on building a production-oriented pipeline rather than a prototype chatbot.

Core Features
Legal RAG Pipeline

Implements a Retrieval-Augmented Generation workflow where answers are generated using retrieved case law documents instead of relying solely on LLM knowledge.

DB-First Retrieval Strategy

The system first checks whether the requested case already exists in the vector database. If it exists, retrieval happens locally. If not, the case is fetched from CourtListener and stored.

CourtListener Integration

The application integrates with the CourtListener API to retrieve real judicial opinions, citations, judges, and metadata.

Semantic Search

Case opinions are chunked and stored in ChromaDB with embeddings. Queries are matched against these embeddings to retrieve the most relevant parts of a case.

Query Classification

The system restricts queries to supported categories such as:

Case brief

Rule of law

Legal issue

Case summary

Majority reasoning

Unsupported queries such as cross-case comparisons or hypothetical questions are rejected.

Deterministic Response via Caching

To ensure consistent answers for repeated queries, the system implements an in-memory LRU cache. If the same case and question are asked again, the stored answer is returned without calling the LLM.

Safety Validation

Generated responses are validated against retrieved chunks to ensure answers remain grounded in the source material.

System Architecture

The application follows a modular architecture separating retrieval, prompting, generation, and safety validation.

High-level workflow:

User submits a case question

Query classification validates the request

System checks in-memory cache

System checks vector database

If case not found, fetch from CourtListener

Store case data in ChromaDB

Retrieve relevant chunks

Build prompt for LLM

Generate answer

Validate response

Store response in cache

Return answer to user

User Flow

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

Project Structure
legal_study_bot/
│
├── chat/
│   ├── views.py
│   ├── urls.py
│   ├── chroma_store.py
│   │
│   ├── rag/
│   │   ├── retriever.py
│   │   ├── prompt.py
│   │   ├── generator.py
│   │   └── safety.py
│   │
│   ├── memory/
│   │   ├── in_memory_cache.py
│   │   └── memory.py
│   │
│   ├── models.py
│   └── utils/
│
├── chroma_db/
│
├── manage.py
├── requirements.txt
└── README.md
Key Components
views.py

Handles API requests and orchestrates the pipeline including caching, retrieval, and generation.

chroma_store.py

Responsible for storing case data in the vector database. This includes chunking judicial opinions and attaching metadata.

retriever.py

Handles semantic search queries against ChromaDB using case filters and embedding similarity.

prompt.py

Defines prompt templates used to structure LLM input for different query categories.

generator.py

Handles interaction with the language model.

safety.py

Validates generated responses to ensure they remain grounded in retrieved legal content.

in_memory_cache.py

Implements an LRU cache to store previously generated answers for repeated queries.

Data Processing Pipeline

When a case is fetched from CourtListener:

Case metadata is extracted

Judicial opinions are cleaned and converted to text

Text is split into chunks using recursive text splitting

Each chunk is embedded

Embeddings are stored in ChromaDB with metadata

Metadata stored with each chunk includes:

case_name

case_id

citation_key

opinion_type

author

chunk_index

Query Processing

When a user asks a question:

System validates the query category

Cache is checked for identical (case_id + query)

If cached, response is returned immediately

If not cached:

retrieve relevant chunks from ChromaDB

if case missing, fetch from CourtListener

generate answer using retrieved context

Store answer in cache for future requests

Caching Strategy

The system uses an in-memory LRU cache to ensure deterministic responses.

Cache key format:

case_id + query

Benefits:

Prevents repeated LLM calls

Reduces latency

Ensures consistent answers

Controls memory usage with LRU eviction

Example API Request
GET /chat/ask/question/

Parameters:
case_id = Roe v. Wade
citation = 410 U.S. 113
query = what was the legal issue in this case

Example response:

{
  "case_id": "Roe v. Wade",
  "question": "what was the legal issue in this case",
  "answer": "...",
  "chunks_used": 4,
  "source": "vector_db"
}
Technologies Used

Python

Django

ChromaDB

SentenceTransformers

CourtListener API

REST APIs

Vector Databases

Retrieval Augmented Generation

Prompt Engineering

Motivation
StudyBuddy Legal RAG Chatbot
Overview

This project is a Legal Retrieval-Augmented Generation (RAG) system designed to answer questions about judicial cases using primary legal sources. The system retrieves case law from the CourtListener API, stores it in a vector database, and uses a controlled LLM pipeline to generate grounded answers.

The goal of the project is to build a system that answers case-specific questions while minimizing hallucination and ensuring that answers are derived only from the retrieved legal documents.

The system follows a DB-first retrieval strategy, meaning the application always checks the local vector database before fetching data from external sources.

This project was developed as part of an AI/ML internship and focuses on building a production-oriented pipeline rather than a prototype chatbot.

Core Features
Legal RAG Pipeline

Implements a Retrieval-Augmented Generation workflow where answers are generated using retrieved case law documents instead of relying solely on LLM knowledge.

DB-First Retrieval Strategy

The system first checks whether the requested case already exists in the vector database. If it exists, retrieval happens locally. If not, the case is fetched from CourtListener and stored.

CourtListener Integration

The application integrates with the CourtListener API to retrieve real judicial opinions, citations, judges, and metadata.

Semantic Search

Case opinions are chunked and stored in ChromaDB with embeddings. Queries are matched against these embeddings to retrieve the most relevant parts of a case.

Query Classification

The system restricts queries to supported categories such as:

Case brief

Rule of law

Legal issue

Case summary

Majority reasoning

Unsupported queries such as cross-case comparisons or hypothetical questions are rejected.

Deterministic Response via Caching

To ensure consistent answers for repeated queries, the system implements an in-memory LRU cache. If the same case and question are asked again, the stored answer is returned without calling the LLM.

Safety Validation

Generated responses are validated against retrieved chunks to ensure answers remain grounded in the source material.

System Architecture

The application follows a modular architecture separating retrieval, prompting, generation, and safety validation.

High-level workflow:

User submits a case question

Query classification validates the request

System checks in-memory cache

System checks vector database

If case not found, fetch from CourtListener

Store case data in ChromaDB

Retrieve relevant chunks

Build prompt for LLM

Generate answer

Validate response

Store response in cache

Return answer to user

User Flow

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

Project Structure
legal_study_bot/
│
├── chat/
│   ├── views.py
│   ├── urls.py
│   ├── chroma_store.py
│   │
│   ├── rag/
│   │   ├── retriever.py
│   │   ├── prompt.py
│   │   ├── generator.py
│   │   └── safety.py
│   │
│   ├── memory/
│   │   ├── in_memory_cache.py
│   │   └── memory.py
│   │
│   ├── models.py
│   └── utils/
│
├── chroma_db/
│
├── manage.py
├── requirements.txt
└── README.md
Key Components
views.py

Handles API requests and orchestrates the pipeline including caching, retrieval, and generation.

chroma_store.py

Responsible for storing case data in the vector database. This includes chunking judicial opinions and attaching metadata.

retriever.py

Handles semantic search queries against ChromaDB using case filters and embedding similarity.

prompt.py

Defines prompt templates used to structure LLM input for different query categories.

generator.py

Handles interaction with the language model.

safety.py

Validates generated responses to ensure they remain grounded in retrieved legal content.

in_memory_cache.py

Implements an LRU cache to store previously generated answers for repeated queries.

Data Processing Pipeline

When a case is fetched from CourtListener:

Case metadata is extracted

Judicial opinions are cleaned and converted to text

Text is split into chunks using recursive text splitting

Each chunk is embedded

Embeddings are stored in ChromaDB with metadata

Metadata stored with each chunk includes:

case_name

case_id

citation_key

opinion_type

author

chunk_index

Query Processing

When a user asks a question:

System validates the query category

Cache is checked for identical (case_id + query)

If cached, response is returned immediately

If not cached:

retrieve relevant chunks from ChromaDB

if case missing, fetch from CourtListener

generate answer using retrieved context

Store answer in cache for future requests

Caching Strategy

The system uses an in-memory LRU cache to ensure deterministic responses.

Cache key format:

case_id + query

Benefits:

Prevents repeated LLM calls

Reduces latency

Ensures consistent answers

Controls memory usage with LRU eviction

Example API Request
GET /chat/ask/question/

Parameters:
case_id = Roe v. Wade
citation = 410 U.S. 113
query = what was the legal issue in this case

Example response:

{
  "case_id": "Roe v. Wade",
  "question": "what was the legal issue in this case",
  "answer": "...",
  "chunks_used": 4,
  "source": "vector_db"
}
Technologies Used

Python

Django

ChromaDB

SentenceTransformers

CourtListener API

REST APIs

Vector Databases

Retrieval Augmented Generation

Prompt Engineering

Running the Project

Clone the repository

git clone <repo_url>
cd legal_study_bot

Create virtual environment

python -m venv venv

Activate environment

Linux / Mac

source venv/bin/activate

Windows

venv\Scripts\activate

Install dependencies

pip install -r requirements.txt

Run Django server

python manage.py runserver
Environment Variables

Create a .env file and add:

COURTLISTENER_TOKEN=your_api_token
OPENAI_API_KEY=your_api_key
Future Improvements

Possible improvements for the system include:

Redis based distributed caching

Streaming responses for large answers

Case comparison support

Multi-case reasoning

Deployment with Docker and Gunicorn

Persistent memory storage

Query intent classification using ML

Motivation

Legal documents are long and difficult to navigate. The goal of this project was to design a system that allows users to ask natural language questions about cases while ensuring answers remain grounded in the original judicial opinions.

Instead of relying purely on language models, the system prioritizes document retrieval and structured reasoning.

Legal documents are long and difficult to navigate. The goal of this project was to design a system that allows users to ask natural language questions about cases while ensuring answers remain grounded in the original judicial opinions.

Instead of relying purely on language models, the system prioritizes document retrieval and structured reasoning.
