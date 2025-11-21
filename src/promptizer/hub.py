"""Central hub for managing prompt refinement iterations."""

from .models import HubState, RefinementRequest, RefinementResponse, ModelType
from .config import Config


class RefinementHub:
    """Central controller for managing collaborative prompt refinement."""

    def __init__(self, initial_prompt: str):
        """Initialize the hub with an initial prompt."""
        self.state = HubState(
            original_prompt=initial_prompt,
            current_prompt=initial_prompt,
            iteration=0,
        )

    def create_refinement_request(
        self, model_type: ModelType
    ) -> RefinementRequest:
        """Create a refinement request for a specific model."""
        previous_refinements = [
            r.refined_prompt for r in self.state.refinement_history[-3:]
        ]

        return RefinementRequest(
            prompt=self.state.current_prompt,
            iteration=self.state.iteration + 1,
            previous_refinements=previous_refinements,
            model_type=model_type,
        )

    def process_response(self, response: RefinementResponse) -> None:
        """Process a refinement response and update hub state."""
        self.state.update(response)

    def finalize_iteration(self) -> None:
        """Finalize the current iteration by selecting the best prompt."""
        self.state.finalize_iteration()

    def should_continue(self) -> bool:
        """Determine if the refinement loop should continue."""
        # Stop if both models accepted
        if self.state.is_converged:
            return False

        # Stop if max iterations reached
        if self.state.iteration >= Config.MAX_ITERATIONS:
            self.state.convergence_reason = (
                f"Maximum iterations ({Config.MAX_ITERATIONS}) reached"
            )
            return False

        return True

    def get_final_prompt(self) -> str:
        """Get the final refined prompt."""
        return self.state.current_prompt

    def get_state_summary(self) -> dict:
        """Get a summary of the current state."""
        return {
            "iteration": self.state.iteration,
            "current_prompt": self.state.current_prompt,
            "openai_accepted": self.state.openai_accepted,
            "gemini_accepted": self.state.gemini_accepted,
            "is_converged": self.state.is_converged,
            "convergence_reason": self.state.convergence_reason,
            "refinement_count": len(self.state.refinement_history),
        }

