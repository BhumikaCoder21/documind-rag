import chromadb
from sentence_transformers import SentenceTransformer


model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_collection(
    name="documents"
)


def retrieve(question, top_k=3, document_id=None):

    embedding = model.encode(question).tolist()

    query_kwargs = {
        "query_embeddings": [embedding],
        "n_results": top_k
    }

    # Retrieve ONLY from the selected document
    if document_id:

        query_kwargs["where"] = {
            "document_id": document_id
        }

    results = collection.query(
        **query_kwargs
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    return documents, metadatas