import os
import streamlit as st
from agent.agent import run_agent

st.set_page_config(page_title="AI Lead Research & Outreach Agent", page_icon="🤖", layout="wide")

st.title("🤖 AI Lead Research & Outreach Agent")
st.caption("Research a company → score the lead → generate personalized outreach for human approval.")

with st.sidebar:
    st.header("Configuration")
    st.info("Add OPENAI_API_KEY to .env to enable LLM generation. The app also includes a deterministic demo fallback.")
    st.markdown("**ICP example**")
    st.write("- B2B technology company")
    st.write("- 20+ employees")
    st.write("- Potential automation / AI need")


st.divider()
st.header("📊 Batch CSV Processing")
st.caption("Optional stretch goal: upload multiple companies and download the research, score, and outreach results.")

csv_file = st.file_uploader(
    "Upload CSV with a 'company' column",
    type=["csv"],
    help="Example: company\\nhttps://example.com\\nhttps://anothercompany.com"
)

if csv_file is not None:
    import pandas as pd
    df = pd.read_csv(csv_file)

    if "company" not in df.columns:
        st.error("CSV must contain a column named 'company'.")
    else:
        if st.button("Process CSV", type="secondary"):
            results = []
            companies = df["company"].dropna().astype(str).str.strip()
            progress = st.progress(0)

            for i, company_value in enumerate(companies):
                try:
                    result = run_agent(company_value)
                    research = result["research"]
                    results.append({
                        "company": company_value,
                        "company_name": research["company_name"],
                        "industry": research["industry"],
                        "size": research["size"],
                        "lead_score": result["score"],
                        "description": research["description"],
                        "pain_points": " | ".join(research["pain_points"]),
                        "cold_email": result["email"],
                        "linkedin_message": result["linkedin"],
                    })
                except Exception as exc:
                    results.append({
                        "company": company_value,
                        "company_name": "",
                        "industry": "",
                        "size": "",
                        "lead_score": "",
                        "description": "",
                        "pain_points": "",
                        "cold_email": "",
                        "linkedin_message": f"Processing failed: {exc}",
                    })
                progress.progress((i + 1) / max(len(companies), 1))

            result_df = pd.DataFrame(results)
            st.success(f"Processed {len(result_df)} lead(s).")
            st.dataframe(result_df, use_container_width=True)

            csv_output = result_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "⬇️ Download results.csv",
                data=csv_output,
                file_name="results.csv",
                mime="text/csv",
                use_container_width=True,
            )

st.divider()


company = st.text_input("Company name or website", placeholder="e.g. https://example.com")
run = st.button("Research & Generate", type="primary", use_container_width=True)

if run:
    if not company.strip():
        st.warning("Please enter a company name or URL.")
    else:
        with st.spinner("Researching company and preparing outreach..."):
            result = run_agent(company.strip())

        st.subheader("Company Research")
        r = result["research"]
        c1, c2, c3 = st.columns(3)
        c1.metric("Company", r["company_name"])
        c2.metric("Estimated Size", r["size"])
        c3.metric("Lead Score", f'{result["score"]}/10')

        st.write("**What they do:**", r["description"])
        st.write("**Likely pain points:**")
        for p in r["pain_points"]:
            st.write("•", p)

        with st.expander("Research evidence / notes"):
            st.write(r["evidence"])

        st.subheader("Personalized Outreach")
        tab1, tab2 = st.tabs(["Cold Email", "LinkedIn Message"])
        with tab1:
            st.text_area("Draft email", result["email"], height=260)
        with tab2:
            st.text_area("Draft LinkedIn message", result["linkedin"], height=220)

        st.success("Human approval required before sending. No message is sent automatically.")
