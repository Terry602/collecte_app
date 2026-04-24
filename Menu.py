import streamlit as st
import pandas as pd
import plotly.express as px
import time
import numpy as np
import streamlit.components.v1 as components

# ==========================================================
#  CONFIG PAGE
# ==========================================================
st.set_page_config(
    page_title="SmartStudent Analytics - Advanced",
    layout="wide"
)

# ==========================================================
#  CHARGEMENT DONNÉES
# ==========================================================
@st.cache_data(ttl=5)
def load_data():
    return pd.read_csv("data_students.csv")
try:
    df = load_data()
except:
    st.error(" Aucune donnée disponible, veuillez remplir le formulaire dans le menu retractable.")
    st.stop()

# ==========================================================
#  HEADER
# ==========================================================
components.html("""
<div style="
    background: linear-gradient(135deg, #0F172A, #111827);
    padding: 28px 20px;
    border-radius: 18px;
    border: 1px solid #1F2937;
    text-align: center;
    margin-bottom: 18px;
    box-shadow: 0 10px 35px rgba(0,0,0,0.35);
    font-family: Arial;
">

    <div style="
        display:flex;
        align-items:center;
        justify-content:center;
        gap:14px;
    ">

        <!-- 🧠 AI + DATA NETWORK ICON (WOW STYLE) -->
        <svg width="48" height="48" viewBox="0 0 24 24"
             fill="none"
             stroke="#22D3EE"
             stroke-width="2.2"
             stroke-linecap="round"
             stroke-linejoin="round">

            <!-- brain core -->
            <path d="M9 3c-2 0-3.5 1.5-3.5 3.5S7 10 7 10"/>
            <path d="M15 3c2 0 3.5 1.5 3.5 3.5S17 10 17 10"/>
            <path d="M7 10c-1.5 0-2.5 1-2.5 2.5S6 15 7 15"/>
            <path d="M17 10c1.5 0 2.5 1 2.5 2.5S18 15 17 15"/>

            <!-- data network nodes -->
            <circle cx="5" cy="18" r="1.2"/>
            <circle cx="12" cy="20" r="1.2"/>
            <circle cx="19" cy="18" r="1.2"/>

            <!-- connections -->
            <line x1="7" y1="14" x2="5" y2="18"/>
            <line x1="12" y1="14" x2="12" y2="20"/>
            <line x1="17" y1="14" x2="19" y2="18"/>

        </svg>

        <div style="
            font-size:25px;
            font-weight:800;
            color:#F8FAFC;
            letter-spacing:-0.5px;
        ">
             Application d'Analyse des Étudiants
        </div>

    </div>

    <div style="
        display:inline-block;
        margin-top:14px;
        padding:6px 14px;
        font-size:12px;
        color:#22D3EE;
        border:1px solid rgba(34, 211, 238, 0.3);
        border-radius:20px;
        background: rgba(34, 211, 238, 0.08);
    ">
        AI • Data Science • Predictive Intelligence
    </div>

</div>
""", height=200)
st.divider()

# =========================
# DATA 
# =========================
  # refresh auto toutes les 5 secondes
def load_data():
    return pd.read_csv("data_students.csv")


    df = load_data()
st.markdown("""
<div style="
    font-size:14px;
    color:#94A3B8;
    margin-top:10px;
    letter-spacing:0.3px;
">
    Dashboard intelligent d’analyse des performances étudiantes basé sur la Data Science & l’IA
</div>
""", unsafe_allow_html=True)

st.divider()

# =========================
# OBJECTIFS (ANIMATION ULTRA FLUIDE - VERSION AMÉLIORÉE)
# =========================

st.markdown("### 🧭 Objectif du projet")

