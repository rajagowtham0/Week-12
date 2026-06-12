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
│   ├── clinical_note_generation.py
│   └── ...
│
├── voice_to_text_service/
│   ├── whisper_engine.py
│   ├── clinical_note_generation.py
│   ├── voice_response.py
│   └── ...
│
├── models/
│   ├── models.py
│   └── ...
│
├── utils/
│   ├── logger.py
│   └── ...
│
└── README.md
```

---