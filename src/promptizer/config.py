"""Configuration management for Promptizer."""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuration class for API keys and model settings."""

    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4")

    # Google Gemini Configuration
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

    # System Configuration
    MAX_ITERATIONS: int = int(os.getenv("MAX_ITERATIONS", "10"))

    @classmethod
    def validate(cls) -> None:
        """Validate that required API keys are set."""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set in environment variables")
        if not cls.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY is not set in environment variables")

