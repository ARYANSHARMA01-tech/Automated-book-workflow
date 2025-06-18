import streamlit as st
import os
from datetime import datetime

from scraping.content_scraper import fetch_text_from_url
from scraping.screenshot_runner import take_screenshot
from agents.ai_writer import spin_content
from agents.ai_reviewer import review_content
from versioning.content_store import save_version
import asyncio, sys
if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())


def remove_duplicate_paragraphs(text):
    paragraphs = text.strip().split("\n")
    cleaned = []
    seen = set()
    for para in paragraphs:
        p = para.strip()
        if p and p not in seen:
            seen.add(p)
            cleaned.append(p)
    return "\n\n".join(cleaned)

def save_output(text, filename, version_type="final"):
    os.makedirs("versions", exist_ok=True)
    filepath = f"versions/{filename}_{version_type}.txt"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text)
    return filepath

st.set_page_config(page_title="📚 Book Publication Workflow", layout="wide")
st.title("📖 Automated Book Publication Workflow")

# Input Section
url = st.text_input("Enter Chapter URL", "https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1")

if st.button("Process Chapter"):
    with st.spinner("Fetching and processing..."):
        try:
            content = fetch_text_from_url(url)
            take_screenshot(url)

            ai_output = spin_content(content)
            ai_output = remove_duplicate_paragraphs(ai_output)

            st.session_state['original'] = content
            st.session_state['ai'] = ai_output
            st.session_state['human'] = ai_output  # default to same
            st.session_state['reviewed'] = review_content(ai_output)

            st.success("Chapter processed successfully!")

        except Exception as e:
            st.error(f"Failed to process: {e}")

if "ai" in st.session_state:
    st.subheader("🧠 AI Writer Output")
    st.text_area("AI Output", value=st.session_state['ai'], height=250)

    st.subheader("📝 Human Edits (Optional)")
    human_input = st.text_area("Edit the AI output here", value=st.session_state['ai'], key="human_edit", height=250)
    st.session_state['human'] = human_input

    st.subheader("🔍 AI Reviewer Output")
    st.text_area("AI Reviewer Output", value=st.session_state['reviewed'], height=250)

    st.subheader("✅ Final Approval")
    final_input = st.text_area("Final content for saving", value=st.session_state['reviewed'], height=250)

    if st.button("Save Final Version"):
        cleaned_final = remove_duplicate_paragraphs(final_input)
        filename = "Gates_of_Morning_Chapter_1"

        save_output(st.session_state['ai'], filename, "ai_writer")
        save_output(st.session_state['human'], filename, "human")
        save_output(cleaned_final, filename, "final")
        save_version("Gates of Morning - Chapter 1", cleaned_final)

        st.success("✅ All versions saved successfully!")

