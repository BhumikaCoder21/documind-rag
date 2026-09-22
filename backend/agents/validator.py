import ollama


def validate_answer(question, answer, documents):

    context = "\n\n".join(documents)

    prompt = f"""
You are the Validator Agent.

Check whether the answer is supported by the provided context.

Question:
{question}

Context:
{context}

Answer:
{answer}

Respond with ONLY one word:

SUPPORTED

or

UNSUPPORTED
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

    result = response["message"]["content"].strip().upper()

    return "SUPPORTED" in result