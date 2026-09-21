def create_chunks(text, chunk_size=500, overlap=50):
    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end]
        chunks.append(chunk)

        start = end - overlap

    return chunks

sample_text = """
Students must maintain a minimum attendance of 75%.
Students below 75% attendance may not be permitted
to appear for the semester examination.
Medical exemptions are subject to approval.
"""

chunks = create_chunks(sample_text, chunk_size=100, overlap=20)

for i, chunk in enumerate(chunks):
    print(f"\n--- Chunk {i + 1} ---")
    print(chunk)