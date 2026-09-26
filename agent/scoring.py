def score_lead(research):
    score = 4

    industry = research["industry"].lower()
    if any(x in industry for x in ["technology", "software", "saas", "fintech"]):
        score += 2

    if research["size"] in ["51-200", "201-500", "500+"]:
        score += 2
    elif research["size"] == "20-50":
        score += 1

    if len(research["pain_points"]) >= 2:
        score += 1

    return min(score, 10)
