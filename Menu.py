import streamlit as st
import pandas as pd
import plotly.express as px
import time
# ==========================================================
# ⚙️ CONFIG PAGE
# ==========================================================
st.set_page_config(
    page_title="SmartStudent Analytics - Advanced",
    layout="wide"
)

# ==========================================================
# 📦 CHARGEMENT DONNÉES
# ==========================================================
@st.cache_data(ttl=5)
def load_data():
    return pd.read_csv("data_students.csv")
try:
    df = load_data()
except:
    st.error("❌ Aucune donnée disponible.")
    st.stop()

# ==========================================================
# 🎨 HEADER STYLE FINTECH PREMIUM
# ==========================================================

st.markdown("""
<style>

/* ===== FINTECH HEADER WRAPPER ===== */
.fintech-header {
    background: linear-gradient(135deg, #0F172A, #111827);
    padding: 28px 20px;
    border-radius: 16px;
    border: 1px solid #1F2937;
    text-align: center;
    margin-bottom: 18px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.25);
}

/* TITLE FINTECH */
.fintech-title {
    font-size: 32px;
    font-weight: 800;
    color: #F8FAFC;
    letter-spacing: -0.5px;
}

/* SUBTITLE FINTECH */
.fintech-subtitle {
    font-size: 14px;
    color: #94A3B8;
    margin-top: 8px;
    letter-spacing: 0.3px;
}

/* SMALL FINTECH TAG */
.fintech-tag {
    display: inline-block;
    margin-top: 12px;
    padding: 6px 12px;
    font-size: 12px;
    color: #22D3EE;
    border: 1px solid rgba(34, 211, 238, 0.3);
    border-radius: 20px;
    background: rgba(34, 211, 238, 0.08);
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="fintech-header">
    <div class="fintech-title">🎓 Application d'Analyse des Étudiants</div>
    <div class="fintech-subtitle">
       Dashboard intelligent d’analyse des performances étudiantes basé sur la Data Science & l’IA 
    </div>
    <div class="fintech-tag">AI • Data Science • Predictive Analytics</div>
</div>
""", unsafe_allow_html=True)

st.divider()

# =========================
# DATA (SANS BUG)
# =========================
  # refresh auto toutes les 5 secondes
def load_data():
    return pd.read_csv("data_students.csv")


    df = load_data()


# =========================
# OBJECTIFS (ANIMATION ULTRA FLUIDE - VERSION AMÉLIORÉE)
# =========================

st.markdown("## 🧭 Objectif du projet")

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
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 6px;
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
        <div class="title" style="color:#2563EB;">📥 Collecte intelligente des données</div>
        <div class="desc">Centralisation et structuration des données étudiantes pour analyse.</div>
    </div>

    <div class="objective">
        <div class="title" style="color:#059669;">📊 Analyse comportementale & académique</div>
        <div class="desc">Étude des performances et comportements des étudiants.</div>
    </div>

    <div class="objective">
        <div class="title" style="color:#7C3AED;">🧠 Identification des facteurs de réussite</div>
        <div class="desc">Détection des variables influençant les résultats académiques.</div>
    </div>

    <div class="objective">
        <div class="title" style="color:#DC2626;">🤖 Prédiction des performances</div>
        <div class="desc">Utilisation de modèles IA pour anticiper les résultats.</div>
    </div>

    <div class="objective">
        <div class="title" style="color:#EA580C;">📑 Génération de rapports intelligents</div>
        <div class="desc">Production automatique d’insights pour la prise de décision.</div>
    </div>

    <div class="objective">
        <div class="title" style="color:#0EA5E9;">🧹 Data Cleaning & Preprocessing</div>
        <div class="desc">Nettoyage, transformation et préparation des données.</div>
    </div>

    <div class="objective">
        <div class="title" style="color:#16A34A;">📈 Data Visualization Avancée</div>
        <div class="desc">Création de dashboards interactifs et visuels.</div>
    </div>

    <div class="objective">
        <div class="title" style="color:#9333EA;">🧪 Feature Engineering & Model Evaluation</div>
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
st.markdown("## ⚙️ Indicateurs globaux")

col1, col2, col3, col4 = st.columns(4)

col1.markdown(f"""
<div class="card">
<div class="icon">👨‍🎓</div>
<div class="kpi">{len(df)}</div>
<div class="small">Étudiants</div>
</div>
""", unsafe_allow_html=True)

col2.markdown(f"""
<div class="card">
<div class="icon">🎓</div>
<div class="kpi">{round(df['moyenne'].mean(),2)}</div>
<div class="small">Moyenne générale</div>
</div>
""", unsafe_allow_html=True)