st.components.v1.html("""
<style>
.container {
    position: relative;
    height: 100px;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* OBJECTIF GLOBAL */
.objective {
    position: absolute;
    opacity: 0;
    text-align: center;
    padding: 18px 28px;
    border-radius: 14px;
    border: 1px solid #E5E7EB;
    background: #FFFFFF;
    box-shadow: 0 6px 18px rgba(0,0,0,0.06);
    transition: opacity 0.8s ease, transform 0.8s ease;
    transform: translateY(10px);
    width: 80%;
}

/* TITRE */
.title {
    font-size: 13px;
    font-weight: 500;
    margin-bottom: 4px;
}

/* DESCRIPTION */
.desc {
    font-size: 13px;
    color: #000000;
}

/* ACTIVE */
.objective.active {
    opacity: 1;
    transform: translateY(0);
}
</style>

<div class="container">

    <div class="objective active">
        <div class="title" style="color:#2563EB;">Collecte intelligente des données</div>
        <div class="desc">Centralisation et structuration des données étudiantes pour analyse.</div>
    </div>

    <div class="objective">
        <div class="title" style="color:#059669;">Analyse comportementale & académique</div>
        <div class="desc">Étude des performances et comportements des étudiants.</div>
    </div>

    <div class="objective">
        <div class="title" style="color:#7C3AED;"> Identification des facteurs de réussite</div>
        <div class="desc">Détection des variables influençant les résultats académiques.</div>
    </div>

    <div class="objective">
        <div class="title" style="color:#DC2626;"> Prédiction des performances</div>
        <div class="desc">Utilisation de modèles IA pour anticiper les résultats.</div>
    </div>

    <div class="objective">
        <div class="title" style="color:#EA580C;"> Génération de rapports intelligents</div>
        <div class="desc">Production automatique d’insights pour la prise de décision.</div>
    </div>

    <div class="objective">
        <div class="title" style="color:#0EA5E9;"> Data Cleaning & Preprocessing</div>
        <div class="desc">Nettoyage, transformation et préparation des données.</div>
    </div>

    <div class="objective">
        <div class="title" style="color:#16A34A;"> Data Visualization Avancée</div>
        <div class="desc">Création de dashboards interactifs et visuels.</div>
    </div>

    <div class="objective">
        <div class="title" style="color:#9333EA;"> Feature Engineering & Model Evaluation</div>
        <div class="desc">Optimisation des variables et évaluation des modèles.</div>
    </div>

</div>

<script>
let index = 0;
const items = document.querySelectorAll('.objective');

function showNext() {
    items[index].classList.remove('active');
    index = (index + 1) % items.length;
    items[index].classList.add('active');
}

setInterval(showNext, 3000);
</script>
""", height=140)

st.divider()

