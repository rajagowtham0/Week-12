# Import regular expression utilities
import re

# Import application logger
from utils.logger import logger


# Extract structured clinical information from translated OCR text
def generate_clinical_description(text):

    try:

        logger.info(
            "Clinical information extraction started"
        )

        result = {

            "patient_name": "",

            "diagnosis": "",

            "medications": [],

            "recommendations": []
        }

        # Validate input text
        if not text:

            logger.warning(
                "Empty text received for clinical information extraction"
            )

            return result

        # Split text into lines
        lines = text.split(
            "\n"
        )

        for line in lines:

            clean_line = line.strip()

            if not clean_line:

                continue

            lower_line = clean_line.lower()

            # Extract Patient Name
            if (
                "patient name" in lower_line
                or
                lower_line.startswith("name:")
            ):

                result["patient_name"] = re.sub(
                    r"(?i)(patient\s*name\s*:|name\s*:)",
                    "",
                    clean_line
                ).strip()

                continue

            # Extract Diagnosis
            if (
                "diagnosis" in lower_line
                or
                "impression" in lower_line
            ):

                result["diagnosis"] = re.sub(
                    r"(?i)(diagnosis\s*:|impression\s*:)",
                    "",
                    clean_line
                ).strip()

                continue

            # Extract Medications
            if re.search(

                r"\b("
                r"tablet|tab|capsule|cap|syrup|"
                r"inj|injection|cream|ointment|"
                r"paracetamol|dolo|crocin|"
                r"azithromycin|amoxicillin|"
                r"cetirizine|ibuprofen|"
                r"pantoprazole|omeprazole"
                r")\b",

                lower_line

            ):

                result[
                    "medications"
                ].append(
                    clean_line
                )

                continue

            # Extract Recommendations
            if any(

                keyword in lower_line

                for keyword in [

                    "recommendation",

                    "recommended",

                    "advice",

                    "follow up",

                    "review after",

                    "consult",

                    "take rest",

                    "avoid",

                    "drink plenty of water",

                    "bed rest"
                ]

            ):

                result[
                    "recommendations"
                ].append(
                    clean_line
                )

        logger.info(
            "Clinical information extraction completed successfully"
        )

        return result

    except Exception as e:

        logger.error(
            f"Clinical information extraction error: {str(e)}"
        )

        return {

            "patient_name": "",

            "diagnosis": "",

            "medications": [],

            "recommendations": []
        }