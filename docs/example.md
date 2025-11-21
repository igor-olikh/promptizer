# Example: Complete Refinement Process

This document shows a complete example of how Promptizer refines a prompt from start to finish.

## Input

**Initial Prompt:**
```
Write code
```

## Iteration 1

### OpenAI Response
**Status:** `NEEDS_IMPROVEMENT`

**Reasoning:**
"The prompt 'Write code' is extremely vague and lacks essential details. It doesn't specify the programming language, the purpose of the code, the problem to solve, or any requirements. A good prompt should include context, desired functionality, and constraints."

**Refined Prompt:**
```
Write clean, well-documented code in Python that solves a specific problem. Include error handling, type hints, and a brief explanation of the approach.
```

### Gemini Response
**Status:** `NEEDS_IMPROVEMENT`

**Reasoning:**
"The original prompt is too generic. It needs to specify what kind of code, for what purpose, and what the expected outcome should be. Adding language, purpose, and quality requirements would significantly improve it."

**Refined Prompt:**
```
Create a Python function that implements a specific algorithm or solves a particular problem. The code should be production-ready with proper error handling, documentation, and follow best practices.
```

### Hub Decision
The hub selects the more detailed prompt (OpenAI's version) as the current prompt.

**Current Prompt:** OpenAI's refined version

---

## Iteration 2

### OpenAI Response
**Status:** `NEEDS_IMPROVEMENT`

**Reasoning:**
"While the prompt now includes language and quality requirements, it still lacks specificity about the actual problem to solve. A truly effective prompt should either specify a concrete problem or ask the user to provide one, along with expected inputs/outputs and edge cases to consider."

**Refined Prompt:**
```
Write clean, well-documented Python code that solves a specific problem. The code should include:
- Clear function signatures with type hints
- Comprehensive error handling for edge cases
- Docstrings explaining the approach and parameters
- Example usage demonstrating the functionality
- Consideration of time/space complexity where relevant

Please specify the problem you want to solve, or if this is a general template, indicate what type of problem (e.g., data processing, algorithm implementation, API integration).
```

### Gemini Response
**Status:** `NEEDS_IMPROVEMENT`

**Reasoning:**
"The prompt is better but could be more structured. It should explicitly request the problem statement and provide a clear template for what the response should include. Adding structure and specific deliverables would make it more actionable."

**Refined Prompt:**
```
Develop a Python solution for a specific programming problem. Your implementation should:

1. Problem Statement: Clearly define what problem you're solving
2. Solution Approach: Explain your algorithm or method
3. Code Implementation: Provide complete, runnable code with:
   - Type hints for all functions
   - Error handling for invalid inputs
   - Comprehensive docstrings
   - Unit test examples
4. Complexity Analysis: Discuss time and space complexity
5. Usage Examples: Show how to use the code with sample inputs

Specify the exact problem you need solved, or describe the domain (e.g., data structures, web scraping, machine learning).
```

### Hub Decision
The hub selects Gemini's more structured version.

**Current Prompt:** Gemini's refined version

---

## Iteration 3

### OpenAI Response
**Status:** `ACCEPTED`

**Reasoning:**
"This prompt is now comprehensive and well-structured. It clearly outlines what is expected, provides a logical flow (problem → approach → implementation → analysis → examples), and includes all necessary elements for producing high-quality code. The prompt is specific enough to guide the developer while remaining flexible enough to accommodate various problem types."

**Refined Prompt:** (Same as current - no changes needed)

### Gemini Response
**Status:** `ACCEPTED`

**Reasoning:**
"The prompt now has excellent structure and clarity. It provides a clear framework for code development, includes all essential components (problem definition, approach, implementation, testing, analysis), and gives enough guidance without being overly prescriptive. This is a high-quality prompt that should produce excellent results."

**Refined Prompt:** (Same as current - no changes needed)

### Hub Decision
**Both models have accepted!** The refinement process is complete.

---

## Final Output

**Final Refined Prompt:**
```
Develop a Python solution for a specific programming problem. Your implementation should:

1. Problem Statement: Clearly define what problem you're solving
2. Solution Approach: Explain your algorithm or method
3. Code Implementation: Provide complete, runnable code with:
   - Type hints for all functions
   - Error handling for invalid inputs
   - Comprehensive docstrings
   - Unit test examples
4. Complexity Analysis: Discuss time and space complexity
5. Usage Examples: Show how to use the code with sample inputs

Specify the exact problem you need solved, or describe the domain (e.g., data structures, web scraping, machine learning).
```

**Summary:**
- **Total Iterations:** 3
- **Total Refinements:** 6 (2 per iteration)
- **Convergence Reason:** Both models accepted the prompt
- **Improvement:** The prompt evolved from a 2-word vague request to a comprehensive, structured prompt with clear requirements and deliverables

## Key Observations

1. **Progressive Refinement:** Each iteration built upon the previous one, adding more structure and detail
2. **Collaborative Improvement:** Both models contributed different perspectives that were merged
3. **Convergence:** Both models independently reached the conclusion that the prompt was sufficient
4. **Quality Improvement:** The final prompt is significantly more actionable and comprehensive than the original

## Another Example: Marketing Campaign

### Input
```
Create a marketing campaign
```

### Final Output (After 4 iterations)
```
Develop a comprehensive marketing campaign strategy with the following components:

1. Campaign Objectives: Define specific, measurable goals (e.g., brand awareness, lead generation, sales conversion)
2. Target Audience: Identify and describe the primary and secondary audience segments with demographics, psychographics, and behavioral insights
3. Key Messages: Craft 2-3 core messages that resonate with the target audience and align with brand values
4. Marketing Channels: Select appropriate channels (social media, email, content marketing, paid advertising, etc.) with rationale
5. Content Strategy: Outline content types, themes, and formats for each channel
6. Timeline and Milestones: Create a detailed schedule with key dates and deliverables
7. Budget Allocation: Estimate costs for each channel and activity
8. Success Metrics: Define KPIs and measurement methods (engagement rates, conversion rates, ROI, etc.)
9. Risk Assessment: Identify potential challenges and mitigation strategies
10. Implementation Plan: Provide actionable steps for execution

Specify the product/service, industry, and any specific constraints or requirements for the campaign.
```

This example shows how the system can handle different types of prompts and adapt the refinement approach accordingly.

