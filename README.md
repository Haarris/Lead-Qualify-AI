# Lead-Qualify-AI
AI-powered lead qualification system

# LLM Key
Add the OpenAI key in config.yml (cfg/config.yml)

# Creating and activating virtual environment
python3.10 -m venv venv
source venv/bin/activate

# Installing requirements:
pip install -r requirements.txt


## Stage 1 Agents: 
# Testing ICP Agent
python test_icp.py

# Testing Budget Agent 
python test_budget.py

# Testing Market Intelligence Agent 
python test_market.py

## Stage 2 Agents
# Testing Competition Agent
python test_competition.py

# Testing Stakeholder Agent
python test_stakeholder.py