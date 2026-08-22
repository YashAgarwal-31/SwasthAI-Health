# SwasthAI Health

### AI-powered personal health management and wellness companion

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)
![Gemini](https://img.shields.io/badge/Google-Gemini%20API-4285F4?logo=google&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Local%20storage-003B57?logo=sqlite&logoColor=white)

**SwasthAI Health** brings a user’s personal health profile, wellness logs, uploaded reports, AI conversations, risk screening, and doctor-visit preparation into one focused Streamlit experience. It is designed as a privacy-conscious, local-first portfolio prototype inspired by modern AI health companions.

> [!IMPORTANT]
> SwasthAI is an educational wellness tool—not a medical device. It does not diagnose illnesses, prescribe treatment, or replace qualified clinical care. For chest pain, breathing difficulty, fainting, severe bleeding, or other immediate danger, contact local emergency services right away.

## Why SwasthAI?

Health information is often spread across reports, prescriptions, notes, and habit-tracking apps. SwasthAI creates one personal health workspace where users can understand their information, observe trends, and prepare more effectively for a clinician visit.

```text
Profile + Daily Logs + Medical Reports
                 │
                 ▼
        SwasthAI Intelligence Layer
  (safe AI chat, triage, lab extraction, risk scoring)
                 │
                 ▼
Insights + Wellness Guidance + Doctor-Visit Readiness
```

## Key Features

| Module | What it does |
| --- | --- |
| Secure local access | Signup/login with bcrypt-hashed passwords and local SQLite persistence. |
| Personal health profile | Captures BMI, conditions, allergies, goals, diet preference, and emergency contact. |
| Daily wellness tracker | Logs weight, water, sleep, activity, BP, glucose, heart rate, SpO₂, stress, and notes. |
| AI Health Assistant | Gemini-powered, multilingual health-information chat with a safe local Demo Mode fallback. |
| Symptom triage | Detects configured red flags and classifies guidance as Emergency, Urgent, or Routine. |
| Report intelligence | Extracts text from PDF/text reports and highlights supported common lab values. |
| Diabetes risk screening | Shows probability, low/medium/high risk band, and the exact factors used. |
| Wellness planner | Produces practical Indian diet and beginner fitness guidance using saved profile context. |
| Health analytics | Interactive Plotly trends for weight, glucose, sleep, water, activity, and health logs. |
| Appointments & emergency | Tracks doctor visits and provides a visible emergency guidance section. |

## Screenshots

Add screenshots here after running the project locally.

| Dashboard | AI Health Assistant |
| --- | --- |
| `assets/dashboard.png` | `assets/ai-assistant.png` |

| Report Analyzer | Risk Prediction |
| --- | --- |
| `assets/report-analyzer.png` | `assets/risk-prediction.png` |

## Technology Stack

| Area | Tools |
| --- | --- |
| Application | Python, Streamlit |
| Data | SQLite, Pandas, NumPy |
| AI | Google Gemini API with safe Demo Mode fallback |
| Report processing | PyMuPDF |
| Analytics | Plotly |
| Security | bcrypt, `python-dotenv` |
| Testing | pytest |
| Future ML foundation | Scikit-learn, joblib |

## Project Structure

```text
SwasthAI-Health/
├── app.py                   # Streamlit application and feature pages
├── utils/
│   ├── ai.py                # Gemini integration and Demo Mode fallback
│   ├── database.py          # SQLite schema and persistence helpers
│   └── health.py            # BMI, score, triage, lab parsing, risk logic
├── tests/
│   └── test_health.py       # Core utility tests
├── data/                    # Local database created at runtime (ignored by Git)
├── requirements.txt
├── .env.example
└── README.md
```

## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/YashAgarwal-31/SwasthAI-Health.git
cd SwasthAI-Health
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

**Windows**

```bash
.venv\Scripts\activate
```

**macOS/Linux**

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure optional Gemini AI

Copy `.env.example` to `.env`, then add your own key:

```env
GEMINI_API_KEY=your_key_here
```

If no key is configured, SwasthAI still runs in a safe, deterministic **Demo Mode**. Never commit `.env` or an API key to GitHub.

### 5. Start the application

```bash
streamlit run app.py
```

## Safety and Data Handling

- The prototype stores data locally in SQLite on the device where it runs.
- Health content is processed only when the user chooses to add it.
- Gemini is optional; health questions get an offline Demo Mode response without it.
- Red-flag phrases are screened before ordinary AI replies.
- Extracted lab values and AI output must always be verified against the original report and discussed with a qualified clinician when needed.

## Limitations

- It does not integrate with hospitals, wearables, pharmacies, insurance providers, or emergency services.
- The lab parser supports a small set of common text-based patterns; it is not a clinical-grade report parser.
- The risk score is a transparent educational screening calculation, not a trained diagnostic model.
- This app is intentionally not suitable for storing real sensitive health records in production.

## Future Enhancements

- OCR support for scanned report images and prescriptions
- Validated public-dataset ML models with SHAP visualizations
- Multi-report comparison and doctor-visit PDF export
- Voice input and accessibility-first elderly mode
- Encrypted storage and consent-based caregiver sharing

## Resume-Ready Summary

> Built **SwasthAI Health**, a Python and Streamlit personal health companion that combines daily wellness tracking, AI health conversations, report-based lab-value extraction, symptom triage, explainable diabetes-risk screening, personalized wellness planning, and interactive analytics using SQLite, Gemini API, Pandas, and Plotly.
