"""Testing for Stakeholder Agent"""

import asyncio
from qualifyai.agents import StakeholderAgent

# Sample leads
good_lead = {
    "company_name": "TechFlow Inc",
    "decision_maker": "Sarah Chen",
    "decision_maker_title": "VP Engineering",
    "champion": "Mike Torres",
    "champion_title": "Platform Engineering Director",
    "champion_engagement": "High - actively pushing for our solution",
    "blockers": "None"
}

bad_lead = {
    "company_name": "Ruby Ltd",
    "decision_maker": "David Park",
    "decision_maker_title": "CTO",
    "champion": "Tom Richards",
    "champion_title": "Junior Software Engineer (2 years exp)",
    "champion_engagement": "Low - interested but no influence",
    "blockers": "CFO imposed budget freeze until Q3, CTO has existing relationship with competitor (attended their conference)"
}


async def main():
    agent = StakeholderAgent()

    print("Testing Stakeholder Agent")

    print("\n--- Good Lead (Strong Champion) ---")
    print(f"Decision Maker: {good_lead['decision_maker']} ({good_lead['decision_maker_title']})")
    print(f"Champion: {good_lead['champion']} ({good_lead['champion_title']})")
    print(f"Engagement: {good_lead['champion_engagement']}")

    result = await agent.evaluate(good_lead)
    print(f"\nScore: {result['score']}")
    print(f"Recommendation: {result['recommendation']}")
    print(f"\nAnalysis:\n{result['reasoning']}")

    print("\n" + "="*60)

    print("\n--- Bad Lead (No Champion, Blockers) ---")
    print(f"Decision Maker: {bad_lead['decision_maker']}")
    print(f"Champion: {bad_lead['champion']}")
    print(f"Blockers: {bad_lead['blockers']}")

    result = await agent.evaluate(bad_lead)
    print(f"\nScore: {result['score']}")
    print(f"Recommendation: {result['recommendation']}")
    print(f"\nAnalysis:\n{result['reasoning']}")


if __name__ == "__main__":
    asyncio.run(main())
