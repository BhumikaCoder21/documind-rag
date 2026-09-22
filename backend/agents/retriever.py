import chromadb
from sentence_transformers import SentenceTransformer


model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_collection(
    name="documents"
)


def retrieve(question, top_k=3, source=None):

    embedding = model.encode(question).tolist()

    query_kwargs = {
        "query_embeddings": [embedding],
        "n_results": top_k
    }

    if source:
        query_kwargs["where"] = {
            "source": source
        }

    results = collection.query(**query_kwargs)

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    return documents, metadatas