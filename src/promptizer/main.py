"""Main entry point for the promptizer CLI."""

import asyncio
import sys
import os
from pathlib import Path
from .orchestrator import PromptRefinementOrchestrator
from .config import Config


def read_prompt_from_file(file_path: str) -> str:
    """Read prompt content from a file."""
    # Check if file exists in prompt folder first
    prompt_folder = Path("prompt")
    if prompt_folder.exists():
        prompt_file = prompt_folder / file_path
        if prompt_file.exists():
            with open(prompt_file, "r", encoding="utf-8") as f:
                return f.read().strip()
    
    # Try as direct path
    file_path_obj = Path(file_path)
    if file_path_obj.exists():
        with open(file_path_obj, "r", encoding="utf-8") as f:
            return f.read().strip()
    
    raise FileNotFoundError(f"File not found: {file_path}")


def write_output_to_file(input_file_path: str, output_content: str) -> str:
    """Write output to a file based on input filename."""
    # Determine output filename
    input_path = Path(input_file_path)
    prompt_folder = Path("prompt")
    
    # Determine output directory based on where the input file was found
    # Check if input file exists in prompt folder
    if prompt_folder.exists() and (prompt_folder / input_path.name).exists():
        output_dir = prompt_folder
        # Use just the filename for output naming
        actual_input_path = prompt_folder / input_path.name
    elif input_path.is_absolute() and input_path.exists():
        # Absolute path that exists
        output_dir = input_path.parent
        actual_input_path = input_path
    elif str(input_path).startswith("prompt/"):
        # Explicitly specified as prompt/ path
        output_dir = prompt_folder
        actual_input_path = prompt_folder / input_path.name
    elif input_path.parent != Path(".") and input_path.exists():
        # Relative path with directory that exists
        output_dir = input_path.parent
        actual_input_path = input_path
    else:
        # Default to prompt folder for relative filenames
        output_dir = prompt_folder
        actual_input_path = input_path
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create output filename: "filename output.txt"
    if actual_input_path.suffix:
        # Remove extension, add " output" and restore extension
        base_name = actual_input_path.stem
        output_filename = f"{base_name} output{actual_input_path.suffix}"
    else:
        # No extension, just add " output.txt"
        output_filename = f"{actual_input_path.name} output.txt"
    
    output_path = output_dir / output_filename
    
    # Write output
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(output_content)
    
    return str(output_path)


def is_file_path(input_str: str) -> bool:
    """Check if input string is likely a file path."""
    # Check if it's a single word/argument that looks like a filename
    # or if it contains path separators
    if "/" in input_str or "\\" in input_str:
        return True
    
    # Check if it ends with common text file extensions
    if input_str.endswith((".txt", ".md", ".prompt", ".text")):
        return True
    
    # Check if file exists (in prompt folder or as direct path)
    prompt_folder = Path("prompt")
    if prompt_folder.exists():
        if (prompt_folder / input_str).exists():
            return True
    
    if Path(input_str).exists():
        return True
    
    return False


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
    input_source = None
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
        
        # Check if input is a file path
        if is_file_path(user_input):
            try:
                initial_prompt = read_prompt_from_file(user_input)
                input_source = user_input
                print(f"📄 Reading prompt from file: {user_input}")
            except FileNotFoundError as e:
                print(f"❌ Error: {e}")
                sys.exit(1)
        else:
            # Treat as direct prompt text
            initial_prompt = user_input
    else:
        print("Enter your initial prompt or file path (or press Ctrl+D to exit):")
        try:
            user_input = input().strip()
            if is_file_path(user_input):
                try:
                    initial_prompt = read_prompt_from_file(user_input)
                    input_source = user_input
                    print(f"📄 Reading prompt from file: {user_input}")
                except FileNotFoundError as e:
                    print(f"❌ Error: {e}")
                    sys.exit(1)
            else:
                initial_prompt = user_input
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
        
        # Write to file if input was from a file
        if input_source:
            output_file = write_output_to_file(input_source, final_prompt)
            print(f"💾 Output written to: {output_file}")
        
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

