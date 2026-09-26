import re
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup

def _fallback(company):
    name = company.replace("https://", "").replace("http://", "").split("/")[0]
    name = name.replace("www.", "").split(".")[0].replace("-", " ").title()
    return {
        "company_name": name,
        "industry": "Technology / Business Services",
        "size": "20-50",
        "description": f"{name} appears to operate a technology or business-focused service.",
        "pain_points": [
            "Reducing repetitive manual work",
            "Improving customer and sales workflows",
            "Using data more effectively"
        ],
        "evidence": "Demo fallback research was used because no public page could be reliably retrieved."
    }

def research_company(company_input):
    url = company_input.strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        response = requests.get(
            url,
            timeout=8,
            headers={"User-Agent": "Mozilla/5.0 LeadResearchDemo/1.0"}
        )
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.get_text(" ", strip=True) if soup.title else ""
        text = " ".join(soup.stripped_strings)
        text = re.sub(r"\s+", " ", text)[:2500]

        host = urlparse(url).netloc.replace("www.", "")
        name = title.split("|")[0].strip() if title else host.split(".")[0].title()

        return {
            "company_name": name,
            "industry": "Technology / Business Services",
            "size": "Unknown",
            "description": text[:500] or f"{name} is a company with a public website.",
            "pain_points": [
                "Improving operational efficiency",
                "Reducing repetitive manual work",
                "Improving customer workflows"
            ],
            "evidence": f"Public website: {url}\nPage title: {title}\nRetrieved text sample: {text[:900]}"
        }
    except Exception:
        return _fallback(company_input)
