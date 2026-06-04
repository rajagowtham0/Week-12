# Import required libraries
import re
import spacy

# Import logger
from utils.logger import logger

# Import response model
from voice_to_text_service.voice_response import (
    ClinicalNoteResponse
)

# Load spaCy model
logger.info(
    "Loading spaCy model..."
)

nlp = spacy.load(
    "en_core_web_sm"
)

logger.info(
    "spaCy model loaded successfully"
)


# Preprocess clinical text
# Removes narrative phrases while
# preserving clinical meaning
def preprocess_text(
    text: str
) -> str:

    # Convert text to lowercase
    text = text.lower()

    # Common narrative phrases
    filler_phrases = [

        "the patient",

        "patient",

        "has complained of",

        "complains of",

        "complained of",

        "has been experiencing",

        "reports",

        "reported",

        "experiencing",

        "suffering from",

        "states that",

        "mentions"
    ]

    # Remove narrative phrases
    for phrase in filler_phrases:

        text = text.replace(
            phrase,
            " "
        )

    # Remove extra spaces
    text = re.sub(

        r"\s+",

        " ",

        text
    )

    return text.strip()


# Extract duration information
def extract_duration(
    text: str
) -> str:

    duration_match = re.search(

        r'((?:\d+|one|two|three|four|five|six|seven|eight|nine|ten)\s+'
        r'(?:day|days|week|weeks|month|months|year|years))',

        text,

        re.IGNORECASE
    )

    if duration_match:

        return duration_match.group(1)

    return ""


# Extract meaningful clinical phrase
# using POS tags instead of hardcoded words
def extract_clinical_phrase(
    text: str
) -> str:

    doc = nlp(
        text
    )

    phrase_tokens = []

    for token in doc:

        if token.pos_ in [

            "ADJ",

            "NOUN",

            "PROPN"
        ]:

            phrase_tokens.append(
                token.text
            )

    return " ".join(
        phrase_tokens
    ).strip()


# Generate clinical note
def generate_clinical_note(
    translated_text: str
) -> ClinicalNoteResponse:

    try:

        logger.info(
            "Starting clinical note generation"
        )

        # Validate translated text
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

        # Preprocess translated text
        translated_text = preprocess_text(
            translated_text
        )

        logger.info(
            f"Preprocessed Text: {translated_text}"
        )

        # Extract duration
        duration = extract_duration(
            translated_text
        )

        logger.info(
            f"Duration extracted: {duration}"
        )

        # Split text into sentences
        sentences = [

            sentence.strip()

            for sentence in re.split(
                r"[.]",
                translated_text
            )

            if sentence.strip()
        ]

        chief_complaint = ""

        symptoms = []

        # Process first sentence
        if len(sentences) > 0:

            first_sentence = (
                sentences[0]
            )

            # Remove duration from complaint sentence
            if duration:

                first_sentence = re.sub(

                    re.escape(duration),

                    "",

                    first_sentence,

                    flags=re.IGNORECASE
                )

            # Extract symptom after "with"
            if " with " in first_sentence.lower():

                split_text = re.split(

                    r"\bwith\b",

                    first_sentence,

                    flags=re.IGNORECASE
                )

                complaint_text = (
                    split_text[0]
                )

                if len(split_text) > 1:

                    symptoms.append(

                        split_text[1]
                        .strip()
                    )

            else:

                complaint_text = (
                    first_sentence
                )

            # Extract chief complaint
            chief_complaint = (

                extract_clinical_phrase(
                    complaint_text
                )
            )

        # Process remaining sentences
        for sentence in sentences[1:]:

            parts = re.split(

                r"\band\b",

                sentence,

                flags=re.IGNORECASE
            )

            for part in parts:

                part = (
                    part.strip()
                )

                if len(part) > 3:

                    symptoms.append(
                        part
                    )

        # Clean symptoms
        cleaned_symptoms = []

        for symptom in symptoms:

            symptom = (
                symptom.strip()
            )

            symptom = (
                symptom.strip(
                    "., "
                )
            )

            if len(symptom) < 3:

                continue

            cleaned_symptoms.append(
                symptom
            )

        # Remove duplicates
        symptoms = list(

            dict.fromkeys(
                cleaned_symptoms
            )
        )

        logger.info(
            f"Chief Complaint: {chief_complaint}"
        )

        logger.info(
            f"Symptoms Extracted: {symptoms}"
        )

        return ClinicalNoteResponse(

            chief_complaint=
                chief_complaint,

            duration=
                duration,

            symptoms=
                symptoms,

            source=
                "voice"
        )

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

