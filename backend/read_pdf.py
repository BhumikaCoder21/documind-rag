import pymupdf


def create_chunks(text, chunk_size=500, overlap=50):
    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end]
        chunks.append(chunk)

        start = end - overlap

    return chunks


pdf_path = "documents/college_rules.pdf"

document = pymupdf.open(pdf_path)

all_chunks = []

for page_number, page in enumerate(document):

    text = page.get_text()

    chunks = create_chunks(text)

    for chunk in chunks:

        all_chunks.append({
            "text": chunk,
            "page": page_number + 1,
            "source": "college_rules.pdf"
        })

document.close()


for i, chunk in enumerate(all_chunks[:5]):

    print(f"\n--- Chunk {i + 1} ---")
    print(f"Page: {chunk['page']}")
    print(f"Source: {chunk['source']}")
    print(chunk["text"])