"""Data models for prompt refinement system."""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class ModelType(str, Enum):
    """Enumeration of model types."""

    OPENAI = "openai"
    GEMINI = "gemini"


class EvaluationStatus(str, Enum):
    """Status of prompt evaluation."""

    ACCEPTED = "ACCEPTED"
    NEEDS_IMPROVEMENT = "NEEDS_IMPROVEMENT"
    REJECTED = "REJECTED"


class RefinementRequest(BaseModel):
    """Request for prompt refinement."""

    prompt: str = Field(..., description="The current prompt to refine")
    iteration: int = Field(..., description="Current iteration number")
    previous_refinements: list[str] = Field(
        default_factory=list, description="History of previous refinements"
    )
    model_type: ModelType = Field(..., description="Type of model making the request")


class RefinementResponse(BaseModel):
    """Response from a model refinement."""

    refined_prompt: str = Field(..., description="The refined version of the prompt")
    evaluation_status: EvaluationStatus = Field(
        ..., description="Whether the prompt is acceptable"
    )
    reasoning: str = Field(
        ..., description="Explanation for the refinement and evaluation"
    )
    model_type: ModelType = Field(..., description="Type of model that produced this")
    timestamp: datetime = Field(default_factory=datetime.now)


class HubState(BaseModel):
    """State maintained by the central hub."""

    original_prompt: str
    current_prompt: str
    iteration: int = 0
    refinement_history: list[RefinementResponse] = Field(default_factory=list)
    openai_accepted: bool = False
    gemini_accepted: bool = False
    is_converged: bool = False
    convergence_reason: Optional[str] = None
    _pending_responses: list[RefinementResponse] = Field(default_factory=list, exclude=True)

    def update(self, response: RefinementResponse) -> None:
        """Update hub state with a new refinement response."""
        self.refinement_history.append(response)
        self._pending_responses.append(response)

        if response.model_type == ModelType.OPENAI:
            self.openai_accepted = response.evaluation_status == EvaluationStatus.ACCEPTED
        elif response.model_type == ModelType.GEMINI:
            self.gemini_accepted = response.evaluation_status == EvaluationStatus.ACCEPTED

    def finalize_iteration(self) -> None:
        """Finalize the iteration by selecting the best prompt from responses."""
        if not self._pending_responses:
            return

        # Select the best prompt
        best_response = self._select_best_response(self._pending_responses)
        self.current_prompt = best_response.refined_prompt
        self.iteration += 1

        # Clear pending responses
        self._pending_responses = []

        # Check convergence
        if self.openai_accepted and self.gemini_accepted:
            self.is_converged = True
            self.convergence_reason = "Both models accepted the prompt"

    def _select_best_response(self, responses: list[RefinementResponse]) -> RefinementResponse:
        """Select the best response from a list of responses."""
        # Prefer accepted responses
        accepted = [r for r in responses if r.evaluation_status == EvaluationStatus.ACCEPTED]
        if accepted:
            # If multiple accepted, prefer the longer/more detailed one
            return max(accepted, key=lambda r: len(r.refined_prompt))

        # If none accepted, prefer the longer/more detailed one
        return max(responses, key=lambda r: len(r.refined_prompt))

