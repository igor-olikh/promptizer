"""Custom exceptions for the promptizer system."""


class PromptizerError(Exception):
    """Base exception for promptizer errors."""

    pass


class APIError(PromptizerError):
    """Exception raised when an API call fails."""

    def __init__(self, model_type: str, message: str, original_error: Exception = None):
        self.model_type = model_type
        self.original_error = original_error
        super().__init__(f"{model_type} API Error: {message}")


class ModelNotFoundError(APIError):
    """Exception raised when a model is not found."""

    pass

