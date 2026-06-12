# Import FastAPI and file upload utilities
from fastapi import FastAPI, UploadFile, File

# Import temporary file handling utilities
import tempfile

# Import operating system utilities
import os

# Import application logger
from utils.logger import logger

# Import Whisper voice-to-text service
from voice_to_text_service.whisper_engine import (
    transcribe_audio
)

# Import Clinical Note Generation service
from voice_to_text_service.clinical_note_generation import (
    generate_clinical_note
)

# Import OCR service
from image_to_text_service.ocr_engine import (
    extract_text
)

# Import OCR Translation service
from image_to_text_service.ocr_text_translation import (
    translate_to_english
)

# Import Clinical Information Extraction service
from image_to_text_service.image_clinical_description import (
    generate_clinical_description
)

# Import Models
from models.models import (
    AudioRequestSchema,
    ImageRequestSchema,
    ErrorResponse,
    SpeechToTextResponse,
    ClinicalNoteVoiceResponse,
    OCRResponse,
    ClinicalNoteFromImageResponse
)

# Create FastAPI application
app = FastAPI(
    title="Multimodal CCMS_AI"
)


@app.get("/")
def home():

    logger.info("Home endpoint accessed")

    return {
        "message": "Multimodal CCMS_AI Services Running Successfully"
    }


@app.post(
    "/speech-to-text",
    response_model=SpeechToTextResponse
)
async def speech_to_text(
    file: UploadFile = File(...)
):

    temp_file = None

    try:

        logger.info(
            f"Voice-to-Text request received: {file.filename}"
        )

        if not AudioRequestSchema.validate_audio_file(
            file.filename
        ):

            logger.warning(
                f"Unsupported audio format: {file.filename}"
            )

            return {
                "status": "error",
                "message": "Unsupported audio format"
            }

        file_extension = os.path.splitext(
            file.filename
        )[1].lower()

        temp_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=file_extension,
            mode="wb"
        )

        content = await file.read()

        temp_file.write(content)
        temp_file.close()

        logger.info(
            "Audio file saved successfully"
        )

        result = transcribe_audio(
            temp_file.name
        )

        logger.info(
            "Voice-to-Text processing completed successfully"
        )

        return {
            "service": "voice_to_text",
            "input_filename": file.filename,
            "detected_language": result.detected_language,
            "original_transcription": result.original_transcription,
            "english_translation": result.english_translation
        }

    except Exception as e:

        logger.error(
            f"Voice-to-Text error: {str(e)}"
        )

        return {
            "status": "error",
            "service": "voice_to_text",
            "message": str(e)
        }

    finally:

        if (
            temp_file is not None
            and os.path.exists(temp_file.name)
        ):

            os.unlink(temp_file.name)

            logger.info(
                "Temporary audio file deleted"
            )


@app.post(
    "/clinical-note-from-voice",
    response_model=ClinicalNoteVoiceResponse
)
async def clinical_note_from_voice(
    file: UploadFile = File(...)
):

    temp_file = None

    try:

        logger.info(
            f"Clinical Note request received: {file.filename}"
        )

        if not AudioRequestSchema.validate_audio_file(
            file.filename
        ):

            logger.warning(
                f"Unsupported audio format: {file.filename}"
            )

            return ClinicalNoteVoiceResponse(
                chief_complaint="",
                duration="",
                symptoms=[],
                source="voice"
            )

        file_extension = os.path.splitext(
            file.filename
        )[1].lower()

        temp_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=file_extension,
            mode="wb"
        )

        content = await file.read()

        temp_file.write(content)
        temp_file.close()

        logger.info(
            "Audio file saved successfully"
        )

        transcription_response = transcribe_audio(
            temp_file.name
        )

        clinical_note = generate_clinical_note(
            transcription_response.english_translation
        )

        logger.info(
            "Clinical note generated successfully"
        )

        return clinical_note

    except Exception as e:

        logger.error(
            f"Clinical Note generation error: {str(e)}"
        )

        return ClinicalNoteVoiceResponse(
            chief_complaint="",
            duration="",
            symptoms=[],
            source="voice"
        )

    finally:

        if (
            temp_file is not None
            and os.path.exists(temp_file.name)
        ):

            os.unlink(temp_file.name)

            logger.info(
                "Temporary audio file deleted"
            )


@app.post(
    "/ocr",
    response_model=OCRResponse
)
async def ocr_extraction(
    file: UploadFile = File(...)
):

    temp_file = None

    try:

        logger.info(
            f"OCR request received: {file.filename}"
        )

        if not ImageRequestSchema.validate_image_file(
            file.filename
        ):

            logger.warning(
                f"Unsupported image format: {file.filename}"
            )

            return {
                "status": "error",
                "message": "Unsupported image format"
            }

        file_extension = os.path.splitext(
            file.filename
        )[1].lower()

        temp_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=file_extension,
            mode="wb"
        )

        content = await file.read()

        temp_file.write(content)
        temp_file.close()

        extracted_text = extract_text(
            temp_file.name
        )

        english_translation = translate_to_english(
            extracted_text["text"]
        )

        return {
            "service": "ocr_picture_to_text",
            "input_filename": file.filename,
            "extracted_text": {
                "language": extracted_text["language"],
                "original_text": extracted_text["text"],
                "english_translation": english_translation
            }
        }

    except Exception as e:

        logger.error(
            f"OCR extraction error: {str(e)}"
        )

        return {
            "status": "error",
            "service": "ocr_picture_to_text",
            "message": str(e)
        }

    finally:

        if (
            temp_file is not None
            and os.path.exists(temp_file.name)
        ):

            os.unlink(temp_file.name)


@app.post(
    "/clinical-note-from-image",
    response_model=ClinicalNoteFromImageResponse
)
async def clinical_note_from_image(
    file: UploadFile = File(...)
):

    temp_file = None

    try:

        logger.info(
            f"Clinical Note From Image request received: {file.filename}"
        )

        if not ImageRequestSchema.validate_image_file(
            file.filename
        ):

            logger.warning(
                f"Unsupported image format: {file.filename}"
            )

            return {
                "status": "error",
                "message": "Unsupported image format"
            }

        file_extension = os.path.splitext(
            file.filename
        )[1].lower()

        temp_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=file_extension,
            mode="wb"
        )

        content = await file.read()

        temp_file.write(content)
        temp_file.close()

        extracted_text = extract_text(
            temp_file.name
        )

        english_translation = translate_to_english(
            extracted_text.get("text", "")
        )

        clinical_note = generate_clinical_description(
            english_translation
        )

        return {
            "service": "clinical_note_from_image",
            "input_filename": file.filename,
            "clinical_note": clinical_note
        }

    except Exception as e:

        logger.error(
            f"Clinical note from image error: {str(e)}"
        )

        return {
            "status": "error",
            "service": "clinical_note_from_image",
            "message": str(e)
        }

    finally:

        if (
            temp_file is not None
            and os.path.exists(temp_file.name)
        ):

            os.unlink(temp_file.name)

            logger.info(
                "Temporary image file deleted"
            )