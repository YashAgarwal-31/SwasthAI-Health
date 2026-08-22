"""Health calculations, safe triage, parsing and demo predictions."""
from __future__ import annotations
import re
from datetime import date
from typing import Iterable

RED_FLAGS = ("chest pain", "difficulty breathing", "shortness of breath", "fainting", "unconscious", "severe bleeding", "suicidal", "self harm")
LAB_RANGES = {"glucose": (70, 140, "mg/dL"), "haemoglobin": (12, 17.5, "g/dL"), "hemoglobin": (12, 17.5, "g/dL"), "cholesterol": (0, 200, "mg/dL"), "hba1c": (0, 5.7, "%")}

def bmi(weight_kg: float | None, height_cm: float | None) -> float | None:
    if not weight_kg or not height_cm or height_cm <= 0: return None
    return round(weight_kg / ((height_cm / 100) ** 2), 1)

def health_score(log: dict) -> int:
    score = 50
    score += 15 if (log.get("water") or 0) >= 2 else 5
    score += 15 if 7 <= (log.get("sleep") or 0) <= 9 else 3
    score += 10 if (log.get("steps") or 0) >= 6000 else 3
    score += 10 if 95 <= (log.get("spo2") or 98) <= 100 else 0
    return min(100, max(0, score))

def triage(text: str, severity: str = "Mild") -> tuple[str, str]:
    lower = text.lower()
    if any(flag in lower for flag in RED_FLAGS):
        return "Emergency", "This may need urgent in-person evaluation. Contact local emergency services or go to the nearest emergency department now."
    if severity == "Severe" or any(k in lower for k in ("high fever", "persistent vomiting", "severe pain")):
        return "Urgent", "Please contact a qualified clinician promptly, especially if symptoms worsen."
    return "Routine", "Track symptoms, rest and hydration where appropriate, and consider a routine clinician consultation if symptoms persist."

def extract_labs(text: str) -> list[dict]:
    findings = []
    for name, (lo, hi, unit) in LAB_RANGES.items():
        match = re.search(rf"{name}\s*[:=-]?\s*(\d+(?:\.\d+)?)", text, re.I)
        if match:
            value = float(match.group(1)); status = "Normal" if lo <= value <= hi else "Abnormal"
            findings.append({"Test": name.title(), "Value": value, "Unit": unit, "Reference": f"{lo}–{hi}", "Status": status})
    return findings

def diabetes_risk(age: float, bmi_value: float, glucose: float, bp: float) -> tuple[float, str, list[str]]:
    raw = -8 + 0.045 * age + 0.10 * bmi_value + 0.035 * glucose + 0.012 * bp
    probability = 1 / (1 + 2.71828 ** (-raw))
    risk = "High" if probability >= .65 else "Medium" if probability >= .35 else "Low"
    factors = [f"Glucose: {glucose} mg/dL", f"BMI: {bmi_value}", f"Age: {age}", f"Blood pressure: {bp} mmHg"]
    return round(probability, 2), risk, factors

def today() -> str: return date.today().isoformat()
