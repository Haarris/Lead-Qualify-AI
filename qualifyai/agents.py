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


class MarketIntelAgent(Agent):
    """
    Market Intelligence Agent.
    Evaluates: Market position, competitive landscape, industry trends.
    Uses LLM (OpenAI API).
    """

    def __init__(self):
        super().__init__("Market Intelligence Agent")

    async def evaluate(self, lead_data: dict) -> dict:
        """Analyze market position."""

        prompt = f"""Evaluate this prospect's market fit. Score each criterion and sum for total.

PROSPECT DATA:
- Industry: {lead_data.get('industry', 'Unknown')}
- Growth Rate: {lead_data.get('growth_rate', 'Unknown')}
- Market Position: {lead_data.get('market_position', 'Unknown')}

Scoring sheet (max 100 points):

1. INDUSTRY ALIGNMENT (0-40 points):
   - Exact match (B2B SaaS, Technology, FinTech, Enterprise Software): 40 pts
   - Related tech industry (Healthcare Tech, EdTech, etc.): 25 pts
   - Non-tech but uses software heavily: 15 pts
   - Non-tech/traditional industry: 0 pts

2. GROWTH RATE (0-35 points):
   - 15%+ YoY growth: 35 pts
   - 10-14% YoY growth: 25 pts
   - 5-9% YoY growth: 15 pts
   - Below 5% or flat/declining: 0 pts

3. MARKET POSITION (0-25 points):
   - Market leader or dominant player: 25 pts
   - Strong challenger or fast-growing: 20 pts
   - Established mid-market player: 15 pts
   - Small/local/niche player: 5 pts

Provide your evaluation:
- State points awarded for each criterion with brief justification
- Calculate total score
- End with: MARKET_FIT_SCORE: [total]/100"""

        try:
            response = await call_llm(prompt)

            # Extract score from response
            score = 50  # Base / threshold scor
            score_match = re.search(r'MARKET_FIT_SCORE:\s*(\d+)', response)
            if score_match:
                score = min(int(score_match.group(1)), 100)

            recommendation = "PROCEED" if score >= 70 else "REJECT"

            return {
                "agent": self.name,
                "score": score,
                "reasoning": response,
                "recommendation": recommendation
            }
        except Exception as e:
            return {
                "agent": self.name,
                "score": 50,
                "reasoning": f"Error during evaluation: {str(e)}",
                "recommendation": "REJECT"
            }


# Stage 2: Win Probability Assessment Agents
class CompetitionAgent(Agent):
    """
    Competition Agent.
    Evaluates: Competitors in deal, positioning, differentiation.
    Rule based implementation.
    """

    def __init__(self):
        super().__init__("Competition Agent")

    async def evaluate(self, lead_data: dict) -> dict:
        """Evaluate competitors in deal."""

        score = 70  # Base score
        reasons = []

        # Check number of competitors
        competitors = lead_data.get("competitors", [])
        num_competitors = len(competitors)

        if num_competitors == 0:
            score += 20
            reasons.append("No known competitors")
        elif num_competitors == 1:
            score += 5
            reasons.append(f"Single competitor: {competitors[0]}")
        else:
            score -= 10
            reasons.append(f"Multiple competitors ({num_competitors}): {', '.join(competitors)}")

        # Check current solution and satisfaction
        current_solution = lead_data.get("current_solution", "").lower()
        satisfaction = lead_data.get("satisfaction_with_current", "").lower()

        if not current_solution or current_solution == "none":
            score += 15
            reasons.append("No current solution in place")
        else:
            # They have something, check satisfaction factor
            if satisfaction == "low":
                score += 10
                reasons.append(f"Using {lead_data.get('current_solution')} but unhappy. Open to switch")
            elif satisfaction == "medium":
                score -= 5
                reasons.append(f"Using {lead_data.get('current_solution')} with moderate satisfaction")
            elif satisfaction == "high":
                score -= 20
                reasons.append(f"Happy with {lead_data.get('current_solution')}. Hard to displace")

        # Check our competitive advantage
        our_advantage = lead_data.get("our_advantage", "").lower()
        if "strong" in our_advantage or "unique" in our_advantage:
            score += 15
            reasons.append(f"Strong differentiation: {lead_data.get('our_advantage')}")
        elif our_advantage:
            score += 5
            reasons.append(f"Some differentiation: {lead_data.get('our_advantage')}")

        # Cap score
        score = max(0, min(score, 100))

        recommendation = "PROCEED" if score >= 70 else "REJECT"

        return {
            "agent": self.name,
            "score": score,
            "reasoning": ". ".join(reasons) if reasons else "Insufficient competitive information",
            "recommendation": recommendation
        }


class StakeholderAgent(Agent):
    """
    Stakeholder Agent.
    Evaluates: Decision-makers, champion strength, organizational dynamics.
    Uses LLM (OpenAI API).
    """

    def __init__(self):
        super().__init__("Stakeholder Agent")

    async def evaluate(self, lead_data: dict) -> dict:
        """Analyze stakeholder dynamics and champion strength."""

        prompt = f"""Analyze the stakeholder dynamics for this deal. Score each criterion and sum for total.

STAKEHOLDER DATA:
- Decision Maker: {lead_data.get('decision_maker', 'Unknown')}
- Decision Maker Title: {lead_data.get('decision_maker_title', 'Unknown')}
- Champion: {lead_data.get('champion', 'None')}
- Champion Title: {lead_data.get('champion_title', 'Unknown')}
- Champion Engagement: {lead_data.get('champion_engagement', 'Unknown')}
- Known Blockers: {lead_data.get('blockers', 'None')}

SCORING RUBRIC (max 100 points):

1. CHAMPION STRENGTH (0-40 points):
   - Strong champion with budget authority: 40 pts
   - Engaged champion without direct authority: 30 pts
   - Weak or passive champion: 15 pts
   - No identified champion: 0 pts

2. DECISION MAKER ACCESS (0-40 points):
   - Direct access to final decision maker: 40 pts
   - Access through champion: 30 pts
   - Indirect access only: 15 pts
   - No access identified: 0 pts

3. BLOCKER RISK (0-20 points):
   - No known blockers: 20 pts
   - Minor blockers (can be managed): 10 pts
   - Significant blockers present: 5 pts
   - Strong opposition identified: 0 pts

Provide brief analysis for each criterion with points awarded.
End with: CHAMPION_STRENGTH_SCORE: [total]/100"""

        try:
            response = await call_llm(prompt)

            # Extract score from response
            score = 50
            score_match = re.search(r'CHAMPION_STRENGTH_SCORE:\s*(\d+)', response)
            if score_match:
                score = min(int(score_match.group(1)), 100)

            recommendation = "PROCEED" if score >= 70 else "REJECT"

            return {
                "agent": self.name,
                "score": score,
                "reasoning": response,
                "recommendation": recommendation
            }
        except Exception as e:
            return {
                "agent": self.name,
                "score": 50,
                "reasoning": f"Error during evaluation: {str(e)}",
                "recommendation": "REJECT"
            }
