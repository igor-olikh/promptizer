# Creating a GitHub Release

## Manual Release Creation

To create a release on GitHub:

1. Go to: https://github.com/igor-olikh/promptizer/releases/new

2. Select the tag: `v0.1.0`

3. Release title: `v0.1.0 - Initial Public Release`

4. Description (copy from `.github/release-notes.md` or use the following):

```markdown
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

Comprehensive documentation available in the `docs/` folder.

## 📝 License

MIT License - see LICENSE file for details
```

5. Check "Set as the latest release"

6. Click "Publish release"

## Using GitHub CLI (gh)

Alternatively, you can use GitHub CLI:

```bash
gh release create v0.1.0 \
  --title "v0.1.0 - Initial Public Release" \
  --notes-file .github/release-notes.md \
  --latest
```

