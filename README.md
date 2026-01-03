# Lead-Qualify-AI
AI-powered lead qualification system

## 1. Setup Instructions

### Creating and activating virtual environment
python3.10 -m venv venv
source venv/bin/activate

### Installing requirements:
pip install -r requirements.txt

- **LLM Key::** Add the OpenAI key in config.yml (cfg/config.yml)

## 2. Architecture Overview

**3 Stages (sequential):**
- Stage 1 - Fit Assessment: ICPAgent, BudgetAgent, MarketIntelAgent
- Stage 2 - Win Probability: CompetitionAgent, StakeholderAgent, TechnicalFitAgent
- Stage 3 - Strategy & Execution: RiskAgent, ResourceAgent, StrategyAgent

Agents within each stage run in parallel. Pipeline stops at first rejection.

## 3. Design Decisions

- **Hybrid agents:** 4 LLM-based (nuanced judgment) + 5 rule-based (deterministic, faster)
- **Early exit:** Stops at first stage rejection to save API calls
- **Consistent scoring:** All agents output 0-100 scores

## 4. Running the System

```bash
# Run full demo with all 5 test cases
python demo.py

# Run specific test case
python demo.py perfect         # Perfect lead - QUALIFIED
python demo.py stage1_reject   # Poor ICP fit - REJECTED at Stage 1
python demo.py stage2_reject   # Low win probability - REJECTED at Stage 2
python demo.py stage3_reject   # High risk - REJECTED at Stage 3
python demo.py borderline      # Just passes - QUALIFIED

# Test individual agents (run from test_scripts folder)
cd test_scripts
python test_icp.py
python test_budget.py
python test_market.py
python test_competition.py
python test_stakeholder.py
python test_technical.py
python test_risk.py
python test_resource.py
python test_strategy.py

# Test full pipeline
python test_pipeline.py
```

## 5. Example Output

```
==================================================
Running Fit Assessment...
==================================================
Decision: PROCEED
Reasoning: Scores: ICP Agent: 95, Budget Agent: 100, Market Intelligence Agent: 100. All agents scored >= 70.

==================================================
Running Win Probability...
==================================================
Decision: PROCEED
Reasoning: Scores: Competition Agent: 100, Stakeholder Agent: 80, Technical Fit Agent: 100. Avg: 93.3, Min: 80. Passed (avg >= 75, min >= 60).

==================================================
Running Strategy & Execution...
==================================================
Decision: QUALIFIED
Reasoning: Risk: LOW, Resource: 80, Strategy: 85. All criteria met.

============================================================
FINAL RESULT
============================================================
Decision: QUALIFIED
Summary: Lead passed all stages and is qualified.
```

## 6. Assumptions & Limitations

### Assumptions:
- Lead data is provided in the expected dictionary format with all required fields.
- OpenAI API key is valid and has sufficient credits / quota.
- Budget and revenue values are in USD.

### Limitations & Improvements:
- LLM based agents may produce slightly different scores across runs due to model non determinism. (Still have tried to cater with a low temperature value).
- No persistent storage. Currently all results are in memory only. 
- CLI interface only. No web UI or API endpoints.
- Prompts / Response caching can be implemented to save API calls. 

