import streamlit as st
import pandas as pd
from PIL import Image
import io

# App-Konfiguration für Mobile-Optik
st.set_page_config(page_title="TrainingsPlan Digital", layout="centered")

# Styling für bessere Buttons auf dem Handy
st.markdown("""
    <style>
    .stButton>button { width: 100%; height: 3em; border-radius: 10px; }
    .stDataFrame { border: 1px solid #4CAF50; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏋️ Mein Digitaler Plan")

# SEKTION 1: Plan hochladen
with st.expander("📸 Neuen Plan scannen / hochladen", expanded=True):
    uploaded_file = st.file_uploader("Bild vom Trainingsplan", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="Dein Originalplan", use_container_width=True)
        st.success("Bild erfolgreich geladen!")

st.divider()

# SEKTION 2: Digitale Erfassung (Vorausgefüllte Vorlage)
st.subheader("📝 Training tracken")
st.info("Tippe in die Felder, um Gewicht oder Wiederholungen zu ändern.")

# Beispiel-Datenstruktur, die normalerweise per KI aus dem Bild käme
# Hier kannst du deine Standardübungen eintragen
if 'df' not in st.session_state:
    data = {
        "Übung": ["Bankdrücken", "Kniebeugen", "Schulterdrücken", "Bizeps-Curls"],
        "Sätze": ["3", "4", "3", "3"],
        "Ziel-Wdh": ["8-12", "6-10", "10", "12"],
        "Gewicht (kg)": [60.0, 80.0, 40.0, 12.5],
        "Done": [False, False, False, False]
    }
    st.session_state.df = pd.DataFrame(data)

# Der interaktive Editor - hier drückst du nur noch auf die Zahlen
edited_df = st.data_editor(
    st.session_state.df,
    column_config={
        "Done": st.column_config.CheckboxColumn("Erledigt?"),
        "Gewicht (kg)": st.column_config.NumberColumn("Kg", format="%.1f"),
        "Übung": st.column_config.TextColumn("Übung", disabled=True)
    },
    hide_index=True,
    num_rows="dynamic"
)

# SEKTION 3: Speichern
if st.button("Training abschließen & Speichern"):
    st.session_state.df = edited_df
    st.balloons()
    st.success("Training lokal gespeichert! Top Leistung!")
    
    # Export-Option für Excel/CSV
    csv = edited_df.to_csv(index=False).encode('utf-8')
    st.download_button("Plan als CSV Datei laden", data=csv, file_name="training_log.csv")
