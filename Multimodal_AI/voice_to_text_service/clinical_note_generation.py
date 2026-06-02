# Import required libraries
import re
import spacy

# Import logger
from utils.logger import logger

# Import response model
from text_to_voice_service.voice_response import (
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


# Clinical Note Generation Function
# Input:
#   English translated text from Whisper
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

        for sentence in doc.sents:

            sentence_text = (
                sentence.text.strip()
            )

            if not sentence_text:

                continue

            if (

                chief_complaint

                and

                chief_complaint.lower()

                in sentence_text.lower()

            ):

                continue

            symptoms.append(
                sentence_text
            )

        # Remove duplicate symptom entries
        symptoms = list(

            dict.fromkeys(
                symptoms
            )
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