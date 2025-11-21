# System Architecture

## Overview

Promptizer is a collaborative prompt refinement system that leverages two independent Large Language Models (OpenAI GPT-4 and Google Gemini) to iteratively improve user-provided prompts until both models agree on the quality.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Input                               │
│                    (Initial Prompt)                              │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    RefinementHub                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  State Management:                                        │  │
│  │  - Current prompt                                         │  │
│  │  - Iteration counter                                      │  │
│  │  - Refinement history                                     │  │
│  │  - Convergence flags                                      │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────┬───────────────────────────────┬────────────────────┘
             │                               │
             │ RefinementRequest             │ RefinementRequest
             │                               │
             ▼                               ▼
┌─────────────────────────┐    ┌─────────────────────────┐
│   OpenAI Client         │    │   Gemini Client         │
│                         │    │                         │
│  - GPT-4 Model          │    │  - Gemini Pro Model     │
│  - Async API Calls      │    │  - Async API Calls      │
│  - JSON Response        │    │  - JSON Response        │
└──────────┬──────────────┘    └──────────┬──────────────┘
           │                               │
           │ RefinementResponse            │ RefinementResponse
           │                               │
           └───────────────┬───────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Hub Processes Responses                       │
│  - Updates current prompt                                       │
│  - Checks convergence (both models accepted?)                   │
│  - Checks max iterations                                        │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
                    ┌────────────────┐
                    │  Converged?    │
                    └────┬───────┬───┘
                         │       │
                    Yes  │       │  No
                         │       │
                         ▼       ▼
              ┌──────────────┐  ┌──────────────┐
              │   Return     │  │   Continue   │
              │ Final Prompt │  │   Loop       │
              └──────────────┘  └──────────────┘
```

## Component Details

### 1. RefinementHub (Central Controller)

The hub is the central orchestrator that:
- Maintains the current state of the refinement process
- Creates refinement requests for each model
- Processes responses from both models
- Determines when to stop the iteration loop
- Tracks convergence status

**Key Responsibilities:**
- State management (current prompt, iteration count, history)
- Request generation for each model
- Response processing and state updates
- Convergence detection
- Loop control

### 2. OpenAI Client

Handles all interactions with the OpenAI API:
- Sends refinement requests to GPT-4
- Parses JSON responses
- Handles errors gracefully
- Returns structured `RefinementResponse` objects

**API Details:**
- Model: Configurable (default: `gpt-4`)
- Response Format: JSON object
- Temperature: 0.7 (for creative but consistent refinements)
- Error Handling: Raises exceptions immediately on errors

### 3. Gemini Client

Handles all interactions with the Google Gemini API:
- Sends refinement requests to Gemini Pro
- Parses JSON responses (handles markdown-wrapped JSON)
- Handles errors gracefully
- Returns structured `RefinementResponse` objects

**API Details:**
- Model: Configurable (default: `gemini-1.5-flash`)
- Response Format: JSON object (extracted from text)
- Error Handling: Raises exceptions immediately on errors

### 4. PromptRefinementOrchestrator

The main orchestrator that:
- Coordinates the entire refinement process
- Manages the iteration loop
- Runs both model refinements concurrently
- Provides verbose output for monitoring

## Data Flow

### Iteration Flow

1. **Initialization**: Hub is created with the initial prompt
2. **Request Creation**: Hub creates `RefinementRequest` objects for both models
3. **Parallel Execution**: Both models refine the prompt concurrently
4. **Response Processing**: Hub processes both responses and updates state
5. **Convergence Check**: Hub checks if both models accepted
6. **Loop Control**: If not converged and under max iterations, repeat from step 2
7. **Termination**: Return final prompt when converged or max iterations reached

### Message Exchange Format

#### RefinementRequest
```json
{
  "prompt": "string - current prompt to refine",
  "iteration": "integer - current iteration number",
  "previous_refinements": ["string - array of previous prompts"],
  "model_type": "openai | gemini"
}
```

#### RefinementResponse
```json
{
  "refined_prompt": "string - improved prompt",
  "evaluation_status": "ACCEPTED | NEEDS_IMPROVEMENT | REJECTED",
  "reasoning": "string - explanation of changes",
  "model_type": "openai | gemini",
  "timestamp": "datetime - when response was generated"
}
```

## Convergence Detection

The system stops iterating when:

1. **Both Models Accept**: Both OpenAI and Gemini respond with `ACCEPTED` status
2. **Max Iterations Reached**: Prevents infinite loops (default: 10 iterations)

The convergence logic ensures:
- Both models independently evaluate the prompt
- No single model can force termination
- System has a safety mechanism to prevent infinite loops

## Error Handling

The system implements immediate error stopping to prevent wasting tokens:

- **API Errors**: Both clients raise exceptions immediately on API errors (no fallback responses)
- **Model Not Found**: Raises `ModelNotFoundError` with helpful suggestions
- **JSON Parsing Errors**: Raises `APIError` to stop the process
- **Network Errors**: Raises `APIError` to stop the process
- **Configuration Errors**: System validates API keys before starting
- **Exception Propagation**: Errors are caught in the orchestrator and re-raised to stop immediately

**Error Types:**
- `APIError`: General API errors
- `ModelNotFoundError`: Specific error for 404/model not found errors

The main entry point provides user-friendly error messages with suggestions for fixing issues.

## Performance Considerations

- **Asynchronous Processing**: Both model API calls run in parallel using `asyncio.gather()`
- **Concurrent Refinement**: Each iteration processes both models simultaneously
- **Efficient State Management**: Only stores last 3 refinements in request history

## Output Generation

The system generates multiple output formats:

1. **Text Output**: Refined prompt saved to `[filename] output.txt`
2. **Markdown Comparison**: Color-coded markdown file `[filename].md` containing:
   - Summary statistics
   - Original prompt (yellow/amber background)
   - Refined prompt (green background)
   - Side-by-side comparison table
   - Refinement details

The markdown files use HTML styling for visual distinction and work in most markdown viewers (GitHub, VS Code, etc.).

## File Input/Output

The system supports:
- Reading prompts from files (automatic detection)
- Writing outputs to corresponding files
- Generating markdown comparison files
- Working with both relative and absolute paths
- Default `prompt/` folder for file operations

## Extensibility

The system is designed to be extensible:
- Easy to add new model providers
- Configurable evaluation criteria
- Pluggable convergence strategies
- Customizable iteration limits
- Custom output formatters

