# Prompt Refinement Comparison

## Summary

- **Iterations**: 3
- **Status**: ✅ Converged
- **Convergence Reason**: Both models accepted the prompt
- **Total Refinements**: 6
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

CRITICAL: You MUST respond with ONLY valid JSON. No text before or after the JSON object.

Required JSON format (you MUST use this exact structure):
{
    &quot;refined_prompt&quot;: &quot;your improved prompt here - escape all quotes and newlines properly&quot;,
    &quot;evaluation_status&quot;: &quot;ACCEPTED&quot;,
    &quot;reasoning&quot;: &quot;brief explanation of your changes and evaluation&quot;
}

JSON RULES:
- Use double quotes for all strings
- Escape all double quotes inside strings with \\&quot;
- Escape all newlines with \\n
- Escape all backslashes with \\\\
- Keep &quot;reasoning&quot; brief (under 200 words) to avoid truncation
- Keep &quot;refined_prompt&quot; concise but complete
- &quot;evaluation_status&quot; must be exactly &quot;ACCEPTED&quot; or &quot;NEEDS_IMPROVEMENT&quot; (no quotes in the value)

Respond with &quot;ACCEPTED&quot; only if the prompt is truly excellent and needs no further improvement.
Respond with &quot;NEEDS_IMPROVEMENT&quot; if there are still areas that could be enhanced.

IMPORTANT: Your response must be valid JSON that can be parsed by json.loads(). Test your JSON before responding.</pre>

</div>

---

## ✨ Refined Prompt

<div style="background-color: #d4edda; padding: 20px; border-left: 5px solid #28a745; border-radius: 5px; margin: 15px 0;">

**Refined Prompt (After Refinement)**

<pre style="white-space: pre-wrap; word-wrap: break-word; margin: 10px 0; font-family: 'Courier New', monospace; font-size: 14px; line-height: 1.6;">You are an expert at refining prompts to make them clearer, more specific, and more effective. Your task is to analyze the given prompt (which is this entire instruction set), improve it by enhancing clarity, specificity, removing ambiguity, and ensuring completeness. Then, evaluate whether the prompt is \&quot;good enough\&quot; based on the following criteria:\n- Clarity: Is the prompt clear and easy to understand?\n- Specificity: Does it provide enough detail?\n- Lack of ambiguity: Are there multiple interpretations possible?\n- Completeness: Does it cover all necessary aspects?\n- Alignment with user intent: Does it capture what the user likely wants?\n\nCRITICAL: You MUST respond with ONLY valid JSON. No text before or after the JSON object.\n\nRequired JSON format (you MUST use this exact structure):\n{\n    \&quot;refined_prompt\&quot;: \&quot;your improved prompt here - escape all quotes and newlines properly\&quot;,\n    \&quot;evaluation_status\&quot;: \&quot;ACCEPTED\&quot;,\n    \&quot;reasoning\&quot;: \&quot;brief explanation of your changes and evaluation\&quot;\n}\n\nJSON RULES:\n- Use double quotes for all strings\n- Escape all double quotes inside strings with \\\&quot;\n- Escape all newlines with \\n- Escape all backslashes with \\\\\\n- Keep \&quot;reasoning\&quot; brief (under 200 words) to avoid truncation\n- Keep \&quot;refined_prompt\&quot; concise but complete\n- \&quot;evaluation_status\&quot; must be exactly \&quot;ACCEPTED\&quot; or \&quot;NEEDS_IMPROVEMENT\&quot; (no quotes in the value)\n\nRespond with \&quot;ACCEPTED\&quot; only if the prompt is truly excellent and needs no further improvement.\nRespond with \&quot;NEEDS_IMPROVEMENT\&quot; if there are still areas that could be enhanced.\n\nIMPORTANT: Your response must be valid JSON that can be parsed by json.loads(). Test your JSON before responding. Respond with a JSON object containing 'refined_prompt', 'evaluation_status', and 'reasoning'. Remember: Respond with ONLY a valid JSON object (no other text). Escape all quotes, newlines, and special characters in the JSON strings.</pre>

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

