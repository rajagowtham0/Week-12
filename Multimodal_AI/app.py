
# Import FastAPI and file upload utilities
from fastapi import FastAPI, UploadFile, File

# Import temporary file handling utilities
import tempfile

# Import operating system utilities
import os

# Import application logger
from utils.logger import logger

# Import Whisper voice-to-text service
from text_to_voice_service.whisper_engine import (
    transcribe_audio
)

# Import Clinical Note Generation service
from text_to_voice_service.clinical_note_generation import (
    generate_clinical_note
)

# Import OCR service
from image_to_text_service.ocr_engine import (
    extract_text
)

# Import Pydantic response models
from voice_to_text_service.voice_response import (
    ClinicalNoteResponse
)

# Create FastAPI application
app = FastAPI(
    title="Multimodal CCMS_AI"
)


# Home Endpoint
# Verifies that the API service is running successfully
@app.get("/")
def home():

    logger.info(
        "Home endpoint accessed"
    )

    return {

        "message":
            "Multimodal CCMS_AI Services Running Successfully"
    }


# Voice-to-Text Endpoint
# Converts multilingual speech into text and English translation
@app.post("/speech-to-text")
async def speech_to_text(
    file: UploadFile = File(...)
):

    temp_file = None

    try:

        logger.info(
            f"Voice-to-Text request received: {file.filename}"
        )

        # Supported audio formats
        allowed_audio_formats = [
            ".wav",
            ".mp3",
            ".m4a"
        ]

        # Extract uploaded file extension
        file_extension = os.path.splitext(
            file.filename
        )[1].lower()

        # Validate audio format
        if file_extension not in allowed_audio_formats:

            logger.warning(
                f"Unsupported audio format: {file_extension}"
            )

            return {

                "status": "error",

                "message":
                    "Unsupported audio format"
            }

        # Create temporary audio file
        temp_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=file_extension,
            mode="wb"
        )

        # Read uploaded audio file
        content = await file.read()

        # Save audio into temporary file
        temp_file.write(content)

        temp_file.close()

        logger.info(
            "Audio file saved successfully"
        )

        # Perform speech transcription
        result = transcribe_audio(
            temp_file.name
        )

        logger.info(
            "Voice-to-Text processing completed successfully"
        )

        return {

            "service":
                "voice_to_text",

            "input_filename":
                file.filename,

            "detected_language":
                result.detected_language,

            "original_transcription":
                result.original_transcription,

            "english_translation":
                result.english_translation
        }

    except Exception as e:

        logger.error(
            f"Voice-to-Text error: {str(e)}"
        )

        return {

            "status": "error",

            "service":
                "voice_to_text",

            "message":
                str(e)
        }

    finally:

        # Delete temporary audio file
        if temp_file is not None:

            if os.path.exists(
                temp_file.name
            ):

                os.unlink(
                    temp_file.name
                )

                logger.info(
                    "Temporary audio file deleted"
                )


# Clinical Note Generation Endpoint
# Converts multilingual voice input into structured clinical notes
@app.post(
    "/clinical-note-from-voice",
    response_model=ClinicalNoteResponse
)
async def clinical_note_from_voice(
    file: UploadFile = File(...)
):

    temp_file = None

    try:

        logger.info(
            f"Clinical Note request received: {file.filename}"
        )

        # Supported audio formats
        allowed_audio_formats = [
            ".wav",
            ".mp3",
            ".m4a"
        ]

        # Extract uploaded file extension
        file_extension = os.path.splitext(
            file.filename
        )[1].lower()

        # Validate audio format
        if file_extension not in allowed_audio_formats:

            logger.warning(
                f"Unsupported audio format: {file_extension}"
            )

            return ClinicalNoteResponse(

                chief_complaint="",

                duration="",

                symptoms=[],

                source="voice"
            )

        # Create temporary audio file
        temp_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=file_extension,
            mode="wb"
        )

        # Read uploaded audio file
        content = await file.read()

        # Save audio into temporary file
        temp_file.write(content)

        temp_file.close()

        logger.info(
            "Audio file saved successfully"
        )

        # Generate speech transcription
        transcription_response = (
            transcribe_audio(
                temp_file.name
            )
        )

        # Generate structured clinical note
        clinical_note = (
            generate_clinical_note(

                transcription_response.
                english_translation
            )
        )

        logger.info(
            "Clinical note generated successfully"
        )

        return clinical_note

    except Exception as e:

        logger.error(
            f"Clinical Note generation error: {str(e)}"
        )

        return ClinicalNoteResponse(

            chief_complaint="",

            duration="",

            symptoms=[],

            source="voice"
        )

    finally:

        # Delete temporary audio file
        if temp_file is not None:

            if os.path.exists(
                temp_file.name
            ):

                os.unlink(
                    temp_file.name
                )

                logger.info(
                    "Temporary audio file deleted"
                )


# OCR Endpoint
# Extracts text from uploaded images and clinical documents
@app.post("/ocr")
async def ocr_extraction(
    file: UploadFile = File(...)
):

    temp_file = None

    try:

        logger.info(
            f"OCR request received: {file.filename}"
        )

        # Supported image formats
        allowed_image_formats = [
            ".png",
            ".jpg",
            ".jpeg"
        ]

        # Extract uploaded image extension
        file_extension = os.path.splitext(
            file.filename
        )[1].lower()

        # Validate image format
        if file_extension not in allowed_image_formats:

            logger.warning(
                f"Unsupported image format: {file_extension}"
            )

            return {

                "status": "error",

                "message":
                    "Unsupported image format"
            }

        # Create temporary image file
        temp_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=file_extension,
            mode="wb"
        )

        # Read uploaded image
        content = await file.read()

        # Save image into temporary file
        temp_file.write(content)

        temp_file.close()

        logger.info(
            "Image file saved successfully"
        )

        # Extract text using OCR
        extracted_text = extract_text(
            temp_file.name
        )

        logger.info(
            "OCR extraction completed successfully"
        )

        return {

            "service":
                "ocr_picture_to_text",

            "input_filename":
                file.filename,

            "extracted_text":
                extracted_text
        }

    except Exception as e:

        logger.error(
            f"OCR extraction error: {str(e)}"
        )

        return {

            "status": "error",

            "service":
                "ocr_picture_to_text",

            "message":
                str(e)
        }

    finally:

        # Delete temporary image file
        if temp_file is not None:

            if os.path.exists(
                temp_file.name
            ):

                os.unlink(
                    temp_file.name
                )

                logger.info(
                    "Temporary image file deleted"
                )
