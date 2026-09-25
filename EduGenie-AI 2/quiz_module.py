from schemas import QuizQuestion, QuizResponse


async def generate_quiz(text: str, num_questions: int = 5) -> QuizResponse:
    topic = text.strip()
    questions = [
        QuizQuestion(
            question=f"Which statement best describes {topic}?",
            options=[
                f"A foundational idea related to {topic}",
                "An unrelated process",
                "A measurement unit",
                "A fictional example",
            ],
            answer=f"A foundational idea related to {topic}",
        )
        for _ in range(num_questions)
    ]
    return QuizResponse(questions=questions)