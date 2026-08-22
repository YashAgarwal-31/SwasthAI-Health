from utils.health import bmi, health_score, triage, extract_labs
from utils.rag import chunk_text, retrieve_report_chunks
from utils.trends import analyze_trends

def test_bmi(): assert bmi(70,175)==22.9
def test_score_is_bounded(): assert 0 <= health_score({"water":4,"sleep":8,"steps":9000,"spo2":98}) <= 100
def test_red_flag_triage(): assert triage("I have chest pain")[0] == "Emergency"
def test_extract_labs(): assert extract_labs("Glucose: 160 Haemoglobin: 13")
def test_rag_retrieves_relevant_report():
    reports=[{"filename":"blood.pdf","extracted_text":"HbA1c 7.2 and glucose 160"},{"filename":"other.pdf","extracted_text":"Vitamin D 30"}]
    assert retrieve_report_chunks("glucose trend",reports)[0]["source"]=="blood.pdf"
def test_trend_warning():
    rows=[{"logged_on":"2026-01-01","glucose":100},{"logged_on":"2026-01-02","glucose":145}]
    assert any(x["metric"]=="glucose" for x in analyze_trends(rows))
