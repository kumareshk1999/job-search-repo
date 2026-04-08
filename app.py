import streamlit as st
import feedparser
import requests
import webbrowser

st.set_page_config(page_title="Job Assistant", layout="wide")

st.title("🚀 Smart Job Assistant (India)")

# 🔍 Inputs
keyword = st.text_input("Enter Skill / Role", "python developer")
location = st.text_input("Location", "India")

exp_level = st.selectbox(
    "Experience Level",
    ["Fresher", "Junior", "Mid", "Senior"]
)

# 🔹 Keyword Expansion
def expand_keywords(keyword):
    keyword = keyword.lower()

    mapping = {
        "python": ["python developer", "django", "flask"],
        "java": ["java developer", "spring boot"],
        "db2": ["db2 dba", "database administrator"],
        "full stack": ["full stack developer", "mern", "react node"]
    }

    return mapping.get(keyword, [keyword])


# 🔹 Indeed Fetch (may fail sometimes)
def fetch_indeed_jobs(keyword, location):
    jobs = []
    try:
        url = f"https://www.indeed.co.in/rss?q={keyword.replace(' ','+')}&l={location}"
        feed = feedparser.parse(url)

        for entry in feed.entries:
            jobs.append({
                "title": entry.title,
                "company": entry.get("author", "Unknown"),
                "link": entry.link
            })
    except:
        pass

    return jobs


# 🔹 Remote Jobs API (ALWAYS RETURNS DATA)
def fetch_remote_jobs(keyword):
    jobs = []
    try:
        url = f"https://remotive.com/api/remote-jobs?search={keyword}"
        response = requests.get(url).json()

        for job in response.get("jobs", []):
            jobs.append({
                "title": job["title"],
                "company": job["company_name"],
                "link": job["url"]
            })
    except:
        pass

    return jobs


# 🔹 Experience Filter
def filter_experience(jobs, exp_level):
    filtered = []

    for job in jobs:
        title = job["title"].lower()

        if exp_level == "Fresher":
            if any(x in title for x in ["senior", "lead", "manager"]):
                continue

        elif exp_level == "Junior":
            if "senior" in title:
                continue

        elif exp_level == "Senior":
            if not any(x in title for x in ["senior", "lead"]):
                continue

        filtered.append(job)

    return filtered


# 🔘 Search
if st.button("🔍 Search Jobs"):

    all_jobs = []

    keywords = expand_keywords(keyword)

    # 1️⃣ Try Indeed
    for key in keywords:
        all_jobs.extend(fetch_indeed_jobs(key, location))

    # 2️⃣ Always add Remote jobs
    for key in keywords:
        all_jobs.extend(fetch_remote_jobs(key))

    # Remove duplicates
    all_jobs = list({job['link']: job for job in all_jobs}.values())

    # Apply experience filter
    all_jobs = filter_experience(all_jobs, exp_level)

    # 🚨 FINAL FALLBACK (NEVER EMPTY)
    if len(all_jobs) == 0:
        st.warning("No jobs found. Showing general developer jobs...")
        all_jobs = fetch_remote_jobs("developer")

    st.success(f"Found {len(all_jobs)} jobs")

    # 📋 Display
    for i, job in enumerate(all_jobs[:50]):  # limit for performance

        st.subheader(job["title"])
        st.write(f"🏢 {job['company']}")

        col1, col2 = st.columns(2)

        with col1:
            if st.button(f"Apply {i}"):
                webbrowser.open(job["link"])

        with col2:
            st.markdown(f"[View Job]({job['link']})")

        st.divider()
