import streamlit as st
import feedparser
import webbrowser

st.set_page_config(page_title="Job Assistant", layout="wide")

st.title("🚀 Smart Job Assistant (India)")

# 🔍 User Inputs
keyword = st.text_input("Enter Skill / Role", "python")
location = st.text_input("Location", "India")

exp_level = st.selectbox(
    "Experience Level",
    ["Fresher", "Junior", "Mid", "Senior"]
)

# 🔹 Keyword Expansion
def expand_keywords(keyword):
    keyword = keyword.lower()

    mapping = {
        "python": ["python", "django", "flask", "backend"],
        "java": ["java", "spring", "spring boot"],
        "db2": ["db2", "database", "sql", "dba"],
        "full stack": ["full stack", "mern", "mean", "react", "node"]
    }

    return mapping.get(keyword, [keyword])


# 🔹 Fetch Jobs from Indeed RSS
def fetch_jobs(keyword, location):
    keywords = expand_keywords(keyword)
    all_jobs = []

    for key in keywords:
        query = key.replace(" ", "+")
        loc = location.replace(" ", "+")

        url = f"https://www.indeed.co.in/rss?q={query}&l={loc}"

        feed = feedparser.parse(url)

        for entry in feed.entries:
            all_jobs.append({
                "title": entry.title,
                "company": entry.get("author", "Unknown"),
                "link": entry.link
            })

    return all_jobs


# 🔹 Experience Filter (Light filtering)
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


# 🔘 Search Button
if st.button("🔍 Search Jobs"):

    jobs = fetch_jobs(keyword, location)

    # Remove duplicates
    jobs = list({job['link']: job for job in jobs}.values())

    # Apply experience filter
    jobs = filter_experience(jobs, exp_level)

    # 🚨 Fallback if no jobs
    if len(jobs) == 0:
        st.warning("No exact match found. Showing related jobs...")
        jobs = fetch_jobs("developer", location)
        jobs = list({job['link']: job for job in jobs}.values())

    st.success(f"Found {len(jobs)} jobs")

    # 📋 Display Jobs
    for i, job in enumerate(jobs):

        st.subheader(job["title"])
        st.write(f"🏢 {job['company']}")
        st.write(f"📍 {location}")

        col1, col2 = st.columns(2)

        with col1:
            if st.button(f"Apply {i}"):
                webbrowser.open(job["link"])

        with col2:
            st.markdown(f"[View Job]({job['link']})")

        st.divider()
