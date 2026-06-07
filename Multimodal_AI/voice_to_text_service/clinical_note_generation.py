import re

from utils.logger import logger
from voice_to_text_service.voice_response import ClinicalNoteResponse


# Body parts used to construct the chief complaint
# Example:
# lower back + pain -> lower back pain
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


# Primary symptoms that form the chief complaint
PRIMARY_SYMPTOMS = [
    "pain",
    "stiffness",
    "swelling",
    "weakness",
    "instability",
    "tenderness",
    "spasm",
    "cramp",
    "soreness",
    "aching",
    "discomfort",
    "tightness",
    "inflammation"
]


# Secondary symptoms extracted as associated symptoms
SECONDARY_SYMPTOMS = [

    # Neurological symptoms
    "numbness",
    "tingling",
    "burning",
    "burning sensation",
    "loss of sensation",
    "pins and needles",
    "radiating pain",
    "shooting pain",
    "referred pain",

    # Functional limitations
    "difficulty walking",
    "difficulty standing",
    "difficulty sitting",
    "difficulty bending",
    "difficulty lifting",
    "difficulty climbing stairs",
    "difficulty reaching",
    "difficulty turning",
    "difficulty squatting",
    "difficulty running",
    "difficulty sleeping",

    # Movement restrictions
    "restricted movement",
    "reduced range of motion",
    "limited mobility",
    "joint locking",
    "joint clicking",
    "joint popping",

    # Balance and gait symptoms
    "loss of balance",
    "unsteady gait",
    "gait difficulty",

    # Muscle-related symptoms
    "muscle weakness",
    "muscle tightness",
    "muscle fatigue",
    "muscle spasm",

    # General symptoms
    "fatigue",
    "tiredness",
    "headache",
    "dizziness",
    "vertigo",
    "fever",
    "chills",
    "nausea",
    "vomiting",

    # Respiratory symptoms
    "cough",
    "shortness of breath",
    "breathlessness",

    # Physiotherapy-specific symptoms
    "pain while walking",
    "pain while standing",
    "pain while sitting",
    "pain while bending",
    "pain while lifting",
    "pain during movement",
    "pain at rest",
    "morning stiffness",
    "night pain",
    "weight bearing pain"
]


# Regex pattern to extract duration
# Examples:
# three weeks
# two months
# five years
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


# Clean and normalize incoming voice-transcribed text
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

    # Normalize common speech variations
    text = text.replace("paining", "pain")
    text = text.replace("spreading", "radiating")

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# Extract duration from the text
def extract_duration(text: str) -> str:

    match = DURATION_PATTERN.search(text)

    if match:
        return match.group(1).strip()

    return ""


# Extract the most specific body part
# Example:
# lower back preferred over back
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


# Extract the primary symptom
def extract_primary_symptom(text: str) -> str:

    for symptom in PRIMARY_SYMPTOMS:

        if symptom in text:
            return symptom

    return ""


# Construct chief complaint
# Example:
# lower back + pain -> lower back pain
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


# Extract associated symptoms
def extract_secondary_symptoms(text: str) -> list:

    detected = []

    # Detect symptoms from symptom dictionary
    for symptom in SECONDARY_SYMPTOMS:

        if symptom in text:
            detected.append(symptom)

    # Detect radiating pain pattern
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

    # Detect common activity aggravation patterns
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

    # Remove duplicate symptoms
    detected = list(
        dict.fromkeys(detected)
    )

    return detected


# Main function used by the API endpoint
# Converts translated voice text into a structured clinical note
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