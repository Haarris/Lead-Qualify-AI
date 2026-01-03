"""Testing for Technical Fit Agent"""

import sys
sys.path.insert(0, '..')

import asyncio
from qualifyai.agents import TechnicalFitAgent

# Sample leads
good_lead = {
    "company_name": "TechFlow Inc",
    "tech_stack": ["AWS", "Kubernetes", "Docker", "Python", "React"],
    "integration_complexity": "Low",
    "technical_requirements": "Need security and compliance features"
}

bad_lead = {
    "company_name": "Ruby Ltd",
    "tech_stack": ["Java", "Azure"],
    "integration_complexity": "High",
    "technical_requirements": "Must integrate with legacy mainframe systems"
}


async def main():
    agent = TechnicalFitAgent()

    print("Testing Technical Fit Agent")

    print("\n--- Good Lead (Modern Stack) ---")
    print(f"Tech Stack: {good_lead['tech_stack']}")
    print(f"Complexity: {good_lead['integration_complexity']}")
    print(f"Requirements: {good_lead['technical_requirements']}")

    result = await agent.evaluate(good_lead)
    print(f"\nScore: {result['score']}")
    print(f"Recommendation: {result['recommendation']}")
    print(f"Reasoning: {result['reasoning']}")

    print("\n--- Bad Lead (Legacy Stack) ---")
    print(f"Tech Stack: {bad_lead['tech_stack']}")
    print(f"Complexity: {bad_lead['integration_complexity']}")
    print(f"Requirements: {bad_lead['technical_requirements']}")

    result = await agent.evaluate(bad_lead)
    print(f"\nScore: {result['score']}")
    print(f"Recommendation: {result['recommendation']}")
    print(f"Reasoning: {result['reasoning']}")


if __name__ == "__main__":
    asyncio.run(main())
