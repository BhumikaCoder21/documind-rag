import chromadb

# Create a local ChromaDB client
client = chromadb.PersistentClient(path="./chroma_db")

# Create a collection
collection = client.get_or_create_collection(
    name="college_rules"
)

print("Collection created successfully!")
print("Collection name:", collection.name)