import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components

st.set_page_config(page_title="Analyse Globale", layout="wide")

# =========================
# HEADER GLOBAL
# =========================
components.html("""
<div style="
    background: linear-gradient(135deg, #EEF2FF, #FEF3C7);
    padding: 24px;
    border-radius: 18px;
    border: 1px solid #E5E7EB;
    text-align: center;
    margin-bottom: 14px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.08);
    font-family: Arial;
">
    <div style="font-size:30px;font-weight:800;color:#0F172A;">
        📊 Analyse Académique Complète
    </div>
    <div style="font-size:13px;color:#64748B;margin-top:6px;">
        Filières • Niveaux • Performance • Corrélations • Insights
    </div>
</div>
""", height=140)

# =========================
# DATA
# =========================
@st.cache_data
def load_data():
    return pd.read_csv("data_students.csv")

df = load_data()

# =========================
# FILTRE FILIÈRE (POINT CENTRAL)
# =========================
st.subheader("📌 Sélection de la filière")

filiere_selected = st.selectbox(
    " Choisir une filière",
    df["filiere"].dropna().unique()
)

df_fil = df[df["filiere"] == filiere_selected]

if df_fil.empty:
    st.warning(" Aucune donnée pour cette filière")
    st.stop()

st.divider()

# =========================================================
# 🟡 PARTIE 1 : ANALYSE FILIÈRE
# =========================================================
st.subheader(f"📚 Analyse de la filière - {filiere_selected}")

# KPI FILIERE
st.markdown("""<style>
.kpi-card {
    background: linear-gradient(135deg, #FFFFFF, #F8FAFC);
    border: 1px solid #E2E8F0;
    border-radius: 16px;
    padding: 10px;
    text-align: center;
    box-shadow: 0 6px 18px rgba(0,0,0,0.06);
    transition: 0.3s;
}
.kpi-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
}
.kpi-value {font-size:18px;font-weight:800;}
.kpi-label {font-size:12px;color:#64748B;}
</style>""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

col1.markdown(f"""<div class="kpi-card"><div class="kpi-value">{round(df_fil["moyenne"].mean(),2)}</div><div class="kpi-label">Moyenne</div></div>""", unsafe_allow_html=True)
col2.markdown(f"""<div class="kpi-card"><div class="kpi-value">{round(df_fil["stress"].mean(),2)}</div><div class="kpi-label">Stress</div></div>""", unsafe_allow_html=True)
col3.markdown(f"""<div class="kpi-card"><div class="kpi-value">{round(df_fil["heures_etude"].mean(),2)}</div><div class="kpi-label">Heures étude</div></div>""", unsafe_allow_html=True)
col4.markdown(f"""<div class="kpi-card"><div class="kpi-value">{len(df_fil)}</div><div class="kpi-label">Étudiants</div></div>""", unsafe_allow_html=True)

# Sexe
sex_counts = df_fil["sexe"].value_counts().reset_index()
sex_counts.columns = ["sexe", "count"]

fig_sex = px.pie(
    sex_counts,
    names="sexe",
    values="count",
    hole=0.5,
    title=" Répartition du sexe",
    color_discrete_sequence=["#FF9F1C", "#2EC4B6"]
)
st.plotly_chart(fig_sex, use_container_width=True)

# Corrélation
numeric_df = df_fil.select_dtypes(include=["int64", "float64"])
fig_corr = px.imshow(
    numeric_df.corr(),
    text_auto=True,
    color_continuous_scale="RdBu",
    title=" Corrélation des variables"
)
st.plotly_chart(fig_corr, use_container_width=True)

# Scatter
st.plotly_chart(px.scatter(df_fil, x="heures_etude", y="moyenne", trendline="ols", title=" Études vs Performance"), use_container_width=True)
st.plotly_chart(px.scatter(df_fil, x="motivation", y="moyenne", trendline="ols", title=" Motivation vs Performance"), use_container_width=True)

st.divider()

# =========================================================
# 🔵 PARTIE 2 : ANALYSE PAR NIVEAU (DANS LA FILIÈRE)
# =========================================================
st.subheader(f"🎓 Analyse par niveau - {filiere_selected}")

niveau_group = df_fil.groupby("niveau").mean(numeric_only=True).reset_index()

# KPI NIVEAU
col1, col2, col3 = st.columns(3)

col1.metric("🎓 Meilleure moyenne", round(niveau_group["moyenne"].max(),2))
col2.metric("😰 Stress moyen", round(df_fil["stress"].mean(),2))
col3.metric("👨‍🎓 Étudiants", len(df_fil))

# Graphes
st.plotly_chart(px.bar(niveau_group, x="niveau", y="moyenne", color="niveau",
                       title=" Moyenne par niveau"), use_container_width=True)

st.plotly_chart(px.bar(niveau_group, x="niveau", y="stress", color="niveau",
                       title=" Stress par niveau"), use_container_width=True)

st.plotly_chart(px.bar(niveau_group, x="niveau", y="heures_etude", color="niveau",
                       title=" Heures d'étude par niveau"), use_container_width=True)

# Répartition niveau
st.plotly_chart(px.pie(df_fil, names="niveau",
                       title=" Répartition des niveaux"), use_container_width=True)

st.divider()

# =========================================================
# 🧠 PARTIE 3 : COMPARAISONS GLOBALES
# =========================================================
st.subheader("⚖️ Comparaison des filières")

st.plotly_chart(px.bar(df.groupby("filiere")["moyenne"].mean().reset_index(),
                       x="filiere", y="moyenne", color="filiere",
                       title=" Moyenne par filière"), use_container_width=True)

st.plotly_chart(px.bar(df.groupby("filiere")["stress"].mean().reset_index(),
                       x="filiere", y="stress", color="filiere",
                       title=" Stress par filière"), use_container_width=True)

st.divider()

# =========================================================
# 🤖 INSIGHTS IA
# =========================================================
st.subheader("🔁 Analyse intelligente")

best = df.groupby("filiere")["moyenne"].mean().idxmax()
worst = df.groupby("filiere")["moyenne"].mean().idxmin()

st.success(f" Filière la plus performante : {best}")
st.error(f" Filière la moins performante : {worst}")
