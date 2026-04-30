import streamlit as st
from groq import Groq

client = Groq(api_key=st.secrets["GROQ_API_KEY"])


@st.cache_data(show_spinner=False)
def check_ambiguity(topic):
    predefined_ambiguities = {
        "orange": ["Fruit", "Color"],
        "java": ["Programming Language", "Coffee", "Island"],
        "python": ["Programming Language", "Snake"],
        "apple": ["Fruit", "Technology Company"],
        "amazon": ["Company", "Rainforest", "River"]
    }

    topic_lower = topic.strip().lower()

    if topic_lower in predefined_ambiguities:
        return "AMBIGUOUS: " + " | ".join(predefined_ambiguities[topic_lower])

    prompt = f"""
Classify whether the following term is ambiguous:

TERM: "{topic}"

Definition of ambiguous:
A term is ambiguous ONLY if it has multiple clearly different common meanings in everyday/general use.

OUTPUT:
- If ambiguous: AMBIGUOUS: Meaning1 | Meaning2
- Else: NOT_AMBIGUOUS

NO explanation.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()


@st.cache_data(show_spinner=False)
def generate_explanation(topic, language="English"):
    prompt = f"""
Explain '{topic}' in simple and easy-to-understand {language}.

Rules:
- Keep explanation beginner friendly
- Use clear language
- Structure response professionally
- Focus specifically on the exact topic provided
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

@st.cache_data(show_spinner=False)
def refine_explanation(topic, current_explanation, refinement_type, language="English"):
    prompt = f"""
The topic is: {topic}

Current Explanation:
{current_explanation}

Modify the explanation according to this instruction:
{refinement_type}

Rules:
- Keep response in {language}
- Maintain factual correctness
- Do not mention that you are modifying/refining
- Return only the revised explanation
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

@st.cache_data(show_spinner=False)
def correct_topic_spelling(topic):
    prompt = f"""
Correct the spelling of the following educational/technical topic if needed.

INPUT:
{topic}

RULES:
1. If spelling is incorrect:
   Return ONLY the corrected version.
2. If already correct:
   Return EXACTLY the same input.
3. Do NOT explain anything.
4. Do NOT add quotes or commentary.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()