col3.markdown(f"""
<div class="card">
<div class="icon">😰</div>
<div class="kpi">{round(df['stress'].mean(),2)}</div>
<div class="small">Stress moyen</div>
</div>
""", unsafe_allow_html=True)

col4.markdown(f"""
<div class="card">
<div class="icon">📚</div>
<div class="kpi">{round(df['heures_etude'].mean(),2)}</div>
<div class="small">Heures d'étude</div>
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

col1.success(f"🏆 Meilleure filière : {best}")
col2.error(f"⚠️ Filière faible : {worst}")
col3.info(f"📊 Total filières : {df['filiere'].nunique()}")

col1, col2, col3 = st.columns(3)

stress_high = df.groupby("filiere")["stress"].mean().idxmax()
study_high = df.groupby("filiere")["heures_etude"].mean().idxmax()
motivation_high = df.groupby("filiere")["motivation"].mean().idxmax()

col1.warning(f"😰 Filière la plus stressée : {stress_high}")
col2.info(f"📚 Filière la plus travailleuse : {study_high}")
col3.success(f"🔥 Filière la plus motivée : {motivation_high}")

st.divider()

# =========================
# PERFORMANCE
# =========================
st.markdown("## 📈 Performance globale")

pass_rate = (df["moyenne"] >= 10).mean() * 100

col1, col2 = st.columns(2)

col1.metric("✔ Taux de réussite", f"{pass_rate:.1f}%")
col2.metric("❌ Taux d'échec", f"{100-pass_rate:.1f}%")

st.divider()
# ==========================================================
#  DISTRIBUTION DES NOTES
# ==========================================================
st.subheader("📈 Distribution des performances")

fig_hist = px.histogram(
    df,
    x="moyenne",
    nbins=20,
    title="Distribution des moyennes",
    marginal="box"
)

st.plotly_chart(fig_hist, use_container_width=True)
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
#  TENDANCES
# ==========================================================
st.subheader("📈 Tendances globales")

trend = df.groupby("niveau")["moyenne"].mean().reset_index()

fig_trend = px.line(
    trend,
    x="niveau",
    y="moyenne",
    markers=True,
    title="Évolution des performances par niveau"
)

st.plotly_chart(fig_trend, use_container_width=True)

st.divider()

# ==========================================================
# 🧠 CONCLUSION IA
# ==========================================================
st.subheader("🧠 Conclusion intelligente")

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

# =========================
# 🎨 STYLE PRO (AMÉLIORÉ + LISIBLE + MODERNE)
# =========================
st.markdown("""
<style>

/* =========================
   GLOBAL BACKGROUND (LIGHT PRO DASHBOARD)
========================= */
.main {
    background-color: #F5F7FB;
}

/* TITRES */
h1, h2, h3 {
    color: #0F172A;
    font-weight: 700;
}

/* =========================
   KPI / CARDS (STYLE GLASS CLEAN)
========================= */
.card {
    background: #FFFFFF;
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #E5E7EB;
    text-align: center;
    transition: all 0.25s ease;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 10px 25px rgba(0,0,0,0.08);
    border-color: #93C5FD;
}

/* ICON */
.icon {
    font-size: 28px;
    margin-bottom: 8px;
}

/* KPI VALUE */
.kpi {
    font-size: 24px;
    font-weight: 800;
    color: #111827;
}

/* SMALL TEXT */
.small {
    font-size: 13px;
    color: #6B7280;
    margin-top: 5px;
}

/* =========================
   STREAMLIT METRICS CLEAN
========================= */
[data-testid="stMetric"] {
    background: #FFFFFF;
    border-radius: 14px;
    padding: 15px;
    border: 1px solid #E5E7EB;
    box-shadow: 0 2px 6px rgba(0,0,0,0.04);
}

/* =========================
   TABLE CLEAN
========================= */
.stDataFrame {
    background: white;
    border-radius: 12px;
    overflow: hidden;
}

/* =========================
   PLOTLY BACKGROUND CLEAN
========================= */
.js-plotly-plot {
    background: white;
    border-radius: 12px;
    padding: 10px;
}

/* =========================
   SUCCESS / WARNING / INFO CLEAN
========================= */
.stSuccess, .stWarning, .stInfo {
    border-radius: 12px;
    padding: 10px;
}



</style>
""", unsafe_allow_html=True)


# =========================
# 🔄 BOUTON REFRESH (IMPORTANT)
# =========================
if st.button("🔄 Actualiser les données"):
    st.cache_data.clear()
    st.rerun()

