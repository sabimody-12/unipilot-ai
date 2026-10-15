
import os
import streamlit as st
from ai import analyze_document

# --------------------------------------------------
# 1. PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="UniPilot AI | Student Companion",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------
# 2. PROFESSIONAL BLUE THEME
# --------------------------------------------------
st.markdown(
    """
    <style>
    @import url(
      'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
    );

    :root {
        --primary: #2563eb;
        --primary-dark: #1d4ed8;
        --background: #f5f8ff;
        --text: #172554;
        --muted: #64748b;
        --border: #dbeafe;
        --surface: #ffffff;
    }

    .stApp {
        background: var(--background);
        color: var(--text);
        font-family: 'Inter', sans-serif;
    }

    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid var(--border);
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: var(--text);
    }

    .brand {
        font-size: 1.55rem;
        font-weight: 800;
        color: var(--primary);
        letter-spacing: -0.8px;
        margin-bottom: 0;
    }

    .brand-subtitle {
        color: var(--muted);
        font-size: 0.82rem;
        margin-top: 2px;
        margin-bottom: 18px;
    }

    .hero {
        background: linear-gradient(
            125deg, #1d4ed8 0%, #2563eb 55%, #60a5fa 100%
        );
        color: white;
        border-radius: 22px;
        padding: 30px 26px;
        margin: 6px 0 24px 0;
        box-shadow: 0 12px 30px rgba(37, 99, 235, 0.15);
    }

    .hero h1 {
        color: white !important;
        font-size: clamp(1.8rem, 5vw, 2.7rem);
        font-weight: 800;
        line-height: 1.15;
        margin-bottom: 10px;
    }

    .hero p {
        color: #eff6ff;
        font-size: 1rem;
        margin-bottom: 0;
    }

    .section-title {
        font-size: 1.25rem;
        font-weight: 750;
        color: var(--text);
        margin: 20px 0 12px 0;
    }

    .feature-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 19px;
        min-height: 130px;
        margin-bottom: 12px;
        box-shadow: 0 4px 14px rgba(30, 64, 175, 0.035);
    }

    .feature-card h3 {
        font-size: 1.05rem;
        color: var(--text);
        margin: 8px 0;
    }

    .feature-card p {
        font-size: 0.9rem;
        color: var(--muted);
        margin-bottom: 0;
    }

    .eyebrow {
        color: #dbeafe;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 1.3px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    .muted {
        color: var(--muted);
        font-size: 0.9rem;
    }

    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
        min-height: 42px;
        border-color: var(--border);
    }

    .stButton > button[kind="primary"] {
        background: var(--primary);
        border-color: var(--primary);
        color: white;
    }

    .stButton > button[kind="primary"]:hover {
        background: var(--primary-dark);
        border-color: var(--primary-dark);
    }

    [data-testid="stChatMessage"] {
        background: white;
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 12px;
        margin-bottom: 10px;
    }

    [data-testid="stChatInput"] {
        border-color: #bfdbfe;
    }

    .footer {
        border-top: 1px solid var(--border);
        margin-top: 30px;
        padding-top: 15px;
        color: var(--muted);
        font-size: 0.8rem;
        text-align: center;
    }

    @media (max-width: 640px) {
        .hero {
            padding: 23px 18px;
            border-radius: 16px;
        }
        .feature-card {
            padding: 15px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# 3. SECURE API KEY LOADING
# --------------------------------------------------
api_key = os.getenv("GEMINI_API_KEY", "")

try:
    api_key = st.secrets.get("GEMINI_API_KEY", api_key)
except Exception:
    # Environment variable can still be used if secrets
    # are not configured.
    pass

# --------------------------------------------------
# 4. SESSION STATE
# --------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "Home"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Welcome to **UniPilot AI!** 🎓\n\n"
                "I'm your study companion. Ask me about "
                "Python, computer science, assignments, "
                "exam preparation, or career planning."
            ),
        }
    ]

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None

# --------------------------------------------------
# 5. HELPER FUNCTIONS
# --------------------------------------------------
def open_chat_with(question):
    """Queue a shortcut question and open the chat page."""
    st.session_state.pending_prompt = question
    st.session_state.page = "AI Chat"
    st.rerun()


def get_demo_answer(question):
    """Fallback answers when the AI API is not configured."""
    q = question.lower()

    if any(x in q for x in ["python", "programming", "coding"]):
        return (
            "Let's learn programming step by step! 🐍\n\n"
            "1. Variables and data types\n"
            "2. Conditions and loops\n"
            "3. Functions\n"
            "4. Lists and dictionaries\n"
            "5. A small practical project\n\n"
            "Tell me your current skill level to get started."
        )

    if any(x in q for x in ["assignment", "project", "report"]):
        return (
            "Let's plan your assignment. 📝\n\n"
            "Share its topic, instructions, and deadline. "
            "We'll break it into manageable steps."
        )

    if any(x in q for x in ["career", "job", "future"]):
        return (
            "Possible IT career paths include software "
            "development, cybersecurity, cloud engineering, "
            "data science, and AI development.\n\n"
            "Tell me which subjects interest you most."
        )

    if any(x in q for x in ["study", "exam", "semester"]):
        return (
            "Let's create a study plan! 📚\n\n"
            "Share your subjects, exam dates, and daily "
            "study time so we can organise your revision."
        )

    return (
        "The AI service is not configured yet. Add your "
        "Gemini API key under Streamlit Secrets to enable "
        "AI-generated responses."
    )


def get_ai_answer(question):
    """Request a response from Gemini using OpenAI compatibility."""
    if not api_key:
        return get_demo_answer(question)

    try:
        from openai import OpenAI

        client = OpenAI(
            api_key=api_key,
            base_url=(
                "https://generativelanguage.googleapis.com/"
                "v1beta/openai/"
            ),
            timeout=45.0,
            max_retries=1,
        )

        system_message = {
            "role": "system",
            "content": (
                "You are UniPilot AI, a friendly and reliable "
                "university study assistant. Explain concepts "
                "clearly, use examples, and encourage students "
                "to learn rather than merely copy answers. "
                "For programming, explain code step by step. "
                "Never invent official university rules, "
                "admission policies, or deadlines. Recommend "
                "checking official sources for such information. "
                "Use clear headings and readable formatting."
            ),
        }

        # Send recent conversation context to the model.
        recent_messages = st.session_state.messages[-13:-1]

        conversation = [
            system_message,
            *[
                {"role": item["role"], "content": item["content"]}
                for item in recent_messages
                if item["role"] in ("user", "assistant")
            ],
            {"role": "user", "content": question},
        ]

        response = client.chat.completions.create(
            model="gemini-3.5-flash-lite",
            messages=conversation,
            max_tokens=900,
        )

        answer = response.choices[0].message.content

        if not answer or not answer.strip():
            return (
                "I received an empty response. Please try "
                "asking your question again."
            )

        return answer.strip()

    except Exception as error:
        # Keep technical details out of the visible chat.
        print(f"Gemini API error: {error}")
        return (
            "I'm having trouble connecting to the AI service "
            "right now. Please try again in a moment. If the "
            "problem continues, check the app logs and API "
            "configuration."
        )


# --------------------------------------------------
# 6. SIDEBAR NAVIGATION
# --------------------------------------------------
with st.sidebar:
    st.markdown(
        '<div class="brand">🎓 UniPilot AI</div>'
        '<div class="brand-subtitle">'
        'Your personal university companion'
        '</div>',
        unsafe_allow_html=True,
    )

    st.divider()
    st.markdown("##### WORKSPACE")

    pages = [
        "Home",
        "AI Chat",
        "Document Analyzer",
        "Study Tools",
        "About",
    ]

    selected_page = st.radio(
        "Navigate",
        pages,
        index=pages.index(st.session_state.page),
        label_visibility="collapsed",
    )

    st.session_state.page = selected_page

    st.divider()

    if api_key:
        st.success("AI connection configured")
    else:
        st.warning("Demo mode: API key not found")

    st.caption("Version 1.0 • Student Edition")


# --------------------------------------------------
# 7. HOME DASHBOARD
# --------------------------------------------------
if st.session_state.page == "Home":
    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">YOUR LEARNING SPACE</div>
            <h1>Learn smarter.<br>Achieve more.</h1>
            <p>
                Your AI-powered companion for studying,
                programming, assignments, and career growth.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-title">What would you like to do?</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div class="feature-card">
                <div>💻</div>
                <h3>Learn Programming</h3>
                <p>Understand coding concepts with examples.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button(
            "Start learning →",
            key="home_programming",
            use_container_width=True,
            type="primary",
        ):
            open_chat_with(
                "Teach me programming from the beginning, "
                "starting with Python."
            )

        st.markdown(
            """
            <div class="feature-card">
                <div>📝</div>
                <h3>Assignment Help</h3>
                <p>Understand topics and plan your assignments.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button(
            "Plan an assignment →",
            key="home_assignment",
            use_container_width=True,
        ):
            open_chat_with(
                "Help me understand and plan an assignment."
            )

    with col2:
        st.markdown(
            """
            <div class="feature-card">
                <div>📚</div>
                <h3>Study Help</h3>
                <p>Build a study plan and prepare for exams.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button(
            "Create a study plan →",
            key="home_study",
            use_container_width=True,
            type="primary",
        ):
            open_chat_with(
                "Help me create a practical study plan."
            )

        st.markdown(
            """
            <div class="feature-card">
                <div>🎯</div>
                <h3>Career Guidance</h3>
                <p>Explore IT careers and skills to develop.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button(
            "Explore careers →",
            key="home_career",
            use_container_width=True,
        ):
            open_chat_with(
                "Suggest suitable IT career paths and skills "
                "I can start learning."
            )

    st.markdown(
        '<div class="section-title">Your workspace</div>',
        unsafe_allow_html=True,
    )

    left, right = st.columns(2)

    with left:
        st.info(
            "**Document Analyzer**\n\n"
            "Upload a text file to inspect its content and statistics."
        )
        if st.button("Open Document Analyzer", use_container_width=True):
            st.session_state.page = "Document Analyzer"
            st.rerun()

    with right:
        st.info(
            "**AI Chat**\n\n"
            "Ask questions and continue your learning conversation."
        )
        if st.button("Open AI Chat", use_container_width=True):
            st.session_state.page = "AI Chat"
            st.rerun()


# --------------------------------------------------
# 8. AI CHAT
# --------------------------------------------------
elif st.session_state.page == "AI Chat":
    st.title("💬 AI Study Assistant")
    st.caption(
        "Ask questions, practise coding, or get help with your studies."
    )

    top_left, top_right = st.columns([3, 1])

    with top_left:
        st.markdown(
            '<p class="muted">'
            'Tip: Ask one clear question at a time for the best results.'
            '</p>',
            unsafe_allow_html=True,
        )

    with top_right:
        if st.button("🗑️ Clear chat", use_container_width=True):
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": (
                        "Chat cleared! What would you like "
                        "to learn today? 🎓"
                    ),
                }
            ]
            st.session_state.pending_prompt = None
            st.rerun()

    st.markdown("**Quick prompts**")

    q1, q2 = st.columns(2)

    with q1:
        if st.button("🐍 Teach me Python", use_container_width=True):
            open_chat_with("Teach me Python from zero, one lesson at a time.")

    with q2:
        if st.button("📚 Exam preparation", use_container_width=True):
            open_chat_with("Help me prepare for my upcoming exams.")

    q3, q4 = st.columns(2)

    with q3:
        if st.button("💻 Explain a coding problem", use_container_width=True):
            open_chat_with(
                "Teach me how to solve a programming problem "
                "step by step."
            )

    with q4:
        if st.button("🎯 Explore IT careers", use_container_width=True):
            open_chat_with(
                "Explain IT career options for a beginner."
            )

    st.divider()

    # Display previous messages.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    typed_prompt = st.chat_input(
        "Ask UniPilot AI anything..."
    )

    # Process either a shortcut prompt or a typed prompt.
    prompt = typed_prompt

    if st.session_state.pending_prompt:
        prompt = st.session_state.pending_prompt
        st.session_state.pending_prompt = None

    if prompt:
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("UniPilot is thinking..."):
                answer = get_ai_answer(prompt)

            st.markdown(answer)

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )


