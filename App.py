import streamlit as st
import pandas as pd
from PIL import Image
import datetime

# --- OPTIK & THEME ---
st.set_page_config(page_title="PRO-Gym Tracker", page_icon="💪", layout="wide")

# Custom CSS für den "Coolness-Faktor"
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div.stButton > button:first-child {
        background-color: #00ffbd; color: black; border: none;
        font-weight: bold; border-radius: 20px; transition: 0.3s;
    }
    div.stButton > button:hover { background-color: #00d4a0; transform: scale(1.05); }
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 20px; border-radius: 15px; border-left: 5px solid #00ffbd;
    }
    </style>
    """, unsafe_allow_html=True)

# --- APP HEADER ---
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🚀 PRO-Gym Tracker")
    st.write(f"Willkommen zurück! Heute ist {datetime.date.today().strftime('%d. %B %Y')}")

with col2:
    if st.button("🔄 Reset Plan"):
        st.session_state.clear()
        st.rerun()

# --- SIDEBAR: PHOTO UPLOAD ---
with st.sidebar:
    st.header("📸 Plan Scan")
    uploaded_file = st.file_uploader("Foto hochladen", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        st.image(uploaded_file, caption="Dein Original-Plan")
        st.success("Scan bereit!")

# --- TRAININGSDATEN ---
if 'workout_data' not in st.session_state:
    st.session_state.workout_data = [
        {"Übung": "Bankdrücken", "Sätze": 3, "Wdh": "10", "Gewicht": 60.0, "Erledigt": False},
        {"Übung": "Kniebeugen", "Sätze": 4, "Wdh": "8", "Gewicht": 80.0, "Erledigt": False},
        {"Übung": "Kreuzheben", "Sätze": 3, "Wdh": "5", "Gewicht": 100.0, "Erledigt": False},
        {"Übung": "Klimmzüge", "Sätze": 3, "Wdh": "Max", "Gewicht": 0.0, "Erledigt": False},
    ]

# --- DASHBOARD LAYOUT ---
st.subheader("Dein Workout heute:")

# Fortschrittsbalken berechnen
done_count = sum(1 for ex in st.session_state.workout_data if ex["Erledigt"])
progress = done_count / len(st.session_state.workout_data)
st.progress(progress)
st.write(f"Fortschritt: {int(progress*100)}%")

# Übungen als interaktive Liste
for i, exercise in enumerate(st.session_state.workout_data):
    with st.container():
        # Karten-Optik für jede Übung
        c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
        
        with c1:
            st.markdown(f"### {exercise['Übung']}")
        with c2:
            st.session_state.workout_data[i]["Gewicht"] = st.number_input(
                "Kg", value=exercise["Gewicht"], key=f"w_{i}", step=2.5
            )
        with c3:
            st.session_state.workout_data[i]["Sätze"] = st.number_input(
                "Sätze", value=exercise["Sätze"], key=f"s_{i}"
            )
        with c4:
            st.write("Status")
            st.session_state.workout_data[i]["Erledigt"] = st.checkbox(
                "Fertig", value=exercise["Erledigt"], key=f"c_{i}"
            )
        st.divider()

# --- SAVE BUTTON ---
if st.button("🏁 TRAINING BEENDEN"):
    st.balloons()
    st.confetti() # Falls verfügbar, sonst Ballons
    st.success(f"Mega! Du hast {done_count} Übungen durchgezogen!")
    
    # Tabelle für den Export
    final_df = pd.DataFrame(st.session_state.workout_data)
    st.dataframe(final_df)
