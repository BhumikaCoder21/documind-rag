from agents.planner import plan_question
from agents.retriever import retrieve
from agents.answerer import generate_answer
from agents.validator import validate_answer


def run_documind(question, document_id=None):

    # 1. Planner Agent
    plan = plan_question(question)

    # 2. Retriever Agent
    documents, metadatas = retrieve(
        plan["question"],
        top_k=3,
        document_id=document_id
    )

    # 3. Answer Agent
    answer = generate_answer(
        question,
        documents,
        metadatas
    )

    # 4. Validator Agent
    is_supported = validate_answer(
        question,
        answer,
        documents
    )

    return answer, metadatas, is_supported


# Allow this file to still be tested directly
if __name__ == "__main__":

    question = input(
        "\nAsk a question about the academic regulations: "
    )

    answer, sources, is_supported = run_documind(question)

    print("\n===== DOCUMIND =====\n")

    if is_supported:
        print(answer)
    else:
        print(
            "I couldn't verify this answer against "
            "the provided document."
        )

    print("\n===== SOURCES =====\n")

    seen = set()

    for source in sources:

        key = (
            source["source"],
            source["page"]
        )

        if key not in seen:

            print(
                f"- {source['source']}, "
                f"Page {source['page']}"
            )

            seen.add(key)