
# 📚 Automated Book Publication Workflow

This project streamlines the end-to-end process of publishing public domain books using AI and human-in-the-loop workflows. It includes scraping chapters, AI rewriting, human editing, AI reviewing, and final versioning with metadata storage.

**DEMO**
"https://drive.google.com/file/d/1FnlTpbZDH2LL-J1QC20_YaLVkGdgC_01/preview"


## 🚀 Features

- ✅ Scrape chapter text and take a screenshot from any Wikisource chapter URL
- 🧠 AI Writer: Rewrites content with creative flow
- ✍️ Human-in-the-loop: Optional manual edits
- 🔍 AI Reviewer: Provides suggestions or enhanced clarity
- 📂 Versioning: Saves AI, human, and final versions as `.txt` in `/versions`
- 🧠 Memory: Saves metadata and content in ChromaDB for retrieval
- 🌐 Streamlit UI: Interactive web interface for the complete workflow

## 📦 Folder Structure

```
.
├── app.py                          # Streamlit app
├── scraping/
│   ├── content_scraper.py         # HTML scraper
│   └── screenshot_runner.py       # URL screenshot using Playwright
├── agents/
│   ├── ai_writer.py               # Content rewriting with Gemini
│   └── ai_reviewer.py             # Review using Gemini
├── versioning/
│   └── content_store.py           # Save versions & ChromaDB logic
├── versions/                      # Output directory for saved content
├── workflow.log                   # Logs
└── requirements.txt               # Python dependencies
```

## 🧪 How to Run

1. Install dependencies:

```
pip install -r requirements.txt
```

2. Run Streamlit app:

```
streamlit run app.py
```

3. Paste any [Wikisource chapter URL](https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1), click **"Process Chapter"**, and follow the flow.

## 🛠️ Tech Stack

- Python, Streamlit
- Playwright (for screenshots)
- Gemini 1.5 Flash (via Google API)
- ChromaDB (for metadata)
- Logging for workflow tracking

## ✍️ Author

Aryan Sharma