# =========================
# KPI CARDS
# =========================
st.markdown("""
<style>

/* ===== SOFT KPI CARDS (SAAS STYLE) ===== */
.card {
    background: linear-gradient(135deg, #FFFFFF, #F8FAFC);
    border: 1px solid #E2E8F0;
    border-radius: 16px;
    padding: 10px 8px;
    text-align: center;
    box-shadow: 0 6px 18px rgba(15, 23, 42, 0.06);
    transition: all 0.25s ease;
}

/* hover effect */
.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 25px rgba(99, 102, 241, 0.15);
    border-color: #C7D2FE;
}

/* icon */
.icon {
    font-size: 12px;
    margin-bottom: 6px;
}

/* KPI number */
.kpi {
    font-size: 14px;
    font-weight: 500;
    color: #0F172A;
    letter-spacing: -0.5px;
}

/* label */
.small {
    font-size: 12.5px;
    color: #64748B;
    margin-top: 4px;
}

/* section title */
h2 {
    font-size: 22px;
    font-weight: 800;
    color: #0F172A;
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)
st.markdown("## 🌍 Indicateurs globaux")

col1, col2, col3, col4 = st.columns(4)

# sécurisation des valeurs (évite NaN / erreurs)
nb_etudiants = len(df)
moyenne_gen = round(df['moyenne'].mean(), 2) if 'moyenne' in df else 0
stress_moy = round(df['stress'].mean(), 2) if 'stress' in df else 0
heures_moy = round(df['heures_etude'].mean(), 2) if 'heures_etude' in df else 0


col1.markdown(f"""
<div class="card">
    <div class="icon">👨‍🎓</div>
    <div class="kpi">{nb_etudiants}</div>
    <div class="small">Étudiants enregistrés</div>
</div>
""", unsafe_allow_html=True)

col2.markdown(f"""
<div class="card">
    <div class="icon">🎓</div>
    <div class="kpi">{moyenne_gen}</div>
    <div class="small">Moyenne générale</div>
</div>
""", unsafe_allow_html=True)

col3.markdown(f"""
<div class="card">
    <div class="icon">😰</div>
    <div class="kpi">{stress_moy}</div>
    <div class="small">Niveau de stress moyen</div>
</div>
""", unsafe_allow_html=True)

col4.markdown(f"""
<div class="card">
    <div class="icon">📚</div>
    <div class="kpi">{heures_moy}</div>
    <div class="small">Heures d'étude moyennes</div>
</div>
""", unsafe_allow_html=True)

st.divider()

# =========================
# INSIGHTS
# =========================
st.markdown("## 🧠 Insights automatiques")

best = df.groupby("filiere")["moyenne"].mean().idxmax()
worst = df.groupby("filiere")["moyenne"].mean().idxmin()

col1, col2, col3 = st.columns(3)

col1.success(f" Meilleure filière : {best}")
col2.error(f" Filière faible : {worst}")
col3.info(f" Total filières : {df['filiere'].nunique()}")

col1, col2, col3 = st.columns(3)

stress_high = df.groupby("filiere")["stress"].mean().idxmax()
study_high = df.groupby("filiere")["heures_etude"].mean().idxmax()
motivation_high = df.groupby("filiere")["motivation"].mean().idxmax()

col1.warning(f" Filière la plus stressée : {stress_high}")
col2.info(f" Filière la plus travailleuse : {study_high}")
col3.success(f" Filière la plus motivée : {motivation_high}")

st.divider()
# =========================
# PERFORMANCE
# =========================
st.markdown("## 📈 Performance globale")

pass_rate = (df["moyenne"] >= 10).mean() * 100

col1, col2 = st.columns(2)

col1.markdown(f"""
<div style="text-align:center;">
    <div style="font-size:16px; font-weight:600; color:#6B4226;">
         Taux de réussite
    </div>
    <div style="font-size:26px; font-weight:800; color:#16A34A;">
        {pass_rate:.1f}%
    </div>
</div>
""", unsafe_allow_html=True)

col2.markdown(f"""
<div style="text-align:center;">
    <div style="font-size:16px; font-weight:600; color:#6B4226;">
         Taux d'échec
    </div>
    <div style="font-size:26px; font-weight:800; color:#DC2626;">
        {100-pass_rate:.1f}%
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()
# ==========================================================
#  TOP ÉTUDIANTS
# ==========================================================

st.subheader("🏆 Top étudiants")

top_students = df.sort_values("moyenne", ascending=False).head(10)

st.dataframe(
    top_students[
        [
            "nom",
            "age",
            "sexe",
            "filiere",
            "niveau",
            "heures_etude",
            "methode",
            "regularite",
            "sommeil",
            "sport",
            "telephone",
            "stress",
            "concentration",
            "motivation",
            "moyenne",
            "credits"
        ]
    ],
    use_container_width=True
)

st.divider()

# ==========================================================
#  FACTEURS D’IMPACT
# ==========================================================
st.subheader("📊 Facteurs influençant la performance")

correlation = df.select_dtypes(include="number").corr()["moyenne"].sort_values()

fig_corr = px.bar(
    correlation,
    title="Impact des variables sur la moyenne"
)

st.plotly_chart(fig_corr, use_container_width=True)

st.divider()



# ==========================================================
#  PROFIL IDÉAL
# ==========================================================
st.subheader("🌟 Profil étudiant idéal")

best_student = df.sort_values("moyenne", ascending=False).iloc[0]

st.success(f"""
🎓 Meilleure moyenne : {round(best_student['moyenne'],2)}

📚 Heures d'étude : {best_student['heures_etude']}  
🔥 Motivation : {best_student['motivation']}  
🧠 Concentration : {best_student['concentration']}  
😴 Sommeil : {best_student['sommeil']}  
""")

st.divider()

# ==========================================================
# CONCLUSION IA
# ==========================================================
st.subheader("💡 Espace recommandation")

if df["stress"].mean() > 6:
    st.warning(" Le stress est un facteur critique global")

if df["heures_etude"].mean() < 3:
    st.warning(" Temps d’étude global insuffisant")

if df["motivation"].mean() > 7:
    st.success(" Bonne motivation globale des étudiants")

st.info("""
- Augmenter les heures d’étude
- Réduire le stress
- Améliorer la régularité
""")
st.divider()
st.info(""" Utiliser l'onglet  [<<]  visible au dessus a gauche de votre écran pour remplir le formulaire et naviguer dans l'application""")

