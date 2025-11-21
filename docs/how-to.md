# How-To Guide

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/igor-olikh/promptizer.git
cd promptizer

# Install dependencies
poetry install

# Create .env file
cp .env.example .env
```

### 2. Configuration

Edit the `.env` file and add your API keys:

```bash
OPENAI_API_KEY=sk-your-openai-key-here
GOOGLE_API_KEY=your-google-api-key-here
```

**Getting API Keys:**

- **OpenAI**: Sign up at https://platform.openai.com/ and create an API key
- **Google Gemini**: Get your API key from https://makersuite.google.com/app/apikey

### 3. Basic Usage

#### Command Line

```bash
# Run with a prompt as argument
poetry run python -m promptizer.main "Write a blog post about AI"

# Or run interactively
poetry run python -m promptizer.main
# Then enter your prompt when prompted
```

#### Python Script

```python
import asyncio
from promptizer.orchestrator import PromptRefinementOrchestrator

async def main():
    orchestrator = PromptRefinementOrchestrator()
    final_prompt, summary = await orchestrator.refine(
        "Write a blog post about AI",
        verbose=True
    )
    print(f"\nFinal prompt: {final_prompt}")

asyncio.run(main())
```

## Advanced Usage

### Custom Configuration

You can customize the system behavior via environment variables:

```bash
# Use different models
OPENAI_MODEL=gpt-3.5-turbo
GEMINI_MODEL=gemini-pro-vision

# Set maximum iterations
MAX_ITERATIONS=15
```

### Programmatic Usage

```python
from promptizer.orchestrator import PromptRefinementOrchestrator
from promptizer.config import Config

# Customize config before creating orchestrator
Config.MAX_ITERATIONS = 20
Config.OPENAI_MODEL = "gpt-4-turbo-preview"

orchestrator = PromptRefinementOrchestrator()
final_prompt, state = await orchestrator.refine(
    "Your prompt here",
    verbose=False  # Disable verbose output
)
```

### Accessing Refinement History

```python
from promptizer.hub import RefinementHub
from promptizer.orchestrator import PromptRefinementOrchestrator

orchestrator = PromptRefinementOrchestrator()

# After refinement, you can access the hub's state
# Note: This requires modifying the orchestrator to expose the hub
# For now, the state_summary provides key information
final_prompt, state_summary = await orchestrator.refine("Your prompt")

print(f"Iterations: {state_summary['iteration']}")
print(f"OpenAI accepted: {state_summary['openai_accepted']}")
print(f"Gemini accepted: {state_summary['gemini_accepted']}")
```

## Understanding the Output

### Verbose Mode

When `verbose=True`, you'll see:

```
Starting refinement process...
Original prompt: Write a blog post about AI

============================================================
Iteration 1
============================================================
Running OpenAI and Gemini refinements in parallel...

OpenAI Response:
  Status: NEEDS_IMPROVEMENT
  Reasoning: The prompt lacks specificity about target audience...
  Refined prompt: Write a comprehensive, engaging blog post about artificial intelligence...

Gemini Response:
  Status: NEEDS_IMPROVEMENT
  Reasoning: The prompt could benefit from more context...
  Refined prompt: Create a well-researched blog post about AI that...

Hub State:
  Current prompt: [merged/selected prompt]
  OpenAI accepted: False
  Gemini accepted: False

============================================================
Iteration 2
============================================================
...

============================================================
REFINEMENT COMPLETE
============================================================
Final prompt: [final refined prompt]

