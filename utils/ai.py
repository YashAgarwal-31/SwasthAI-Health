"""Structured, safety-oriented Gemini integration with an offline fallback."""
from __future__ import annotations
import os
import json
from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError
from .health import triage

load_dotenv()
SYSTEM = """You are SwasthAI, a cautious personal-health information assistant.
Use only the supplied user context and retrieved report evidence for personalized claims.
Never diagnose, prescribe, change medication doses, or replace a clinician. Clearly state
uncertainty, distinguish observation from inference, and escalate red flags. Reply in the
user's language (English, Hindi, or Hinglish)."""

class HealthResponse(BaseModel):
    summary: str
    observations: list[str] = Field(default_factory=list)
    next_steps: list[str] = Field(default_factory=list)
    doctor_questions: list[str] = Field(default_factory=list)
    urgency: str = "Routine"
    limitations: str = "Educational information only; not a medical diagnosis."

def _format(result: HealthResponse) -> str:
    parts = [result.summary]
    if result.observations: parts.append("\n**Observations**\n" + "\n".join(f"- {x}" for x in result.observations))
    if result.next_steps: parts.append("\n**Suggested next steps**\n" + "\n".join(f"- {x}" for x in result.next_steps))
    if result.doctor_questions: parts.append("\n**Questions for your clinician**\n" + "\n".join(f"- {x}" for x in result.doctor_questions))
    parts.append(f"\n**Urgency:** {result.urgency}\n\n_{result.limitations}_")
    return "\n".join(parts)

def reply(question: str, context: str = "") -> str:
    level, alert = triage(question)
    if level == "Emergency": return f"⚠️ **{level}:** {alert}"
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        return ("**Demo Mode response:** I can help you understand health information and habits, but I cannot diagnose conditions. "
                f"Based on what you shared, this looks **{level.lower()}**. {alert}\n\n"
                "For a personalized AI response, add `GEMINI_API_KEY` to a local `.env` file.")
    try:
        from google import genai
        from google.genai import types
        client = genai.Client(api_key=key)
        response = client.models.generate_content(
            model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
            contents=f"User context and retrieved evidence:\n{context}\n\nUser question: {question}",
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM,
                temperature=0.2,
                response_mime_type="application/json",
                response_schema=HealthResponse,
            ),
        )
        parsed = response.parsed if isinstance(response.parsed, HealthResponse) else HealthResponse.model_validate_json(response.text)
        return _format(parsed)
    except (ValidationError, json.JSONDecodeError, Exception):
        return "The AI service is unavailable right now. Please try again later; this app is not a substitute for medical care."
