async def answer_question(text: str) -> str:
    return (
        f"To answer your question about {text.strip()}, identify the key concept, "
        "check its definition, and apply it to the specific details in the question."
    )