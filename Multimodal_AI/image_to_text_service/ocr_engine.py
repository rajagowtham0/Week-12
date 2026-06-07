import warnings

# Ignore unnecessary warnings
warnings.filterwarnings("ignore")

# Import required libraries
import easyocr
import cv2
from langdetect import detect

# Load EasyOCR models
print("Loading EasyOCR models...")

# Separate readers because EasyOCR does not allow
# Tamil, Telugu and Hindi in a single reader

english_reader = easyocr.Reader(
    ['en'],
    gpu=False
)

hindi_reader = easyocr.Reader(
    ['hi', 'en'],
    gpu=False
)

tamil_reader = easyocr.Reader(
    ['ta', 'en'],
    gpu=False
)

telugu_reader = easyocr.Reader(
    ['te', 'en'],
    gpu=False
)

print("All EasyOCR models loaded successfully")


# Language Mapping
LANGUAGE_NAMES = {
    "en": "English",
    "hi": "Hindi",
    "ta": "Tamil",
    "te": "Telugu"
}


# Detect language using langdetect
def detect_language(text):

    try:

        language_code = detect(text)

        return LANGUAGE_NAMES.get(
            language_code,
            f"Unknown Language ({language_code})"
        )

    except Exception:

        return "Unable to Detect Language"


# Text Cleaning Function
def clean_text(text):

    print("Starting text cleaning process...")

    text = " ".join(text.split())

    print("Extra spaces removed")

    text = text.replace(
        "\n",
        " "
    )

    text = " ".join(text.split())

    print("Text formatting cleanup completed")

    return text.strip()


# OCR Helper Function
def perform_ocr(reader, image):

    try:

        results = reader.readtext(
            image,
            paragraph=True
        )

        extracted_text = []

        for result in results:

            if len(result) < 2:
                continue

            extracted_text.append(
                result[1].strip()
            )

        final_text = " ".join(
            extracted_text
        )

        return clean_text(
            final_text
        )

    except Exception as e:

        print(f"OCR Error: {str(e)}")

        return ""


# Main OCR Function
def extract_text(image_path):

    try:

        print("Starting OCR Extraction Pipeline")

        print(
            f"Processing Image: {image_path}"
        )

        image = cv2.imread(
            image_path
        )

        if image is None:

            print(
                "Image loading failed"
            )

            return {
                "language": "Unknown",
                "text": "Unable to read image"
            }

        print(
            "Image loaded successfully"
        )

        # Resize image for better OCR accuracy
        image = cv2.resize(
            image,
            None,
            fx=3,
            fy=3,
            interpolation=cv2.INTER_CUBIC
        )

        print(
            "Image resized successfully"
        )

        # OCR using all supported readers
        print(
            "Running multilingual OCR..."
        )

        english_text = perform_ocr(
            english_reader,
            image
        )

        hindi_text = perform_ocr(
            hindi_reader,
            image
        )

        tamil_text = perform_ocr(
            tamil_reader,
            image
        )

        telugu_text = perform_ocr(
            telugu_reader,
            image
        )

        # Store OCR results
        ocr_results = {
            "English": english_text,
            "Hindi": hindi_text,
            "Tamil": tamil_text,
            "Telugu": telugu_text
        }

        # Select the result containing
        # maximum extracted characters
        detected_language = max(
            ocr_results,
            key=lambda x: len(
                ocr_results[x]
            )
        )

        final_text = ocr_results[
            detected_language
        ]

        # If OCR result is empty
        if not final_text:

            return {
                "language": "Unknown",
                "text": "No text detected"
            }

        # Additional verification
        auto_detected_language = detect_language(
            final_text
        )

        print(
            f"EasyOCR Language: {detected_language}"
        )

        print(
            f"LangDetect Language: {auto_detected_language}"
        )

        print(
            "Final Extracted Text:"
        )

        print(
            final_text
        )

        return {
            "language": detected_language,
            "detected_language": auto_detected_language,
            "text": final_text
        }

    except Exception as e:

        print(
            "OCR Extraction Error:"
        )

        print(
            str(e)
        )

        return {
            "language": "Unknown",
            "text": f"OCR Extraction Error: {str(e)}"
        }


# Example Usage
if __name__ == "__main__":

    result = extract_text(
        "sample_image.jpg"
    )

    print("\nDetected Language:")
    print(
        result["language"]
    )

    print("\nLanguage Verification:")
    print(
        result.get(
            "detected_language",
            "N/A"
        )
    )

    print("\nExtracted Text:")
    print(
        result["text"]
    )