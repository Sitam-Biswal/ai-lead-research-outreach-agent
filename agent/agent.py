import os
import re
from tools.research import research_company
from agent.scoring import score_lead
from agent.prompts import build_prompt

def _llm_generate(research, score):
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        return None

    try:
        from openai import OpenAI
        client = OpenAI(api_key=key)
        prompt = build_prompt(research, score)
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            temperature=0.4,
            messages=[
                {"role": "system", "content": "You are a careful B2B sales assistant. Use only supplied evidence. Never invent facts."},
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content
    except Exception:
        return None

def _fallback(research, score):
    company = research["company_name"]
    pains = ", ".join(research["pain_points"][:2])
    email = f"""Subject: Idea for {company}

Hi {company} team,

I was researching {company} and noticed that you {research["description"].lower()}

Teams in this situation often look for ways to improve {pains}. I’d be happy to share a few practical ideas around automation and AI that could fit your workflow.

Would a short conversation next week be useful?

Best,
Sales Team"""

    linkedin = f"""Hi {company} team — I was looking into {company} and your work in this area stood out. I see potential around {pains}. Would be happy to share a couple of practical AI/automation ideas if useful."""

    return email, linkedin

def run_agent(company_input):
    research = research_company(company_input)
    score = score_lead(research)

    generated = _llm_generate(research, score)
    if generated:
        parts = re.split(r'\n\s*---\s*\n', generated, maxsplit=1)
        if len(parts) == 2:
            email, linkedin = parts
        else:
            email, linkedin = generated, "Please extract a LinkedIn version from the approved email."
    else:
        email, linkedin = _fallback(research, score)

    return {
        "research": research,
        "score": score,
        "email": email.strip(),
        "linkedin": linkedin.strip(),
    }
