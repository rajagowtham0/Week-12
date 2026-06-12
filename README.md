# Multimodal AI Clinical Documentation System

A FastAPI-based Multimodal AI application that converts clinical information from multiple input modalities into structured clinical notes.

The system supports:

- 🎤 Voice-to-Text Processing
- 🖼️ Image-to-Text Extraction (OCR)
- 🌍 Multi-language Translation
- 🏥 Clinical Note Generation
- ⚡ FastAPI REST APIs
- 📄 Structured JSON Responses


# Project Structure

```text
Multimodal_AI/
│
├── app.py
│
├── image_to_text_service/
│   ├── ocr_engine.py
│   ├── ocr_text_translation.py
│   ├── image_clinical_description.py
│
├── voice_to_text_service/
│   ├── whisper_engine.py
│   ├── clinical_note_generation.py
│   ├── voice_response.py
│
├── models/
│   ├── models.py
│
├── utils/
│   ├── logger.py
│   └── config.py
```

# Project Structure Overview

## app.py

Main entry point of the FastAPI application. Defines API endpoints and coordinates requests between image, voice, and clinical processing services. Handles request validation, response generation, and error management.

## image_to_text_service/

Contains all image-processing modules used for extracting and interpreting information from uploaded images. Responsible for OCR, language translation, and generation of structured clinical descriptions. Enables conversion of prescriptions and medical documents into machine-readable clinical data.

### ocr_engine.py

Extracts text from uploaded images using Optical Character Recognition (OCR). Supports printed and handwritten medical content. Produces raw text for downstream processing.

### ocr_text_translation.py

Translates extracted OCR text into English when required. Supports multilingual medical documents and prescriptions. Ensures a consistent language format for further analysis.

### image_clinical_description.py

Converts extracted text into structured clinical information. Identifies diagnoses, medications, and recommendations from image content. Generates a standardized clinical summary.

## voice_to_text_service/

Contains modules for speech transcription and clinical note generation from audio recordings. Processes spoken patient information into structured healthcare documentation. Provides the complete voice-to-clinical-note workflow.

### whisper_engine.py

Performs speech-to-text conversion using the Whisper model. Supports multiple audio formats and languages. Produces accurate transcriptions from uploaded recordings.

### clinical_note_generation.py

Analyzes transcribed speech and extracts clinically relevant information. Identifies symptoms, diagnoses, medications, and recommendations. Generates structured clinical notes from conversational input.

### voice_response.py

Defines response structures for voice-processing APIs. Ensures consistent and validated output formatting. Standardizes API responses across voice-related services.

## models/

Contains shared Pydantic models used throughout the application. Defines request and response schemas for validation and serialization. Improves API consistency and documentation generation.

### models.py

Stores all application-wide data models and response schemas. Provides type validation and structured data handling. Serves as the central location for API contracts.

## utils/

Contains reusable utility modules shared across multiple services. Provides common functionality such as logging and configuration management. Helps maintain a clean and modular codebase.

### logger.py

Implements centralized logging for application monitoring and debugging. Records informational messages, warnings, and errors. Supports troubleshooting and operational visibility.

### config.py

Stores application configurations, constants, and environment-specific settings. Centralizes configurable parameters used across services. Simplifies deployment and maintenance.

# Features

## Voice-to-Text Clinical Documentation

- Upload audio files
- Speech transcription using Whisper
- Clinical entity extraction
- Structured note generation

Supported Audio Formats:

- WAV
- MP3
- M4A
- FLAC

---

## Image-to-Text Clinical Documentation

- Upload medical prescriptions
- Upload handwritten notes
- OCR text extraction
- Translation support
- Clinical note generation

Supported Image Formats:

- JPG
- JPEG
- PNG

---

## Clinical Note Generation

The system automatically extracts:

- Patient Name
- Chief Complaint
- Diagnosis
- Medications
- Recommendations

and converts them into a structured clinical note.

---

# Installation Guide

This project requires Python, FFmpeg, and Tesseract OCR to support multimodal processing, including speech transcription, optical character recognition (OCR), translation, and clinical note generation.

## Prerequisites

Before installing the application, ensure the following software is available on your system:

Python 3.10 or higher
FFmpeg (for audio processing and Whisper transcription)
Tesseract OCR (for image text extraction)


