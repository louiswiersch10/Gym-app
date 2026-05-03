import streamlit as st
import pandas as pd
from PIL import Image
import pytesseract
import re

# --- KONFIGURATION ---
st.set_page_config(page_title="NEON-FORGE ULTRA", page_icon="⚡", layout="wide")

# --- HIGH-END STYLING (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    .stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: #00ffcc; font-family: 'Orbitron', sans-serif; }
    
    /* Glasmorphismus Effekt für Karten */
    .exercise-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 255, 204, 0.3);
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 8px 32px 0 rgba(0, 255, 204, 0.2);
    }
    
    /* Neon Button */
    div.stButton > button {
        background: none; color: #00ffcc;
        border: 2px solid #00ffcc; border-radius: 50px;
        font-weight: bold; text-transform: uppercase;
        letter-spacing: 2px; transition: 0.4s;
        width: 100%; box-shadow: 0 0 10px #00ffcc;
    }
    div.stButton > button:hover {
        background: #00ffcc; color: #000;
        box-shadow: 0 0 30px #00ffcc; transform: translateY(-3px);
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNKTION: KI SCANNER ---
def scan_image(image):
    # Erkennt Text auf dem Bild
    text = pytesseract.image_to_string(image, lang='deu+eng')
    # Suche nach Mustern wie "Übung - Sätze x Wdh"
    lines = text.split('\n')
    extracted_data = []
    for line in lines:
        if len(line.strip()) > 5:
            # Versuche Zahlen zu finden für Sätze/Wdh
            numbers = re.findall(r'\d+', line)
            saetze = numbers[0] if len(numbers) > 0 else "3"
            wdh = numbers[1] if len(numbers) > 1 else "10"
            name = re.sub(r'[^a-zA-ZäöüÄÖÜ\s]', '', line).strip()
            if name:
                extracted_data.append({"Übung": name[:20], "Sätze": saetze, "Wdh": wdh, "Kg": 0.0, "Done": False})
    return extracted_data

# --- APP LOGIK ---
st.title("⚡ NEON-FORGE ULTRA")
st.markdown("---")

if 'exercises' not in st.session_state:
    st.session_state.exercises = []

# SIDEBAR FÜR DEN SCAN
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/684/684062.png", width=100)
    st.header("SYSTEM SCAN")
    uploaded_file = st.file_uploader("Trainingsplan scannen", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="Scan-Quelle")
        if st.button("KI-ANALYSE STARTEN"):
            with st.spinner("Extrahiere Daten..."):
                st.session_state.exercises = scan_image(img)
            st.success("Plan digitalisiert!")

# HAUPTANSICHT
if not st.session_state.exercises:
    st.warning("KEIN PLAN AKTIV. Lade ein Bild hoch oder scanne deinen Plan.")
else:
    col1, col2 = st.columns([2,1])
    
    with col2:
        done_count = sum(1 for ex in st.session_state.exercises if ex["Done"])
        total = len(st.session_state.exercises)
        st.metric("POWER LEVEL", f"{int((done_count/total)*100)}%")
        st.progress(done_count/total)

    with col1:
        for i, ex in enumerate(st.session_state.exercises):
            st.markdown(f'<div class="exercise-card">', unsafe_allow_html=True)
            c1, c2, c3, c4 = st.columns([2,1,1,1])
            with c1:
                st.markdown(f"**{ex['Übung']}**")
            with c2:
                st.session_state.exercises[i]["Kg"] = st.number_input("KG", value=float(ex["Kg"]), key=f"k{i}", step=2.5)
            with c3:
                st.write(f"{ex['Sätze']}x{ex['Wdh']}")
            with c4:
                st.session_state.exercises[i]["Done"] = st.checkbox("DONE", value=ex["Done"], key=f"d{i}")
            st.markdown('</div>', unsafe_allow_html=True)

if st.button("MISSION COMPLETE"):
    st.balloons()
    st.snow()
    st.success("WORKOUT GESPEICHERT. DU BIST EINE MASCHINE!")