Total iterations: 3
Convergence reason: Both models accepted the prompt
```

### State Summary

The `state_summary` dictionary contains:

```python
{
    "iteration": 3,  # Number of iterations completed
    "current_prompt": "...",  # Final refined prompt
    "openai_accepted": True,  # Whether OpenAI accepted
    "gemini_accepted": True,  # Whether Gemini accepted
    "is_converged": True,  # Whether both models agreed
    "convergence_reason": "Both models accepted the prompt",
    "refinement_count": 6  # Total number of refinements (2 per iteration)
}
```

## Troubleshooting

### API Key Errors

**Error**: `Configuration error: OPENAI_API_KEY is not set`

**Solution**: Make sure your `.env` file exists and contains valid API keys.

### JSON Parsing Errors

**Error**: `Failed to parse JSON response`

**Solution**: This is handled automatically - the system will use the previous prompt and continue. If it persists, try:
- Using a different model
- Checking your API quota/limits
- Verifying your API keys are valid

### Infinite Loop Prevention

The system automatically stops after `MAX_ITERATIONS` (default: 10). If you need more iterations:

```bash
# In .env file
MAX_ITERATIONS=20
```

### Model Not Responding

If one model fails, the system continues with the other model's response. Check:
- API key validity
- API quota/rate limits
- Network connectivity
- Model availability

## Best Practices

1. **Start with Clear Prompts**: Even though the system refines prompts, starting with a clear intent helps
2. **Monitor Iterations**: Use verbose mode to understand how prompts evolve
3. **Set Appropriate Limits**: Adjust `MAX_ITERATIONS` based on your needs
4. **Handle Errors**: Always check the `state_summary` for convergence status
5. **Save Results**: Store the final prompt and refinement history for analysis

## Examples

### Example 1: Simple Prompt Refinement

```python
import asyncio
from promptizer.orchestrator import PromptRefinementOrchestrator

async def refine():
    orchestrator = PromptRefinementOrchestrator()
    final, _ = await orchestrator.refine("Write code", verbose=True)
    return final

result = asyncio.run(refine())
```

**Output Evolution:**
- Iteration 1: "Write code" → "Write clean, well-documented code"
- Iteration 2: → "Write clean, well-documented code in Python with error handling"
- Iteration 3: → Both models accept

### Example 2: Complex Prompt

```python
final_prompt, summary = await orchestrator.refine(
    "Create a marketing campaign",
    verbose=True
)
```

The system will refine this to include:
- Target audience
- Campaign objectives
- Key messages
- Success metrics
- Timeline

## Integration Examples

### Flask Web Application

```python
from flask import Flask, request, jsonify
from promptizer.orchestrator import PromptRefinementOrchestrator
import asyncio

app = Flask(__name__)

@app.route('/refine', methods=['POST'])
def refine_prompt():
    data = request.json
    prompt = data.get('prompt', '')
    
    orchestrator = PromptRefinementOrchestrator()
    final, summary = asyncio.run(
        orchestrator.refine(prompt, verbose=False)
    )
    
    return jsonify({
        'refined_prompt': final,
        'summary': summary
    })
```

### Batch Processing

```python
import asyncio
from promptizer.orchestrator import PromptRefinementOrchestrator

prompts = [
    "Write a story",
    "Create a recipe",
    "Design a logo"
]

async def process_all():
    orchestrator = PromptRefinementOrchestrator()
    results = []
    
    for prompt in prompts:
        final, summary = await orchestrator.refine(prompt, verbose=False)
        results.append({
            'original': prompt,
            'refined': final,
            'iterations': summary['iteration']
        })
    
    return results

results = asyncio.run(process_all())
```

## Performance Tips

1. **Use Async Properly**: The system already uses async - don't block the event loop
2. **Batch Processing**: Process multiple prompts sequentially to avoid rate limits
3. **Cache Results**: Store refined prompts to avoid re-processing
4. **Monitor API Usage**: Track your API calls to manage costs

## Security Considerations

1. **Never Commit .env**: The `.env` file is in `.gitignore` - keep it that way
2. **Rotate API Keys**: Regularly rotate your API keys
3. **Use Environment Variables**: In production, use secure environment variable management
4. **Rate Limiting**: Implement rate limiting if building a web service

## Getting Help

- Check the [Architecture Documentation](architecture.md) for system details
- Review the code comments for implementation details
- Open an issue on GitHub for bugs or feature requests

