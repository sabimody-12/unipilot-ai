
def analyze_document(text):
    """
    UniPilot AI document analysis module.
    Current stage: text validation and basic analysis.
    Future stage: connect to an LLM on AMD Developer Cloud.
    """

    if not text or not text.strip():
        return "No document text available."

    text = text.strip()
    words = text.split()
    sentences = [
        s.strip()
        for s in text.replace("!", ".").replace("?", ".").split(".")
        if s.strip()
    ]

    return {
        "status": "success",
        "message": "Document received successfully.",
        "characters": len(text),
        "words": len(words),
        "sentences": len(sentences),
        "preview": text[:500],
        "ai_analysis": (
            "AI model not connected yet. "
            "Connect an LLM to generate summaries, "
            "explanations, and key points."
        )
    }
