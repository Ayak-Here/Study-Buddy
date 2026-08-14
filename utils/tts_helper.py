import tempfile
import streamlit as st
from sarvamai import SarvamAI


client = SarvamAI(
    api_subscription_key=st.secrets["SARVAM_API_KEY"]
)


LANGUAGE_CODES = {
    "English": "en-IN",
    "Hindi": "hi-IN",
    "Bengali": "bn-IN"
}


def text_to_speech(text, language="English"):
    """
    Generate MP3 audio using Sarvam AI Bulbul v3.
    Returns the generated MP3 file path.
    """

    target_language = LANGUAGE_CODES.get(language, "en-IN")

    # Sarvam supports up to 3500 characters
    text = text[:3500]

    # Temporary MP3 file
    audio_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".mp3"
    )

    audio_file.close()

    # Generate streaming MP3 audio
    with open(audio_file.name, "wb") as f:

        for chunk in client.text_to_speech.convert_stream(
            text=text,
            language_code=target_language,
            speaker="shubh",
            model="bulbul:v3",
            output_audio_codec="mp3",
            output_audio_bitrate="128k",
            pace=1.0
        ):
            f.write(chunk)

    return audio_file.name
