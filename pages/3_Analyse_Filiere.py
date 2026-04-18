import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Analyse par Filière", layout="wide")

st.title("🎓 Analyse par Filière")

DATA_FILE = "data_students.csv"

# =========================
# CHARGEMENT DONNÉES
# =========================
@st.cache_data
def load_data():
    return pd.read_csv(DATA_FILE)

# bouton refresh
if st.button("🔄 Rafraîchir"):
    st.cache_data.clear()
    st.rerun()

try:
    df = load_data()
except:
    st.error("❌ Aucune donnée disponible.")
    st.stop()

# =========================
# FILTRES
# =========================
filiere_selected = st.selectbox(
    "🎯 Choisir une filière",
    df["filiere"].dropna().unique()
)

df_fil = df[df["filiere"] == filiere_selected]

# =========================
# KPI FILIERE + SEXE (SEMI CIRCLE)
# =========================
st.subheader(f"📊 Indicateurs - {filiere_selected}")

col1, col2, col3, col4 = st.columns(4)

# ===== KPI classiques
col1.metric("🎓 Moyenne", round(df_fil["moyenne"].mean(), 2))
col2.metric("😰 Stress", round(df_fil["stress"].mean(), 2))
col3.metric("📚 Heures étude", round(df_fil["heures_etude"].mean(), 2))
col4.metric("👨‍🎓 Total étudiants", len(df_fil))

st.divider()

# =========================
# 🥧 SEMI-CIRCLE SEXE DISTRIBUTION
# =========================
st.subheader("👤 Répartition du sexe (filière sélectionnée)")

sex_counts = df_fil["sexe"].value_counts().reset_index()
sex_counts.columns = ["sexe", "count"]

fig_sex = px.pie(
    sex_counts,
    names="sexe",
    values="count",
    hole=0.5,  # 👉 donut effect
    title="Répartition des sexes",
    color_discrete_sequence=["#FF9F1C", "#2EC4B6"]
)

# 🔥 transformation en semi-cercle
fig_sex.update_traces(textinfo="percent+label")

fig_sex.update_layout(
    showlegend=True,
    height=400,
    annotations=[dict(text="Sexe", x=0.5, y=0.5, font_size=18, showarrow=False)],
    margin=dict(t=40, b=0)
)

st.plotly_chart(fig_sex, use_container_width=True)

# =========================
# COMPARAISON ENTRE FILIERES (PLOTLY)
# =========================
st.subheader("🏆 Comparaison des filières")

moyenne_filiere = df.groupby("filiere")["moyenne"].mean().reset_index()

fig1 = px.bar(
    moyenne_filiere,
    x="filiere",
    y="moyenne",
    color="filiere",
    title="📊 Moyenne académique par filière",
    color_discrete_sequence=px.colors.qualitative.Set3
)

st.plotly_chart(fig1, use_container_width=True)

# =========================
# STRESS PAR FILIERE (PLOTLY)
# =========================
st.subheader("😰 Niveau de stress par filière")

stress_filiere = df.groupby("filiere")["stress"].mean().reset_index()

fig2 = px.bar(
    stress_filiere,
    x="filiere",
    y="stress",
    color="filiere",
    title="😰 Stress moyen par filière",
    color_discrete_sequence=px.colors.qualitative.Pastel
)

st.plotly_chart(fig2, use_container_width=True)

# =========================
# HEURES D'ÉTUDE PAR FILIERE (PLOTLY)
# =========================
st.subheader("📚 Effort d'étude par filière")

study_filiere = df.groupby("filiere")["heures_etude"].mean().reset_index()

fig3 = px.bar(
    study_filiere,
    x="filiere",
    y="heures_etude",
    color="filiere",
    title="📚 Heures d'étude moyennes par filière",
    color_discrete_sequence=px.colors.qualitative.Bold
)

st.plotly_chart(fig3, use_container_width=True)

# =========================
# BOXPLOT (NE PAS MODIFIER 🔥)
# =========================
st.subheader("📦 Distribution des notes par filière")

fig4, ax4 = plt.subplots(figsize=(10,6))
sns.boxplot(data=df, x="filiere", y="moyenne", ax=ax4, palette="Set2")

ax4.set_title("Répartition des moyennes par filière")
ax4.set_xlabel("Filière")
ax4.set_ylabel("Moyenne")

plt.xticks(rotation=45)

st.pyplot(fig4)

# =========================
# INSIGHTS AUTOMATIQUES
# =========================
st.subheader("🧠 Analyse intelligente")

best_filiere = df.groupby("filiere")["moyenne"].mean().idxmax()
worst_filiere = df.groupby("filiere")["moyenne"].mean().idxmin()
stress_high = df.groupby("filiere")["stress"].mean().idxmax()

st.success(f"🏆 Filière la plus performante : {best_filiere}")
st.error(f"⚠️ Filière la moins performante : {worst_filiere}")
st.warning(f"😰 Filière la plus stressée : {stress_high}")