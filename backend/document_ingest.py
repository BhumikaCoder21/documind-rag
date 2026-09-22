import pymupdf
import chromadb
from sentence_transformers import SentenceTransformer
import uuid


model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="documents"
)


def ingest_pdf(pdf_path, filename):

    document = pymupdf.open(pdf_path)

    texts = []
    embeddings = []
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

                metadata = {
                    "source": filename,
                    "page": page_number + 1
                }

                metadatas.append(metadata)

                ids.append(
                    str(uuid.uuid4())
                )

            start = end - overlap

    document.close()

    if not texts:
        return 0

    embeddings = model.encode(texts).tolist()

    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas
    )

    return len(texts)