"""Testing for Risk Agent"""

import sys
sys.path.insert(0, '..')

import asyncio
from qualifyai.agents import RiskAgent

# Sample leads
good_lead = {
    "company_name": "TechFlow Inc",
    "budget_freeze": False,
    "recent_layoffs": False,
    "competitor_relationship": False,
    "timeline": "Q2 decision",
    "has_champion": True,
    "deal_size": 100000
}

bad_lead = {
    "company_name": "Ruby Ltd",
    "budget_freeze": True,
    "recent_layoffs": True,
    "competitor_relationship": True,
    "timeline": "Urgent - need ASAP",
    "has_champion": False,
    "deal_size": 750000
}


async def main():
    agent = RiskAgent()

    print("Testing Risk Agent")

    print("\n--- Good Lead (Low Risk) ---")
    print(f"Budget Freeze: {good_lead['budget_freeze']}")
    print(f"Recent Layoffs: {good_lead['recent_layoffs']}")
    print(f"Has Champion: {good_lead['has_champion']}")

    result = await agent.evaluate(good_lead)
    print(f"\nScore: {result['score']}")
    print(f"Risk Level: {result['risk_level']}")
    print(f"Concerns: {result['concerns']}")
    print(f"Recommendation: {result['recommendation']}")

    print("\n--- Bad Lead (High Risk) ---")
    print(f"Budget Freeze: {bad_lead['budget_freeze']}")
    print(f"Recent Layoffs: {bad_lead['recent_layoffs']}")
    print(f"Competitor Relationship: {bad_lead['competitor_relationship']}")
    print(f"Timeline: {bad_lead['timeline']}")

    result = await agent.evaluate(bad_lead)
    print(f"\nScore: {result['score']}")
    print(f"Risk Level: {result['risk_level']}")
    print(f"Concerns: {result['concerns']}")
    print(f"Recommendation: {result['recommendation']}")


if __name__ == "__main__":
    asyncio.run(main())
