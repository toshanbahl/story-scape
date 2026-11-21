"""Turn a voice recording into text with SpeechRecognition. Stage 7."""
import io

import speech_recognition as sr


def transcribe(wav_bytes):
    """Return (text, error). Exactly one of them is None."""
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(io.BytesIO(wav_bytes)) as source:
            audio = recognizer.record(source)
        return recognizer.recognize_google(audio), None
    except sr.UnknownValueError:
        return None, "Sorry, I couldn't understand the recording. Try speaking more clearly or type instead."
    except (sr.RequestError, ValueError) as e:
        return None, f"Voice service unavailable ({e}). Please type your story instead."
