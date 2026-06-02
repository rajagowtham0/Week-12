# Import FastAPI and file handling utilities
from fastapi import FastAPI, UploadFile, File

# Import temporary file handling library
import tempfile

# Import operating system utilities
import os

# Import Whisper voice-to-text function
from voice_to_text_service.whisper_engine import (
    transcribe_audio
)

# Import OCR text extraction function
from image_to_text_service.ocr_engine import (
    extract_text
)

# Create FastAPI application
app = FastAPI(
    title="Multimodal CCMS_AI"
)


# Home API Endpoint
# Checks whether API service is running successfully
@app.get("/")
def home():

    return {

        "message":
            "Multimodal CCMS_AI Services Running Successfully"
    }


# Voice-to-Text API Endpoint
# Converts uploaded multilingual audio into text
@app.post("/speech-to-text")
async def speech_to_text(
    file: UploadFile = File(...)
):

    # Initialize temporary file variable
    temp_file = None

    try:

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

        # Write uploaded audio into temporary file
        temp_file.write(content)

        # Close temporary file
        temp_file.close()

        # Perform Whisper transcription
        result = transcribe_audio(
            temp_file.name
        )

        # Return structured response
        return {

            "service": "voice_to_text",

            "input_filename":
                file.filename,

            "detected_language":
                result.get(
                    "detected_language"
                ),

            "original_transcription":
                result.get(
                    "original_transcription"
                ),

            "english_translation":
                result.get(
                    "english_translation"
                )
        }

    except Exception as e:

        # Return error response
        return {

            "status": "error",

            "service": "voice_to_text",

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


# OCR / Picture-to-Text API Endpoint
# Extracts text from uploaded clinical images/documents
@app.post("/ocr")
async def ocr_extraction(
    file: UploadFile = File(...)
):

    # Initialize temporary file variable
    temp_file = None

    try:

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

        # Write image into temporary file
        temp_file.write(content)

        # Close temporary file
        temp_file.close()

        # Perform OCR extraction
        extracted_text = extract_text(
            temp_file.name
        )

        # Return structured OCR response
        return {

            "service": "ocr_picture_to_text",

            "input_filename":
                file.filename,

            "extracted_text":
                extracted_text
        }

    except Exception as e:

        # Return OCR error response
        return {

            "status": "error",

            "service": "ocr_picture_to_text",

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