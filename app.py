from __future__ import annotations
import json
from datetime import date
import bcrypt
import fitz
import pandas as pd
import plotly.express as px
import streamlit as st
from reportlab.pdfgen import canvas
from io import BytesIO
from utils.database import init_db, execute, one, all_rows
from utils.health import bmi, health_score, triage, extract_labs, diabetes_risk, today
from utils.ai import reply

st.set_page_config(page_title="SwasthAI Health", page_icon="🩺", layout="wide")
init_db()
st.markdown("""<style>.stApp{background:#f6fbfc}.hero{padding:1.5rem;border-radius:18px;background:linear-gradient(135deg,#067f86,#14919b);color:white}.alert{padding:.8rem;border-radius:10px;background:#fff3cd}</style>""", unsafe_allow_html=True)

def login() -> int | None:
    st.markdown("<div class='hero'><h1>🩺 SwasthAI Health</h1><p>Your private AI health companion</p></div>", unsafe_allow_html=True)
    a,b=st.tabs(["Login","Create account"])
    with a:
        u=st.text_input("Username", key="lu"); p=st.text_input("Password", type="password", key="lp")
        if st.button("Login"):
            user=one("SELECT * FROM users WHERE username=?",(u,))
            if user and bcrypt.checkpw(p.encode(),user["password_hash"].encode()): st.session_state.uid=user["id"]; st.rerun()
            st.error("Invalid username or password.")
    with b:
        u=st.text_input("Username", key="su"); p=st.text_input("Password", type="password", key="sp")
        if st.button("Create account"):
            if len(u)<3 or len(p)<6: st.warning("Use a 3+ character username and 6+ character password.")
            else:
                try:
                    execute("INSERT INTO users(username,password_hash) VALUES(?,?)",(u,bcrypt.hashpw(p.encode(),bcrypt.gensalt()).decode())); st.success("Account created. Please log in.")
                except Exception: st.error("Username already exists.")
    return None

if "uid" not in st.session_state: login(); st.stop()
uid=st.session_state.uid
profile=one("SELECT * FROM profiles WHERE user_id=?",(uid,))
name=(profile["name"] if profile and profile["name"] else "there")
st.sidebar.title("SwasthAI Health")
page=st.sidebar.radio("Navigate",["Dashboard","Health Profile","Daily Tracker","AI Health Assistant","Symptom Checker","Report Analyzer","Risk Prediction","Wellness Planner","Analytics & Timeline","Appointments & Emergency"])
if st.sidebar.button("Logout"): st.session_state.clear(); st.rerun()
st.caption("⚠️ Educational wellness tool only — not a diagnosis, treatment plan, or emergency service.")

if page=="Dashboard":
    logs=all_rows("SELECT * FROM health_logs WHERE user_id=? ORDER BY logged_on DESC",(uid,)); last=dict(logs[0]) if logs else {}
    st.markdown(f"<div class='hero'><h1>Good day, {name} 👋</h1><p>Your health snapshot, in one calm place.</p></div>",unsafe_allow_html=True)
    cols=st.columns(5); vals=[("Health score",f"{health_score(last)} / 100"),("BMI",str(bmi(profile['weight'],profile['height']) if profile else '—')),("Sleep",f"{last.get('sleep','—')} h"),("Water",f"{last.get('water','—')} L"),("Steps",str(last.get('steps','—')))]
    for c,(label,value) in zip(cols,vals): c.metric(label,value)
    st.subheader("What needs attention")
    if logs: st.info("Log consistent daily values to reveal useful trends. If a value worries you, discuss it with a qualified clinician.")
    else: st.info("Start with your profile and a daily health log.")

