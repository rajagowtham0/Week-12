from typing import List, Optional

from pydantic import BaseModel

import os


# ==========================================================
# REQUEST SCHEMAS
# ==========================================================

class AudioRequestSchema:

    ALLOWED_AUDIO_FORMATS = [
        ".wav",
        ".mp3",
        ".mp4"
    ]

    @staticmethod
    def validate_audio_file(
        filename: str
    ) -> bool:

        extension = os.path.splitext(
            filename
        )[1].lower()

        return (
            extension in
            AudioRequestSchema.ALLOWED_AUDIO_FORMATS
        )


class ImageRequestSchema:

    ALLOWED_IMAGE_FORMATS = [
        ".png",
        ".jpg",
        ".jpeg"
    ]

    @staticmethod
    def validate_image_file(
        filename: str
    ) -> bool:

        extension = os.path.splitext(
            filename
        )[1].lower()

        return (
            extension in
            ImageRequestSchema.ALLOWED_IMAGE_FORMATS
        )


# ==========================================================
# COMMON ERROR RESPONSE
# ==========================================================

class ErrorResponse(BaseModel):

    status: str = "error"
    service: Optional[str] = None
    message: str


# ==========================================================
# SPEECH TO TEXT RESPONSE
# ==========================================================

class SpeechToTextResponse(BaseModel):

    service: str
    input_filename: str
    detected_language: str
    original_transcription: str
    english_translation: str


# ==========================================================
# CLINICAL NOTE FROM VOICE RESPONSE
# ==========================================================

class ClinicalNoteVoiceResponse(BaseModel):

    chief_complaint: str = ""
    duration: str = ""
    symptoms: List[str] = []
    source: str = "voice"


# ==========================================================
# OCR RESPONSE
# ==========================================================

class OCRTextData(BaseModel):

    language: str
    original_text: str
    english_translation: str


class OCRResponse(BaseModel):

    service: str
    input_filename: str
    extracted_text: OCRTextData


# ==========================================================
# CLINICAL NOTE FROM IMAGE RESPONSE
# ==========================================================

class ClinicalImageNote(BaseModel):

    patient_name: str = ""
    diagnosis: str = ""
    medications: List[str] = []
    recommendations: List[str] = []


class ClinicalNoteFromImageResponse(BaseModel):

    service: str
    input_filename: str
    clinical_note: ClinicalImageNote