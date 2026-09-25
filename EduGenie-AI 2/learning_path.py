from schemas import LearningPathResponse


async def get_learning_recommendations(
    topic: str,
    level: str = "beginner",
) -> LearningPathResponse:
    return LearningPathResponse(
        topic=topic.strip(),
        level=level,
        recommendations=[
            f"Review the {level}-level foundations of {topic}.",
            f"Work through a guided example involving {topic}.",
            f"Solve three practice problems about {topic}.",
            f"Explain {topic} in your own words and identify any gaps.",
        ],
    )