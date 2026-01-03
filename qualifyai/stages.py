"""Stage implementations with decision logic."""

import asyncio
from .agents import (
    ICPAgent, BudgetAgent, MarketIntelAgent,
    CompetitionAgent, StakeholderAgent, TechnicalFitAgent,
    RiskAgent, ResourceAgent, StrategyAgent
)


class Stage:
    """Base stage class."""

    def __init__(self, name: str, agents: list):
        self.name = name
        self.agents = agents  # Must be exactly 3

    async def evaluate(self, lead_data: dict) -> dict:
        """Run all 3 agents in parallel and make decision."""
        raise NotImplementedError


class Stage1(Stage):
    """
    Stage 1: Fit Assessment
    Question: Is this lead a good fit for our product?
    Decision Rule: PROCEED if ALL three agents score >= 70
    """

    def __init__(self):
        agents = [ICPAgent(), BudgetAgent(), MarketIntelAgent()]
        super().__init__("Fit Assessment", agents)

    async def evaluate(self, lead_data: dict) -> dict:
        """Run all 3 agents in parallel and check if ALL scored >= 70."""
        # Run agents in parallel
        results = await asyncio.gather(*[agent.evaluate(lead_data) for agent in self.agents])

        # Get all scores
        scores = [r["score"] for r in results]

        # Decision: ALL must be >= 70
        all_pass = all(score >= 70 for score in scores)
        decision = "PROCEED" if all_pass else "REJECT"

        # Build reasoning
        score_parts = [f"{r['agent']}: {r['score']}" for r in results]
        reasoning = f"Scores: {', '.join(score_parts)}. "

        if all_pass:
            reasoning += "All agents scored >= 70."
        else:
            failed = [r["agent"] for r in results if r["score"] < 70]
            reasoning += f"Failed agents (< 70): {', '.join(failed)}."

        return {
            "stage": self.name,
            "decision": decision,
            "agent_results": results,
            "reasoning": reasoning
        }


class Stage2(Stage):
    """
    Stage 2: Win Probability Assessment
    Question: Can we win this deal?
    Decision Rule: PROCEED if average score >= 75 AND no individual score < 60
    """

    def __init__(self):
        agents = [CompetitionAgent(), StakeholderAgent(), TechnicalFitAgent()]
        super().__init__("Win Probability", agents)

    async def evaluate(self, lead_data: dict) -> dict:
        """Run all 3 agents in parallel. PROCEED if average >= 75 AND min >= 60."""
        # Run agents in parallel
        results = await asyncio.gather(*[agent.evaluate(lead_data) for agent in self.agents])

        # Calculate average and minimum
        scores = [r["score"] for r in results]
        avg_score = sum(scores) / len(scores)
        min_score = min(scores)

        # Decision: avg >= 75 AND min >= 60
        decision = "PROCEED" if (avg_score >= 75 and min_score >= 60) else "REJECT"

        # Build reasoning
        score_parts = [f"{r['agent']}: {r['score']}" for r in results]
        reasoning = f"Scores: {', '.join(score_parts)}. Avg: {avg_score:.1f}, Min: {min_score}. "

        if decision == "PROCEED":
            reasoning += "Passed (avg >= 75, min >= 60)."
        else:
            reasoning += "Failed: "
            if avg_score < 75:
                reasoning += f"avg {avg_score:.1f} < 75. "
            if min_score < 60:
                reasoning += f"min {min_score} < 60."

        return {
            "stage": self.name,
            "decision": decision,
            "agent_results": results,
            "reasoning": reasoning
        }


class Stage3(Stage):
    """
    Stage 3: Strategy & Execution Assessment
    Question: Do we have a clear path to close?
    Decision Rule: QUALIFIED if risk_level <= MEDIUM AND resource_score >= 70 AND strategy_score >= 70
    """

    def __init__(self):
        agents = [RiskAgent(), ResourceAgent(), StrategyAgent()]
        super().__init__("Strategy & Execution", agents)

    async def evaluate(self, lead_data: dict) -> dict:
        """Run all 3 agents. QUALIFIED if risk <= MEDIUM AND resource >= 70 AND strategy >= 70."""
        # Run agents in parallel
        results = await asyncio.gather(*[agent.evaluate(lead_data) for agent in self.agents])

        # Extract scores (RiskAgent, ResourceAgent, StrategyAgent)
        risk_level = results[0].get("risk_level", "HIGH")
        resource_score = results[1]["score"]
        strategy_score = results[2]["score"]

        # Decision: risk OK AND resource >= 70 AND strategy >= 70
        risk_ok = risk_level in ["LOW", "MEDIUM"]
        decision = "QUALIFIED" if (risk_ok and resource_score >= 70 and strategy_score >= 70) else "REJECT"

        # Build reasoning
        reasoning = f"Risk: {risk_level}, Resource: {resource_score}, Strategy: {strategy_score}. "

        if decision == "QUALIFIED":
            reasoning += "All criteria met."
        else:
            issues = []
            if not risk_ok:
                issues.append(f"risk {risk_level} too high")
            if resource_score < 70:
                issues.append(f"resource {resource_score} < 70")
            if strategy_score < 70:
                issues.append(f"strategy {strategy_score} < 70")
            reasoning += f"Failed: {', '.join(issues)}."

        return {
            "stage": self.name,
            "decision": decision,
            "agent_results": results,
            "reasoning": reasoning
        }
