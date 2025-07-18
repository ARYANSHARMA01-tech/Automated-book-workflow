from agents.ai_writer import model

def review_content(spun_text):
    prompt = f"Review the following rewritten chapter for grammar, coherence, and flow. Suggest improvements or apply changes:\n\n{spun_text}"
    response = model.generate_content(prompt)
    return response.text