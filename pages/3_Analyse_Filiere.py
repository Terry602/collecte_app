import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components

st.set_page_config(page_title="Analyse Filière & Niveau", layout="wide")

# =========================
# HEADER UNIQUE
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
">

    <div style="display:flex; align-items:center; justify-content:center; gap:14px;">

        <svg width="45" height="45" viewBox="0 0 24 24"
             fill="none" stroke="#4F46E5" stroke-width="2.2">

            <path d="M3 9l9-4 9 4-9 4-9-4z"/>
            <path d="M7 12v4c0 1 2 3 5 3s5-2 5-3v-4"/>
            <line x1="8" y1="20" x2="8" y2="16"/>
            <line x1="12" y1="20" x2="12" y2="14"/>
            <line x1="16" y1="20" x2="16" y2="10"/>
        </svg>

        <div style="font-size:30px; font-weight:800;">
            Analyse Filière & Niveau Académique
        </div>

    </div>

    <div style="font-size:13px; color:#64748B; margin-top:6px;">
        Analyse complète des performances, comportements et évolutions étudiantes
    </div>
</div>
""", height=160)

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
filiere_selected = st.selectbox(
    "📌 Choisir une filière",
    df["filiere"].dropna().unique()
)

df_fil = df[df["filiere"] == filiere_selected]

if df_fil.empty:
    st.warning("Aucune donnée pour cette filière")
    st.stop()

st.divider()

# =========================
# KPI GLOBAL FILIÈRE
# =========================
st.subheader(f"🌍 Indicateurs globaux - {filiere_selected}")

col1, col2, col3, col4 = st.columns(4)

col1.metric("🎓 Moyenne", round(df_fil["moyenne"].mean(), 2))
col2.metric("😰 Stress", round(df_fil["stress"].mean(), 2))
col3.metric("📚 Étude", round(df_fil["heures_etude"].mean(), 2))
col4.metric("👨‍🎓 Étudiants", len(df_fil))

st.divider()

# =========================
# ANALYSE FILIÈRE
# =========================
st.subheader("🔬 Analyse de la filière")

fig_sex = px.pie(
    df_fil,
    names="sexe",
    hole=0.5,
    title="Répartition du sexe"
)
st.plotly_chart(fig_sex, use_container_width=True)

numeric_df = df_fil.select_dtypes(include=["int64", "float64"])
fig_corr = px.imshow(numeric_df.corr(), text_auto=True, title="Corrélation")
st.plotly_chart(fig_corr, use_container_width=True)

# =========================
# RELATIONS
# =========================
st.subheader("📊 Relations clés")

fig = px.scatter(df_fil, x="heures_etude", y="moyenne", trendline="ols",
                 title="Études vs Performance")
st.plotly_chart(fig, use_container_width=True)

fig = px.scatter(df_fil, x="motivation", y="moyenne", trendline="ols",
                 title="Motivation vs Performance")
st.plotly_chart(fig, use_container_width=True)

# =========================
# ANALYSE PAR NIVEAU
# =========================
st.divider()
st.subheader("🎓 Analyse par niveau")

niveau_group = df_fil.groupby("niveau").mean(numeric_only=True).reset_index()

fig1 = px.bar(niveau_group, x="niveau", y="moyenne",
              title="Moyenne par niveau")
st.plotly_chart(fig1, use_container_width=True)

fig2 = px.bar(niveau_group, x="niveau", y="stress",
              title="Stress par niveau")
st.plotly_chart(fig2, use_container_width=True)

fig3 = px.bar(niveau_group, x="niveau", y="heures_etude",
              title="Étude par niveau")
st.plotly_chart(fig3, use_container_width=True)

fig4 = px.pie(df_fil, names="niveau", title="Répartition des niveaux")
st.plotly_chart(fig4, use_container_width=True)

# =========================
# COMPARAISONS FILIÈRES
# =========================
st.divider()
st.subheader("⚖️ Comparaison des filières")

fig = px.bar(df.groupby("filiere")["moyenne"].mean().reset_index(),
             x="filiere", y="moyenne", title="Moyenne par filière")
st.plotly_chart(fig, use_container_width=True)

fig = px.bar(df.groupby("filiere")["stress"].mean().reset_index(),
             x="filiere", y="stress", title="Stress par filière")
st.plotly_chart(fig, use_container_width=True)

# =========================
# INSIGHTS
# =========================
st.divider()
st.subheader("🧠 Insights intelligents")

st.success(f"Meilleure filière : {df.groupby('filiere')['moyenne'].mean().idxmax()}")
st.error(f"Moins performante : {df.groupby('filiere')['moyenne'].mean().idxmin()}")
st.warning(f"Plus stressée : {df.groupby('filiere')['stress'].mean().idxmax()}")
