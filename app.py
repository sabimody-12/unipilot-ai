
import os
import streamlit as st
from ai import analyze_document

st.set_page_config(
    page_title="UniPilot AI",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 UniPilot AI")
st.subheader("Your AI-powered university companion")

st.write(
    "Get help with studying, programming, assignments, "
    "university planning, and learning new skills."
)

st.divider()
st.header("📄 Document Analyzer")

uploaded_file = st.file_uploader(
    "Upload a text document",
    type=["txt"],
    key="document_upload"
)

if uploaded_file is not None:
    try:
        document_text = uploaded_file.getvalue().decode("utf-8")
        result = analyze_document(document_text)

        if isinstance(result, dict):
            st.success(result["message"])

            col_a, col_b, col_c = st.columns(3)
            col_a.metric("Characters", result["characters"])
            col_b.metric("Words", result["words"])
            col_c.metric("Sentences", result["sentences"])

            st.subheader("Document Preview")
            st.text(result["preview"])
            st.info(result["ai_analysis"])
        else:
            st.warning(result)

    except UnicodeDecodeError:
        st.error("Please upload a UTF-8 encoded text file.")
    except Exception as e:
        st.error(f"Document analysis error: {e}")

# Get Gemini API key from Streamlit Secrets or environment
api_key = os.getenv("GEMINI_API_KEY", "")

try:
    api_key = st.secrets.get("GEMINI_API_KEY", api_key)
except Exception:
    pass

# Initialise chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Welcome to UniPilot AI! 👋\n\n"
                "I'm here to help with your studies. "
                "Ask me about programming, assignments, "
                "computer science, or university life."
            )
        }
    ]

# Feature shortcuts
st.markdown("### What do you want to do?")
col1, col2 = st.columns(2)

if col1.button("💻 Learn programming", use_container_width=True):
    st.session_state.pending_prompt = (
        "Help me start learning programming."
    )
    st.rerun()

if col2.button("📚 Study help", use_container_width=True):
    st.session_state.pending_prompt = (
        "Help me create a study plan."
    )
    st.rerun()

if col1.button("📝 Assignment help", use_container_width=True):
    st.session_state.pending_prompt = (
        "Help me understand and plan an assignment."
    )
    st.rerun()

if col2.button("🎯 Career guidance", use_container_width=True):
    st.session_state.pending_prompt = (
        "Suggest a career path in information technology."
    )
    st.rerun()

st.divider()
st.markdown("### Chat with UniPilot")

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


def get_demo_answer(question):
    q = question.lower()

    if any(word in q for word in ["python", "programming", "coding"]):
        return (
            "Let's learn programming step by step! 🐍\n\n"
            "1. Understand variables and data types.\n"
            "2. Learn conditions and loops.\n"
            "3. Practise functions.\n"
            "4. Build a small project.\n\n"
            "Tell me your current skill level so we can begin."
        )

    if any(word in q for word in ["assignment", "project", "report"]):
        return (
            "I can help you plan your assignment. 📝\n\n"
            "Share the topic, instructions, and deadline. "
            "We'll break it into manageable steps and work "
            "through the concepts together."
        )

    if any(word in q for word in ["career", "job", "future"]):
        return (
            "For an IT student, possible paths include "
            "software development, data science, cybersecurity, "
            "cloud engineering, and AI development.\n\n"
            "Tell me which subjects you enjoy most, and "
            "we'll explore suitable options."
        )

    if any(word in q for word in ["study", "exam", "semester"]):
        return (
            "Let's make a study plan! 📚\n\n"
            "List your subjects, exam dates, and available "
            "study hours. I'll help you organise your revision."
        )

    return (
        "I'm currently running in starter mode because the "
        "Gemini API key is not configured. Please check your "
        "Streamlit Secrets settings to enable AI-generated answers."
    )


# Handle typed messages and shortcut prompts
prompt = st.chat_input("Ask UniPilot AI anything...")

if not prompt and "pending_prompt" in st.session_state:
    prompt = st.session_state.pop("pending_prompt")

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if api_key:
            try:
                from openai import OpenAI

                client = OpenAI(
                    api_key=api_key,
                    base_url=(
                        "https://generativelanguage.googleapis.com/"
                        "v1beta/openai/"
                    )
                )

                response = client.chat.completions.create(
                    model="gemini-3.5-flash-lite",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are UniPilot AI, a helpful "
                                "university study assistant. Explain "
                                "concepts clearly, encourage learning, "
                                "and never invent official university "
                                "policies. Recommend checking official "
                                "sources for admissions and deadlines."
                            )
                        }
                    ] + [
                        {
                            "role": message["role"],
                            "content": message["content"]
                        }
                        for message in st.session_state.messages
                        if message["role"] in ("user", "assistant")
                    ],
                    max_tokens=700
                )

                answer = response.choices[0].message.content

                if not answer:
                    answer = (
                        "The AI returned an empty response. "
                        "Please try asking again."
                    )

                st.markdown(answer)

            except Exception as e:
                st.error(f"Gemini API error: {e}")
                answer = (
                    "Sorry, I couldn't get an AI response. "
                    "Please check the error above."
                )

        else:
            answer = get_demo_answer(prompt)
            st.markdown(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

st.divider()
st.caption("UniPilot AI • Early prototype • Built for learners")
