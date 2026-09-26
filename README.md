# AI Lead Research & Outreach Agent

An interview-ready MVP that accepts a company name or website, researches public website information, scores the lead against a simple ICP, and drafts personalized email and LinkedIn outreach for human approval.

## Features

- Company URL/name input
- Public website research
- Company description and evidence
- Simple ICP-based 1–10 lead scoring
- Personalized cold email
- Personalized LinkedIn message
- Human-in-the-loop approval
- LLM support through OpenAI API
- Deterministic fallback when no API key is available
- Simple Streamlit UI

## Tech Stack

- Python
- Streamlit
- OpenAI API (optional)
- Requests
- BeautifulSoup
- Rule-based lead scoring

## Architecture

See `architecture.png`.

## Setup

```bash
git clone <your-repository-url>
cd ai-lead-research-outreach-agent

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
```

Copy `.env.example` to `.env` and add your OpenAI API key if desired.

Run:

```bash
streamlit run app.py
```

<<<<<<< HEAD
## Batch CSV Processing (Stretch Goal)

Upload a CSV containing a `company` column. The app researches each company, calculates its ICP score, generates email and LinkedIn outreach, displays the results, and provides a `results.csv` download.

Example CSV:

```csv
company
https://example.com
https://anothercompany.com
```

=======
>>>>>>> 8e9f4fee57b050da91d7f875fb6f9caf4ea988cc
## Demo Flow

1. Enter a company website.
2. Click Research & Generate.
3. Review company research and evidence.
4. Review the ICP score.
5. Review the generated cold email and LinkedIn message.
6. Human approves before any external sending.

## ICP

This demo targets B2B technology/business companies that may benefit from automation and AI. The scoring is intentionally simple and explainable.

## Safety / Reliability

The app does not automatically send outreach. A human must review the generated content. When LLM access is unavailable, a deterministic fallback is used. Research failures do not cause invented company facts.

## Future Improvements

- Batch CSV processing
- Google Sheets / CRM integration
- Search API and richer company enrichment
- Persistent lead history
- Better evidence extraction and source citations
- Automated evaluation for factuality and personalization
- Retry, rate-limit handling, logging, and monitoring
- LangGraph-based multi-step agent orchestration
- Production authentication and role-based access
