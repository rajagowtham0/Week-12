import warnings

# Ignore unnecessary warnings
warnings.filterwarnings("ignore")

# Import required libraries
import easyocr
import cv2

# Load EasyOCR model
print("Loading EasyOCR model...")

# Initialize EasyOCR Reader
# ['en'] -> English language support
# gpu=False -> Uses CPU for processing
reader = easyocr.Reader(
    ['en'],
    gpu=False
)

print("EasyOCR model loaded successfully")


# Text Cleaning Function
# Cleans extracted OCR text without modifying original words
def clean_text(text):

    print("Starting text cleaning process...")

    # Remove extra spaces
    text = " ".join(text.split())

    print("Extra spaces removed")

    # Replace newline characters with spaces
    text = text.replace(
        "\n",
        " "
    )

    # Remove repeated spaces again
    text = " ".join(text.split())

    print("Text formatting cleanup completed")

    # Return cleaned text
    return text.strip()


# OCR Text Extraction Function
def extract_text(image_path):

    try:

        print("Starting OCR Extraction Pipeline")

        # Display image path
        print(f"Processing Image: {image_path}")

        # Read image using OpenCV
        image = cv2.imread(image_path)

        # Validate image loading
        if image is None:

            print("Image loading failed")

            return "Unable to read image"

        print("Image loaded successfully")

        # Resize image
        # Enlarging image improves OCR accuracy
        image = cv2.resize(
            image,
            None,
            fx=3,
            fy=3,
            interpolation=cv2.INTER_CUBIC
        )

        print("Image resized successfully")

        # Perform OCR extraction
        print("Starting OCR text detection...")

        results = reader.readtext(
            image,
            paragraph=True
        )

        print("OCR text detection completed")

        # Display raw OCR results
        print("OCR Raw Results:")
        print(results)

        # Store extracted text
        extracted_text = []

        # Loop through OCR results
        for result in results:

            # Validate OCR result structure
            if len(result) < 2:

                continue

            # Extract detected text
            text = result[1]

            print(f"Detected Text: {text}")

            # Store extracted text
            extracted_text.append(
                text.strip()
            )

        print("All detected text collected successfully")

        # Combine extracted text
        final_text = " ".join(extracted_text)

        print("Text combination completed")

        # Clean extracted text
        final_text = clean_text(
            final_text
        )

        print("Text cleaning completed")

        # Handle empty OCR output
        if final_text == "":

            print("No text detected in image")

            return "No text detected"

        # Display final extracted text
        print("Final Extracted Text:")
        print(final_text)

        # Return final extracted text
        return final_text

    except Exception as e:

        # Print OCR extraction error
        print("OCR Extraction Error:")
        print(str(e))

        # Return error message
        return f"OCR Extraction Error: {str(e)}"