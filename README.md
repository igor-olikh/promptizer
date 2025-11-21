# Promptizer

A collaborative LLM system that uses OpenAI and Google Gemini to iteratively refine prompts until both models agree on the quality.

## Overview

Promptizer implements a sophisticated prompt refinement system where two independent Large Language Models (OpenAI GPT-4 and Google Gemini) work together to progressively improve a user-provided prompt. The system continues iterating until both models independently determine that the prompt has reached acceptable quality.

## Features

- **Collaborative Refinement**: Two LLMs work together to improve prompts
- **Automatic Evaluation**: Models independently evaluate prompt quality
- **Convergence Detection**: System stops when both models accept the prompt
- **Asynchronous Processing**: Parallel API calls for efficiency
- **Iteration Control**: Prevents infinite loops with configurable max iterations
- **State Tracking**: Maintains history of all refinements
- **File Input/Output**: Read prompts from files and automatically save outputs
- **Markdown Comparison**: Generates color-coded markdown files comparing original vs refined prompts
- **Error Handling**: Stops immediately on API errors to prevent wasting tokens

## Installation

1. Clone the repository:
```bash
git clone https://github.com/igor-olikh/promptizer.git
cd promptizer
```

2. Install dependencies using Poetry:
```bash
poetry install
```

3. Create a `.env` file in the project root:
```bash
cp .env.example .env
```

4. Edit `.env` and add your API keys:
```
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
```

## Usage

### Command Line

**List available models:**
```bash
poetry run python -m promptizer.main --list-models
# Shows all available OpenAI and Gemini models
# Validates your current configuration
```

**Direct prompt input:**
```bash
poetry run python -m promptizer.main "Your initial prompt here"
```

**File-based input:**
```bash
# Place your prompt in the prompt/ folder, then:
poetry run python -m promptizer.main "example.txt"
# Output will be written to "example output.txt" in the same folder
```

**Interactive mode:**
```bash
poetry run python -m promptizer.main
# Then enter your prompt or file path when prompted
```

### File Input/Output

The system supports reading prompts from files and automatically writing outputs:

1. **Place your prompt file** in the `prompt/` folder (or provide a full path)
2. **Run with the filename**: `poetry run python -m promptizer.main "my-prompt.txt"`
3. **Output is automatically written** to a corresponding file: `my-prompt output.txt`

Example:
- Input file: `prompt/code prompt to improve.txt`
- Output file: `prompt/code prompt to improve output.txt`

The system automatically detects if the input is a file path (by checking for file extensions like `.txt`, `.md`, or if the file exists).

### Markdown Comparison Output

When refinement completes successfully, the system automatically generates a markdown comparison file:

- **Input file**: `prompt/my-prompt.txt`
- **Output file**: `prompt/my-prompt output.txt` (refined prompt)
- **Markdown file**: `prompt/my-prompt.md` (color-coded comparison)

The markdown file includes:
- Summary of the refinement process
- Original prompt (yellow/amber background)
- Refined prompt (green background)
- Side-by-side comparison table
- Refinement statistics

### Python API

```python
import asyncio
from promptizer.orchestrator import PromptRefinementOrchestrator

async def refine_prompt():
    orchestrator = PromptRefinementOrchestrator()
    final_prompt, state_summary = await orchestrator.refine(
        "Your initial prompt here",
        verbose=True
    )
    return final_prompt

# Run it
final = asyncio.run(refine_prompt())
print(final)
```

## Configuration

You can configure the system via environment variables in your `.env` file:

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `GOOGLE_API_KEY`: Your Google Gemini API key (required)
- `OPENAI_MODEL`: OpenAI model to use (default: `gpt-4`)
- `GEMINI_MODEL`: Gemini model to use (default: `gemini-1.5-flash`)
- `MAX_ITERATIONS`: Maximum number of iterations (default: `10`)

### Checking Available Models

If you encounter model not found errors, use the model listing feature:

```bash
poetry run python -m promptizer.main --list-models
```

This will:
- List all available OpenAI models
- List all available Gemini models (with generateContent support)
- Show your current configuration
- Validate if your configured models are available
- Provide recommendations for fixing configuration issues

## How It Works

1. **Initial Prompt**: User provides a raw prompt
2. **Iteration Loop**:
   - Model A (OpenAI) receives the current prompt and generates an improved version
   - Model B (Gemini) receives the current prompt and generates an improved version
   - Both models evaluate whether the prompt is "good enough"
   - The hub merges the results and updates the current prompt
3. **Convergence**: When both models respond with "ACCEPTED", the loop stops
4. **Output**: The final refined prompt is returned

## Architecture

See the [documentation](docs/) folder for detailed architecture diagrams and system design.

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

