import chromadb
from sentence_transformers import SentenceTransformer


# Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


# Connect to our existing ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_collection(
    name="college_rules"
)


# User's question
question = "What is the minimum attendance required?"


# Convert question into an embedding
question_embedding = model.encode(question).tolist()


# Search ChromaDB
results = collection.query(
    query_embeddings=[question_embedding],
    n_results=3
)


# Display the results
print("\n===== SEARCH RESULTS =====\n")

for i in range(len(results["documents"][0])):

    print(f"--- Result {i + 1} ---")

    print("Page:", results["metadatas"][0][i]["page"])
    print("Source:", results["metadatas"][0][i]["source"])

    print("\nText:")
    print(results["documents"][0][i])

    print("\nDistance:")
    print(results["distances"][0][i])

    print()