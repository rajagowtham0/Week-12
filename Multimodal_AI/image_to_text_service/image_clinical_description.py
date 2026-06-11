# Import regular expression utilities
import re

# Import application logger
from utils.logger import logger


# Extract structured clinical information
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

        # Validate input
        if not text:

            return result

        # Normalize spaces
        text = re.sub(
            r"\s+",
            " ",
            text
        ).strip()

        logger.info(
            f"Clinical Text Received: {text}"
        )

        # Patient Name
        patient_match = re.search(
            r"Patient\s*Name\s*[:\-]?\s*([A-Za-z\s]+)",
            text,
            re.IGNORECASE
        )

        if patient_match:

            result["patient_name"] = (
                patient_match.group(1).strip()
            )

        # Diagnosis
        diagnosis_match = re.search(
            r"Diagnosis\s*[:\-]?\s*(.*?)(?=Medications?|Medicines?|Prescription|Recommendations?|Advice|$)",
            text,
            re.IGNORECASE
        )

        if diagnosis_match:

            result["diagnosis"] = (
                diagnosis_match.group(1).strip()
            )

        # Medications
        medication_match = re.search(
            r"(?:Medications?|Medicines?|Prescription)\s*[:\-]?\s*(.*?)(?=Recommendations?|Advice|$)",
            text,
            re.IGNORECASE
        )

        if medication_match:

            medications_text = (
                medication_match.group(1).strip()
            )

            medications = [

                med.strip()

                for med in re.split(
                    r"[,;\n]",
                    medications_text
                )

                if med.strip()
            ]

            result["medications"] = medications

        # Recommendations
        recommendation_match = re.search(
            r"(?:Recommendations?|Advice)\s*[:\-]?\s*(.*)",
            text,
            re.IGNORECASE
        )

        if recommendation_match:

            recommendations_text = (
                recommendation_match.group(1).strip()
            )

            recommendations = [

                rec.strip()

                for rec in re.split(
                    r"[,;\n]",
                    recommendations_text
                )

                if rec.strip()
            ]

            result["recommendations"] = recommendations

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