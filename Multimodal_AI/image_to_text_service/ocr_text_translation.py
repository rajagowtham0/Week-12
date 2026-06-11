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

        # Preserve line structure before translation
        lines = [

            line.strip()

            for line in text.splitlines()

            if line.strip()

        ]

        translated_lines = []

        # Translate line by line
        for line in lines:

            try:

                translated_line = GoogleTranslator(
                    source="auto",
                    target="en"
                ).translate(
                    line
                )

                translated_lines.append(
                    translated_line
                )

            except Exception as line_error:

                logger.warning(
                    f"Line translation failed: {str(line_error)}"
                )

                translated_lines.append(
                    line
                )

        # Reconstruct translated text with original line breaks
        translated_text = "\n".join(
            translated_lines
        )

        logger.info(
            "OCR text translation completed successfully"
        )

        logger.info(
            f"Translated {len(lines)} text segments successfully"
        )

        return translated_text

    except Exception as e:

        logger.error(
            f"OCR translation error: {str(e)}"
        )

        # Return original text if translation fails
        return text