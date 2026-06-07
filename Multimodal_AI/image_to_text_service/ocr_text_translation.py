# Import required libraries
from deep_translator import GoogleTranslator


# ==========================================================
# TRANSLATE TEXT TO ENGLISH
# ==========================================================

def translate_to_english(text):

    try:

        if not text:

            return ""

        translated_text = GoogleTranslator(
            source="auto",
            target="en"
        ).translate(
            text
        )

        return translated_text

    except Exception as e:

        print(
            f"Translation Error: {str(e)}"
        )

        return text