import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Analyse par Niveau", layout="wide")

st.title("🏫 Analyse par Niveau Académique (par Filière)")

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
st.subheader("🎯 Sélection de la filière")

filiere_selected = st.selectbox(
    "📚 Choisir une filière",
    df["filiere"].dropna().unique()
)

df_fil = df[df["filiere"] == filiere_selected]

# =========================
# CAS VIDE
# =========================
if df_fil.empty:
    st.warning("⚠️ Aucune donnée pour cette filière")
    st.stop()

# =========================
# KPI NIVEAU GLOBAL FILTRÉ
# =========================
st.subheader(f"📊 Indicateurs - {filiere_selected}")

niveau_group = df_fil.groupby("niveau").mean(numeric_only=True).reset_index()

col1, col2, col3 = st.columns(3)

col1.metric("🎓 Meilleure moyenne", round(niveau_group["moyenne"].max(), 2))
col2.metric("😰 Stress moyen", round(df_fil["stress"].mean(), 2))
col3.metric("📚 Étudiants", len(df_fil))

# =========================
# ANALYSE PAR NIVEAU
# =========================
st.subheader("📈 Analyse par niveau dans la filière")

fig1 = px.bar(
    niveau_group,
    x="niveau",
    y="moyenne",
    color="niveau",
    title=f"🎓 Moyenne par niveau - {filiere_selected}",
    color_discrete_sequence=px.colors.qualitative.Set3
)

st.plotly_chart(fig1, use_container_width=True)

fig2 = px.bar(
    niveau_group,
    x="niveau",
    y="stress",
    color="niveau",
    title=f"😰 Stress par niveau - {filiere_selected}",
    color_discrete_sequence=px.colors.qualitative.Pastel
)

st.plotly_chart(fig2, use_container_width=True)

fig3 = px.bar(
    niveau_group,
    x="niveau",
    y="heures_etude",
    color="niveau",
    title=f"📚 Heures d'étude par niveau - {filiere_selected}",
    color_discrete_sequence=px.colors.qualitative.Bold
)

st.plotly_chart(fig3, use_container_width=True)

# =========================
# RÉPARTITION NIVEAU (FILTRÉE)
# =========================
st.subheader("👨‍🎓 Répartition des étudiants")

fig4 = px.pie(
    df_fil,
    names="niveau",
    title=f"Répartition des niveaux - {filiere_selected}",
    color_discrete_sequence=px.colors.qualitative.Set3
)

st.plotly_chart(fig4, use_container_width=True)