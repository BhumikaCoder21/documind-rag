import ollama


def generate_answer(question, documents, metadatas):

    context_parts = []

    for document, metadata in zip(documents, metadatas):

        context_parts.append(
            f"[Source: {metadata['source']}, "
            f"Page: {metadata['page']}]\n"
            f"{document}"
        )

    context = "\n\n".join(context_parts)

    prompt = f"""
You are the Answer Agent in DocuMind.

Answer the user's question using ONLY the provided context.

Do not invent information.

If the context does not contain the answer, say:
"I couldn't find this information in the provided document."

Question:
{question}

Context:
{context}

Answer:
"""

    response = ollama.chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]