# --------------------------------------------------
# 9. DOCUMENT ANALYZER
# --------------------------------------------------
elif st.session_state.page == "Document Analyzer":
    st.title("📄 Document Analyzer")
    st.caption(
        "Upload a UTF-8 text file to inspect its contents."
    )

    st.info(
        "Current version supports .txt files. PDF and Word "
        "support can be added in a later update."
    )

    uploaded_file = st.file_uploader(
        "Choose a text document",
        type=["txt"],
        key="document_upload",
    )

    if uploaded_file is not None:
        try:
            document_text = uploaded_file.getvalue().decode("utf-8")

            if not document_text.strip():
                st.warning("This document appears to be empty.")
            else:
                with st.spinner("Analyzing your document..."):
                    result = analyze_document(document_text)

                if isinstance(result, dict):
                    st.success(
                        result.get(
                            "message",
                            "Document analyzed successfully.",
                        )
                    )

                    a, b, c = st.columns(3)

                    a.metric(
                        "Characters",
                        result.get("characters", 0),
                    )
                    b.metric(
                        "Words",
                        result.get("words", 0),
                    )
                    c.metric(
                        "Sentences",
                        result.get("sentences", 0),
                    )

                    st.subheader("Document Preview")
                    st.text(result.get("preview", ""))

                    if result.get("ai_analysis"):
                        st.subheader("Analysis")
                        st.info(result["ai_analysis"])
                else:
                    st.warning(str(result))

        except UnicodeDecodeError:
            st.error(
                "Please upload a UTF-8 encoded text file."
            )
        except Exception as error:
            print(f"Document analyzer error: {error}")
            st.error(
                "The document could not be analyzed. "
                "Please check the file and try again."
            )


# --------------------------------------------------
# 10. STUDY TOOLS
# --------------------------------------------------
elif st.session_state.page == "Study Tools":
    st.title("📚 Study Tools")
    st.caption(
        "Choose a tool to begin. More learning tools can be added later."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div class="feature-card">
                <h3>🧠 Learn a concept</h3>
                <p>Get a simple explanation with examples.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Explain a concept", use_container_width=True):
            open_chat_with(
                "Explain a computer science concept in si