elif page=="Health Profile":
    st.header("My Health Profile")
    with st.form("profile"):
        c1,c2,c3=st.columns(3); n=c1.text_input("Name", value=profile['name'] if profile else ''); age=c2.number_input("Age",1,120,value=int(profile['age'] or 22) if profile else 22); gender=c3.selectbox("Gender",["Prefer not to say","Female","Male","Other"], index=0)
        h=c1.number_input("Height (cm)",80.,230.,value=float(profile['height'] or 170) if profile else 170.); w=c2.number_input("Weight (kg)",20.,250.,value=float(profile['weight'] or 65) if profile else 65.); c3.metric("BMI",bmi(w,h))
        conditions=st.text_area("Existing conditions",value=profile['conditions'] if profile else ''); allergies=st.text_area("Allergies",value=profile['allergies'] if profile else '')
        goal=st.selectbox("Health goal",["General wellness","Weight management","Fitness","Better sleep","Diabetes prevention"]); diet=st.selectbox("Diet preference",["Vegetarian","Non-vegetarian","Vegan","No preference"]); contact=st.text_input("Emergency contact",value=profile['emergency_contact'] if profile else '')
        if st.form_submit_button("Save profile"):
            execute("INSERT INTO profiles VALUES(?,?,?,?,?,?,?,?,?,?,?) ON CONFLICT(user_id) DO UPDATE SET name=excluded.name,age=excluded.age,gender=excluded.gender,height=excluded.height,weight=excluded.weight,conditions=excluded.conditions,allergies=excluded.allergies,goal=excluded.goal,diet=excluded.diet,emergency_contact=excluded.emergency_contact",(uid,n,age,gender,h,w,conditions,allergies,goal,diet,contact)); st.success("Profile saved.")

elif page=="Daily Tracker":
    st.header("Daily Health Tracker")
    with st.form("log"):
        c=st.columns(4); weight=c[0].number_input("Weight (kg)",20.,250.,65.); water=c[1].number_input("Water (L)",0.,10.,2.); sleep=c[2].number_input("Sleep (hours)",0.,24.,7.); steps=c[3].number_input("Steps",0,100000,5000)
        systolic=c[0].number_input("BP systolic",0.,250.,120.); diastolic=c[1].number_input("BP diastolic",0.,180.,80.); glucose=c[2].number_input("Glucose (mg/dL)",0.,600.,100.); hr=c[3].number_input("Heart rate",0.,250.,72.)
        spo2=c[0].number_input("SpO₂ (%)",0.,100.,98.); stress=c[1].slider("Stress",1,10,5); note=st.text_area("Notes or symptoms")
        if st.form_submit_button("Save today’s log"):
            execute("INSERT INTO health_logs(user_id,logged_on,weight,water,sleep,steps,systolic,diastolic,glucose,heart_rate,spo2,stress,note) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",(uid,today(),weight,water,sleep,steps,systolic,diastolic,glucose,hr,spo2,stress,note)); st.success(f"Saved. Daily health score: {health_score({'water':water,'sleep':sleep,'steps':steps,'spo2':spo2})}/100")

elif page=="AI Health Assistant":
    st.header("AI Health Assistant")
    st.info("Ask general wellness questions in English, Hindi, or Hinglish. This assistant does not diagnose or prescribe.")
    for row in all_rows("SELECT role,message FROM chats WHERE user_id=? ORDER BY id DESC LIMIT 12",(uid,))[::-1]:
        with st.chat_message(row['role']): st.markdown(row['message'])
    q=st.chat_input("Ask about reports, habits, sleep, fitness, or preparing for a doctor visit")
    if q:
        execute("INSERT INTO chats(user_id,created_on,role,message) VALUES(?,?,?,?)",(uid,today(),'user',q)); context=f"Profile: {dict(profile) if profile else {}}; latest log: {dict(all_rows('SELECT * FROM health_logs WHERE user_id=? ORDER BY id DESC LIMIT 1',(uid,))[0]) if all_rows('SELECT * FROM health_logs WHERE user_id=? ORDER BY id DESC LIMIT 1',(uid,)) else {}}"
        ans=reply(q,context); execute("INSERT INTO chats(user_id,created_on,role,message) VALUES(?,?,?,?)",(uid,today(),'assistant',ans)); st.rerun()

