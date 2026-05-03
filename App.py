import streamlit as st
import pandas as pd

# --- CONFIG & STYLING ---
st.set_page_config(page_title="CORE-AI WORKOUT", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;700&display=swap');
    .stApp { background-color: #000000; color: #ffffff; font-family: 'Inter', sans-serif; }
    
    /* Neon Glow Design */
    .main-title {
        font-size: 3.5rem; font-weight: 700; text-align: center;
        background: linear-gradient(135deg, #60efff 0%, #00ff87 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 30px;
    }
    
    .card {
        background: #111111; border: 1px solid #222;
        border-radius: 15px; padding: 20px; margin-bottom: 15px;
        transition: 0.3s;
    }
    .card:hover { border-color: #00ff87; box-shadow: 0 0 20px rgba(0, 255, 135, 0.1); }
    
    /* Input Styling */
    input { background-color: #1a1a1a !important; color: white !important; border-radius: 8px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- APP LOGIK (DYNAMIC) ---
if 'workout_list' not in st.session_state:
    st.session_state.workout_list = []

def add_exercise():
    st.session_state.workout_list.append({"name": "Neue Übung", "sets": 3, "reps": "12", "weight": 0.0, "done": False})

def clear_plan():
    st.session_state.workout_list = []

# --- HEADER ---
st.markdown('<h1 class="main-title">CORE-AI TRACKER</h1>', unsafe_allow_html=True)

# --- SMART CONTROLS ---
col_a, col_b, col_c = st.columns([1,1,1])
with col_a:
    if st.button("➕ ÜBUNG HINZUFÜGEN"):
        add_exercise()
with col_b:
    if st.button("🗑️ PLAN LEEREN"):
        clear_plan()
with col_c:
    # Hier simulieren wir den "Universal-Import"
    if st.button("📸 SCAN-DATEN IMPORTIEREN"):
        # Diese Liste könnte von jeder KI kommen - sie ist absolut flexibel
        st.session_state.workout_list = [
            {"name": "Kniebeugen", "sets": 4, "reps": "10", "weight": 80.0, "done": False},
            {"name": "Bankdrücken", "sets": 3, "reps": "8", "weight": 60.0, "done": False},
            {"name": "Kreuzheben", "sets": 3, "reps": "6", "weight": 100.0, "done": False}
        ]

st.markdown("---")

# --- DYNAMISCHE LISTE ---
if not st.session_state.workout_list:
    st.info("Dein Plan ist leer. Füge Übungen hinzu oder nutze den Scan-Import.")
else:
    for i, ex in enumerate(st.session_state.workout_list):
        st.markdown('<div class="card">', unsafe_allow_html=True)
        c1, c2, c3, c4, c5 = st.columns([2, 1, 1, 1, 0.5])
        
        with c1:
            st.session_state.workout_list[i]["name"] = st.text_input(f"Übung {i+1}", value=ex["name"], key=f"n_{i}")
        with c2:
            st.session_state.workout_list[i]["weight"] = st.number_input("KG", value=float(ex["weight"]), key=f"w_{i}", step=2.5)
        with c3:
            st.session_state.workout_list[i]["sets"] = st.number_input("Sätze", value=int(ex["sets"]), key=f"s_{i}")
        with c4:
            st.session_state.workout_list[i]["reps"] = st.text_input("Wdh", value=ex["reps"], key=f"r_{i}")
        with c5:
            st.write("Done")
            st.session_state.workout_list[i]["done"] = st.checkbox("", value=ex["done"], key=f"d_{i}")
        st.markdown('</div>', unsafe_allow_html=True)

# --- PROGRESS & FINISH ---
if st.session_state.workout_list:
    done_count = sum(1 for x in st.session_state.workout_list if x["done"])
    progress = done_count / len(st.session_state.workout_list)
    
    st.write("##")
    st.markdown(f"### Fortschritt: {int(progress*100)}%")
    st.progress(progress)
    
    if st.button("🚀 SESSION ABSCHLIESSEN"):
        st.balloons()
        st.success("Training beendet! Alle Daten wurden optimiert.")
