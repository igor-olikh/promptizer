"""Custom exceptions for the promptizer system."""

import traceback


class PromptizerError(Exception):
    """Base exception for promptizer errors."""

    pass


class APIError(PromptizerError):
    """Exception raised when an API call fails."""

    def __init__(self, model_type: str, message: str, original_error: Exception = None):
        self.model_type = model_type
        self.original_error = original_error
        self.original_traceback = None
        if original_error:
            try:
                self.original_traceback = traceback.format_exception(
                    type(original_error), original_error, original_error.__traceback__
                )
            except Exception:
                pass
        super().__init__(f"{model_type} API Error: {message}")

    def get_original_error_details(self) -> str:
        """Get formatted details of the original error."""
        if not self.original_error:
            return ""
        
        details = []
        details.append(f"\n{'='*60}")
        details.append(f"Original {self.model_type} Exception:")
        details.append(f"{'='*60}")
        details.append(f"Exception Type: {type(self.original_error).__name__}")
        details.append(f"Exception Message: {str(self.original_error)}")
        
        if self.original_traceback:
            details.append(f"\nFull Traceback:")
            details.append("".join(self.original_traceback))
        else:
            # Fallback if traceback formatting failed
            details.append(f"\nException Details: {repr(self.original_error)}")
        
        return "\n".join(details)


class ModelNotFoundError(APIError):
    """Exception raised when a model is not found."""

    pass


class TimeoutError(APIError):
    """Exception raised when an API call times out."""

    pass