CRITICAL: You MUST respond with ONLY valid JSON. No text before or after the JSON object.

Required JSON format (you MUST use this exact structure):
{
    &quot;refined_prompt&quot;: &quot;your improved prompt here - escape all quotes and newlines properly&quot;,
    &quot;evaluation_status&quot;: &quot;ACCEPTED&quot;,
    &quot;reasoning&quot;: &quot;brief explanation of your changes and evaluation&quot;
}

JSON RULES:
- Use double quotes for all strings
- Escape all double quotes inside strings with \\&quot;
- Escape all newlines with \\n
- Escape all backslashes with \\\\
- Keep &quot;reasoning&quot; brief (under 200 words) to avoid truncation
- Keep &quot;refined_prompt&quot; concise but complete
- &quot;evaluation_status&quot; must be exactly &quot;ACCEPTED&quot; or &quot;NEEDS_IMPROVEMENT&quot; (no quotes in the value)

Respond with &quot;ACCEPTED&quot; only if the prompt is truly excellent and needs no further improvement.
Respond with &quot;NEEDS_IMPROVEMENT&quot; if there are still areas that could be enhanced.

IMPORTANT: Your response must be valid JSON that can be parsed by json.loads(). Test your JSON before responding.</pre>
</td>
<td style="padding: 15px; vertical-align: top; border: 2px solid #28a745; background-color: #f0f9f2;">
<pre style="white-space: pre-wrap; word-wrap: break-word; margin: 0; font-family: 'Courier New', monospace; font-size: 13px; line-height: 1.5;">You are an expert at refining prompts to make them clearer, more specific, and more effective. Your task is to analyze the given prompt (which is this entire instruction set), improve it by enhancing clarity, specificity, removing ambiguity, and ensuring completeness. Then, evaluate whether the prompt is \&quot;good enough\&quot; based on the following criteria:\n- Clarity: Is the prompt clear and easy to understand?\n- Specificity: Does it provide enough detail?\n- Lack of ambiguity: Are there multiple interpretations possible?\n- Completeness: Does it cover all necessary aspects?\n- Alignment with user intent: Does it capture what the user likely wants?\n\nCRITICAL: You MUST respond with ONLY valid JSON. No text before or after the JSON object.\n\nRequired JSON format (you MUST use this exact structure):\n{\n    \&quot;refined_prompt\&quot;: \&quot;your improved prompt here - escape all quotes and newlines properly\&quot;,\n    \&quot;evaluation_status\&quot;: \&quot;ACCEPTED\&quot;,\n    \&quot;reasoning\&quot;: \&quot;brief explanation of your changes and evaluation\&quot;\n}\n\nJSON RULES:\n- Use double quotes for all strings\n- Escape all double quotes inside strings with \\\&quot;\n- Escape all newlines with \\n- Escape all backslashes with \\\\\\n- Keep \&quot;reasoning\&quot; brief (under 200 words) to avoid truncation\n- Keep \&quot;refined_prompt\&quot; concise but complete\n- \&quot;evaluation_status\&quot; must be exactly \&quot;ACCEPTED\&quot; or \&quot;NEEDS_IMPROVEMENT\&quot; (no quotes in the value)\n\nRespond with \&quot;ACCEPTED\&quot; only if the prompt is truly excellent and needs no further improvement.\nRespond with \&quot;NEEDS_IMPROVEMENT\&quot; if there are still areas that could be enhanced.\n\nIMPORTANT: Your response must be valid JSON that can be parsed by json.loads(). Test your JSON before responding. Respond with a JSON object containing 'refined_prompt', 'evaluation_status', and 'reasoning'. Remember: Respond with ONLY a valid JSON object (no other text). Escape all quotes, newlines, and special characters in the JSON strings.</pre>
</td>
</tr>
</table>

---

*Generated by Promptizer - Collaborative LLM Prompt Refinement System*
