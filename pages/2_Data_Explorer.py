import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Data Explorer PRO", layout="wide")

st.title("📊 Data Explorer PRO")

# =========================
# LOAD DATA SAFE
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv("data_students.csv")

    # 🔥 COMPATIBILITÉ ANCIENNES DONNÉES
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
st.sidebar.header("🎛️ Filtres")

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
st.markdown("## 🔎 Recherche étudiant")

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

# =========================
# KPIs
# =========================
st.markdown("## 📌 Indicateurs clés")

col1, col2, col3, col4 = st.columns(4)

col1.metric("👨‍🎓 Étudiants", len(df_filtered))
col2.metric("🎓 Moyenne", round(df_filtered["moyenne"].mean(), 2))
col3.metric("😰 Stress", round(df_filtered["stress"].mean(), 2))
col4.metric("📚 Étude", round(df_filtered["heures_etude"].mean(), 2))

st.divider()

# =========================
# FILIERE BAR CHART (SAFE)
# =========================
st.markdown("## 📚 Répartition par filière")

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

# =========================
# PIE CHART SEXE
# =========================
st.markdown("## 👤 Répartition par sexe")

fig2 = px.pie(
    df_filtered,
    names="sexe",
    color_discrete_sequence=px.colors.qualitative.Pastel
)

st.plotly_chart(fig2, use_container_width=True)

# =========================
# HISTOGRAMME
# =========================
st.markdown("## 📊 Distribution des moyennes")

fig3 = px.histogram(
    df_filtered,
    x="moyenne",
    nbins=10,
    color_discrete_sequence=["#FF9800"]
)

st.plotly_chart(fig3, use_container_width=True)

# =========================
# CORRELATION
# =========================
st.markdown("## 🔥 Corrélation")

numeric_df = df_filtered.select_dtypes(include=["int64", "float64"])

fig4 = px.imshow(
    numeric_df.corr(),
    text_auto=True,
    color_continuous_scale="RdBu"
)

st.plotly_chart(fig4, use_container_width=True)