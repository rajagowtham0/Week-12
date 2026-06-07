import re
from collections import Counter

from utils.logger import logger
from voice_to_text_service.voice_response import ClinicalNoteResponse


BODY_PARTS = [
    "lower back",
    "upper back",
    "middle back",
    "back",
    "neck",
    "shoulder",
    "right shoulder",
    "left shoulder",
    "arm",
    "elbow",
    "wrist",
    "hand",
    "finger",
    "hip",
    "pelvis",
    "thigh",
    "leg",
    "right leg",
    "left leg",
    "knee",
    "right knee",
    "left knee",
    "calf",
    "ankle",
    "foot",
    "heel",
    "spine"
]


PRIMARY_SYMPTOMS = [
    "pain",
    "stiffness",
    "swelling",
    "weakness",
    "instability",
    "tenderness",
    "spasm",
    "cramp"
]


SECONDARY_SYMPTOMS = [
    "numbness",
    "tingling",
    "burning",
    "burning sensation",
    "radiating pain",
    "restricted movement",
    "difficulty walking",
    "difficulty standing",
    "difficulty sitting",
    "difficulty bending",
    "difficulty lifting",
    "difficulty climbing stairs",
    "loss of balance",
    "reduced range of motion",
    "muscle tightness",
    "muscle weakness",
    "gait difficulty"
]


DURATION_PATTERN = re.compile(
    r"(?:for|since|past|last)?\s*"
    r"("
    r"(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten|"
    r"eleven|twelve)"
    r"\s+"
    r"(?:day|days|week|weeks|month|months|year|years)"
    r")",
    re.IGNORECASE
)


def preprocess_text(text: str) -> str:

    if not text:
        return ""

    text = text.lower()

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

    text = text.replace("paining", "pain")
    text = text.replace("spreading", "radiating")

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def extract_duration(text: str) -> str:

    match = DURATION_PATTERN.search(text)

    if match:
        return match.group(1).strip()

    return ""


def extract_body_part(text: str) -> str:

    matched_parts = []

    for part in BODY_PARTS:

        if part in text:
            matched_parts.append(part)

    if not matched_parts:
        return ""

    matched_parts.sort(
        key=len,
        reverse=True
    )

    return matched_parts[0]


def extract_primary_symptom(text: str) -> str:

    for symptom in PRIMARY_SYMPTOMS:

        if symptom in text:
            return symptom

    return ""


def build_chief_complaint(text: str) -> str:

    body_part = extract_body_part(text)

    primary_symptom = extract_primary_symptom(text)

    if body_part and primary_symptom:
        return f"{body_part} {primary_symptom}"

    if body_part:
        return body_part

    if primary_symptom:
        return primary_symptom

    return ""


def extract_secondary_symptoms(text: str) -> list:

    detected = []

    for symptom in SECONDARY_SYMPTOMS:

        if symptom in text:
            detected.append(symptom)

    if "radiating" in text:

        leg_match = re.search(
            r"radiating.*?(left leg|right leg|leg)",
            text
        )

        if leg_match:
            detected.append(
                f"radiating pain to {leg_match.group(1)}"
            )
        else:
            detected.append(
                "radiating pain"
            )

    if "standing" in text:
        detected.append(
            "pain aggravated by standing"
        )

    if "walking" in text:
        detected.append(
            "difficulty walking"
        )

    if "bending" in text:
        detected.append(
            "difficulty bending"
        )

    if "lifting" in text:
        detected.append(
            "difficulty lifting"
        )

    detected = list(
        dict.fromkeys(detected)
    )

    return detected


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

        chief_complaint = build_chief_complaint(
            processed_text
        )

        symptoms = extract_secondary_symptoms(
            processed_text
        )

        return ClinicalNoteResponse(
            chief_complaint=chief_complaint,
            duration=duration,
            symptoms=symptoms,
            source="voice"
        )

    except Exception as error:

        logger.error(
            f"Clinical note generation error: {str(error)}"
        )

        return ClinicalNoteResponse(
            chief_complaint="",
            duration="",
            symptoms=[],
            source="voice"
        )