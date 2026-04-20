import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Profil Étudiant", layout="wide")

st.title("👤 Profil Intelligent de l'Étudiant")

DATA_FILE = "data_students.csv"
st.divider()
# =========================
# CHARGEMENT DONNÉES
# =========================
@st.cache_data
def load_data():
    return pd.read_csv(DATA_FILE)

try:
    df = load_data()
except:
    st.error("❌ Aucune donnée disponible.")
    st.stop()

# =========================
# FORMULAIRE PROFIL
# =========================
st.subheader("📥 Entre tes données pour analyse")

col1, col2 = st.columns(2)

with col1:
    heures_etude = st.slider("📚 Heures d'étude/jour", 0, 12, 3)
    sommeil = st.slider("😴 Heures de sommeil", 0, 12, 6)
    stress = st.slider("😰 Stress (1-10)", 1, 10, 5)

with col2:
    motivation = st.slider("🔥 Motivation (1-10)", 1, 10, 5)
    concentration = st.slider("🧠 Concentration (1-10)", 1, 10, 5)
    telephone = st.slider("📱 Temps téléphone (h)", 0, 12, 4)
st.divider()
# =========================
# SCORE DE RISQUE
# =========================
st.subheader("🧠 Résultat d'analyse")

# Normalisation simple
stress_n = stress / 10
sommeil_risk = max(0, (7 - sommeil) / 7)
etude_risk = max(0, (4 - heures_etude) / 4)
motivation_risk = (10 - motivation) / 10

# SCORE GLOBAL
score_risque = (
    0.35 * stress_n +
    0.25 * sommeil_risk +
    0.25 * etude_risk +
    0.15 * motivation_risk
)

# =========================
# INTERPRÉTATION
# =========================
if score_risque < 0.3:
    niveau = "🟢 Faible risque"
    commentaire = "Tu es sur une bonne trajectoire 👍"
elif score_risque < 0.6:
    niveau = "🟠 Risque moyen"
    commentaire = "Attention à ton équilibre travail/repos ⚠️"
else:
    niveau = "🔴 Risque élevé"
    commentaire = "Risque de baisse de performance important ❌"

st.metric("Score de risque", round(score_risque, 2))
st.subheader(niveau)
st.write(commentaire)
st.divider()

# =========================
# RADAR SIMPLE (VISUEL)
# =========================
st.subheader("📡 Profil global")

categories = ["Étude", "Sommeil", "Stress", "Motivation"]
values = [
    heures_etude/12,
    sommeil/12,
    stress/10,
    motivation/10
]

st.bar_chart(dict(zip(categories, values)))

# =========================
# RECOMMANDATIONS AUTOMATIQUES
# =========================
st.subheader("💡 Recommandations personnalisées")

if sommeil < 6:
    st.info("😴 Essaie de dormir au moins 6h par nuit")

if heures_etude < 4:
    st.info("📚 Augmente progressivement ton temps d'étude")

if stress > 7:
    st.info("🧘 Fais des pauses, des distractions et gère ton stress")

if motivation < 5:
    st.info("🔥 Fixe-toi des objectifs courts et motivants")

if telephone > 6:
    st.info("📵 Réduis le temps passé sur téléphone")
else:
    st.info("🟩 Allez, nos encouragements")