import pymupdf
import chromadb
from sentence_transformers import SentenceTransformer


# -----------------------------
# 1. Load embedding model
# -----------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")


# -----------------------------
# 2. Connect to ChromaDB
# -----------------------------
client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="college_rules"
)


# -----------------------------
# 3. Open PDF
# -----------------------------
pdf_path = "documents/college_rules.pdf"

document = pymupdf.open(pdf_path)


# -----------------------------
# 4. Extract and chunk text
# -----------------------------
all_chunks = []

for page_number, page in enumerate(document):

    text = page.get_text()

    chunk_size = 500
    overlap = 50

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            all_chunks.append({
                "text": chunk,
                "page": page_number + 1,
                "source": "college_rules.pdf"
            })

        start = end - overlap


document.close()


# -----------------------------
# 5. Generate embeddings
# -----------------------------
texts = [chunk["text"] for chunk in all_chunks]

embeddings = model.encode(texts).tolist()


# -----------------------------
# 6. Store in ChromaDB
# -----------------------------
ids = [f"chunk_{i}" for i in range(len(all_chunks))]

metadatas = [
    {
        "page": chunk["page"],
        "source": chunk["source"]
    }
    for chunk in all_chunks
]

collection.add(
    ids=ids,
    documents=texts,
    embeddings=embeddings,
    metadatas=metadatas
)


print("Documents added successfully!")
print("Number of chunks:", len(all_chunks))
print("Stored in collection:", collection.name)