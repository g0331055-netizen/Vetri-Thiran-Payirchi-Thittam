async def summarize_text(text: str) -> str:
    words = text.split()
    if len(words) <= 40:
        return text.strip()
    return " ".join(words[:40]).rstrip(".,;:") + "..."