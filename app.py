import streamlit as st

from utils.ai_helper import (
    generate_explanation,
    check_ambiguity,
    refine_explanation,
    correct_topic_spelling
)
from utils.tts_helper import text_to_speech
from utils.download_helper import generate_pdf

st.set_page_config(
    page_title="Study Buddy",
    page_icon="📚",
    layout="wide"
)

# ---------- SESSION STATE ----------
defaults = {
    "ambiguity_options": None,
    "original_topic": "",
    "current_topic": "",
    "current_explanation": None,
    "current_audio": None,
    "correction_message": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ---------- HELPERS ----------
def reset_all_states():
    st.session_state.ambiguity_options = None
    st.session_state.original_topic = ""
    st.session_state.current_topic = ""
    st.session_state.current_explanation = None
    st.session_state.current_audio = None
    st.session_state.correction_message = None


def generate_and_store_explanation(final_topic, language):
    explanation = generate_explanation(final_topic, language)

    st.session_state.current_topic = final_topic
    st.session_state.current_explanation = explanation
    st.session_state.current_audio = None


# ---------- PREMIUM UI ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0F172A 0%, #111827 100%);
    color: white;
}

.hero-container {
    padding: 2rem;
    border-radius: 20px;
    text-align: center;
    margin-bottom: 2rem;
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.08);
}

.hero-title {
    font-size: 3.2rem;
    font-weight: 800;
    background: linear-gradient(90deg, #60A5FA, #A78BFA);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    font-size: 1.15rem;
    color: #CBD5E1;
    margin-top: 0.5rem;
}

.result-card {
    padding: 1.5rem;
    border-radius: 18px;
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.08);
    margin-top: 1.5rem;
}

.stButton > button {
    width: 100%;
    border-radius: 12px;
    height: 3em;
    font-weight: 600;
    border: none;
    background: linear-gradient(90deg, #2563EB, #7C3AED);
    color: white;
}

.stButton > button:hover {
    box-shadow: 0 8px 20px rgba(99,102,241,0.35);
    transform: translateY(-1px);
}

.stTextInput input,
.stSelectbox div[data-baseweb="select"] {
    border-radius: 12px !important;
}
</style>
""", unsafe_allow_html=True)


# ---------- HERO ----------
st.markdown("""
<div class="hero-container">
    <div class="hero-title">📚 Study Buddy</div>
    <div class="hero-subtitle">
        Your AI-Powered Intelligent Learning Companion
    </div>
</div>
""", unsafe_allow_html=True)


# ---------- INPUTS ----------
col1, col2 = st.columns([3, 1])

with col1:
    topic = st.text_input(
        "Enter a Topic to Learn",
        placeholder="e.g. Machine Learning, Orange, Java"
    )

with col2:
    language = st.selectbox(
        "Choose Language",
        ["English", "Hindi", "Bengali"]
    )


# ---------- SEARCH ----------
if st.button("✨ Explain Topic"):
    reset_all_states()

    if topic:
        corrected_topic = correct_topic_spelling(topic)

        if corrected_topic.lower() != topic.lower():
            st.session_state.correction_message = (
                f'Did you mean: "{corrected_topic}"? '
                f'Proceeding with corrected topic.'
            )

        final_input_topic = corrected_topic

        ambiguity_result = check_ambiguity(final_input_topic)

        if ambiguity_result.startswith("AMBIGUOUS:"):
            meanings_text = ambiguity_result.replace("AMBIGUOUS:", "").strip()

            st.session_state.ambiguity_options = [
                m.strip() for m in meanings_text.split("|")
            ]

            st.session_state.original_topic = final_input_topic
            st.rerun()

        else:
            with st.spinner("Generating Explanation..."):
                generate_and_store_explanation(final_input_topic, language)

            st.rerun()

    else:
        st.warning("Please enter a topic first.")


# ---------- SPELL CORRECTION MESSAGE ----------
if st.session_state.correction_message:
    st.info(st.session_state.correction_message)


# ---------- AMBIGUITY UI ----------
if st.session_state.ambiguity_options:
    st.warning(
        f'The term "{st.session_state.original_topic}" can have multiple meanings. '
        'Please select what you want to learn about:'
    )

    selected_meaning = st.selectbox(
        "Choose Meaning",
        st.session_state.ambiguity_options
    )

    if st.button("Continue with Selected Meaning"):
        final_topic = f"{st.session_state.original_topic} ({selected_meaning})"

        st.session_state.ambiguity_options = None

        with st.spinner("Generating Explanation..."):
            generate_and_store_explanation(final_topic, language)

        st.rerun()


# ---------- DISPLAY RESULT ----------
if st.session_state.current_explanation:

    st.markdown('<div class="result-card">', unsafe_allow_html=True)

    st.markdown("## 📖 Explanation")
    st.write(st.session_state.current_explanation)

    col_pdf, _ = st.columns([1, 1])

    with col_pdf:
        pdf_file = generate_pdf(st.session_state.current_explanation)

        with open(pdf_file, "rb") as file:
            st.download_button(
                "⬇ Download PDF",
                file,
                "study_buddy_explanation.pdf",
                mime="application/pdf"
            )

    st.markdown("### ✨ Refine Explanation")
    col1, col2, col3 = st.columns(3)

    if col1.button("📏 Make it Shorter"):
        with st.spinner("Refining Explanation..."):
            st.session_state.current_explanation = refine_explanation(
                st.session_state.current_topic,
                st.session_state.current_explanation,
                "Make it shorter",
                language
            )
            st.session_state.current_audio = None
        st.rerun()

    if col2.button("📚 Explain More"):
        with st.spinner("Refining Explanation..."):
            st.session_state.current_explanation = refine_explanation(
                st.session_state.current_topic,
                st.session_state.current_explanation,
                "Explain in more detail",
                language
            )
            st.session_state.current_audio = None
        st.rerun()

    if col3.button("🧠 Simplify Further"):
        with st.spinner("Refining Explanation..."):
            st.session_state.current_explanation = refine_explanation(
                st.session_state.current_topic,
                st.session_state.current_explanation,
                "Simplify further",
                language
            )
            st.session_state.current_audio = None
        st.rerun()

    st.markdown("### 🔊 Audio Explanation")

    if st.session_state.current_audio is None:
        if st.button("Generate Audio"):
            with st.spinner("Generating Audio..."):
                st.session_state.current_audio = text_to_speech(
                    st.session_state.current_explanation
                )
            st.rerun()

    if st.session_state.current_audio:
        st.audio(st.session_state.current_audio)

        with open(st.session_state.current_audio, "rb") as file:
            st.download_button(
                "⬇ Download MP3",
                file,
                "study_buddy_explanation.mp3",
                mime="audio/mp3"
            )

    st.markdown('</div>', unsafe_allow_html=True)