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

        if not text:

            return result

        # Normalize spaces
        text = re.sub(
            r"\s+",
            " ",
            text
        ).strip()

        # Patient Name
        patient_match = re.search(
            r"Patient\s*Name:\s*(.*?)\s*Diagnosis:",
            text,
            re.IGNORECASE
        )

        if patient_match:

            result["patient_name"] = (
                patient_match.group(1).strip()
            )

        # Diagnosis
        diagnosis_match = re.search(
            r"Diagnosis:\s*(.*?)\s*Medications:",
            text,
            re.IGNORECASE
        )

        if diagnosis_match:

            result["diagnosis"] = (
                diagnosis_match.group(1).strip()
            )

        # Medications
        medication_match = re.search(
            r"Medications:\s*(.*?)\s*Recommendations:",
            text,
            re.IGNORECASE
        )

        if medication_match:

            medications_text = (
                medication_match.group(1).strip()
            )

            result["medications"] = [
                medications_text
            ]

        # Recommendations
        recommendation_match = re.search(
            r"Recommendations:\s*(.*)",
            text,
            re.IGNORECASE
        )

        if recommendation_match:

            recommendations_text = (
                recommendation_match.group(1).strip()
            )

            result["recommendations"] = [
                recommendations_text
            ]

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