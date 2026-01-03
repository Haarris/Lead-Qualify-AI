"""Test full qualification pipeline"""

import sys
sys.path.insert(0, '..')

import asyncio
from qualifyai.pipeline import LeadQualifyPipeline
from qualifyai.stages import Stage1, Stage2, Stage3

test_lead = {
    # Stage 1: Fit Assessment
    "company_name": "TechFlow Inc",
    "industry": "B2B SaaS",
    "employee_count": 500,
    "annual_revenue": 50000000,
    "budget": 150000,
    "funding_stage": "Series C",
    "growth_rate": "11% YoY",
    "market_position": "Market leader in DevOps tools",

    # Stage 2: Win Probability
    "competitors": [],
    "current_solution": "None",
    "satisfaction_with_current": "",
    "our_advantage": "Strong AI capabilities",
    "decision_maker": "Sarah Chen",
    "decision_maker_title": "VP Engineering",
    "champion": "Mike Torres",
    "champion_title": "Platform Director",
    "champion_engagement": "High",
    "blockers": "None",
    "tech_stack": ["AWS", "Kubernetes", "Docker", "Python"],
    "integration_complexity": "Low",

    # Stage 3: Strategy & Execution
    "budget_freeze": False,
    "recent_layoffs": False,
    "competitor_relationship": False,
    "has_champion": True,
    "deal_size": 150000,
    "timeline": "Q2 decision",
    "implementation_complexity": "Low",
    "stakeholders": [
        "Sarah Chen (VP Engineering) - Decision maker",
        "Mike Torres (Platform Director) - Champion"
    ]
}


async def main():
    # Create stages
    stages = [Stage1(), Stage2(), Stage3()]

    # Create pipeline
    pipeline = LeadQualifyPipeline(stages)

    print("Lead qualification test")
    print(f"Company: {test_lead['company_name']}")
    print(f"Industry: {test_lead['industry']}")
    print(f"Deal Size: ${test_lead['deal_size']:,}")

    result = await pipeline.qualify(test_lead)

    print("Final qualification result")
    print(f"Decision: {result['final_decision']}")
    print(f"Summary: {result['summary']}")

    if result['rejected_at_stage']:
        print(f"Rejected at: {result['rejected_at_stage']}")


if __name__ == "__main__":
    asyncio.run(main())
