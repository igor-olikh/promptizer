# Promptizer Documentation

Welcome to the Promptizer documentation! This directory contains comprehensive documentation for the collaborative LLM prompt refinement system.

## Documentation Index

### [Architecture Documentation](architecture.md)
Complete system architecture, component details, data flow, and design decisions. This document explains:
- System architecture and component interactions
- Data flow and message exchange formats
- Convergence detection mechanisms
- Error handling strategies
- Performance considerations
- Extensibility features

### [How-To Guide](how-to.md)
Step-by-step guide for using Promptizer. Includes:
- Quick start instructions
- Installation and configuration
- Basic and advanced usage examples
- Troubleshooting tips
- Integration examples
- Best practices

### [Example Walkthrough](example.md)
Detailed example showing a complete refinement process from start to finish. Demonstrates:
- How prompts evolve through iterations
- How both models collaborate
- Convergence detection in action
- Real-world refinement scenarios

## Quick Links

- **Main README**: [../README.md](../README.md)
- **GitHub Repository**: https://github.com/igor-olikh/promptizer

## System Overview

Promptizer is a collaborative prompt refinement system that uses two independent Large Language Models (OpenAI GPT-4 and Google Gemini) to iteratively improve user-provided prompts until both models agree on the quality.

### Key Features

- **Collaborative Refinement**: Two LLMs work together to improve prompts
- **Automatic Evaluation**: Models independently evaluate prompt quality
- **Convergence Detection**: System stops when both models accept the prompt
- **Asynchronous Processing**: Parallel API calls for efficiency
- **Iteration Control**: Prevents infinite loops with configurable max iterations
- **State Tracking**: Maintains history of all refinements
- **File Input/Output**: Read prompts from files and automatically save outputs
- **Markdown Comparison**: Generates color-coded markdown files comparing original vs refined prompts
- **Error Handling**: Stops immediately on API errors to prevent wasting tokens

### How It Works

1. User provides an initial prompt
2. Both models (OpenAI and Gemini) refine the prompt in parallel
3. The hub selects the best refinement and updates the current prompt
4. Both models evaluate whether the prompt is "good enough"
5. If both models accept, the process stops
6. Otherwise, the loop continues with the refined prompt
7. Maximum iterations prevent infinite loops

### Getting Started

1. Install dependencies: `poetry install`
2. Configure API keys in `.env` file
3. Run: `poetry run python -m promptizer.main "Your prompt here"`

For detailed instructions, see the [How-To Guide](how-to.md).

## Architecture Highlights

### Components

- **RefinementHub**: Central controller managing state and iterations
- **OpenAIClient**: Handles OpenAI API interactions
- **GeminiClient**: Handles Google Gemini API interactions
- **PromptRefinementOrchestrator**: Main orchestrator coordinating the process

### Data Models

- **RefinementRequest**: Request sent to models for refinement
- **RefinementResponse**: Response from models with refined prompt and evaluation
- **HubState**: Central state tracking all refinement history

### Convergence Strategy

The system converges when:
1. Both models independently respond with "ACCEPTED" status
2. Maximum iterations are reached (safety mechanism)

## API Reference

### Main Entry Point

```python
from promptizer.orchestrator import PromptRefinementOrchestrator

orchestrator = PromptRefinementOrchestrator()
final_prompt, state_summary = await orchestrator.refine(
    "Your initial prompt",
    verbose=True
)
```

### Configuration

Environment variables in `.env`:
- `OPENAI_API_KEY`: Required
- `GOOGLE_API_KEY`: Required
- `OPENAI_MODEL`: Optional (default: `gpt-4`)
- `GEMINI_MODEL`: Optional (default: `gemini-1.5-flash`)
- `MAX_ITERATIONS`: Optional (default: `10`)

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests on GitHub.

## License

MIT License

