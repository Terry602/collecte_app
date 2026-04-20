import streamlit as st
import pandas as pd
import plotly.express as px

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
# 🎨 TITRE
# ==========================================================
st.title("Application D'analyse Étudiants ")
st.write("Dashboard intelligent d’analyse des performances étudiantes")

st.divider()

# =========================
# DATA (SANS BUG)
# =========================
  # refresh auto toutes les 5 secondes
def load_data():
    return pd.read_csv("data_students.csv")


    df = load_data()

# =========================
# PRESENTATION
# =========================
st.markdown("##  Objectif du projet")


col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    📥 **Collecte intelligente des données**  
    

    📊 **Analyse comportementale & académique**  
    

    🧠 **Identification des facteurs de réussite**  
     

    🤖 **Prédiction des performances**  
    
    """)

with col2:
    st.markdown("""
    📑 **Génération de rapports intelligents**  
    

    🧹 **Data Cleaning & Preprocessing**  
    

    📈 **Data Visualization Avancée**  
     

    🧪 **Feature Engineering & Model Evaluation**  
     
    """)

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



# ==========================================================
#  TOP ÉTUDIANTS
# ==========================================================
st.subheader("🏆 Top étudiants")

top_students = df.sort_values("moyenne", ascending=False).head(5)

st.dataframe(
    top_students[["filiere", "niveau", "moyenne"]],
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
    st.warning("👉 Le stress est un facteur critique global")

if df["heures_etude"].mean() < 3:
    st.warning("👉 Temps d’étude global insuffisant")

if df["motivation"].mean() > 7:
    st.success("👉 Bonne motivation globale des étudiants")

st.info("""
💡 Recommandation globale :
- Augmenter les heures d’étude
- Réduire le stress
- Améliorer la régularité
""")

# =========================
# 🎨 STYLE PRO
# =========================
st.markdown("""
<style>
.main {
    background-color: #0B0F19;
}
h1, h2, h3 {
    color: #00E5FF;
    font-weight: 700;
}
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
.icon { font-size: 28px; }
.kpi { font-size: 22px; font-weight: bold; color: white; }
.small { color: #9CA3AF; }
</style>
""", unsafe_allow_html=True)


# =========================
# 🔄 BOUTON REFRESH (IMPORTANT)
# =========================
if st.button("🔄 Actualiser les données"):
    st.cache_data.clear()
    st.rerun()

