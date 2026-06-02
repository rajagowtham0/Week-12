# Import operating system utilities
import os

# Load environment variables
from dotenv import load_dotenv

# Import Whisper model
import whisper

# Import logger
from utils.logger import logger

# Import Pydantic response model
from voice_to_text_service.voice_response import (
    VoiceTranscriptionResponse
)

# Load environment variables from .env file

load_dotenv()

ffmpeg_path = r"C:\ffmpeg\bin"

os.environ["PATH"] += (
    os.pathsep +
    ffmpeg_path
)

logger.info(
    f"FFMPEG Path: {ffmpeg_path}"
)

# Load Whisper model
logger.info(
    "Loading Whisper model..."
)

# Medium model provides good multilingual accuracy
model = whisper.load_model(
    "medium"
)

logger.info(
    "Whisper model loaded successfully"
)

# Supported language mapping
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
# Performs:
# 1. Language Detection
# 2. Original Language Transcription
# 3. English Translation
def transcribe_audio(
    audio_path
) -> VoiceTranscriptionResponse:

    try:

        logger.info(
            f"Processing audio file: {audio_path}"
        )

        # Generate transcription in original language
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

        logger.info(
            "Original language transcription completed"
        )

        # Generate English translation
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

        logger.info(
            "English translation completed"
        )

        # Extract detected language code
        language_code = (
            transcription_result["language"]
        )

        # Convert language code to readable language name
        language_name = LANGUAGE_MAP.get(

            language_code,

            "Unknown"
        )

        logger.info(
            f"Detected language: {language_name}"
        )

        # Create structured response model
        response = VoiceTranscriptionResponse(

            detected_language=
                language_name,

            original_transcription=
                transcription_result[
                    "text"
                ].strip(),

            english_translation=
                translation_result[
                    "text"
                ].strip()
        )

        logger.info(
            "Voice-to-text processing completed successfully"
        )

        return response

    except Exception as e:

        logger.error(
            f"Voice processing error: {str(e)}"
        )

        return VoiceTranscriptionResponse(

            detected_language=
                "Unknown",

            original_transcription=
                "",

            english_translation=
                ""
        )