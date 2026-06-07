import re
import spacy

from utils.logger import logger
from voice_to_text_service.voice_response import ClinicalNoteResponse


logger.info("Loading spaCy model...")

try:
    nlp = spacy.load("en_core_sci_sm")
except Exception:
    nlp = spacy.load("en_core_web_sm")

logger.info("spaCy model loaded successfully")


def preprocess_text(text: str) -> str:

    if not text:
        return ""

    text = text.lower().strip()

    filler_phrases = [
        "the patient",
        "patient",
        "reports",
        "reported",
        "complains of",
        "complained of",
        "has complained of",
        "states that",
        "mentions"
    ]

    for phrase in filler_phrases:
        text = text.replace(phrase, " ")

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def extract_duration(text: str) -> str:

    pattern = re.compile(
        r"(?:for|since|past|last)?\s*"
        r"("
        r"(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten|"
        r"eleven|twelve)"
        r"\s+"
        r"(?:day|days|week|weeks|month|months|year|years)"
        r")",
        re.IGNORECASE
    )

    match = pattern.search(text)

    if match:
        return match.group(1).strip()

    return ""


def extract_symptoms(text: str) -> list:

    symptom_keywords = [
        "pain",
        "headache",
        "fever",
        "nausea",
        "vomiting",
        "dizziness",
        "swelling",
        "cough",
        "fatigue",
        "weakness",
        "numbness",
        "seizure",
        "breathlessness"
    ]

    symptoms = []

    doc = nlp(text)

    for token in doc:

        word = token.text.lower()

        if word in symptom_keywords:

            if word not in symptoms:
                symptoms.append(word)

    return symptoms


def extract_chief_complaint(symptoms: list) -> str:

    if symptoms:
        return symptoms[0]

    return ""


def generate_clinical_note(
    translated_text: str
) -> ClinicalNoteResponse:

    try:

        logger.info(
            "Starting clinical note generation"
        )

        if not translated_text:

            return ClinicalNoteResponse(
                chief_complaint="",
                duration="",
                symptoms=[],
                source="voice"
            )

        processed_text = preprocess_text(
            translated_text
        )

        duration = extract_duration(
            processed_text
        )

        symptoms = extract_symptoms(
            processed_text
        )

        chief_complaint = extract_chief_complaint(
            symptoms
        )

        remaining_symptoms = [
            symptom
            for symptom in symptoms
            if symptom != chief_complaint
        ]

        return ClinicalNoteResponse(
            chief_complaint=chief_complaint,
            duration=duration,
            symptoms=remaining_symptoms,
            source="voice"
        )

    except Exception as error:

        logger.error(
            f"Clinical note generation error: {error}"
        )

        return ClinicalNoteResponse(
            chief_complaint="",
            duration="",
            symptoms=[],
            source="voice"
        )