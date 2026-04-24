import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components

st.set_page_config(page_title="Analyse Académique", layout="wide")

# =========================
# HEADER GLOBAL
# =========================
components.html("""
<div style="
    background: linear-gradient(135deg, #EEF2FF, #E0E7FF);
    padding: 24px;
    border-radius: 16px;
    border: 1px solid #C7D2FE;
    text-align: center;
    margin-bottom: 15px;
    box-shadow: 0 10px 25px rgba(79,70,229,0.12);
    font-family: Arial;
">
    <div style="font-size:28px; font-weight:800; color:#1E1B4B;">
        📊 Analyse Académique Intelligente
    </div>
    <div style="font-size:13px; color:#4338CA;">
        Analyse par filière + niveau • Performance • Comportement • Insights
    </div>
</div>
""", height=130)

# =========================
# DATA
# =========================
@st.cache_data
def load_data():
    return pd.read_csv("data_students.csv")

df = load_data()

# =========================
# FILTRE FILIÈRE
# =========================
st.subheader("📌 Sélection de la filière")

filiere_selected = st.selectbox(
    "Choisir une filière",
    df["filiere"].dropna().unique()
)

df_fil = df[df["filiere"] == filiere_selected]

if df_fil.empty:
    st.warning("Aucune donnée disponible")
    st.stop()

st.divider()

# =========================
# KPI GLOBAL FILIÈRE (UNE SEULE FOIS)
# =========================
st.subheader(f"🌍 Indicateurs globaux - {filiere_selected}")

col1, col2, col3, col4 = st.columns(4)

col1.metric("🎓 Moyenne", round(df_fil["moyenne"].mean(), 2))
col2.metric("😰 Stress", round(df_fil["stress"].mean(), 2))
col3.metric("📚 Heures étude", round(df_fil["heures_etude"].mean(), 2))
col4.metric("👨‍🎓 Étudiants", len(df_fil))

st.divider()

# =========================
# 🔵 ANALYSE PAR NIVEAU (PREMIER BLOC)
# =========================
st.subheader("🎓 Analyse par niveau académique")

niveau_group = df_fil.groupby("niveau").mean(numeric_only=True).reset_index()

fig1 = px.bar(
    niveau_group,
    x="niveau",
    y="moyenne",
    color="niveau",
    title="Moyenne par niveau"
)
st.plotly_chart(fig1, use_container_width=True)

fig2 = px.bar(
    niveau_group,
    x="niveau",
    y="stress",
    color="niveau",
    title="Stress par niveau"
)
st.plotly_chart(fig2, use_container_width=True)

fig3 = px.bar(
    niveau_group,
    x="niveau",
    y="heures_etude",
    color="niveau",
    title="Heures d'étude par niveau"
)
st.plotly_chart(fig3, use_container_width=True)

fig4 = px.pie(
    df_fil,
    names="niveau",
    title="Répartition des niveaux"
)
st.plotly_chart(fig4, use_container_width=True)

st.divider()

# =========================
# 🟡 ANALYSE FILIÈRE (SUITE LOGIQUE)
# =========================
st.subheader("📚 Analyse approfondie de la filière")

# Sexe
sex_counts = df_fil["sexe"].value_counts().reset_index()
sex_counts.columns = ["sexe", "count"]

fig_sex = px.pie(
    sex_counts,
    names="sexe",
    values="count",
    hole=0.5,
    title="Répartition du sexe"
)
st.plotly_chart(fig_sex, use_container_width=True)

# Corrélation
numeric_df = df_fil.select_dtypes(include=["int64", "float64"])

fig_corr = px.imshow(
    numeric_df.corr(),
    text_auto=True,
    title="Corrélation des variables"
)
st.plotly_chart(fig_corr, use_container_width=True)

# Relations clés
st.subheader("📈 Relations clés")

fig_a = px.scatter(df_fil, x="heures_etude", y="moyenne", trendline="ols")
st.plotly_chart(fig_a, use_container_width=True)

fig_b = px.scatter(df_fil, x="motivation", y="moyenne", trendline="ols")
st.plotly_chart(fig_b, use_container_width=True)

fig_c = px.scatter(df_fil, x="concentration", y="moyenne", trendline="ols")
st.plotly_chart(fig_c, use_container_width=True)

st.divider()

# =========================
# 🔁 COMPARAISON FILIÈRES
# =========================
st.subheader("⚖️ Comparaison des filières")

moyenne_filiere = df.groupby("filiere")["moyenne"].mean().reset_index()

fig_comp = px.bar(
    moyenne_filiere,
    x="filiere",
    y="moyenne",
    color="filiere",
    title="Moyenne par filière"
)
st.plotly_chart(fig_comp, use_container_width=True)

st.divider()

# =========================
# 🤖 INSIGHTS INTELLIGENTS
# =========================
st.subheader("🧠 Insights automatiques")

best = df.groupby("filiere")["moyenne"].mean().idxmax()
worst = df.groupby("filiere")["moyenne"].mean().idxmin()

stress_high = df.groupby("filiere")["stress"].mean().idxmax()

st.success(f"Filière la plus performante : {best}")
st.error(f"Filière la moins performante : {worst}")
st.warning(f"Filière la plus stressée : {stress_high}")
