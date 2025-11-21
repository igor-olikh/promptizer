# Release v0.1.0 - Initial Public Release

## 🎉 First Public Release

This is the initial public release of Promptizer, a collaborative LLM system for prompt refinement.

## ✨ Features

- **Collaborative Refinement**: Two LLMs (OpenAI GPT-4 and Google Gemini) work together to improve prompts
- **Automatic Evaluation**: Models independently evaluate prompt quality
- **Convergence Detection**: System stops when both models accept the prompt
- **File Input/Output**: Read prompts from files and automatically save outputs
- **Markdown Comparison**: Generates color-coded markdown files comparing original vs refined prompts
- **Error Handling**: Stops immediately on API errors to prevent wasting tokens
- **Model Listing**: `--list-models` command to see available models
- **Sequential Execution**: Reliable sequential API calls to avoid timeout issues

## 🚀 Quick Start

1. Install dependencies: `poetry install`
2. Configure API keys in `.env` file
3. Run: `poetry run python -m promptizer.main "Your prompt here"`

## 📚 Documentation

Comprehensive documentation available in the `docs/` folder:
- Architecture documentation
- How-to guide
- Example walkthroughs

## 🔧 Configuration

- Supports OpenAI (GPT-4, GPT-3.5-turbo, etc.)
- Supports Google Gemini (gemini-1.5-flash, gemini-1.5-pro, etc.)
- Configurable max iterations
- Customizable model selection

## 🛡️ Security

- All API keys stored in `.env` file (not tracked in git)
- No sensitive data in codebase
- Proper error handling and validation

## 📝 License

MIT License - see LICENSE file for details

