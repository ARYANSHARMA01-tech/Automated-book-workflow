import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

def spin_content(original_text):
    prompt = f"Rewrite the following chapter in a more engaging, modern tone while keeping the meaning intact:\n\n{original_text}"
    response = model.generate_content(prompt)
    return response.text