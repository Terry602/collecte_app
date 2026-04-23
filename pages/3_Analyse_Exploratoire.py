import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Data Explorer PRO", layout="wide")

st.markdown("""
<style>

/* ===== EXPLORATION HEADER INDIGO STYLE ===== */
.explorer-header {
    background: linear-gradient(135deg, #EEF2FF, #E0E7FF);
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #C7D2FE;
    text-align: center;
    margin-bottom: 12px;
    box-shadow: 0 8px 20px rgba(99,102,241,0.10);
}

/* TITLE */
.explorer-title {
    font-size: 30px;
    font-weight: 800;
    color: #1E1B4B;
    letter-spacing: -0.4px;
}

/* SUBTITLE */
.explorer-subtitle {
    font-size: 13px;
    color: #4338CA;
    margin-top: 6px;
}
</style>

<div class="explorer-header">
    <div class="explorer-title"> Analyse Exploratoire</div>
    <div class="explorer-subtitle">Data Exploration • Patterns Detection • Statistical Insights</div>
</div>
""", unsafe_allow_html=True)

st.divider()

# =========================
# LOAD DATA SAFE
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv("data_students.csv")

    #  COMPATIBILITÉ ANCIENNES DONNÉES
    if "nom" not in df.columns:
        df["nom"] = "Inconnu"

    if "filiere" not in df.columns:
        df["filiere"] = "Non défini"

    if "niveau" not in df.columns:
        df["niveau"] = "Non défini"

    if "sexe" not in df.columns:
        df["sexe"] = "Non défini"

    return df

df = load_data()

# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.header(" Filtres")

filiere = st.sidebar.selectbox("📚 Filière", ["Toutes"] + sorted(df["filiere"].dropna().unique()))
niveau = st.sidebar.selectbox("🎓 Niveau", ["Tous"] + sorted(df["niveau"].dropna().unique()))
sexe = st.sidebar.selectbox("👤 Sexe", ["Tous"] + sorted(df["sexe"].dropna().unique()))

# =========================
# FILTER DATA
# =========================
df_filtered = df.copy()

if filiere != "Toutes":
    df_filtered = df_filtered[df_filtered["filiere"] == filiere]

if niveau != "Tous":
    df_filtered = df_filtered[df_filtered["niveau"] == niveau]

if sexe != "Tous":
    df_filtered = df_filtered[df_filtered["sexe"] == sexe]


# =========================
# SEARCH SAFE
# =========================
st.markdown("##  Recherche étudiant")

search = st.text_input("Tape le nom de l'étudiant")

if search:
    if "nom" in df_filtered.columns:
        result = df_filtered[
            df_filtered["nom"].astype(str).str.contains(search, case=False, na=False)
        ]
        st.dataframe(result)
    else:
        st.warning("Colonne nom absente dans les données")
    st.stop()

st.divider()
# =========================
# KPIs
# =========================
st.markdown("##  Indicateurs clés")

col1, col2, col3, col4 = st.columns(4)

col1.metric("👨‍🎓 Étudiants", len(df_filtered))
col2.metric("🎓 Moyenne", round(df_filtered["moyenne"].mean(), 2))
col3.metric("😰 Stress", round(df_filtered["stress"].mean(), 2))
col4.metric("📚 Étude", round(df_filtered["heures_etude"].mean(), 2))

st.divider()

# =========================
# FILIERE BAR CHART (SAFE)
# =========================
st.markdown("##  Nombre d'étudiants par filière")

filiere_counts = df_filtered["filiere"].value_counts().reset_index()
filiere_counts.columns = ["filiere", "count"]

fig1 = px.bar(
    filiere_counts,
    x="filiere",
    y="count",
    color="filiere",
    color_discrete_sequence=px.colors.qualitative.Set3
)

st.plotly_chart(fig1, use_container_width=True)

