from gtts import gTTS
import tempfile


def text_to_speech(text, lang="en"):
    tts = gTTS(text=text, lang=lang)

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_file.name)

    return temp_file.name