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

Activate the Poetry environment and run:
```bash
poetry run python -m promptizer.main "Your initial prompt here"
```

Or run interactively:
```bash
poetry run python -m promptizer.main
# Then enter your prompt when prompted
```

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
- `GEMINI_MODEL`: Gemini model to use (default: `gemini-pro`)
- `MAX_ITERATIONS`: Maximum number of iterations (default: `10`)

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

