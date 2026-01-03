"""Testing for Resource Agent"""

import sys
sys.path.insert(0, '..')

import asyncio
from qualifyai.agents import ResourceAgent

# Sample leads
good_lead = {
    "company_name": "TechFlow Inc",
    "deal_size": 100000,
    "implementation_complexity": "Low",
    "timeline": "Q4 implementation"
}

bad_lead = {
    "company_name": "Ruby Ltd",
    "deal_size": 750000,
    "implementation_complexity": "High",
    "timeline": "Urgent"
}


async def main():
    agent = ResourceAgent()

    print("Testing Resource Agent")

    print("\n--- Good Lead (Standard Resources) ---")
    print(f"Deal Size: ${good_lead['deal_size']:,}")
    print(f"Complexity: {good_lead['implementation_complexity']}")

    result = await agent.evaluate(good_lead)
    print(f"\nScore: {result['score']}")
    print(f"Resources Needed: {result['resource_requirements']}")
    print(f"Recommendation: {result['recommendation']}")

    print("\n--- Bad Lead (Resource Heavy) ---")
    print(f"Deal Size: ${bad_lead['deal_size']:,}")
    print(f"Complexity: {bad_lead['implementation_complexity']}")
    print(f"Timeline: {bad_lead['timeline']}")

    result = await agent.evaluate(bad_lead)
    print(f"\nScore: {result['score']}")
    print(f"Resources Needed: {result['resource_requirements']}")
    print(f"Recommendation: {result['recommendation']}")


if __name__ == "__main__":
    asyncio.run(main())
