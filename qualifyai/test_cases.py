"""
5 Test Cases:
1. Perfect Lead → QUALIFIED
2. Stage 1 Rejection (poor ICP/budget)
3. Stage 2 Rejection (low win probability)
4. Stage 3 Rejection (high risk)
5. Borderline Pass → QUALIFIED
"""

# Test Case 1: Perfect Lead - Should QUALIFY
perfect_lead = {
    # Stage 1: Fit
    "company_name": "TechFlow Inc",
    "industry": "B2B SaaS",
    "employee_count": 500,
    "annual_revenue": 50000000,
    "budget": 150000,
    "funding_stage": "Series C",
    "growth_rate": "18% YoY",
    "market_position": "Market leader in DevOps tools",

    # Stage 2: Win Probability
    "competitors": [],
    "current_solution": "None",
    "satisfaction_with_current": "",
    "our_advantage": "Strong AI capabilities and unique integration",
    "decision_maker": "Sarah Chen",
    "decision_maker_title": "VP Engineering",
    "champion": "Mike Torres",
    "champion_title": "Platform Engineering Director",
    "champion_engagement": "High - actively pushing for our solution",
    "blockers": "None",
    "tech_stack": ["AWS", "Kubernetes", "Docker", "Python", "React"],
    "integration_complexity": "Low",

    # Stage 3: Strategy
    "budget_freeze": False,
    "recent_layoffs": False,
    "competitor_relationship": False,
    "has_champion": True,
    "deal_size": 150000,
    "timeline": "Q2 decision required",
    "implementation_complexity": "Low",
    "stakeholders": [
        "Sarah Chen (VP Engineering) - Decision maker, data-driven",
        "Mike Torres (Platform Director) - Champion, pushing for our solution",
        "Jennifer Liu (Security Director) - Needs compliance validation",
        "David Park (CTO) - Final sign-off for deals >$100K"
    ]
}

# Test Case 2: Stage 1 Rejection - Poor ICP fit
stage1_reject = {
    # Stage 1: Bad fit
    "company_name": "Haris Pizza Shop",
    "industry": "Food & Beverage",
    "employee_count": 15,
    "annual_revenue": 50000,
    "budget": 5000,
    "funding_stage": "Bootstrapped",
    "growth_rate": "Flat",
    "market_position": "Local shop",

    # Stage 2 (won't reach)
    "competitors": [],
    "current_solution": "None",
    "satisfaction_with_current": "",
    "our_advantage": "",
    "decision_maker": "Haris Farooq",
    "decision_maker_title": "Owner",
    "champion": "None",
    "champion_title": "",
    "champion_engagement": "None",
    "blockers": "None",
    "tech_stack": [],
    "integration_complexity": "High",

    # Stage 3 (won't reach)
    "budget_freeze": False,
    "recent_layoffs": False,
    "competitor_relationship": False,
    "has_champion": False,
    "deal_size": 5000,
    "timeline": "Unknown",
    "implementation_complexity": "High",
    "stakeholders": []
}

# Test Case 3: Stage 2 Rejection - Low win probability
# Good fit but can't win: Ruby Ltd with competitor issues
stage2_reject = {
    # Stage 1: Good fit (passes)
    "company_name": "Ruby Ltd",
    "industry": "Enterprise Software",
    "employee_count": 2000,
    "annual_revenue": 100000000,
    "budget": 200000,
    "funding_stage": "Series D",
    "growth_rate": "12% YoY",
    "market_position": "Industry leader",

    # Stage 2: Poor win probability
    "competitors": ["CircleCI", "GitHub Actions", "Jenkins"],
    "current_solution": "Jenkins",
    "satisfaction_with_current": "High",
    "our_advantage": "",
    "decision_maker": "David Park",
    "decision_maker_title": "CTO",
    "champion": "Tom Richards",
    "champion_title": "Junior Software Engineer (2 years exp)",
    "champion_engagement": "Low - interested but no influence",
    "blockers": "CFO imposed budget freeze until Q3, CTO has existing relationship with competitor",
    "tech_stack": ["Azure", ".NET"],
    "integration_complexity": "High",

    # Stage 3 (won't reach)
    "budget_freeze": True,
    "recent_layoffs": False,
    "competitor_relationship": True,
    "has_champion": False,
    "deal_size": 200000,
    "timeline": "No timeline",
    "implementation_complexity": "High",
    "stakeholders": [
        "David Park (CTO) - Has competitor relationship",
        "Tom Richards (Junior Engineer) - No influence"
    ]
}

