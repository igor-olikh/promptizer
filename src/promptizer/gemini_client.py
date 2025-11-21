"""Google Gemini API client for prompt refinement."""

import asyncio
import json
import re
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
        """Try to fix common JSON issues in the response with comprehensive handling."""
        # Remove any leading/trailing whitespace
        original_content = content
        content = content.strip()
        
        # Step 1: Extract JSON object if it's embedded in other text
        if "{" in content:
            start_idx = content.find("{")
            # Find matching closing brace
            brace_count = 0
            end_idx = start_idx
            in_string = False
            escape_next = False
            
            for i in range(start_idx, len(content)):
                char = content[i]
                
                if escape_next:
                    escape_next = False
                    continue
                
                if char == '\\':
                    escape_next = True
                    continue
                
                if char == '"' and not escape_next:
                    in_string = not in_string
                    continue
                
                if not in_string:
                    if char == "{":
                        brace_count += 1
                    elif char == "}":
                        brace_count -= 1
                        if brace_count == 0:
                            end_idx = i + 1
                            break
            
            if brace_count == 0 and end_idx > start_idx:
                content = content[start_idx:end_idx]
            elif brace_count > 0:
                # Unmatched braces - try to close them
                content = content[start_idx:] + "}" * brace_count
        
        # Step 2: Fix escaping issues - normalize all escape sequences
        # Fix multiple levels of escaping systematically
        # We need to be careful to only fix actual escape sequences, not literal backslashes
        
        # Pattern: Fix double-escaped quotes (\\\" -> \")
        # But we need to be smart about this - only fix if it's inside a string value
        # For now, do a simple replacement but be more careful
        
        # Fix: \\\" -> \" (double-escaped quote)
        content = re.sub(r'\\\\+"', lambda m: '\\"' * (len(m.group(0)) // 3), content)
        
        # More targeted: Fix \\\" specifically (most common case)
        # Replace any sequence of backslashes followed by quote with proper escaping
        # This regex finds \\\" and converts to \"
        def fix_escaped_quotes(match):
            backslashes = match.group(1)
            # If we have 2+ backslashes before quote, reduce to 1
            if len(backslashes) >= 2:
                return '\\"'
            return match.group(0)
        
        content = re.sub(r'(\\+)"', fix_escaped_quotes, content)
        
        # Fix escaped newlines: \\\\n -> \\n -> \n (when parsed)
        # Normalize to single escape: \\n
        content = re.sub(r'\\{2,}n', r'\\n', content)
        
        # Fix escaped backslashes: normalize multiple backslashes
        # But be careful - we want \\ to stay as \\ (for escaped chars)
        # Only fix if there are 4+ backslashes in a row
        content = re.sub(r'\\{4,}', r'\\\\', content)
        
        # Step 3: Fix structural issues
        # Remove trailing commas before closing braces/brackets
        content = re.sub(r',(\s*[}\]])', r'\1', content)
        
        # Step 4: Handle truncated or unclosed strings
        # Check if we have properly closed strings
        # Simple heuristic: count unescaped quotes
        quote_count = 0
        escape_next = False
        for char in content:
            if escape_next:
                escape_next = False
                continue
            if char == '\\':
                escape_next = True
                continue
            if char == '"':
                quote_count += 1
        
        # If odd number of quotes, we might have an unclosed string
        if quote_count % 2 != 0:
            # Try to find where the string should close
            # Look for the last field and try to close it properly
            last_brace = content.rfind('}')
            if last_brace > 0:
                # Check the structure before the last brace
                before_brace = content[:last_brace].rstrip()
                # If it doesn't end with a quote, try to add one
                if not before_brace.endswith('"') and not before_brace.endswith('\\'):
                    # Try to find the last unclosed string
                    # Look for pattern like: "key": "value (missing closing quote)
                    match = re.search(r':\s*"([^"]*)$', before_brace)
                    if match:
                        # Found an unclosed string value, close it
                        content = before_brace + '"' + content[last_brace:]
        
        # Step 5: Try to fix truncated JSON by completing missing fields
        # If we're missing closing braces, try to add them
        open_braces = content.count('{')
        close_braces = content.count('}')
        if open_braces > close_braces:
            content += '}' * (open_braces - close_braces)
        
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

            # Try to parse JSON with multiple attempts
            result = None
            attempts = [
                content,  # Try fixed content first
                original_content,  # Try original content
            ]
            
            last_error = None
            for attempt_content in attempts:
                try:
                    result = json.loads(attempt_content)
                    content = attempt_content  # Use the working version
                    break
                except json.JSONDecodeError as e:
                    last_error = e
                    # Try one more fix pass on this content
                    try:
                        fixed_again = self._try_fix_json(attempt_content)
                        if fixed_again != attempt_content:
                            result = json.loads(fixed_again)
                            content = fixed_again
                            break
                    except (json.JSONDecodeError, Exception):
                        continue
            
            # If all attempts failed, try to extract partial data as last resort
            if result is None:
                # Try to extract at least the refined_prompt field even if JSON is malformed
                refined_prompt_match = re.search(r'"refined_prompt"\s*:\s*"([^"]*(?:\\.[^"]*)*)"', content)
                evaluation_match = re.search(r'"evaluation_status"\s*:\s*"([^"]+)"', content)
                reasoning_match = re.search(r'"reasoning"\s*:\s*"([^"]*(?:\\.[^"]*)*)"', content)
                
                if refined_prompt_match:
                    # We found at least the refined_prompt, create a partial result
                    refined_prompt = refined_prompt_match.group(1)
                    # Unescape the string
                    refined_prompt = refined_prompt.replace('\\"', '"').replace('\\n', '\n')
                    
                    evaluation_status = evaluation_match.group(1) if evaluation_match else "NEEDS_IMPROVEMENT"
                    reasoning = reasoning_match.group(1) if reasoning_match else "Partial extraction due to JSON parsing error"
                    if reasoning_match:
                        reasoning = reasoning.replace('\\"', '"').replace('\\n', '\n')
                    
                    # Create a valid result from extracted data
                    result = {
                        "refined_prompt": refined_prompt,
                        "evaluation_status": evaluation_status,
                        "reasoning": reasoning
                    }
                else:
                    # Couldn't extract anything, raise the error
                    raise last_error

            # Convert escaped newlines to actual newlines for readability
            refined_prompt = result.get("refined_prompt", request.prompt)
            refined_prompt = refined_prompt.replace("\\n", "\n")

            return RefinementResponse(
                refined_prompt=refined_prompt,
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

