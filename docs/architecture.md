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

### 3. Gemini Client

Handles all interactions with the Google Gemini API:
- Sends refinement requests to Gemini Pro
- Parses JSON responses (handles markdown-wrapped JSON)
- Handles errors gracefully
- Returns structured `RefinementResponse` objects

**API Details:**
- Model: Configurable (default: `gemini-pro`)
- Response Format: JSON object (extracted from text)

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

- **API Errors**: Both clients handle API errors gracefully, returning the current prompt with `NEEDS_IMPROVEMENT` status
- **JSON Parsing Errors**: Clients attempt to extract valid JSON from responses, with fallback handling
- **Network Errors**: Async operations handle timeouts and network issues
- **Configuration Errors**: System validates API keys before starting

## Performance Considerations

- **Asynchronous Processing**: Both model API calls run in parallel using `asyncio.gather()`
- **Concurrent Refinement**: Each iteration processes both models simultaneously
- **Efficient State Management**: Only stores last 3 refinements in request history

## Extensibility

The system is designed to be extensible:
- Easy to add new model providers
- Configurable evaluation criteria
- Pluggable convergence strategies
- Customizable iteration limits

