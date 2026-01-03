"""Testing for Market Intelligence Agent"""

import sys
sys.path.insert(0, '..')

import asyncio
from qualifyai.agents import MarketIntelAgent

# Sample leads
good_lead = {
    "company_name": "TechFlow Inc",
    "industry": "B2B SaaS",
    "market_position": "Market leader in DevOps tools",
    "growth_rate": "11% YoY"
}

bad_lead = {
    "company_name": "Haris Pizza Shop",
    "industry": "Food & Beverage",
    "market_position": "Local shop",
    "growth_rate": "Flat"
}


async def main():
    agent = MarketIntelAgent()

    print("Testing Market Intelligence Agent")

    print("\n--- Good Lead ---")
    print(f"Lead: {good_lead['company_name']}")
    print(f"Industry: {good_lead['industry']}")
    print(f"Market Position: {good_lead['market_position']}")

    result = await agent.evaluate(good_lead)
    print(f"\nScore: {result['score']}")
    print(f"Recommendation: {result['recommendation']}")
    print(f"\nAnalysis:\n{result['reasoning']}")

    print("\n" + "="*60)

    print("\n--- Bad Lead ---")
    print(f"Lead: {bad_lead['company_name']}")
    print(f"Industry: {bad_lead['industry']}")

    result = await agent.evaluate(bad_lead)
    print(f"\nScore: {result['score']}")
    print(f"Recommendation: {result['recommendation']}")
    print(f"\nAnalysis:\n{result['reasoning']}")


if __name__ == "__main__":
    asyncio.run(main())
