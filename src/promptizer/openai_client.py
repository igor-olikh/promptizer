"""OpenAI API client for prompt refinement."""

import json
from pathlib import Path
from openai import AsyncOpenAI
from openai import APIError as OpenAIAPIError
from .config import Config
from .models import ModelType, RefinementRequest, RefinementResponse, EvaluationStatus
from .exceptions import APIError, ModelNotFoundError


class OpenAIClient:
    """Client for interacting with OpenAI API."""

    def __init__(self):
        """Initialize OpenAI client."""
        Config.validate()
        self.client = AsyncOpenAI(api_key=Config.OPENAI_API_KEY)
        self.model = Config.OPENAI_MODEL

    def _load_prompt_template(self, filename: str) -> str:
        """Load a prompt template from file."""
        prompt_dir = Path(__file__).parent / "prompts"
        prompt_file = prompt_dir / filename
        if prompt_file.exists():
            return prompt_file.read_text(encoding="utf-8").strip()
        raise FileNotFoundError(f"Prompt template not found: {prompt_file}")

    def _build_system_prompt(self) -> str:
        """Build the system prompt for OpenAI."""
        return self._load_prompt_template("system_prompt.txt")

    def _build_user_prompt(self, request: RefinementRequest) -> str:
        """Build the user prompt for OpenAI."""
        # Build previous refinements section
        previous_refinements_section = ""
        if request.previous_refinements:
            previous_refinements_section = "\nPrevious refinement history:"
            for i, prev in enumerate(request.previous_refinements[-3:], 1):
                previous_refinements_section += f"\n{i}. {prev}"
        
        # Load template and format it
        template = self._load_prompt_template("user_prompt_template.txt")
        return template.format(
            iteration=request.iteration,
            prompt=request.prompt,
            previous_refinements_section=previous_refinements_section
        )

    async def refine_prompt(
        self, request: RefinementRequest
    ) -> RefinementResponse:
        """Refine a prompt using OpenAI.
        
        Raises:
            ModelNotFoundError: If the model is not found
            APIError: If there's an API error
        """
        system_prompt = self._build_system_prompt()
        user_prompt = self._build_user_prompt(request)

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.7,
                response_format={"type": "json_object"},
            )

            content = response.choices[0].message.content
            result = json.loads(content)

            return RefinementResponse(
                refined_prompt=result.get("refined_prompt", request.prompt),
                evaluation_status=EvaluationStatus(
                    result.get("evaluation_status", "NEEDS_IMPROVEMENT")
                ),
                reasoning=result.get("reasoning", "No reasoning provided"),
                model_type=ModelType.OPENAI,
            )
        except OpenAIAPIError as e:
            # OpenAI API error - stop immediately
            error_msg = str(e)
            # Include additional error details if available
            if hasattr(e, 'status_code'):
                error_msg += f" (Status Code: {e.status_code})"
            if hasattr(e, 'code'):
                error_msg += f" (Code: {e.code})"
            if hasattr(e, 'type'):
                error_msg += f" (Type: {e.type})"
            if hasattr(e, 'param'):
                error_msg += f" (Param: {e.param})"
            if "model" in error_msg.lower() and ("not found" in error_msg.lower() or "404" in error_msg):
                raise ModelNotFoundError(
                    "OpenAI",
                    f"Model '{self.model}' not found. Please check your model name in .env file. Error: {error_msg}",
                    e
                )
            raise APIError("OpenAI", error_msg, e)
        except json.JSONDecodeError as e:
            # JSON parsing error - stop immediately
            raise APIError(
                "OpenAI",
                f"Failed to parse JSON response: {str(e)}",
                e
            )
        except Exception as e:
            # Any other error - stop immediately
            error_msg = str(e)
            if "404" in error_msg or "not found" in error_msg.lower():
                raise ModelNotFoundError(
                    "OpenAI",
                    f"Model error: {error_msg}. Please check your model name in .env file.",
                    e
                )
            raise APIError("OpenAI", f"Unexpected error: {error_msg}", e)

