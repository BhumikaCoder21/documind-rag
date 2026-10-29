import chromadb

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="college_rules"
)

print("Collection created successfully!")
print("Collection name:", collection.name)
