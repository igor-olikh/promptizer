"""OpenAI API client for prompt refinement."""

import json
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

    def _build_system_prompt(self) -> str:
        """Build the system prompt for OpenAI."""
        return """You are an expert at refining prompts to make them clearer, more specific, and more effective.

Your task is to:
1. Analyze the given prompt
2. Improve it by enhancing clarity, specificity, removing ambiguity, and ensuring completeness
3. Evaluate whether the prompt is "good enough" based on:
   - Clarity: Is the prompt clear and easy to understand?
   - Specificity: Does it provide enough detail?
   - Lack of ambiguity: Are there multiple interpretations possible?
   - Completeness: Does it cover all necessary aspects?
   - Alignment with user intent: Does it capture what the user likely wants?

After refining, you must respond in the following JSON format:
{
    "refined_prompt": "your improved prompt here",
    "evaluation_status": "ACCEPTED" or "NEEDS_IMPROVEMENT",
    "reasoning": "explanation of your changes and evaluation"
}

Respond with "ACCEPTED" only if the prompt is truly excellent and needs no further improvement.
Respond with "NEEDS_IMPROVEMENT" if there are still areas that could be enhanced."""

    def _build_user_prompt(self, request: RefinementRequest) -> str:
        """Build the user prompt for OpenAI."""
        prompt_parts = [
            f"Current prompt (Iteration {request.iteration}):",
            f"{request.prompt}",
        ]

        if request.previous_refinements:
            prompt_parts.append("\nPrevious refinement history:")
            for i, prev in enumerate(request.previous_refinements[-3:], 1):
                prompt_parts.append(f"{i}. {prev}")

        prompt_parts.append(
            "\nPlease refine this prompt and evaluate whether it's good enough. "
            "Respond with a JSON object containing 'refined_prompt', 'evaluation_status', and 'reasoning'."
        )

        return "\n".join(prompt_parts)

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

