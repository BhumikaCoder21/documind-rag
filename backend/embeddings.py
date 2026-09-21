from sentence_transformers import SentenceTransformer

# Load a free local embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

text = "Students must maintain a minimum attendance of 75%."

embedding = model.encode(text)

print("Number of dimensions:", len(embedding))
print("First 10 values:", embedding[:10])