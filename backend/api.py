from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from document_ingest import ingest_pdf
from multi_agent_rag import run_documind

import os
import shutil


app = FastAPI(title="DocuMind API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


UPLOAD_DIR = "uploaded_documents"

os.makedirs(UPLOAD_DIR, exist_ok=True)


class QuestionRequest(BaseModel):
    question: str
    document_id: str


@app.get("/")
def root():
    return {
        "message": "DocuMind API is running"
    }


@app.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):

    if not file.filename.lower().endswith(".pdf"):
        return {
            "success": False,
            "message": "Only PDF files are supported."
        }

    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    result = ingest_pdf(
        file_path,
        file.filename
    )

    return {
        "success": True,
        "filename": file.filename,
        "document_id": result["document_id"],
        "chunks": result["chunks"]
    }


@app.post("/ask")
def ask_question(request: QuestionRequest):

    answer, sources, is_supported = run_documind(
        request.question,
        request.document_id
    )

    unique_sources = []

    seen = set()

    for source in sources:

        key = (
            source["source"],
            source["page"]
        )

        if key not in seen:

            unique_sources.append({
                "source": source["source"],
                "page": source["page"]
            })

            seen.add(key)

    return {
        "answer": (
            answer
            if is_supported
            else
            "I couldn't verify this answer "
            "against the uploaded document."
        ),
        "sources": unique_sources,
        "supported": is_supported
    }