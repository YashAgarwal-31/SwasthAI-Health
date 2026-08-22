from utils.health import bmi, health_score, triage, extract_labs, diabetes_risk

def test_bmi(): assert bmi(70,175)==22.9
def test_score_is_bounded(): assert 0 <= health_score({"water":4,"sleep":8,"steps":9000,"spo2":98}) <= 100
def test_red_flag_triage(): assert triage("I have chest pain")[0] == "Emergency"
def test_extract_labs(): assert extract_labs("Glucose: 160 Haemoglobin: 13")
def test_risk(): assert diabetes_risk(30,25,100,120)[1] in {"Low","Medium","High"}
