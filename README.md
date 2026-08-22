# SwasthAI Health

**SwasthAI Health** is a Python-based personal health-management and wellness companion inspired by AI health assistants. It centralizes health profiles, daily wellness data, report understanding, symptom triage, AI guidance, transparent diabetes-risk screening, analytics, and appointment preparation in one local Streamlit application.

> **Safety notice:** This is an educational portfolio prototype, not a medical device. It does not diagnose, prescribe treatment, or replace a qualified clinician. For urgent symptoms, seek emergency medical help.

## Features

- Secure local signup/login with bcrypt-hashed passwords
- Personal health profile, BMI, conditions, allergies, goals and emergency contact
- Daily health tracking: water, sleep, activity, BP, glucose, heart rate, SpO₂ and stress
- ChatGPT-style AI health assistant with Gemini integration and safe Demo Mode
- Rule-based red-flag symptom triage
- PDF/text report extraction with common lab-value detection and explanation
- Transparent diabetes-risk screening with probability, risk band and contributing factors
- Indian diet and beginner fitness guidance
- Plotly wellness analytics and a unified health timeline
- Appointment tracker and emergency guidance

## Tech Stack

Python, Streamlit, SQLite, Pandas, NumPy, Plotly, Scikit-learn-ready ML module, Gemini API, PyMuPDF, bcrypt, ReportLab-ready export support, pytest.

## Run Locally

```bash
git clone <your-repository-url>
cd SwasthAI-Health
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env  # Windows
# Add GEMINI_API_KEY to .env only if you want live AI answers.
streamlit run app.py
```

Without a Gemini key, the project runs in safe Demo Mode.

## Project Structure

```text
app.py              # Streamlit application
utils/              # database, health logic, Gemini integration
data/               # local SQLite database created at runtime
tests/              # core unit tests
requirements.txt
```

## Limitations & Future Work

This local portfolio build intentionally does not connect to real hospital systems, health wearables, or emergency services. Future versions can add OCR for scanned reports, trained public-dataset models with SHAP visualizations, wearable integrations, encrypted cloud storage, and clinician-reviewed content.
