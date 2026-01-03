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


class BudgetAgent(Agent):
    """
    Budget Agent.
    Evaluates: Budget signals, financial capacity.
    Rule based implementation.
    """

    def __init__(self):
        super().__init__("Budget Agent")

    async def evaluate(self, lead_data: dict) -> dict:
        """Evaluate budget signals and capacity."""

        score = 50  # Base / threshold score
        reasons = []

        # Check budget
        budget = lead_data.get("budget", 0)
        if budget >= 100000:
            score += 30
            reasons.append(f"Strong budget signal: ${budget:,}")
        elif budget >= 50000:
            score += 20
            reasons.append(f"Moderate budget: ${budget:,}")
        elif budget > 0:
            score += 10
            reasons.append(f"Limited budget: ${budget:,}")
        else:
            reasons.append("No budget information provided")

        # Check funding stage
        funding = lead_data.get("funding_stage", "").lower()
        if funding in ["series c", "series d", "ipo"]:
            score += 20
            reasons.append(f"Strong funding stage: {funding}")
        elif funding in ["series a", "series b"]:
            score += 10
            reasons.append(f"Growth stage funding: {funding}")
        elif funding:
            reasons.append(f"Early stage: {funding}")

        # Cap score at 100 (safety guard)
        score = min(score, 100)

        recommendation = "PROCEED" if score >= 70 else "REJECT"

        return {
            "agent": self.name,
            "score": score,
            "reasoning": ". ".join(reasons) if reasons else "Insufficient budget information",
            "recommendation": recommendation
        }
