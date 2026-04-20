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
st.divider()

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
st.subheader(f"📉 Indicateurs de la filiere - {filiere_selected}")

col1, col2, col3, col4 = st.columns(4)

col1.metric("🎓 Moyenne", round(df_fil["moyenne"].mean(), 2))
col2.metric("😰 Stress", round(df_fil["stress"].mean(), 2))
col3.metric("📚 Heures étude", round(df_fil["heures_etude"].mean(), 2))
col4.metric("👨‍🎓 Total étudiants", len(df_fil))



# =========================
# 🥧 SEMI-CIRCLE SEXE
# =========================
st.subheader(f"📊 Analyse de la filiere - {filiere_selected}")

st.subheader("")

sex_counts = df_fil["sexe"].value_counts().reset_index()
sex_counts.columns = ["sexe", "count"]

fig_sex = px.pie(
    sex_counts,
    names="sexe",
    values="count",
    hole=0.5,
    title="👤 Répartition du sexe",
    color_discrete_sequence=["#FF9F1C", "#2EC4B6"]
)

fig_sex.update_traces(textinfo="percent+label")

fig_sex.update_layout(
    showlegend=True,
    height=400,
    annotations=[dict(text="Sexe", x=0.5, y=0.5, showarrow=False)],
    margin=dict(t=40, b=0)
)

st.plotly_chart(fig_sex, use_container_width=True)



# =========================
# MATRICE DE CORRELATION
# =========================
st.markdown("### 🔥 Matrice de corrélation")

numeric_df = df_fil.select_dtypes(include=["int64", "float64"])

fig_corr = px.imshow(
    numeric_df.corr(),
    text_auto=True,
    color_continuous_scale="RdBu",
    title="📦 Corrélation des variables"
)

st.plotly_chart(fig_corr, use_container_width=True)

# =========================
# NUAGES DE POINTS + RÉGRESSION
# =========================
st.markdown("### 📉 Relations avec performance")

# Études vs performance
fig_a = px.scatter(
    df_fil,
    x="heures_etude",
    y="moyenne",
    trendline="ols",
    title="📚 Études vs Performance"
)
st.plotly_chart(fig_a, use_container_width=True)

# Concentration vs performance
fig_b = px.scatter(
    df_fil,
    x="concentration",
    y="moyenne",
    trendline="ols",
    title="🧠 Concentration vs Performance"
)
st.plotly_chart(fig_b, use_container_width=True)

# Motivation vs performance
fig_c = px.scatter(
    df_fil,
    x="motivation",
    y="moyenne",
    trendline="ols",
    title="🔥 Motivation vs Performance"
)
st.plotly_chart(fig_c, use_container_width=True)

# Régularité vs performance
fig_d = px.scatter(
    df_fil,
    x="regularite",
    y="moyenne",
    trendline="ols",
    title="📖 Régularité vs Performance"
)
st.plotly_chart(fig_d, use_container_width=True)

st.divider()
# =========================
# COMPARAISONS
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
# BOXPLOT (INTOUCHABLE)
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
# INSIGHTS
# =========================
st.subheader("🧠 Analyse intelligente")

# Moyenne
best_filiere = df.groupby("filiere")["moyenne"].mean().idxmax()
worst_filiere = df.groupby("filiere")["moyenne"].mean().idxmin()

# Stress
stress_high = df.groupby("filiere")["stress"].mean().idxmax()
stress_low = df.groupby("filiere")["stress"].mean().idxmin()

# 🔥 NOUVEAUX INSIGHTS
concentration_high = df.groupby("filiere")["concentration"].mean().idxmax()
motivation_high = df.groupby("filiere")["motivation"].mean().idxmax()
regularite_high = df.groupby("filiere")["regularite"].mean().idxmax()

# ⚠️ ces colonnes doivent exister dans ton dataset
age_high = None
credits_high = None

if "age" in df.columns:
    age_high = df.groupby("filiere")["age"].mean().idxmax()

if "credits" in df.columns:
    credits_high = df.groupby("filiere")["credits"].mean().idxmax()

# =========================
# AFFICHAGE
# =========================
st.success(f"🏆 Filière la plus performante : {best_filiere}")
st.error(f"⚠️ Filière la moins performante : {worst_filiere}")

st.warning(f"😰 Filière la plus stressée : {stress_high}")
st.info(f"😌 Filière la moins stressée : {stress_low}")

st.success(f"🧠 Filière la plus concentrée : {concentration_high}")
st.success(f"🔥 Filière la plus motivée : {motivation_high}")
st.success(f"📖 Filière la plus régulière : {regularite_high}")

# Vérification pour éviter crash si colonne absente
if age_high:
    st.info(f"🎂 Filière avec étudiants les plus âgés : {age_high}")

if credits_high:
    st.info(f"🎓 Filière avec le plus de crédits validés : {credits_high}")

