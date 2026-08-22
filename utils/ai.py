"""Safe optional Gemini integration with a deterministic demo fallback."""
from __future__ import annotations
import os
from dotenv import load_dotenv
from .health import triage

load_dotenv()
SYSTEM = """You are SwasthAI, a cautious personal-health information assistant. You do not diagnose, prescribe, or replace a clinician. Be concise, acknowledge uncertainty, ask a useful follow-up where needed, and advise urgent professional care for red flags. Use simple language and the user's requested language."""

def reply(question: str, context: str = "") -> str:
    level, alert = triage(question)
    if level == "Emergency": return f"⚠️ **{level}:** {alert}"
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        return ("**Demo Mode response:** I can help you understand health information and habits, but I cannot diagnose conditions. "
                f"Based on what you shared, this looks **{level.lower()}**. {alert}\n\n"
                "For a personalized AI response, add `GEMINI_API_KEY` to a local `.env` file.")
    try:
        import google.generativeai as genai
        genai.configure(api_key=key)
        model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=SYSTEM)
        return model.generate_content(f"User context:\n{context}\n\nQuestion: {question}").text
    except Exception:
        return "The AI service is unavailable right now. Please try again later; this app is not a substitute for medical care."
