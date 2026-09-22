# DocuMind — Multi-Agent RAG Knowledge Assistant

DocuMind is a full-stack document question-answering system that allows users to upload PDF documents and ask questions about their contents.

It uses Retrieval-Augmented Generation (RAG) to retrieve relevant document sections before generating an answer. A multi-agent workflow is used to plan the task, retrieve relevant information, generate the response, and validate the answer against the retrieved context.

The system runs locally using Sentence Transformers for embeddings, ChromaDB for vector search, and Llama 3.2 through Ollama for answer generation.

---

## Features

- Upload PDF documents dynamically
- Extract and chunk document text
- Generate semantic embeddings locally
- Store and search document chunks using ChromaDB
- Ask natural-language questions about uploaded documents
- Retrieve relevant document sections using semantic search
- Generate grounded answers using a local LLM
- Validate generated answers against retrieved context
- Display source document and page references
- Support replacing previously uploaded documents with the same filename
- Full-stack interface using Next.js and FastAPI
- Runs locally without requiring paid AI APIs

---

## Architecture

```text
                    ┌─────────────────┐
                    │    PDF Upload   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Text Extraction │
                    │   + Chunking    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Local Embeddings│
                    │ SentenceTrans.  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    ChromaDB     │
                    │  Vector Store   │
                    └────────┬────────┘
                             │
                       User Question
                             │
                             ▼
                    ┌─────────────────┐
                    │  Planner Agent  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Retriever Agent │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  Answer Agent   │
                    │  Llama 3.2      │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Validator Agent │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Answer + Sources│
                    └─────────────────┘

Tech Stack

Frontend
    Next.js
    React
    TypeScript
    Tailwind CSS
Backend
    Python
    FastAPI
    PyMuPDF
AI / RAG
    Sentence Transformers
    all-MiniLM-L6-v2
    ChromaDB
    Ollama
    Llama 3.2

Project Structure

documind-rag/
│
├── backend/
│   ├── agents/
│   │   ├── planner.py
│   │   ├── retriever.py
│   │   ├── answerer.py
│   │   └── validator.py
│   │
│   ├── api.py
│   ├── document_ingest.py
│   ├── multi_agent_rag.py
│   └── read_pdf.py
│
├── frontend/
│   ├── app/
│   │   └── page.tsx
│   └── package.json
│
├── .gitignore
├── .env.example
└── README.md


Getting Started
Prerequisites
Python 3.12+
Node.js
Ollama
Clone the Repository
git clone https://github.com/BhumikaCoder21/documind-rag.git
cd documind-rag
Setup Backend
cd backend
python -m venv .venv

On Windows:

.venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt
Setup Ollama

Install Ollama and download the model:

ollama pull llama3.2:3b
Start Backend
uvicorn api:app --reload --port 8000

Backend:

http://127.0.0.1:8000
Start Frontend

Open another terminal:

cd frontend
npm install
npm run dev

Open:

http://localhost:3000


Author

Bhumika Gupta

Computer Science & Engineering
National Institute of Technology Arunachal Pradesh

GitHub: https://github.com/BhumikaCoder21