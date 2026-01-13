import json
import re
from typing import Dict, Any, Optional
from openai import OpenAI, APIError

class PromptOptimizer:
    def __init__(self, base_url: str = "http://localhost:1234/v1", api_key: str = "lm-studio"):
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.system_prompt = """
You are an expert prompt engineer and optimization engine. Your task is to analyze the user's raw prompt and rewrite it into a highly effective, structured prompt using best practices (CRISPE, Chain-of-Thought).

You MUST return the output in strict JSON format with the following structure:
{
    "elements": {
        "persona": "The persona adopted by the AI",
        "context": "Background information and context",
        "instruction": "The primary task or directive",
        "constraints": "Limitations and strict rules to follow",
        "format": "The desired format of the response",
        "exemplars": "Few-shot examples (input -> output)",
        "tone": "The tone and style of the response",
        "delimiters": "Any specific delimiters to use",
        "data": "Input data or variable placeholders",
        "technique": "The prompting strategy used (e.g. Chain-of-thought, etc)"
    },
    "final_prompt": "The complete, polished, and ready-to-use prompt that combines all elements into a cohesive request."
}

Do not include any conversational text, markdown formatting (like ```json), or explanations outside the JSON object. Just return the JSON.
"""

    def optimize_prompt(self, raw_prompt: str, model: str) -> Dict[str, Any]:
        """
        Sends the raw prompt to the LLM and returns the parsed JSON response.
        """
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"Optimize this prompt:\n\n{raw_prompt}"}
                ],
                temperature=0.7,
            )
            
            content = response.choices[0].message.content
            return self._parse_json_response(content)

        except APIError as e:
            return {"error": f"API Error: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected Error: {str(e)}"}

    def _parse_json_response(self, content: str) -> Dict[str, Any]:
        """
        Robustly parses JSON from the LLM response, handling potential markdown blocks.
        """
        try:
            # 1. Try direct parsing
            return json.loads(content)
        except json.JSONDecodeError:
            # 2. Try to find JSON block if wrapped in markdown
            match = re.search(r'```json\s*(\{.*?\})\s*```', content, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(1))
                except json.JSONDecodeError:
                    pass
            
            # 3. Try to find the first { and last }
            match = re.search(r'(\{.*\})', content, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(1))
                except json.JSONDecodeError:
                    pass
            
            # 4. Fallback: Return raw content structure
            return {
                "elements": {
                    "persona": "Error parsing JSON",
                    "context": "The model response could not be parsed as JSON.",
                    "instruction": "N/A",
                    "constraints": "N/A",
                    "format": "N/A",
                    "exemplars": "N/A",
                    "tone": "N/A",
                    "delimiters": "N/A",
                    "data": "N/A",
                    "technique": "N/A"
                },
                "final_prompt": content  # Return the raw content so the user doesn't lose it
            }

    def get_available_models(self) -> list:
        try:
            models = self.client.models.list()
            return [model.id for model in models.data]
        except Exception:
            return []
