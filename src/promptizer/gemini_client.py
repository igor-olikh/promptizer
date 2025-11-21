"""Google Gemini API client for prompt refinement."""

import asyncio
import json
import google.generativeai as genai
from .config import Config
from .models import ModelType, RefinementRequest, RefinementResponse, EvaluationStatus


class GeminiClient:
    """Client for interacting with Google Gemini API."""

    def __init__(self):
        """Initialize Gemini client."""
        Config.validate()
        genai.configure(api_key=Config.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)

    def _build_system_prompt(self) -> str:
        """Build the system prompt for Gemini."""
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
Respond with "NEEDS_IMPROVEMENT" if there are still areas that could be enhanced.

IMPORTANT: Respond ONLY with valid JSON, no additional text before or after."""

    def _build_user_prompt(self, request: RefinementRequest) -> str:
        """Build the user prompt for Gemini."""
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
        """Refine a prompt using Gemini."""
        system_prompt = self._build_system_prompt()
        user_prompt = self._build_user_prompt(request)

        # Combine system and user prompts for Gemini
        full_prompt = f"{system_prompt}\n\n{user_prompt}"

        content = ""
        try:
            # Run in executor since Gemini SDK may not be fully async
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, lambda: self.model.generate_content(full_prompt)
            )

            content = response.text.strip()

            # Try to extract JSON from the response
            # Sometimes Gemini wraps JSON in markdown code blocks
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()

            result = json.loads(content)

            return RefinementResponse(
                refined_prompt=result.get("refined_prompt", request.prompt),
                evaluation_status=EvaluationStatus(
                    result.get("evaluation_status", "NEEDS_IMPROVEMENT")
                ),
                reasoning=result.get("reasoning", "No reasoning provided"),
                model_type=ModelType.GEMINI,
            )
        except json.JSONDecodeError as e:
            # Try to extract prompt from text if JSON parsing fails
            content_preview = content[:200] if content else "No content available"
            return RefinementResponse(
                refined_prompt=request.prompt,
                evaluation_status=EvaluationStatus.NEEDS_IMPROVEMENT,
                reasoning=f"Failed to parse JSON response: {str(e)}. Raw response: {content_preview}",
                model_type=ModelType.GEMINI,
            )
        except Exception as e:
            # Fallback: return the original prompt with needs improvement status
            return RefinementResponse(
                refined_prompt=request.prompt,
                evaluation_status=EvaluationStatus.NEEDS_IMPROVEMENT,
                reasoning=f"Error during refinement: {str(e)}",
                model_type=ModelType.GEMINI,
            )

