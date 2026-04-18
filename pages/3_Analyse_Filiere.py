import streamlit as st
import pandas as pd
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
if st.button("🔄 Rafraîchir"):
    st.cache_data.clear()

df = load_data()
try:
    df = load_data()
except:
    st.error("❌ Aucune donnée disponible.")
    st.stop()

# =========================
# FILTRES
# =========================
filiere_selected = st.selectbox("🎯 Choisir une filière", df["filiere"].unique())

df_fil = df[df["filiere"] == filiere_selected]

# =========================
# KPI FILIERE
# =========================
st.subheader(f"📊 Indicateurs - {filiere_selected}")

col1, col2, col3 = st.columns(3)

col1.metric("🎓 Moyenne", round(df_fil["moyenne"].mean(), 2))
col2.metric("😰 Stress", round(df_fil["stress"].mean(), 2))
col3.metric("📚 Heures étude", round(df_fil["heures_etude"].mean(), 2))

# =========================
# COMPARAISON ENTRE FILIERES
# =========================
st.subheader("🏆 Comparaison des filières")

fig1, ax1 = plt.subplots(figsize=(10,5))
df.groupby("filiere")["moyenne"].mean().sort_values().plot(
    kind="bar",
    ax=ax1,
    color="#4CAF50"
)
ax1.set_title("Moyenne académique par filière")
ax1.set_ylabel("Moyenne")
st.pyplot(fig1)

# =========================
# STRESS PAR FILIERE
# =========================
st.subheader("😰 Niveau de stress par filière")

fig2, ax2 = plt.subplots(figsize=(10,5))
df.groupby("filiere")["stress"].mean().sort_values().plot(
    kind="bar",
    ax=ax2,
    color="#F44336"
)
ax2.set_title("Stress moyen par filière")
ax2.set_ylabel("Stress")
st.pyplot(fig2)

# =========================
# HEURES D'ÉTUDE PAR FILIERE
# =========================
st.subheader("📚 Effort d'étude par filière")

fig3, ax3 = plt.subplots(figsize=(10,5))
df.groupby("filiere")["heures_etude"].mean().sort_values().plot(
    kind="bar",
    ax=ax3,
    color="#2196F3"
)
ax3.set_title("Heures d'étude moyennes par filière")
ax3.set_ylabel("Heures")
st.pyplot(fig3)

# =========================
# BOXPLOT (IMPORTANT 🔥)
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
# INSIGHT AUTOMATIQUE (TRÈS IMPORTANT 🔥)
# =========================
st.subheader("🧠 Analyse intelligente")

best_filiere = df.groupby("filiere")["moyenne"].mean().idxmax()
worst_filiere = df.groupby("filiere")["moyenne"].mean().idxmin()

st.success(f"🏆 Filière la plus performante : {best_filiere}")
st.error(f"⚠️ Filière la moins performante : {worst_filiere}")

# Stress insight
stress_high = df.groupby("filiere")["stress"].mean().idxmax()

st.warning(f"😰 Filière la plus stressée : {stress_high}")