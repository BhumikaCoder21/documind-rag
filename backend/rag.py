import chromadb
from sentence_transformers import SentenceTransformer
import ollama


# 1. Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


# 2. Connect to ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_collection(
    name="college_rules"
)


# 3. Ask the user a question
question = input("\nAsk a question about the academic regulations: ")


# 4. Convert question into an embedding
question_embedding = model.encode(question).tolist()


# 5. Retrieve relevant chunks
results = collection.query(
    query_embeddings=[question_embedding],
    n_results=3
)


# 6. Build context from retrieved chunks
context_parts = []

for i in range(len(results["documents"][0])):
    text = results["documents"][0][i]
    page = results["metadatas"][0][i]["page"]
    source = results["metadatas"][0][i]["source"]

    context_parts.append(
        f"[Source: {source}, Page: {page}]\n{text}"
    )

context = "\n\n".join(context_parts)


# 7. Give retrieved context to Llama
prompt = f"""
You are DocuMind, a document question-answering assistant.

Answer the user's question using ONLY the provided context.

If the answer cannot be found in the context, say:
"I couldn't find this information in the provided document."

Do not make up information.

Context:
{context}

Question:
{question}

Answer:
"""


# 8. Generate answer using local Llama
response = ollama.chat(
    model="llama3.2:3b",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)


# 9. Display answer
print("\n===== DOCUMIND ANSWER =====\n")
print(response["message"]["content"])

print("\n===== SOURCES =====\n")

for metadata in results["metadatas"][0]:
    print(
        f"- {metadata['source']}, Page {metadata['page']}"
    )