elif page=="Symptom Checker":
    st.header("Symptom Checker & Triage")
    text=st.text_area("Describe symptoms"); severity=st.select_slider("Severity",options=["Mild","Moderate","Severe"])
    if st.button("Check urgency") and text:
        level,msg=triage(text,severity); st.markdown(f"### {level}\n{msg}"); st.caption("This is not a medical diagnosis. Seek professional care for concerning symptoms.")

elif page=="Report Analyzer":
    st.header("Medical Report Analyzer")
    f=st.file_uploader("Upload a text PDF report",type=['pdf','txt'])
    if f and st.button("Analyze report"):
        raw=f.read(); text=fitz.open(stream=raw,filetype='pdf').get_page_text(0) if f.name.endswith('.pdf') else raw.decode(errors='ignore'); labs=extract_labs(text)
        execute("INSERT INTO reports(user_id,uploaded_on,filename,extracted_text,summary) VALUES(?,?,?,?,?)",(uid,today(),f.name,text[:10000],"Local extraction complete")); st.success("Report saved.")
        if labs: st.dataframe(pd.DataFrame(labs),use_container_width=True)
        else: st.warning("No supported common lab values were confidently extracted. Verify the original report.")
        st.markdown(reply("Explain these lab results in simple language and suggest doctor questions: "+str(labs)))

elif page=="Risk Prediction":
    st.header("Explainable Diabetes Risk Screening")
    st.caption("Educational screening model, not a diagnosis.")
    c=st.columns(4); age=c[0].number_input("Age",1,120,30); b=c[1].number_input("BMI",10.,70.,25.); glucose=c[2].number_input("Glucose",30.,500.,100.); bp=c[3].number_input("Systolic BP",50.,250.,120.)
    if st.button("Estimate risk"):
        prob,risk,factors=diabetes_risk(age,b,glucose,bp); execute("INSERT INTO predictions(user_id,created_on,model,probability,risk,factors) VALUES(?,?,?,?,?,?)",(uid,today(),'diabetes-screen',prob,risk,json.dumps(factors))); st.metric("Estimated risk",risk,f"{prob:.0%} screening probability"); st.write("**Factors used (transparent explanation):**"); st.write(factors)

elif page=="Wellness Planner":
    st.header("Personalized Wellness Planner")
    if not profile: st.warning("Save your health profile first.")
    else:
        prompt=f"Create a safe practical Indian diet and beginner workout plan for a {profile['age']}-year-old with goal {profile['goal']}, diet {profile['diet']}, conditions {profile['conditions']}."; st.markdown(reply(prompt, str(dict(profile))))

elif page=="Analytics & Timeline":
    st.header("Health Analytics & Timeline")
    logs=all_rows("SELECT * FROM health_logs WHERE user_id=? ORDER BY logged_on",(uid,))
    if logs:
        df=pd.DataFrame([dict(x) for x in logs]); st.plotly_chart(px.line(df,x='logged_on',y=['weight','glucose','sleep','water'],markers=True),use_container_width=True); st.dataframe(df[['logged_on','note','weight','glucose','sleep','steps']],use_container_width=True)
    else: st.info("Add daily logs to see trends.")

else:
    st.header("Appointments & Emergency")
    with st.form("appt"):
        d=st.date_input("Appointment date",date.today()); doctor=st.text_input("Doctor/clinic"); specialty=st.text_input("Specialty"); purpose=st.text_input("Purpose")
        if st.form_submit_button("Save appointment"): execute("INSERT INTO appointments(user_id,scheduled_for,doctor,specialty,purpose) VALUES(?,?,?,?,?)",(uid,d.isoformat(),doctor,specialty,purpose)); st.success("Appointment saved.")
    st.subheader("Emergency guidance")
    contact=profile['emergency_contact'] if profile else ''
    st.error("For chest pain, serious breathing difficulty, fainting, severe bleeding, or immediate danger, contact local emergency services or go to the nearest emergency department. This application cannot place emergency calls.")
    if contact: st.write(f"Saved emergency contact: {contact}")
