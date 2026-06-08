# Import required libraries
import re
import cv2
import pytesseract

# Import configuration
from utils.config import (
    TESSERACT_PATH
)

# Import logger
from utils.logger import logger

# Configure Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = (
    TESSERACT_PATH
)


def clean_text(text):

    text = text.replace(
        "\n",
        " "
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def detect_language(text):

    if re.search(
        r'[\u0B80-\u0BFF]',
        text
    ):
        return "Tamil"

    if re.search(
        r'[\u0C00-\u0C7F]',
        text
    ):
        return "Telugu"

    if re.search(
        r'[\u0900-\u097F]',
        text
    ):
        return "Hindi"

    if re.search(
        r'[A-Za-z]',
        text
    ):
        return "English"

    return "Unknown"


def preprocess_image(image):

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    gray = cv2.resize(
        gray,
        None,
        fx=3,
        fy=3,
        interpolation=cv2.INTER_CUBIC
    )

    gray = cv2.GaussianBlur(
        gray,
        (3, 3),
        0
    )

    gray = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY +
        cv2.THRESH_OTSU
    )[1]

    return gray


def extract_text(image_path):

    try:

        logger.info(
            f"Processing Image: {image_path}"
        )

        image = cv2.imread(
            image_path
        )

        if image is None:

            logger.error(
                "Unable to read image"
            )

            return {
                "language": "Unknown",
                "text": "Unable to read image"
            }

        processed_image = preprocess_image(
            image
        )

        try:

            extracted_text = pytesseract.image_to_string(
                processed_image,
                lang="eng+hin+tam+tel",
                config="--oem 3 --psm 6"
            )

        except Exception as e:

            logger.warning(
                f"Multilingual OCR failed. Falling back to English OCR. Error: {str(e)}"
            )

            extracted_text = pytesseract.image_to_string(
                processed_image,
                lang="eng",
                config="--oem 3 --psm 6"
            )

        extracted_text = clean_text(
            extracted_text
        )

        if not extracted_text:

            logger.warning(
                "No text detected in image"
            )

            return {
                "language": "Unknown",
                "text": "No text detected"
            }

        detected_language = detect_language(
            extracted_text
        )

        # Vital Log 1
        logger.info(
            f"Detected Language: {detected_language}"
        )

        # Vital Log 2
        logger.info(
            f"Extracted Text Preview: {extracted_text[:200]}"
        )

        return {
            "language": detected_language,
            "text": extracted_text
        }

    except Exception as e:

        logger.error(
            f"OCR Error: {str(e)}"
        )

        return {
            "language": "Unknown",
            "text": str(e)
        }