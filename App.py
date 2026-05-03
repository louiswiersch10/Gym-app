import streamlit as st
import re

# --- CONFIG & NEON DESIGN ---
st.set_page_config(page_title="CORE VISION AI", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syncopate:wght@700&family=Inter:wght@400;700&display=swap');
    .stApp { background-color: #050505; color: white; font-family: 'Inter', sans-serif; }
    .neon-text {
        font-family: 'Syncopate', sans-serif; text-align: center;
        background: linear-gradient(90deg, #00f2fe, #4facfe);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 3rem; margin-bottom: 20px;
    }
    .day-container { border-left: 4px solid #00f2fe; padding-left: 20px; margin-top: 40px; margin-bottom: 10px; }
    .exercise-card { background: #111; border: 1px solid #222; border-radius: 12px; padding: 15px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="neon-text">CORE VISION V3</h1>', unsafe_allow_html=True)

# --- SMART PARSER LOGIK ---
def parse_custom_plan(raw_text):
    days = {}
    current_day = "DEIN PLAN"
    
    lines = raw_text.split('\n')
    for line in lines:
        line = line.strip()
        if not line: continue
        
        # Erkennt Tage (z.B. "Tag 1", "Montag", "Tag 2")
        if re.search(r'(Tag|TAG|Day|DAY|Montag|Mittwoch|Freitag)', line):
            current_day = line
            days[current_day] = []
            continue
        
        if current_day not in days: days[current_day] = []
        
        # Versucht Übung, Sätze und Wdh zu trennen
        nums = re.findall(r'\d+', line)
        s = nums[0] if len(nums) > 0 else "3"
        w = nums[1] if len(nums) > 1 else "10"
        name = re.sub(r'\d+|Sätze|Wdh|wdh|x|X|-', '', line).strip()
        
        days[current_day].append({"name": name if name else "Übung", "sets": s, "reps": w, "kg": 0.0, "done": False})
    return days

# --- INPUT AREA ---
with st.expander("📝 PLAN-TEXT HIER EINFÜGEN (VOM FOTO KOPIERT)", expanded=True):
    raw_input = st.text_area("Tippe deinen Plan ein oder kopiere den Text aus deinem Foto hierher:", 
                             placeholder="Tag 1:\n1. Kniebeugen 4x10\n2. Bankdrücken 3x8\n\nTag 2:\n1. Kreuzheben 3x6", height=150)
    if st.button("🚀 PLAN GENERIEREN"):
        st.session_state.full_plan = parse_custom_plan(raw_input)
        st.success("Plan erfolgreich strukturiert!")

# --- DISPLAY ---
if 'full_plan' in st.session_state:
    for day, exercises in st.session_state.full_plan.items():
        st.markdown(f'<div class="day-container"><h2>{day}</h2></div>', unsafe_allow_html=True)
        
        for i, ex in enumerate(exercises):
            st.markdown('<div class="exercise-card">', unsafe_allow_html=True)
            c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
            with c1:
                st.markdown(f"**{ex['name']}**")
            with c2:
                ex["kg"] = st.number_input("KG", 0.0, step=2.5, key=f"k_{day}_{i}")
            with c3:
                st.markdown(f"Ziel: **{ex['sets']} x {ex['reps']}**")
            with c4:
                ex["done"] = st.checkbox("DONE", key=f"d_{day}_{i}")
            st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔥 TRAINING BEENDEN"):
        st.balloons()
        st.success("Mega! Training für heute abgeschlossen.")

