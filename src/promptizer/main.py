"""Main entry point for the promptizer CLI."""

import asyncio
import sys
from .orchestrator import PromptRefinementOrchestrator
from .config import Config


async def main():
    """Main function to run the prompt refinement system."""
    # Validate configuration
    try:
        Config.validate()
    except ValueError as e:
        print(f"Configuration error: {e}")
        print("\nPlease set the following environment variables:")
        print("  - OPENAI_API_KEY")
        print("  - GOOGLE_API_KEY")
        print("\nYou can create a .env file with these values.")
        sys.exit(1)

    # Get initial prompt
    if len(sys.argv) > 1:
        initial_prompt = " ".join(sys.argv[1:])
    else:
        print("Enter your initial prompt (or press Ctrl+D to exit):")
        try:
            initial_prompt = input().strip()
        except EOFError:
            print("\nExiting...")
            sys.exit(0)

    if not initial_prompt:
        print("Error: Prompt cannot be empty")
        sys.exit(1)

    # Run refinement
    orchestrator = PromptRefinementOrchestrator()
    try:
        final_prompt, state_summary = await orchestrator.refine(
            initial_prompt, verbose=True
        )
        print(f"\n✅ Refinement completed successfully!")
        return final_prompt, state_summary
    except KeyboardInterrupt:
        print("\n\nRefinement interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error during refinement: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

