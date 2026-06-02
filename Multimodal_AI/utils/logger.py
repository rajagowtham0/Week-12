import logging

# Configure logging format
logging.basicConfig(

    level=logging.INFO,

    format=
    "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

# Create logger instance
logger = logging.getLogger(
    "Multimodal_CCMS_AI"
)