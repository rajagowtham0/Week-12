# Import required libraries
import re
import spacy

# Import logger
from utils.logger import logger

# Import response model
from voice_to_text_service.voice_response import (
    ClinicalNoteResponse
)

# Load spaCy English NLP model
logger.info(
    "Loading spaCy NLP model..."
)

nlp = spacy.load(
    "en_core_web_sm"
)

logger.info(
    "spaCy NLP model loaded successfully"
)


# Symptom Preprocessing Function
# Converts symptom sentences into
# cleaner symptom phrases using
# spaCy noun phrase extraction
def preprocess_symptoms(
    symptom_sentences: list
) -> list:

    # Store processed symptoms
    cleaned_symptoms = []

    # Process each symptom sentence
    for sentence in symptom_sentences:

        # Apply spaCy NLP processing
        symptom_doc = nlp(
            sentence
        )

        # Extract noun phrases
        for chunk in symptom_doc.noun_chunks:

            symptom = (
                chunk.text.strip()
            )

            # Ignore very short phrases
            if len(symptom) < 3:

                continue

            # Ignore phrases containing numbers
            # to avoid durations appearing as symptoms
            if any(
                char.isdigit()
                for char in symptom
            ):

                continue

            # Store symptom phrase
            cleaned_symptoms.append(
                symptom.title()
            )

    # Remove duplicate symptoms
    cleaned_symptoms = list(

        dict.fromkeys(
            cleaned_symptoms
        )
    )

    return cleaned_symptoms


# Clinical Note Generation Function
# Input:
#   English translated text from Whisper
#
# Output:
#   ClinicalNoteResponse
def generate_clinical_note(
    translated_text: str
) -> ClinicalNoteResponse:

    try:

        logger.info(
            "Starting clinical note generation"
        )

        # Validate input text
        if not translated_text:

            logger.warning(
                "Empty translated text received"
            )

            return ClinicalNoteResponse(

                chief_complaint="",

                duration="",

                symptoms=[],

                source="voice"
            )

        # Process text using spaCy
        doc = nlp(
            translated_text
        )

        logger.info(
            "spaCy text processing completed"
        )

        # Initialize response fields
        chief_complaint = ""

        duration = ""

        symptoms = []

        # Duration Extraction
        duration_match = re.search(

            r'((?:\d+|one|two|three|four|five|six|seven|eight|nine|ten)\s+'
            r'(?:day|days|week|weeks|month|months|year|years))',

            translated_text,

            re.IGNORECASE
        )

        if duration_match:

            duration = (
                duration_match.group(1)
            )

            logger.info(
                f"Duration extracted: {duration}"
            )

        # Chief Complaint Extraction
        noun_phrases = [

            chunk.text.strip()

            for chunk in doc.noun_chunks

            if len(
                chunk.text.strip()
            ) > 3
        ]

        if noun_phrases:

            chief_complaint = max(

                noun_phrases,

                key=len
            )

            logger.info(
                f"Chief complaint extracted: {chief_complaint}"
            )

        # Symptom Extraction

        # Store symptom-related sentences
        symptom_sentences = []

        for sentence in doc.sents:

            sentence_text = (
                sentence.text.strip()
            )

            # Skip empty sentences
            if not sentence_text:

                continue

            # Skip sentence containing
            # the extracted chief complaint
            if (

                chief_complaint

                and

                chief_complaint.lower()

                in sentence_text.lower()

            ):

                continue

            symptom_sentences.append(
                sentence_text
            )

        # Convert symptom sentences into
        # cleaner symptom entities
        symptoms = preprocess_symptoms(
            symptom_sentences
        )

        logger.info(
            f"Symptoms extracted: {len(symptoms)}"
        )

        # Create structured response
        clinical_note = (

            ClinicalNoteResponse(

                chief_complaint=
                    chief_complaint,

                duration=
                    duration,

                symptoms=
                    symptoms,

                source=
                    "voice"
            )
        )

        logger.info(
            "Clinical note generation completed successfully"
        )

        return clinical_note

    except Exception as e:

        logger.error(
            f"Clinical note generation error: {str(e)}"
        )

        return ClinicalNoteResponse(

            chief_complaint="",

            duration="",

            symptoms=[],

            source="voice"
        )