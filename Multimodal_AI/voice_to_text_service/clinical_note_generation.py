import re
import spacy

from utils.logger import logger
from voice_to_text_service.voice_response import ClinicalNoteResponse

logger.info("Loading SciSpaCy model...")
nlp = spacy.load("en_core_sci_sm")
logger.info("SciSpaCy model loaded successfully")

TEMPORAL_WORDS = {
"day",
"days",
"week",
"weeks",
"month",
"months",
"year",
"years",
"past",
"last",
"time",
"today",
"yesterday",
"tomorrow"
}

def preprocess_text(text):

```
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

text = text.replace("paining", "pain")
text = text.replace("spreading", "radiating")

text = re.sub(r"\s+", " ", text)

return text.strip()
```

def extract_duration(text):

```
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
    return match.group(1)

return ""
```

def extract_chief_complaint(text, duration):

```
if duration:
    text = text.replace(duration, "")

first_sentence = re.split(
    r"[.!?]",
    text
)[0]

doc = nlp(first_sentence)

complaint_words = []

for token in doc:

    word = token.text.lower()

    if word in TEMPORAL_WORDS:
        continue

    if token.pos_ in [
        "NOUN",
        "ADJ"
    ]:
        complaint_words.append(word)

complaint = " ".join(
    dict.fromkeys(
        complaint_words
    )
)

complaint = complaint.strip()

complaint = re.sub(
    r"\s+",
    " ",
    complaint
)

return complaint
```

def extract_symptoms(text):

```
symptoms = []

sentences = re.split(
    r"[.!?]",
    text
)

for sentence in sentences[1:]:

    sentence = sentence.strip()

    if not sentence:
        continue

    symptoms.append(
        sentence
    )

return list(
    dict.fromkeys(
        symptoms
    )
)
```

def generate_clinical_note(translated_text):

```
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

    chief_complaint = extract_chief_complaint(
        processed_text,
        duration
    )

    symptoms = extract_symptoms(
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
        f"Clinical note generation error: {error}"
    )

    return ClinicalNoteResponse(
        chief_complaint="",
        duration="",
        symptoms=[],
        source="voice"
    )

