async def explain_topic(text: str, level: str = "beginner") -> str:
    return (
        f"Here is a {level}-level explanation of {text.strip()}: "
        f"start with the core idea, connect it to a familiar example, "
        "and then practise applying it to a new problem."
    )