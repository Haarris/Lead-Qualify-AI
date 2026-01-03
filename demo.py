"""
Demo script for QualifyAI Lead Qualification System.
Runs all 5 test cases through the pipeline.
"""

import asyncio
import sys
from qualifyai.stages import Stage1, Stage2, Stage3
from qualifyai.pipeline import LeadQualifyPipeline
from qualifyai.test_cases import TEST_CASES


async def run_single_case(name: str, lead_data: dict, expected: str):
    """Run a single test case through the pipeline."""
    print(f"\n{'#'*60}")
    print(f"TEST CASE: {name.upper()}")
    print(f"Company: {lead_data['company_name']}")
    print(f"Expected: {expected}")
    print('#'*60)

    # Create pipeline with 3 stages
    pipeline = LeadQualifyPipeline([Stage1(), Stage2(), Stage3()])
    result = await pipeline.qualify(lead_data)

    print(f"\n{'='*60}")
    print("FINAL RESULT")
    print('='*60)
    print(f"Decision: {result['final_decision']}")
    print(f"Summary: {result['summary']}")

    return result


async def run_all_cases():
    """Run all test cases and show summary."""
    results = {}

    for name, case in TEST_CASES.items():
        result = await run_single_case(name, case["data"], case["expected"])
        results[name] = {
            "decision": result["final_decision"],
            "expected": case["expected"],
            "rejected_at": result.get("rejected_at_stage")
        }

    # Print summary
    print(f"\n\n{'='*60}")
    print("SUMMARY OF ALL TEST CASES")
    print('='*60)
    print(f"{'Case':<20} {'Expected':<25} {'Actual':<15}")
    print('-'*60)

    for name, res in results.items():
        actual = res["decision"]
        if res["rejected_at"]:
            actual += f" at {res['rejected_at']}"
        print(f"{name:<20} {res['expected']:<25} {actual:<15}")


async def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        # Run specific case
        case_name = sys.argv[1]
        if case_name in TEST_CASES:
            case = TEST_CASES[case_name]
            await run_single_case(case_name, case["data"], case["expected"])
        else:
            print(f"Unknown case: {case_name}")
            print(f"Available: {', '.join(TEST_CASES.keys())}")
    else:
        # Run all cases
        await run_all_cases()


if __name__ == "__main__":
    asyncio.run(main())
