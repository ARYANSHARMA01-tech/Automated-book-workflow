import os
import re
import logging
from datetime import datetime

from scraping.content_scraper import fetch_text_from_url
from scraping.screenshot_runner import take_screenshot
from agents.ai_writer import spin_content
from agents.ai_reviewer import review_content
from versioning.content_store import save_version

# Setup logging
logging.basicConfig(
    filename='workflow.log',
    filemode='a',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

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
    logging.info(f"Saved {version_type} version to {filepath}")

def main():
    try:
        # Step 1: Scrape content
        url = "https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1"
        content = fetch_text_from_url(url)
        logging.info(f"Fetched content from {url}")

        # Step 2: Screenshot
        take_screenshot(url)
        logging.info("Screenshot taken.")

        # Step 3: AI Writer
        ai_output = spin_content(content)
        ai_output = remove_duplicate_paragraphs(ai_output)
        print("📝 AI Writer Output:\n")
        print(ai_output)
        save_output(ai_output, "Gates_of_Morning_Chapter_1", "ai_writer")

        # Step 4: Human Edits
        human_input = input("\nAny edits? Paste them or press Enter to skip: ")
        if human_input.strip():
            edited_version = human_input.strip()
            save_output(edited_version, "Gates_of_Morning_Chapter_1", "human")
        else:
            edited_version = ai_output

        # Step 5: AI Reviewer
        reviewed_version = review_content(edited_version)
        print("\n🔍 AI Reviewer Output:\n")
        print(reviewed_version)

        # Step 6: Final Approval
        final_input = input("\nFinal approval version? Paste or press Enter to use reviewed version: ")
        final_version = final_input.strip() if final_input.strip() else reviewed_version
        final_version = remove_duplicate_paragraphs(final_version)

        # Step 7: Save All
        save_output(final_version, "Gates_of_Morning_Chapter_1", "final")
        save_version("Gates of Morning - Chapter 1", final_version)  # saves to ChromaDB
        logging.info("✅ Final version saved.")

    except Exception as e:
        logging.error(f"❌ Error in workflow: {e}")
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
