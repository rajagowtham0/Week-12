import warnings
warnings.filterwarnings("ignore")

import easyocr
import cv2
from langdetect import detect

print("OCR Engine Initialized")

# Global Readers
english_reader = None
hindi_reader = None
tamil_reader = None
telugu_reader = None


def get_english_reader():

    global english_reader

    if english_reader is None:

        print("Loading English OCR Model...")

        english_reader = easyocr.Reader(
            ['en'],
            gpu=False
        )

    return english_reader


def get_hindi_reader():

    global hindi_reader

    if hindi_reader is None:

        try:

            print("Loading Hindi OCR Model...")

            hindi_reader = easyocr.Reader(
                ['hi', 'en'],
                gpu=False
            )

        except Exception as e:

            print(
                f"Hindi OCR Model Load Failed: {str(e)}"
            )

            hindi_reader = None

    return hindi_reader


def get_tamil_reader():

    global tamil_reader

    if tamil_reader is None:

        try:

            print("Loading Tamil OCR Model...")

            tamil_reader = easyocr.Reader(
                ['ta', 'en'],
                gpu=False
            )

        except Exception as e:

            print(
                f"Tamil OCR Model Load Failed: {str(e)}"
            )

            tamil_reader = None

    return tamil_reader


def get_telugu_reader():

    global telugu_reader

    if telugu_reader is None:

        try:

            print("Loading Telugu OCR Model...")

            telugu_reader = easyocr.Reader(
                ['te', 'en'],
                gpu=False
            )

        except Exception as e:

            print(
                f"Telugu OCR Model Load Failed: {str(e)}"
            )

            telugu_reader = None

    return telugu_reader


LANGUAGE_MAPPING = {
    "en": "English",
    "hi": "Hindi",
    "ta": "Tamil",
    "te": "Telugu"
}


def detect_language(text):

    try:

        language_code = detect(text)

        return LANGUAGE_MAPPING.get(
            language_code,
            language_code
        )

    except Exception:

        return "Unknown"


def clean_text(text):

    text = text.replace(
        "\n",
        " "
    )

    text = " ".join(
        text.split()
    )

    return text.strip()


def perform_ocr(reader, image):

    try:

        if reader is None:

            return ""

        results = reader.readtext(
            image,
            paragraph=True
        )

        extracted_text = []

        for result in results:

            if len(result) >= 2:

                extracted_text.append(
                    result[1].strip()
                )

        return clean_text(
            " ".join(
                extracted_text
            )
        )

    except Exception as e:

        print(
            f"OCR Error: {str(e)}"
        )

        return ""


def extract_text(image_path):

    try:

        print(
            f"Processing Image: {image_path}"
        )

        image = cv2.imread(
            image_path
        )

        if image is None:

            return {
                "language": "Unknown",
                "text": "Unable to read image"
            }

        image = cv2.resize(
            image,
            None,
            fx=3,
            fy=3,
            interpolation=cv2.INTER_CUBIC
        )

        ocr_results = {}

        english_text = perform_ocr(
            get_english_reader(),
            image
        )

        if english_text:

            ocr_results["English"] = english_text

        hindi_text = perform_ocr(
            get_hindi_reader(),
            image
        )

        if hindi_text:

            ocr_results["Hindi"] = hindi_text

        tamil_text = perform_ocr(
            get_tamil_reader(),
            image
        )

        if tamil_text:

            ocr_results["Tamil"] = tamil_text

        telugu_text = perform_ocr(
            get_telugu_reader(),
            image
        )

        if telugu_text:

            ocr_results["Telugu"] = telugu_text

        if not ocr_results:

            return {
                "language": "Unknown",
                "text": "No text detected"
            }

        detected_language = max(
            ocr_results,
            key=lambda x: len(
                ocr_results[x]
            )
        )

        final_text = ocr_results[
            detected_language
        ]

        verified_language = detect_language(
            final_text
        )

        return {
            "language": detected_language,
            "verified_language": verified_language,
            "text": final_text
        }

    except Exception as e:

        print(
            f"OCR Extraction Error: {str(e)}"
        )

        return {
            "language": "Unknown",
            "text": str(e)
        }