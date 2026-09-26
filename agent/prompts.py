def build_prompt(research, score):
    return f"""
Create personalized B2B outreach using ONLY the evidence below.

Company: {research["company_name"]}
Industry: {research["industry"]}
Size: {research["size"]}
Description: {research["description"]}
Pain points: {research["pain_points"]}
Evidence: {research["evidence"]}
ICP score: {score}/10

Return exactly:
1) A concise cold email with subject line
2) ---
3) A concise LinkedIn message

Do not invent people, revenue, customers, technologies, or company facts.
""".strip()
