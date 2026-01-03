"""Qualify Pipeline"""

from .stages import Stage1, Stage2, Stage3


class QualifyPipeline:
    """Base pipeline class - Main orchestrator"""

    def __init__(self, stages: list):
        """Initialize with list of Stage objects (must be exactly 3)."""
        self.stages = stages  # Must be exactly 3

    async def qualify(self, lead_data: dict) -> dict:
        """
        Run lead through all stages sequentially.
        Stop at first rejection or complete all stages.

        Returns:
        {
            'final_decision': 'QUALIFIED' or 'REJECTED',
            'rejected_at_stage': str or None,
            'stage_results': [...],
            'summary': str
        }
        """
        raise NotImplementedError


class LeadQualifyPipeline(QualifyPipeline):
    """Runs lead through all stages sequentially."""

    async def qualify(self, lead_data: dict) -> dict:
        """
        Run lead through all stages sequentially.
        Stop at first rejection or complete all the stages.
        """
        stage_results = []
        rejected_at_stage = None

        # Run each stage
        for stage in self.stages:
            print(f"\n{'='*50}")
            print(f"Running {stage.name}...")
            print('='*50)

            result = await stage.evaluate(lead_data)
            stage_results.append(result)

            print(f"Decision: {result['decision']}")
            print(f"Reasoning: {result['reasoning']}")

            # Stop if rejected
            if result["decision"] in ["REJECT", "REJECTED"]:
                rejected_at_stage = stage.name
                break

        # Final decision
        if rejected_at_stage:
            final_decision = "REJECTED"
            summary = f"Lead rejected at {rejected_at_stage}."
        else:
            final_decision = "QUALIFIED"
            summary = "Lead passed all stages and is qualified."

        return {
            "final_decision": final_decision,
            "rejected_at_stage": rejected_at_stage,
            "stage_results": stage_results,
            "summary": summary
        }
