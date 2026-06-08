# Import translation library
from deep_translator import GoogleTranslator

# Import application logger
from utils.logger import logger


# Translate extracted OCR text into English
def translate_to_english(text):

    try:

        # Validate input text
        if not text:

            logger.warning(
                "Empty text received for translation"
            )

            return ""

        logger.info(
            "OCR text translation started"
        )

        # Translate text to English
        translated_text = GoogleTranslator(
            source="auto",
            target="en"
        ).translate(
            text
        )

        logger.info(
            "OCR text translation completed successfully"
        )

        return translated_text

    except Exception as e:

        logger.error(
            f"OCR translation error: {str(e)}"
        )

        # Return original text if translation fails
        return text