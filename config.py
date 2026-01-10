import os
from dotenv import load_dotenv


def load_config():
    """
    Load configuration from environment variables.

    Returns:
        dict: Configuration dictionary with api_key and model_name

    Raises:
        ValueError: If required configuration is missing or invalid
    """
    # Load environment variables from .env file
    load_dotenv()

    # Get API key and validate
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY not found. Please set it in your .env file.\n"
            "Get your API key at: https://platform.openai.com/api-keys"
        )

    if api_key == "sk-your-api-key-here":
        raise ValueError(
            "Please replace the placeholder API key in .env with your actual OpenAI API key.\n"
            "Get your API key at: https://platform.openai.com/api-keys"
        )

    # Get optional configuration with defaults
    model_name = os.getenv("MODEL_NAME", "gpt-4o-mini")

    return {
        "api_key": api_key,
        "model_name": model_name
    }