# Test Case 4: Stage 3 Rejection - High risk
# Good fit, can win, but too risky
stage3_reject = {
    # Stage 1: Good fit (passes)
    "company_name": "NewTech Inc",
    "industry": "FinTech",
    "employee_count": 300,
    "annual_revenue": 30000000,
    "budget": 100000,
    "funding_stage": "Series B",
    "growth_rate": "15% YoY",
    "market_position": "Fast-growing challenger",

    # Stage 2: Good win probability (passes)
    "competitors": [],
    "current_solution": "Manual process",
    "satisfaction_with_current": "Low",
    "our_advantage": "Strong automation features",
    "decision_maker": "Jane Smith",
    "decision_maker_title": "VP Operations",
    "champion": "Alex Johnson",
    "champion_title": "Engineering Manager",
    "champion_engagement": "High",
    "blockers": "None",
    "tech_stack": ["AWS", "Python", "Docker", "Kubernetes"],
    "integration_complexity": "Low",

    # Stage 3: High risk (fails)
    "budget_freeze": True,
    "recent_layoffs": True,
    "competitor_relationship": True,
    "has_champion": False,
    "deal_size": 600000,
    "timeline": "Urgent - need ASAP",
    "implementation_complexity": "High",
    "stakeholders": [
        "Jane Smith (VP Ops) - Interested but cautious",
        "Tom Richards (VP Finance) - Blocking all new spend"
    ]
}

# Test Case 5: Borderline Pass - Just meets thresholds
borderline_pass = {
    # Stage 1: Just passes (scores around 70)
    "company_name": "MidTech Solutions",
    "industry": "Technology",
    "employee_count": 150,
    "annual_revenue": 15000000,
    "budget": 60000,
    "funding_stage": "Series A",
    "growth_rate": "10% YoY",
    "market_position": "Established mid-market player",

    # Stage 2: Just passes (avg ~75, min ~60)
    "competitors": ["CircleCI"],
    "current_solution": "Basic tool",
    "satisfaction_with_current": "Medium",
    "our_advantage": "Better integration capabilities",
    "decision_maker": "Robert Kim",
    "decision_maker_title": "Director of Engineering",
    "champion": "Lisa Wang",
    "champion_title": "Senior Engineer",
    "champion_engagement": "Medium - supportive but not driving",
    "blockers": "Minor budget review required",
    "tech_stack": ["AWS", "Docker"],
    "integration_complexity": "Medium",

    # Stage 3: Just passes
    "budget_freeze": False,
    "recent_layoffs": False,
    "competitor_relationship": False,
    "has_champion": True,
    "deal_size": 60000,
    "timeline": "Q3 decision",
    "implementation_complexity": "Medium",
    "stakeholders": [
        "Robert Kim (Director) - Decision maker",
        "Lisa Wang (Sr Engineer) - Champion"
    ]
}

# All test cases with expected outcomes
TEST_CASES = {
    "perfect": {"data": perfect_lead, "expected": "QUALIFIED"},
    "stage1_reject": {"data": stage1_reject, "expected": "REJECTED at Fit Assessment"},
    "stage2_reject": {"data": stage2_reject, "expected": "REJECTED at Win Probability"},
    "stage3_reject": {"data": stage3_reject, "expected": "REJECTED at Strategy & Execution"},
    "borderline": {"data": borderline_pass, "expected": "QUALIFIED"}
}
