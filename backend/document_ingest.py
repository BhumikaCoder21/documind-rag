import os
import uuid

import pymupdf
import chromadb
from sentence_transformers import SentenceTransformer


model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="documents"
)


def ingest_pdf(pdf_path, filename):

    # Generate a unique ID for this upload
    document_id = str(uuid.uuid4())

    # Remove previous versions of the same filename
    # so old chunks cannot interfere.
    collection.delete(
        where={
            "source": filename
        }
    )

    document = pymupdf.open(pdf_path)

    texts = []
    metadatas = []
    ids = []

    for page_number, page in enumerate(document):

        text = page.get_text()

        chunk_size = 500
        overlap = 50

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunk = text[start:end].strip()

            if chunk:

                texts.append(chunk)

                metadatas.append({
                    "source": filename,
                    "page": page_number + 1,
                    "document_id": document_id
                })

                ids.append(
                    f"{document_id}_{uuid.uuid4()}"
                )

            start = end - overlap

    document.close()

    if not texts:
        return {
            "document_id": document_id,
            "chunks": 0
        }

    embeddings = model.encode(texts).tolist()

    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas
    )

    return {
        "document_id": document_id,
        "chunks": len(texts)
    }