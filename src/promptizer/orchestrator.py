"""Main orchestrator for the prompt refinement system."""

import asyncio
from .hub import RefinementHub
from .openai_client import OpenAIClient
from .gemini_client import GeminiClient
from .models import ModelType, RefinementResponse
from .exceptions import APIError, ModelNotFoundError, TimeoutError


class PromptRefinementOrchestrator:
    """Orchestrates the collaborative refinement process."""

    def __init__(self):
        """Initialize the orchestrator with clients."""
        self.openai_client = OpenAIClient()
        self.gemini_client = GeminiClient()

    async def refine(
        self, initial_prompt: str, verbose: bool = True
    ) -> tuple[str, dict]:
        """
        Refine a prompt through collaborative iteration.

        Args:
            initial_prompt: The initial prompt to refine
            verbose: Whether to print progress information

        Returns:
            Tuple of (final_prompt, state_summary)
        """
        hub = RefinementHub(initial_prompt)

        if verbose:
            print(f"Starting refinement process...")
            print(f"Original prompt: {initial_prompt}\n")

        # Iteration loop
        while hub.should_continue():
            iteration = hub.state.iteration + 1

            if verbose:
                print(f"\n{'='*60}")
                print(f"Iteration {iteration}")
                print(f"{'='*60}")

            # Create requests for both models
            openai_request = hub.create_refinement_request(ModelType.OPENAI)
            gemini_request = hub.create_refinement_request(ModelType.GEMINI)

            # Run refinements sequentially to avoid timeout issues
            if verbose:
                print("Running OpenAI and Gemini refinements sequentially...")

            # Run OpenAI first
            if verbose:
                print("  → Calling OpenAI...")
            try:
                openai_response = await self.openai_client.refine_prompt(openai_request)
            except (APIError, ModelNotFoundError, TimeoutError) as e:
                raise e
            except Exception as e:
                raise APIError("OpenAI", f"Unexpected error: {str(e)}", e)
            
            # Then run Gemini
            if verbose:
                print("  → Calling Gemini...")
            try:
                gemini_response = await self.gemini_client.refine_prompt(gemini_request)
            except (APIError, ModelNotFoundError, TimeoutError) as e:
                raise e
            except Exception as e:
                raise APIError("Gemini", f"Unexpected error: {str(e)}", e)

            # Process responses
            hub.process_response(openai_response)
            hub.process_response(gemini_response)
            
            # Finalize iteration by selecting the best prompt
            hub.finalize_iteration()

            if verbose:
                self._print_iteration_results(
                    openai_response, gemini_response, hub
                )

            # Check convergence after processing both responses
            if not hub.should_continue():
                break

        # Get final result
        final_prompt = hub.get_final_prompt()
        state_summary = hub.get_state_summary()

        if verbose:
            print(f"\n{'='*60}")
            print("REFINEMENT COMPLETE")
            print(f"{'='*60}")
            print(f"Final prompt:\n{final_prompt}\n")
            print(f"Total iterations: {state_summary['iteration']}")
            print(f"Convergence reason: {state_summary['convergence_reason']}")

        return final_prompt, state_summary

    def _print_iteration_results(
        self,
        openai_response: RefinementResponse,
        gemini_response: RefinementResponse,
        hub: RefinementHub,
    ) -> None:
        """Print results of an iteration."""
        print(f"\nOpenAI Response:")
        print(f"  Status: {openai_response.evaluation_status.value}")
        print(f"  Reasoning: {openai_response.reasoning[:200]}...")
        print(f"  Refined prompt: {openai_response.refined_prompt[:150]}...")

        print(f"\nGemini Response:")
        print(f"  Status: {gemini_response.evaluation_status.value}")
        print(f"  Reasoning: {gemini_response.reasoning[:200]}...")
        print(f"  Refined prompt: {gemini_response.refined_prompt[:150]}...")

        print(f"\nHub State:")
        print(f"  Current prompt: {hub.state.current_prompt[:150]}...")
        print(f"  OpenAI accepted: {hub.state.openai_accepted}")
        print(f"  Gemini accepted: {hub.state.gemini_accepted}")

