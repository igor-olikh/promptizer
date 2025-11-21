# Prompt Refinement Comparison

## Summary

- **Iterations**: 1
- **Status**: ✅ Converged
- **Convergence Reason**: Both models accepted the prompt
- **Total Refinements**: 2
- **OpenAI Accepted**: ✅ Yes
- **Gemini Accepted**: ✅ Yes

---

## 📝 Original Prompt

<div style="background-color: #fff3cd; padding: 20px; border-left: 5px solid #ffc107; border-radius: 5px; margin: 15px 0;">

**Original Prompt (Before Refinement)**

<pre style="white-space: pre-wrap; word-wrap: break-word; margin: 10px 0; font-family: 'Courier New', monospace; font-size: 14px; line-height: 1.6;">You are an expert at refining prompts to make them clearer, more specific, and more effective.

Your task is to:
1. Analyze the given prompt
2. Improve it by enhancing clarity, specificity, removing ambiguity, and ensuring completeness
3. Evaluate whether the prompt is &quot;good enough&quot; based on:
   - Clarity: Is the prompt clear and easy to understand?
   - Specificity: Does it provide enough detail?
   - Lack of ambiguity: Are there multiple interpretations possible?
   - Completeness: Does it cover all necessary aspects?
   - Alignment with user intent: Does it capture what the user likely wants?

After refining, you must respond in the following JSON format:
{
    &quot;refined_prompt&quot;: &quot;your improved prompt here&quot;,
    &quot;evaluation_status&quot;: &quot;ACCEPTED&quot; or &quot;NEEDS_IMPROVEMENT&quot;,
    &quot;reasoning&quot;: &quot;explanation of your changes and evaluation&quot;
}

Respond with &quot;ACCEPTED&quot; only if the prompt is truly excellent and needs no further improvement.
Respond with &quot;NEEDS_IMPROVEMENT&quot; if there are still areas that could be enhanced.</pre>

</div>

---

## ✨ Refined Prompt

<div style="background-color: #d4edda; padding: 20px; border-left: 5px solid #28a745; border-radius: 5px; margin: 15px 0;">

**Refined Prompt (After Refinement)**

<pre style="white-space: pre-wrap; word-wrap: break-word; margin: 10px 0; font-family: 'Courier New', monospace; font-size: 14px; line-height: 1.6;">You are tasked with refining prompts to improve their clarity, specificity, and effectiveness. Please follow these steps: 1. Analyze the provided prompt for clarity and effectiveness. 2. Enhance the prompt by making it clearer, more specific, and complete while removing any ambiguity. 3. Evaluate the revised prompt based on the following criteria: - Clarity: Is the prompt easy to understand? - Specificity: Does it contain sufficient detail? - Ambiguity: Is there any potential for multiple interpretations? - Completeness: Does it address all necessary aspects? - Alignment with user intent: Does it fulfill the user's likely objectives? After refining, respond in the specified JSON format: { &quot;refined_prompt&quot;: &quot;your improved prompt here&quot;, &quot;evaluation_status&quot;: &quot;ACCEPTED&quot; or &quot;NEEDS_IMPROVEMENT&quot;, &quot;reasoning&quot;: &quot;your explanation here&quot; }. Indicate &quot;ACCEPTED&quot; only if the prompt is excellent and requires no further improvements; otherwise, use &quot;NEEDS_IMPROVEMENT&quot; if further enhancements are possible.</pre>

</div>

---

## 📊 Side-by-Side Comparison

<table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
<tr>
<th style="width: 50%; background-color: #fff3cd; padding: 15px; border: 2px solid #ffc107; text-align: left;">Original Prompt</th>
<th style="width: 50%; background-color: #d4edda; padding: 15px; border: 2px solid #28a745; text-align: left;">Refined Prompt</th>
</tr>
<tr>
<td style="padding: 15px; vertical-align: top; border: 2px solid #ffc107; background-color: #fffbf0;">
<pre style="white-space: pre-wrap; word-wrap: break-word; margin: 0; font-family: 'Courier New', monospace; font-size: 13px; line-height: 1.5;">You are an expert at refining prompts to make them clearer, more specific, and more effective.

Your task is to:
1. Analyze the given prompt
2. Improve it by enhancing clarity, specificity, removing ambiguity, and ensuring completeness
3. Evaluate whether the prompt is &quot;good enough&quot; based on:
   - Clarity: Is the prompt clear and easy to understand?
   - Specificity: Does it provide enough detail?
   - Lack of ambiguity: Are there multiple interpretations possible?
   - Completeness: Does it cover all necessary aspects?
   - Alignment with user intent: Does it capture what the user likely wants?

After refining, you must respond in the following JSON format:
{
    &quot;refined_prompt&quot;: &quot;your improved prompt here&quot;,
    &quot;evaluation_status&quot;: &quot;ACCEPTED&quot; or &quot;NEEDS_IMPROVEMENT&quot;,
    &quot;reasoning&quot;: &quot;explanation of your changes and evaluation&quot;
}

Respond with &quot;ACCEPTED&quot; only if the prompt is truly excellent and needs no further improvement.
Respond with &quot;NEEDS_IMPROVEMENT&quot; if there are still areas that could be enhanced.</pre>
</td>
<td style="padding: 15px; vertical-align: top; border: 2px solid #28a745; background-color: #f0f9f2;">
<pre style="white-space: pre-wrap; word-wrap: break-word; margin: 0; font-family: 'Courier New', monospace; font-size: 13px; line-height: 1.5;">You are tasked with refining prompts to improve their clarity, specificity, and effectiveness. Please follow these steps: 1. Analyze the provided prompt for clarity and effectiveness. 2. Enhance the prompt by making it clearer, more specific, and complete while removing any ambiguity. 3. Evaluate the revised prompt based on the following criteria: - Clarity: Is the prompt easy to understand? - Specificity: Does it contain sufficient detail? - Ambiguity: Is there any potential for multiple interpretations? - Completeness: Does it address all necessary aspects? - Alignment with user intent: Does it fulfill the user's likely objectives? After refining, respond in the specified JSON format: { &quot;refined_prompt&quot;: &quot;your improved prompt here&quot;, &quot;evaluation_status&quot;: &quot;ACCEPTED&quot; or &quot;NEEDS_IMPROVEMENT&quot;, &quot;reasoning&quot;: &quot;your explanation here&quot; }. Indicate &quot;ACCEPTED&quot; only if the prompt is excellent and requires no further improvements; otherwise, use &quot;NEEDS_IMPROVEMENT&quot; if further enhancements are possible.</pre>
</td>
</tr>
</table>

---

*Generated by Promptizer - Collaborative LLM Prompt Refinement System*
