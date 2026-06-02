import os

# Local FFmpeg Path
os.environ["PATH"] += os.pathsep + r"C:\ffmpeg\bin"

# Import Whisper
import whisper

# Load Whisper Model
print("Loading Whisper model...")

# Medium model gives very good multilingual accuracy
model = whisper.load_model("medium")

print("Whisper model loaded successfully")

# Language Mapping
LANGUAGE_MAP = {
    "en": "English",
    "te": "Telugu",
    "hi": "Hindi",
    "ta": "Tamil",
    "ml": "Malayalam",
    "kn": "Kannada",
    "bn": "Bengali"
}


# Voice-to-Text Function
def transcribe_audio(audio_path):

    try:

        # Original Language Transcription
        transcription_result = model.transcribe(
            audio_path,
            task="transcribe",
            fp16=False,
            temperature=0,
            beam_size=10,
            best_of=10,
            patience=2,
            condition_on_previous_text=True
        )

        # English Translation
        translation_result = model.transcribe(
            audio_path,
            task="translate",
            fp16=False,
            temperature=0,
            beam_size=10,
            best_of=10,
            patience=2,
            condition_on_previous_text=True
        )

        # Extract Language Information
        language_code = transcription_result["language"]

        language_name = LANGUAGE_MAP.get(
            language_code,
            "Unknown"
        )

        # Structured Response
        return {

            "detected_language":
                language_name,

            "original_transcription":
                transcription_result["text"].strip(),

            "english_translation":
                translation_result["text"].strip()
        }

    except Exception as e:

        return {

            "detected_language": "Unknown",

            "original_transcription": "",

            "english_translation": "",

            "error": str(e)
        }