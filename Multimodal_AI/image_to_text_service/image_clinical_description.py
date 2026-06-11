# Import regular expression utilities
import re

# Import application logger
from utils.logger import logger


def generate_clinical_description(text):
    """
    Robust clinical note extractor for OCR + translated text.

    Extracts:
    - patient_name
    - diagnosis
    - medications
    - recommendations

    Handles:
    - Single-line translated text
    - Multi-line translated text
    - OCR formatting issues
    - Advice/Suggestion/Recommendation variations
    """

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

        if not text:

            return result

        # ----------------------------------
        # Text Cleaning
        # ----------------------------------

        text = text.replace(
            "\r\n",
            "\n"
        )

        text = text.replace(
            "\r",
            "\n"
        )

        text = re.sub(
            r"[ \t]+",
            " ",
            text
        )

        # ----------------------------------
        # Normalize Section Headers
        # ----------------------------------

        headers = [

            "Patient Name",
            "Patient",

            "Diagnosis",
            "Clinical Diagnosis",
            "Assessment",
            "Description",
            "BD Description",

            "Medicine",
            "Medicines",
            "Medication",
            "Medications",
            "Drug",
            "Drugs",
            "Prescription",
            "Rx",

            "Advice",
            "Advises",
            "Suggestion",
            "Suggestions",
            "Recommendation",
            "Recommendations",
            "Instruction",
            "Instructions",
            "Plan",
            "Follow Up"
        ]

        # Insert newline before section headers
        for header in headers:

            text = re.sub(
                rf"\s*({re.escape(header)}\s*:)",
                r"\n\1",
                text,
                flags=re.IGNORECASE
            )

        text = re.sub(
            r"\n{2,}",
            "\n",
            text
        )

        text = text.strip()

        logger.info(
            f"Normalized Text:\n{text}"
        )

        # ----------------------------------
        # Extract Patient Name
        # ----------------------------------

        patient_match = re.search(
            r"Patient\s*Name\s*:\s*(.*?)(?=\n(?:Diagnosis|Clinical Diagnosis|Assessment|Description|BD Description)\s*:|$)",
            text,
            re.IGNORECASE | re.DOTALL
        )

        if patient_match:

            result["patient_name"] = (
                patient_match.group(1).strip()
            )

        # ----------------------------------
        # Extract Diagnosis
        # ----------------------------------

        diagnosis_match = re.search(
            r"(?:Diagnosis|Clinical Diagnosis|Assessment|Description|BD Description)\s*:\s*(.*?)(?=\n(?:Medicine|Medicines|Medication|Medications|Drug|Drugs|Prescription|Rx)\s*:|$)",
            text,
            re.IGNORECASE | re.DOTALL
        )

        if diagnosis_match:

            result["diagnosis"] = (
                diagnosis_match.group(1).strip()
            )

        # ----------------------------------
        # Extract Medications
        # ----------------------------------

        medication_match = re.search(
            r"(?:Medicine|Medicines|Medication|Medications|Drug|Drugs|Prescription|Rx)\s*:\s*(.*?)(?=\n(?:Advice|Advises|Suggestion|Suggestions|Recommendation|Recommendations|Instruction|Instructions|Plan|Follow Up)\s*:|$)",
            text,
            re.IGNORECASE | re.DOTALL
        )

        if medication_match:

            medications_text = (
                medication_match.group(1).strip()
            )

            medications = [

                item.strip()

                for item in re.split(
                    r"[\n,;•●▪]",
                    medications_text
                )

                if item.strip()
            ]

            result["medications"] = medications

        # ----------------------------------
        # Extract Recommendations
        # ----------------------------------

        recommendation_match = re.search(
            r"(?:Advice|Advises|Suggestion|Suggestions|Recommendation|Recommendations|Instruction|Instructions|Plan|Follow Up)\s*:\s*(.*)",
            text,
            re.IGNORECASE | re.DOTALL
        )

        if recommendation_match:

            recommendations_text = (
                recommendation_match.group(1).strip()
            )

            recommendations = [

                item.strip()

                for item in re.split(
                    r"[\n,;•●▪]",
                    recommendations_text
                )

                if item.strip()
            ]

            result["recommendations"] = recommendations

        # ----------------------------------
        # Remove Duplicates
        # ----------------------------------

        result["medications"] = list(
            dict.fromkeys(
                result["medications"]
            )
        )

        result["recommendations"] = list(
            dict.fromkeys(
                result["recommendations"]
            )
        )

        logger.info(
            f"Extracted Clinical Information: {result}"
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