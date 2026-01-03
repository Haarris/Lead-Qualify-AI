"""Agent implementation"""

import json
import re
from .llm_client import call_llm

class Agent:
    """Base agent class for lead qualification."""

    def __init__(self, name: str):
        self.name = name

    async def evaluate(self, lead_data: dict) -> dict:
        """
        Evaluate lead and return analysis.
        Return format can vary by agent type.
        """
        raise NotImplementedError


# Stage 1: Fit Assessment Agents
class ICPAgent(Agent):
    """
    Ideal Customer Profile Agent.
    Evaluates: Company size, industry, basic fit criteria.
    Uses LLM (OpenAI API).
    """

    def __init__(self):
        super().__init__("ICP Agent")

    async def evaluate(self, lead_data: dict) -> dict:
        """Evaluate if lead matches ideal customer profile."""

        prompt = f"""Analyze this lead against our Ideal Customer Profile (ICP).

Our ICP:
- Target Industries: B2B SaaS, Technology, FinTech, Enterprise Software
- Company Size: 100-5,000 employees
- Annual Revenue: $10M+

Lead Information:
- Company: {lead_data.get('company_name', 'Unknown')}
- Industry: {lead_data.get('industry', 'Unknown')}
- Employee Count: {lead_data.get('employee_count', 'Unknown')}
- Annual Revenue: ${lead_data.get('annual_revenue', 'Unknown')}

Evaluate the fit and provide your response in this exact JSON format:
{{
    "score": <0-100>,
    "reasoning": "<explanation of fit assessment>",
    "recommendation": "<PROCEED or REJECT>"
}}

Score guidelines:
- 90-100: Perfect ICP match
- 70-89: Good fit with minor gaps
- 50-69: Moderate fit, some concerns
- Below 50: Poor fit

Return only valid JSON, no other text."""

        try:
            response = await call_llm(prompt)

            # Parse JSON response
            json_match = re.search(r'\{[^{}]*\}', response, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                return {
                    "agent": self.name,
                    "score": result.get("score", 50),
                    "reasoning": result.get("reasoning", "Analysis completed"),
                    "recommendation": result.get("recommendation", "PROCEED" if result.get("score", 0) >= 70 else "REJECT")
                }
        except Exception as e:
            # Fallback on error
            return {
                "agent": self.name,
                "score": 50,
                "reasoning": f"Error during evaluation: {str(e)}",
                "recommendation": "REJECT"
            }

        return {
            "agent": self.name,
            "score": 50,
            "reasoning": "Could not parse LLM response",
            "recommendation": "REJECT"
        }
