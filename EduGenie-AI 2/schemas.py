from pydantic import BaseModel, Field


class ApiResponse(BaseModel):
    result: str


class TextRequest(BaseModel):
    text: str = Field(min_length=1)


class ExplainRequest(TextRequest):
    level: str = "beginner"


class QuizRequest(TextRequest):
    num_questions: int = Field(default=5, ge=1, le=20)


class QuizQuestion(BaseModel):
    question: str
    options: list[str]
    answer: str


class QuizResponse(BaseModel):
    questions: list[QuizQuestion]


class LearningPathRequest(BaseModel):
    topic: str = Field(min_length=1)
    level: str = "beginner"


class LearningPathResponse(BaseModel):
    topic: str
    level: str
    recommendations: list[str]