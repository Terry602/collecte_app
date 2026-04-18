import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="SmartStudent Analytics",
    page_icon="📊",
    layout="wide"
)

# =========================
# 🎨 STYLE PRO PROPRE (CLEAN FINTECH)
# =========================
st.markdown("""
<style>

.main {
    background-color: #0B0F19;
}

/* TITRES */
h1, h2, h3 {
    color: #00E5FF;
    font-weight: 700;
}

/* CARD CLEAN (plus lisible que avant) */
.card {
    background: #111827;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #1F2937;
    text-align: center;
    transition: 0.3s;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0px 10px 25px rgba(0,229,255,0.15);
}

/* ICON */
.icon {
    font-size: 28px;
}

/* TEXT KPI */
.kpi {
    font-size: 22px;
    font-weight: bold;
    color: white;
}

.small {
    color: #9CA3AF;
}

</style>
""", unsafe_allow_html=True)

# =========================
# TITLE
# =========================
st.title("📊 SmartStudent Analytics Dashboard")
st.subheader("🚀 Analyse intelligente des performances étudiantes")

# =========================
# DATA
# =========================
@st.cache_data
def load_data():
    return pd.read_csv("data_students.csv")

try:
    df = load_data()
except:
    st.error("❌ Aucune donnée disponible.")
    st.stop()

    # =========================
# PRESENTATION
# =========================
st.markdown("## 🎯 Objectif du projet")

st.write("""
Cette application permet de :

✔ Collecter des données étudiants  
✔ Analyser les comportements académiques  
✔ Identifier les facteurs de réussite  
✔ Prédire les performances  
✔ Générer des rapports intelligents  
""")


# =========================
# KPI CARDS
# =========================
st.markdown("## 📌 Indicateurs globaux")

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

st.divider()

# =========================
# 📊 RÉPARTITION (FIX BUG + CLEAN)
# =========================
st.markdown("## 📊 Répartition des étudiants")

col1, col2 = st.columns(2)

# ===== BAR CHART (CORRIGÉ)
with col1:

    filiere_count = df["filiere"].value_counts().reset_index()
    filiere_count.columns = ["filiere", "count"]

    fig_bar = px.bar(
        filiere_count,
        x="filiere",
        y="count",
        color="filiere",
        color_discrete_sequence=[
            "#FF5733", "#FFC300", "#28B463",
            "#3498DB", "#9B59B6"
        ],
        title="📊 Répartition par filière"
    )

    st.plotly_chart(fig_bar, use_container_width=True)

# ===== PIE CHART (CORRIGÉ)
with col2:

    sexe_count = df["sexe"].value_counts().reset_index()
    sexe_count.columns = ["sexe", "count"]

    fig_pie = px.pie(
        sexe_count,
        names="sexe",
        values="count",
        color_discrete_sequence=["#FF9F1C", "#2EC4B6"],
        title="🥧 Répartition par sexe"
    )

    st.plotly_chart(fig_pie, use_container_width=True)

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


