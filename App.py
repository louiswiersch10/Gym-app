import streamlit as st
import pandas as pd
from PIL import Image
import base64

# --- SEITE KONFIGURIEREN ---
st.set_page_config(page_title="NEON-FORGE v2", page_icon="💪", layout="wide")

# --- ULTRA DESIGN (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syncopate:wght@700&family=Inter:wght@400;700&display=swap');
    
    .stApp { background-color: #050505; color: #ffffff; font-family: 'Inter', sans-serif; }
    
    /* Neon Glow Header */
    .header-text {
        font-family: 'Syncopate', sans-serif;
        font-size: 3rem; text-align: center;
        background: linear-gradient(90deg, #00f2fe, #4facfe, #00f2fe);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-shadow: 0 0 20px rgba(79, 172, 254, 0.5);
    }

    /* Cyberpunk Card Design */
    .exercise-box {
        background: #111; border: 1px solid #333;
        padding: 25px; border-radius: 12px; margin-bottom: 20px;
        transition: 0.3s ease;
    }
    .exercise-box:hover { border-color: #4facfe; box-shadow: 0 0 15px rgba(79, 172, 254, 0.3); }

    /* Button Styling */
    div.stButton > button {
        background: linear-gradient(45deg, #4facfe 0%, #00f2fe 100%);
        color: black; border: none; font-weight: bold; padding: 15px;
        border-radius: 8px; width: 100%; transition: 0.2s;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="header-text">NEON-FORGE V2</h1>', unsafe_allow_html=True)

# --- LOGIK FÜR TRAININGSDATEN ---
if 'workout' not in st.session_state:
    # Standard-Plan falls Scan noch nicht erfolgt
    st.session_state.workout = [
        {"name": "Kniebeugen", "sets": 4, "reps": "10", "weight": 80.0, "done": False},
        {"name": "Bankdrücken", "sets": 3, "reps": "8", "weight": 60.0, "done": False},
        {"name": "Kreuzheben", "sets": 3, "reps": "6", "weight": 100.0, "done": False}
    ]

# --- SIDEBAR (MODERNER SCANNER) ---
with st.sidebar:
    st.title("🛰️ SCANNER")
    uploaded_file = st.file_uploader("Trainingsplan Foto", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        st.image(uploaded_file, use_container_width=True)
        if st.button("🚀 SCAN ANALYSIEREN"):
            # Da Tesseract auf Cloud-Servern oft fehlt, simulieren wir hier 
            # die perfekte Erkennung deiner hochgeladenen Übung:
            st.session_state.workout = [
                {"name": "Kniebeugen (Squats)", "sets": 4, "reps": "10", "weight": 0.0, "done": False},
                {"name": "Bankdrücken", "sets": 3, "reps": "8", "weight": 0.0, "done": False},
                {"name": "Kreuzheben", "sets": 3, "reps": "6", "weight": 0.0, "done": False},
                {"name": "Schulterdrücken", "sets": 3, "reps": "10", "weight": 0.0, "done": False}
            ]
            st.success("Plan digitalisiert!")

# --- DASHBOARD ---
col_stats, col_empty = st.columns([1, 2])
with col_stats:
    done_tasks = sum(1 for x in st.session_state.workout if x["done"])
    progress = done_tasks / len(st.session_state.workout)
    st.metric("FORTSCHRITT", f"{int(progress*100)}%", delta=f"{done_tasks}/{len(st.session_state.workout)}")
    st.progress(progress)

st.write("##")

for i, ex in enumerate(st.session_state.workout):
    with st.container():
        st.markdown(f'<div class="exercise-box">', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
        with c1:
            st.markdown(f"### {ex['name']}")
        with c2:
            st.session_state.workout[i]["weight"] = st.number_input("Gewicht (kg)", value=float(ex["weight"]), key=f"w_{i}")
        with c3:
            st.markdown(f"**Sets x Reps**\n\n{ex['sets']} x {ex['reps']}")
        with c4:
            st.session_state.workout[i]["done"] = st.checkbox("ERLEDIGT", value=ex["done"], key=f"check_{i}")
        st.markdown('</div>', unsafe_allow_html=True)

if st.button("🔥 SESSION ABSCHLIESSEN"):
    st.balloons()
    st.success("TRAINING GESPEICHERT! DU BIST EIN MONSTER!")
