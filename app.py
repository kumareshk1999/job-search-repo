import streamlit as st
import feedparser
import webbrowser

st.set_page_config(page_title="Job Assistant", layout="wide")

st.title("🚀 Online Job Assistant (India)")

# 🔍 Keyword Input
keyword = st.text_input("Enter Skill / Role", "python")

# 📊 Experience Filter
exp_level = st.selectbox(
    "Experience Level",
    ["Fresher", "Junior", "Mid", "Senior"]
)

# 🌍 Location
location = st.text_input("Location", "India")

# 🔘 Search Button
if st.button("🔍 Search Jobs"):

    query = keyword.replace(" ", "+")
    loc = location.replace(" ", "+")

    url = f"https://www.indeed.co.in/rss?q={query}&l={loc}"

    feed = feedparser.parse(url)

    jobs = []

    for job in feed.entries:

        title = job.title.lower()

        # 🎯 Experience Filtering (basic keyword logic)
        if exp_level == "Fresher":
            if any(x in title for x in ["senior", "lead", "manager"]):
                continue

        elif exp_level == "Junior":
            if "senior" in title:
                continue

        elif exp_level == "Senior":
            if not any(x in title for x in ["senior", "lead"]):
                continue

        jobs.append(job)

    st.success(f"Found {len(jobs)} jobs")

    # 📋 Display Jobs
    for i, job in enumerate(jobs):

        st.subheader(job.title)
        st.write(f"🏢 {job.get('author', 'Unknown')}")
        st.write(f"📍 {location}")

        col1, col2 = st.columns(2)

        with col1:
            if st.button(f"Apply {i}"):
                webbrowser.open(job.link)

        with col2:
            st.markdown(f"[View Job]({job.link})")

        st.divider()