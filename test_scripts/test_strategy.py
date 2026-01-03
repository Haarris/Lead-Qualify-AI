"""Testing for Strategy Agent"""

import sys
sys.path.insert(0, '..')

import asyncio
from qualifyai.agents import StrategyAgent

# Sample leads
good_lead = {
    "company_name": "TechFlow Inc",
    "deal_size": 150000,
    "timeline": "Q2 decision required",
    "decision_maker": "Sarah Chen",
    "decision_maker_title": "VP Engineering",
    "champion": "Mike Torres (Platform Director) - enthusiastic, has budget influence",
    "blockers": "None significant",
    "competitors": [],
    "stakeholders": [
        "Sarah Chen (VP Engineering) - Decision maker, data-driven",
        "Mike Torres (Platform Director) - Champion, pushing for our solution",
        "Jennifer Liu (Security Director) - Needs compliance validation",
        "David Park (CTO) - Final sign-off for deals >$100K"
    ]
}

bad_lead = {
    "company_name": "Ruby Ltd",
    "deal_size": 500000,
    "timeline": "Unclear - maybe next year",
    "decision_maker": "Unknown",
    "decision_maker_title": "Unknown",
    "champion": "None identified",
    "blockers": "Budget freeze until Q4, CTO attended competitor conference, no executive sponsor",
    "competitors": ["Competitor A", "Competitor B"],
    "stakeholders": [
        "Tom Richards (VP Finance) - Blocking all new spend",
        "Haris Farooq - Has competitor relationship"
    ]
}


async def main():
    agent = StrategyAgent()

    print("Testing Strategy Agent")

    print("\n--- Good Lead (Clear Path) ---")
    print(f"Company: {good_lead['company_name']}")
    print(f"Decision Maker: {good_lead['decision_maker']}")
    print(f"Champion: {good_lead['champion']}")
    print(f"Blockers: {good_lead['blockers']}")

    result = await agent.evaluate(good_lead)
    print(f"\nScore: {result['score']}")
    print(f"Recommendation: {result['recommendation']}")
    print(f"\nStrategy:\n{result['reasoning']}")

    print("\n" + "="*60)

    print("\n--- Bad Lead (No Clear Path) ---")
    print(f"Company: {bad_lead['company_name']}")
    print(f"Decision Maker: {bad_lead['decision_maker']}")
    print(f"Blockers: {bad_lead['blockers']}")

    result = await agent.evaluate(bad_lead)
    print(f"\nScore: {result['score']}")
    print(f"Recommendation: {result['recommendation']}")
    print(f"\nStrategy:\n{result['reasoning']}")


if __name__ == "__main__":
    asyncio.run(main())
