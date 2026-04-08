import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="AI Job Assistant", layout="wide")

st.title("🚀 AI Job Assistant (Pro Version)")

# 🔍 Inputs
keyword = st.text_input("Enter Skill / Role", "python developer")
location = st.text_input("Location", "India")

exp_level = st.selectbox(
    "Experience Level",
    ["Fresher", "Junior", "Mid", "Senior"]
)

# 🔑 Adzuna API
APP_ID = "855feb69"
APP_KEY = "d78e53de76f6ad0a1f0699d2915e7e45"


# 🔹 Fetch Jobs (Google-like aggregation)
def fetch_jobs(keyword):
    jobs = []
    try:
        url = f"https://api.adzuna.com/v1/api/jobs/in/search/1?app_id={APP_ID}&app_key={APP_KEY}&results_per_page=50&what={keyword}"

        res = requests.get(url).json()

        for job in res.get("results", []):
            jobs.append({
                "title": job["title"],
                "company": job["company"]["display_name"],
                "link": job["redirect_url"],
                "description": job.get("description", "")
            })
    except:
        pass

    return jobs


# 🔹 AI Scoring (Keyword-based)
def score_job(job, keyword):
    score = 0
    title = job["title"].lower()
    desc = job["description"].lower()
    keyword = keyword.lower()

    # Strong match
    if keyword in title:
        score += 50

    # Partial match
    for word in keyword.split():
        if word in title:
            score += 10
        if word in desc:
            score += 5

    # Bonus keywords
    bonus_skills = ["python", "java", "react", "node", "sql"]
    for skill in bonus_skills:
        if skill in desc:
            score += 2

    return score


# 🔹 Experience Filter
def filter_experience(job, level):
    title = job["title"].lower()

    if level == "Fresher":
        return not any(x in title for x in ["senior", "lead", "manager"])

    if level == "Junior":
        return "senior" not in title

    if level == "Senior":
        return any(x in title for x in ["senior", "lead"])

    return True


# 🔘 Search
if st.button("🔍 Search Jobs"):

    jobs = fetch_jobs(keyword)

    if not jobs:
        st.error("No jobs found. Try broader keyword like 'developer'")
    else:
        # Apply filters + scoring
        processed_jobs = []

        for job in jobs:
            if filter_experience(job, exp_level):
                score = score_job(job, keyword)
                job["score"] = score
                processed_jobs.append(job)

        # Sort by score
        processed_jobs = sorted(processed_jobs, key=lambda x: x["score"], reverse=True)

        st.success(f"Found {len(processed_jobs)} jobs")

        # 📊 Display as table
        df = pd.DataFrame(processed_jobs)

        for i, job in enumerate(processed_jobs[:50]):

            st.subheader(f"{job['title']}  🔥 {job['score']}% match")
            st.write(f"🏢 {job['company']}")

            # ✅ APPLY BUTTON (WORKING)
            st.markdown(f"[👉 Apply Now]({job['link']})")

            st.divider()
