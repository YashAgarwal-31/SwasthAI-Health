# SwasthAI Health

### AI-powered personal health management and wellness companion

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)
![Gemini](https://img.shields.io/badge/Google-Gemini%20API-4285F4?logo=google&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Local%20storage-003B57?logo=sqlite&logoColor=white)

**SwasthAI Health** brings a user’s personal health profile, wellness logs, uploaded reports, AI conversations, trained risk-screening models, and doctor-visit preparation into one focused Streamlit experience. It combines retrieval-augmented generation (RAG), structured LLM output, classical machine learning, SHAP explainability, and deterministic safety logic instead of acting as a thin chatbot wrapper.

> [!IMPORTANT]
> SwasthAI is an educational wellness tool—not a medical device. It does not diagnose illnesses, prescribe treatment, or replace qualified clinical care. For chest pain, breathing difficulty, fainting, severe bleeding, or other immediate danger, contact local emergency services right away.

## Why SwasthAI?

Health information is often spread across reports, prescriptions, notes, and habit-tracking apps. SwasthAI creates one personal health workspace where users can understand their information, observe trends, and prepare more effectively for a clinician visit.

```text
Profile + Daily Logs + Medical Reports
                 │
                 ▼
        SwasthAI Intelligence Layer
 (RAG + structured AI + trained ML + SHAP + trend detection)
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
| Context-aware AI assistant | Gemini-powered multilingual chat grounded in the profile, seven recent logs, and locally retrieved report passages. |
| Report RAG | Chunks uploaded reports, ranks relevant evidence with TF-IDF/cosine similarity, and supplies cited passages to the LLM. |
| Symptom triage | Detects configured red flags and classifies guidance as Emergency, Urgent, or Routine. |
| Report intelligence | Extracts text from PDF/text reports and highlights supported common lab values. |
| Trained risk models | Reproducible diabetes, heart-disease, and hypertension pipelines sourced from official UCI datasets. |
| Explainable AI | Compares Logistic Regression and Random Forest, reports five evaluation metrics, and produces local SHAP feature impacts. |
| Wellness planner | Produces practical Indian diet and beginner fitness guidance using saved profile context. |
| Trend intelligence | Interactive Plotly analytics plus deterministic threshold and longitudinal-change detection. |
| Evaluation dashboard | Displays Accuracy, Precision, Recall, F1, and ROC-AUC for every trained candidate model. |
| Appointments & emergency | Tracks doctor visits and provides a visible emergency guidance section. |

## Screenshots

The gallery paths below are reserved for locally captured application screenshots.

| Dashboard | AI Health Assistant |
| --- | --- |
| `assets/dashboard.png` | `assets/ai-assistant.png` |

| Report Analyzer | Risk Prediction |
| --- | --- |
| `assets/report-analyzer.png` | `assets/risk-prediction.png` |

## Model Results

The committed artifacts were trained with an 80/20 stratified split (`random_state=42`). The application compares Logistic Regression and Random Forest and selects the higher ROC-AUC candidate.

| Screening model | Selected algorithm | ROC-AUC |
| --- | --- | ---: |
| Diabetes | Random Forest | 0.815 |
| Heart disease | Random Forest | 0.970 |
| Hypertension | Logistic Regression | 0.794 |

Class imbalance makes Accuracy alone misleading, so the in-app evaluation dashboard also reports Precision, Recall, and F1-score.

## Technology Stack

| Area | Tools |
| --- | --- |
| Application | Python, Streamlit |
| Data | SQLite, Pandas, NumPy |
| Generative AI | Google GenAI SDK, Gemini structured JSON output, Pydantic validation |
| Retrieval | TF-IDF vectorization and cosine-similarity report RAG |
| Machine learning | Scikit-learn pipelines, Logistic Regression, Random Forest |
| Explainable AI | SHAP local feature attribution |
| Datasets | UCI CDC Diabetes Health Indicators (ID 891), UCI Heart Disease (ID 45) |
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
│   ├── health.py            # BMI, score, triage and lab parsing
│   ├── rag.py               # Local report retrieval and citations
│   └── trends.py            # Threshold and trend intelligence
├── ml/
│   ├── train_models.py      # UCI ingestion, training and evaluation
│   ├── predictor.py         # Saved-model inference and SHAP factors
│   └── saved_models/        # Versioned pipelines, SHAP backgrounds and metrics
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

### 5. Train the ML models

Pre-trained artifacts are included. To reproduce them, this command downloads the two cited UCI datasets, compares Logistic Regression and Random Forest, then replaces the pipelines, SHAP background samples, and evaluation metadata locally.

```bash
python -m ml.train_models
```

### 6. Start the application

```bash
streamlit run app.py
```

## Safety and Data Handling

- The prototype stores data locally in SQLite on the device where it runs.
- Health content is processed only when the user chooses to add it.
- Gemini is optional; health questions get an offline Demo Mode response without it.
- Red-flag phrases are screened before ordinary AI replies.
- Personalized AI claims are grounded in retrieved user-report passages where available.
- Gemini responses use a validated structured schema: summary, observations, next steps, doctor questions, urgency, and limitations.
- Extracted lab values and AI output must always be verified against the original report and discussed with a qualified clinician when needed.

## Limitations

- It does not integrate with hospitals, wearables, pharmacies, insurance providers, or emergency services.
- The lab parser supports a small set of common text-based patterns; it is not a clinical-grade report parser.
- The trained models are educational screening models based on public datasets; they are not clinically validated diagnostic tools.
- This app is intentionally not suitable for storing real sensitive health records in production.

## Future Enhancements

- OCR support for scanned report images and prescriptions
- Clinician-reviewed evaluation sets and calibration studies
- Multi-report comparison and doctor-visit PDF export
- Voice input and accessibility-first elderly mode
- Encrypted storage and consent-based caregiver sharing

## Resume-Ready Summary

> Built **SwasthAI Health**, a Python personal health companion combining report-grounded RAG, structured Gemini responses, reproducible UCI-based disease-risk pipelines, SHAP explainability, symptom triage, longitudinal anomaly detection, SQLite health records, and interactive Plotly analytics.

## Dataset Attribution

- [CDC Diabetes Health Indicators, UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/891/cdc+diabetes+health+indicators)
- [Heart Disease, UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/45/heart+disease)

## Validation

- `6 passed` with pytest
- All 11 Streamlit pages execute successfully with the official AppTest harness
- Emergency triage, report-grounded Demo Mode chat, ML prediction + SHAP, and appointment workflows verified interactively
