# Import required libraries
from pydantic import BaseModel
from typing import List


# Voice-to-Text Response Model
# Used by:
# POST /speech-to-text
#
# Stores:
# 1. Detected language
# 2. Original transcription
# 3. English translation
class VoiceTranscriptionResponse(
    BaseModel
):

    detected_language: str

    original_transcription: str

    english_translation: str


# Clinical Note Response Model
# Used by:
# POST /clinical-note-from-voice
#
# Stores extracted clinical information
# from the translated speech text.
class ClinicalNoteResponse(
    BaseModel
):

    chief_complaint: str

    duration: str

    symptoms: List[str]

    source: str