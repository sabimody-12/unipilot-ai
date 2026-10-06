def analyze_document(text):
    """
    Temporary AI analysis function.
    We will connect this to an AI model running
    on AMD GPU + ROCm later.
    """

    if not text.strip():
        return "No document text available."

    return f"""
Document received successfully.

Characters extracted: {len(text)}

Next step:
Connect UniPilot AI to an LLM running on AMD
Developer Cloud using ROCm.
"""