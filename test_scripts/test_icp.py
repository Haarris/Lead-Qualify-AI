"""Testing for ICP agent"""

import sys
sys.path.insert(0, '..')

import asyncio
from qualifyai.agents import ICPAgent

# Sample lead data (good and bad)
good_lead = {
    "company_name": "Techflow Inc",
    "industry": "B2B SaaS",
    "employee_count": 500,
    "annual_revenue": 50000000  # $50M
}

bad_lead = {
    "company_name": "Haris Pizza Shop",
    "industry": "Food & Beverage",
    "employee_count": 15,
    "annual_revenue": 50000  # $50K
}


async def main():
    agent = ICPAgent()

    print("Testing ICP Agent")

    print("\n--- Good Lead ---")
    print(f"Lead: {good_lead['company_name']}")
    print(f"Industry: {good_lead['industry']}")
    print(f"Employees: {good_lead['employee_count']}")
    print(f"Revenue: ${good_lead['annual_revenue']:,}")

    result = await agent.evaluate(good_lead)
    print(f"\nResult:")
    print(f"Score: {result['score']}")
    print(f"Recommendation: {result['recommendation']}")
    print(f"Reasoning: {result['reasoning']}")

    print("\n--- Bad Lead (Should REJECT) ---")
    print(f"Lead: {bad_lead['company_name']}")
    print(f"Industry: {bad_lead['industry']}")
    print(f"Employees: {bad_lead['employee_count']}")
    print(f"Revenue: ${bad_lead['annual_revenue']:,}")

    result = await agent.evaluate(bad_lead)
    print(f"\nResult:")
    print(f"Score: {result['score']}")
    print(f"Recommendation: {result['recommendation']}")
    print(f"Reasoning: {result['reasoning']}")


if __name__ == "__main__":
    asyncio.run(main())
