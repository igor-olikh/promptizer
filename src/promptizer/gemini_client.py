"""Google Gemini API client for prompt refinement."""

import asyncio
import json
from pathlib import Path
import google.generativeai as genai
from google.api_core import exceptions as google_exceptions
from .config import Config
from .models import ModelType, RefinementRequest, RefinementResponse, EvaluationStatus
from .exceptions import APIError, ModelNotFoundError, TimeoutError


class GeminiClient:
    """Client for interacting with Google Gemini API."""

    def __init__(self):
        """Initialize Gemini client."""
        Config.validate()
        genai.configure(api_key=Config.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)

    def _load_prompt_template(self, filename: str) -> str:
        """Load a prompt template from file."""
        prompt_dir = Path(__file__).parent / "prompts"
        prompt_file = prompt_dir / filename
        if prompt_file.exists():
            return prompt_file.read_text(encoding="utf-8").strip()
        raise FileNotFoundError(f"Prompt template not found: {prompt_file}")

    def _build_system_prompt(self) -> str:
        """Build the system prompt for Gemini."""
        return self._load_prompt_template("gemini_system_prompt.txt")

    def _try_fix_json(self, content: str) -> str:
        """Try to fix common JSON issues in the response."""
        # Remove any leading/trailing whitespace
        content = content.strip()
        
        # Try to find and extract JSON object
        if "{" in content:
            start_idx = content.find("{")
            # Find matching closing brace
            brace_count = 0
            end_idx = start_idx
            for i in range(start_idx, len(content)):
                if content[i] == "{":
                    brace_count += 1
                elif content[i] == "}":
                    brace_count -= 1
                    if brace_count == 0:
                        end_idx = i + 1
                        break
            
            if brace_count == 0:
                content = content[start_idx:end_idx]
            else:
                # Unmatched braces - try to close them
                content = content[start_idx:] + "}" * brace_count
        
        # Try to fix common issues
        # Remove trailing commas before closing braces/brackets
        import re
        content = re.sub(r',(\s*[}\]])', r'\1', content)
        
        return content

    def _build_user_prompt(self, request: RefinementRequest) -> str:
        """Build the user prompt for Gemini."""
        # Build previous refinements section
        previous_refinements_section = ""
        if request.previous_refinements:
            previous_refinements_section = "\nPrevious refinement history:"
            for i, prev in enumerate(request.previous_refinements[-3:], 1):
                previous_refinements_section += f"\n{i}. {prev}"
        
        # Load template and format it
        template = self._load_prompt_template("user_prompt_template.txt")
        user_prompt = template.format(
            iteration=request.iteration,
            prompt=request.prompt,
            previous_refinements_section=previous_refinements_section
        )
        
        # Add Gemini-specific JSON reminder
        user_prompt += "\n\nRemember: Respond with ONLY a valid JSON object (no other text). Escape all quotes, newlines, and special characters in the JSON strings."
        
        return user_prompt

    async def refine_prompt(
        self, request: RefinementRequest
    ) -> RefinementResponse:
        """Refine a prompt using Gemini.
        
        Raises:
            ModelNotFoundError: If the model is not found
            APIError: If there's an API error
        """
        system_prompt = self._build_system_prompt()
        user_prompt = self._build_user_prompt(request)

        # Combine system and user prompts for Gemini
        full_prompt = f"{system_prompt}\n\n{user_prompt}"

        content = ""
        try:
            # Run in executor since Gemini SDK may not be fully async
            # Configure generation parameters to ensure complete responses
            generation_config = genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=2048,  # Ensure enough tokens for complete JSON
            )
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, 
                lambda: self.model.generate_content(
                    full_prompt,
                    generation_config=generation_config
                )
            )

            content = response.text.strip()

            # Try to extract JSON from the response
            # Sometimes Gemini wraps JSON in markdown code blocks
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()

            # Try to fix common JSON issues
            original_content = content
            content = self._try_fix_json(content)

            # Try to parse JSON
            try:
                result = json.loads(content)
            except json.JSONDecodeError:
                # If fixing didn't work, try the original content
                if content != original_content:
                    try:
                        result = json.loads(original_content)
                        content = original_content
                    except json.JSONDecodeError:
                        # Re-raise with original content for better error message
                        content = original_content
                        raise
                else:
                    raise

            return RefinementResponse(
                refined_prompt=result.get("refined_prompt", request.prompt),
                evaluation_status=EvaluationStatus(
                    result.get("evaluation_status", "NEEDS_IMPROVEMENT")
                ),
                reasoning=result.get("reasoning", "No reasoning provided"),
                model_type=ModelType.GEMINI,
            )
        except google_exceptions.NotFound as e:
            # Model not found - stop immediately
            error_msg = str(e)
            # Include additional error details if available
            if hasattr(e, 'code'):
                error_msg += f" (Code: {e.code})"
            if hasattr(e, 'message'):
                error_msg += f" (Message: {e.message})"
            if "not found" in error_msg.lower() or "404" in error_msg:
                raise ModelNotFoundError(
                    "Gemini",
                    f"Model '{Config.GEMINI_MODEL}' not found. Please check your model name in .env file. Error: {error_msg}",
                    e
                )
            raise APIError("Gemini", error_msg, e)
        except google_exceptions.DeadlineExceeded as e:
            # Timeout error - stop immediately with helpful message
            error_msg = str(e)
            if hasattr(e, 'code'):
                error_msg += f" (Code: {e.code})"
            if hasattr(e, 'message'):
                error_msg += f" (Message: {e.message})"
            raise TimeoutError(
                "Gemini",
                f"Request timed out (504 Deadline Exceeded). This may be due to:\n"
                f"  - Network connectivity issues\n"
                f"  - Gemini API being temporarily overloaded\n"
                f"  - The prompt being too long or complex\n"
                f"  - API rate limiting\n\n"
                f"Please try again in a few moments. If the issue persists, try:\n"
                f"  - Using a shorter prompt\n"
                f"  - Checking your network connection\n"
                f"  - Verifying your API quota/limits\n\n"
                f"Original error: {error_msg}",
                e
            )
        except google_exceptions.InvalidArgument as e:
            # Invalid arguments - stop immediately
            error_msg = str(e)
            if hasattr(e, 'code'):
                error_msg += f" (Code: {e.code})"
            if hasattr(e, 'message'):
                error_msg += f" (Message: {e.message})"
            raise APIError("Gemini", f"Invalid argument: {error_msg}", e)
        except json.JSONDecodeError as e:
            # JSON parsing error - show full response for debugging
            error_msg = f"Failed to parse JSON response: {str(e)}"
            if content:
                error_msg += f"\n\nRaw response (first 1000 chars):\n{content[:1000]}"
                if len(content) > 1000:
                    error_msg += f"\n... (truncated, total length: {len(content)} chars)"
                # Try to show where the error occurred
                if hasattr(e, 'pos') and e.pos:
                    error_msg += f"\n\nError position: {e.pos}"
                    if e.pos < len(content):
                        start = max(0, e.pos - 50)
                        end = min(len(content), e.pos + 50)
                        error_msg += f"\nContext around error:\n{content[start:end]}"
            else:
                error_msg += "\nNo content received from API."
            raise APIError("Gemini", error_msg, e)
        except Exception as e:
            # Any other error - stop immediately
            error_msg = str(e)
            # Check for timeout/deadline errors in the message
            if "504" in error_msg or "deadline exceeded" in error_msg.lower() or "timeout" in error_msg.lower():
                raise TimeoutError(
                    "Gemini",
                    f"Request timed out (504 Deadline Exceeded). This may be due to:\n"
                    f"  - Network connectivity issues\n"
                    f"  - Gemini API being temporarily overloaded\n"
                    f"  - The prompt being too long or complex\n"
                    f"  - API rate limiting\n\n"
                    f"Please try again in a few moments. If the issue persists, try:\n"
                    f"  - Using a shorter prompt\n"
                    f"  - Checking your network connection\n"
                    f"  - Verifying your API quota/limits",
                    e
                )
            if "404" in error_msg or "not found" in error_msg.lower():
                raise ModelNotFoundError(
                    "Gemini",
                    f"Model error: {error_msg}. Please check your model name in .env file.",
                    e
                )
            raise APIError("Gemini", f"Unexpected error: {error_msg}", e)

