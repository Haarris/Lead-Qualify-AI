"""Testing for Budget Agent"""

import asyncio
from qualifyai.agents import BudgetAgent

# Sample leads
good_lead = {
    "company_name": "TechFlow Inc",
    "budget": 150000,  # $150K
    "funding_stage": "Series C"
}

bad_lead = {
    "company_name": "Haris Pizza Shop",
    "budget": 5000,  # $5K
    "funding_stage": "Bootstrapped"
}


async def main():
    agent = BudgetAgent()

    print("Testing Budget Agent")

    print("\n--- Good Lead ---")
    print(f"Lead: {good_lead['company_name']}")
    print(f"Budget: ${good_lead['budget']:,}")
    print(f"Funding: {good_lead['funding_stage']}")

    result = await agent.evaluate(good_lead)
    print(f"\nResult:")
    print(f"Score: {result['score']}")
    print(f"Recommendation: {result['recommendation']}")
    print(f"Reasoning: {result['reasoning']}")

    print("\n--- Bad Lead ---")
    print(f"Lead: {bad_lead['company_name']}")
    print(f"Budget: ${bad_lead['budget']:,}")
    print(f"Funding: {bad_lead['funding_stage']}")

    result = await agent.evaluate(bad_lead)
    print(f"\nResult:")
    print(f"Score: {result['score']}")
    print(f"Recommendation: {result['recommendation']}")
    print(f"Reasoning: {result['reasoning']}")


if __name__ == "__main__":
    asyncio.run(main())
