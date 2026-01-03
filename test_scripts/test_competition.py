"""Testing for Competition Agent"""

import sys
sys.path.insert(0, '..')

import asyncio
from qualifyai.agents import CompetitionAgent

# Sample leads
good_lead = {
    "company_name": "TechFlow Inc",
    "competitors": [],
    "current_solution": "None",
    "satisfaction_with_current": "",
    "our_advantage": "Strong AI capabilities and unique integration"
}

bad_lead = {
    "company_name": "Ruby Ltd",
    "competitors": ["CircleCI", "GitHub Actions"],
    "current_solution": "Jenkins",
    "satisfaction_with_current": "High",
    "our_advantage": ""
}


async def main():
    agent = CompetitionAgent()

    print("Testing Competition Agent")

    print("\n--- Good Lead ---")
    print(f"Competitors: {good_lead['competitors']}")
    print(f"Our Advantage: {good_lead['our_advantage']}")

    result = await agent.evaluate(good_lead)
    print(f"\nScore: {result['score']}")
    print(f"Recommendation: {result['recommendation']}")
    print(f"Reasoning: {result['reasoning']}")

    print("\n--- Bad Lead ---")
    print(f"Competitors: {bad_lead['competitors']}")

    result = await agent.evaluate(bad_lead)
    print(f"\nScore: {result['score']}")
    print(f"Recommendation: {result['recommendation']}")
    print(f"Reasoning: {result['reasoning']}")


if __name__ == "__main__":
    asyncio.run(main())
