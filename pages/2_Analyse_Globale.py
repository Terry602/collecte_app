import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Analyse Globale", layout="wide")

st.title("📊 Analyse Exploratoire des Données Étudiantes")

# =========================
# DATA
# =========================
@st.cache_data
def load_data():
    return pd.read_csv("data_students.csv")
if st.button("🔄 Rafraîchir"):
    st.cache_data.clear()

df = load_data()
try:
    df = load_data()
except:
    st.error("❌ Aucune donnée disponible.")
    st.stop()

numeric_df = df.select_dtypes(include=['int64', 'float64'])

# =========================
# KPIs
# =========================
st.subheader("📈 Indicateurs clés")

col1, col2, col3 = st.columns(3)

col1.metric("🎓 Moyenne générale", round(df["moyenne"].mean(), 2))
col2.metric("😰 Stress moyen", round(df["stress"].mean(), 2))
col3.metric("📚 Heures d'étude", round(df["heures_etude"].mean(), 2))

# =========================
# 🎨 STYLE HISTOGRAMMES PREMIUM
# =========================
st.subheader("📊 Distributions (version améliorée)")

def beautiful_hist(data, title, color):
    fig, ax = plt.subplots()

    ax.hist(
        data,
        bins=12,
        color=color,
        edgecolor="white",
        alpha=0.85
    )

    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.grid(axis="y", linestyle="--", alpha=0.3)

    return fig

# =========================
# HISTOGRAMMES (STYLE PRO)
# =========================
col1, col2, col3 = st.columns(3)

with col1:
    st.pyplot(beautiful_hist(df["moyenne"], "📊 Moyennes des étudiants", "#4CAF50"))

with col2:
    st.pyplot(beautiful_hist(df["stress"], "😰 Niveau de stress", "#F44336"))

with col3:
    st.pyplot(beautiful_hist(df["heures_etude"], "📚 Heures d'étude", "#2196F3"))

# =========================
# 🥧 PIE CHARTS MODERNES
# =========================
st.subheader("🥧 Répartitions")

col1, col2 = st.columns(2)

with col1:
    fig1, ax1 = plt.subplots()
    df["filiere"].value_counts().plot(
        kind="pie",
        autopct="%1.1f%%",
        startangle=90,
        colors=["#FF5733", "#FFC300", "#28B463", "#3498DB", "#9B59B6"],
        ax=ax1
    )
    ax1.set_ylabel("")
    ax1.set_title("🎓 Répartition par filière")
    st.pyplot(fig1)

with col2:
    fig2, ax2 = plt.subplots()
    df["sexe"].value_counts().plot(
        kind="pie",
        autopct="%1.1f%%",
        startangle=90,
        colors=["#FF9F1C", "#2EC4B6"],
        ax=ax2
    )
    ax2.set_ylabel("")
    ax2.set_title("👤 Répartition par sexe")
    st.pyplot(fig2)

# =========================
# 🔥 CORRELATION
# =========================
st.subheader("🔥 Corrélation")

fig3, ax3 = plt.subplots(figsize=(10,6))
sns.heatmap(
    numeric_df.corr(),
    annot=True,
    cmap="coolwarm",
    fmt=".2f",
    ax=ax3
)
ax3.set_title("📊 Matrice de corrélation")
st.pyplot(fig3)

# =========================
# 📉 RELATIONS IMPORTANTES
# =========================
st.subheader("📉 Relations clés")

fig4, ax4 = plt.subplots()
ax4.scatter(df["heures_etude"], df["moyenne"], color="#9C27B0", alpha=0.7)
ax4.set_title("📚 Étude vs Performance")
ax4.set_xlabel("Heures d'étude")
ax4.set_ylabel("Moyenne")
ax4.grid(alpha=0.2)
st.pyplot(fig4)

fig5, ax5 = plt.subplots()
ax5.scatter(df["stress"], df["moyenne"], color="#FF9800", alpha=0.7)
ax5.set_title("😰 Stress vs Performance")
ax5.set_xlabel("Stress")
ax5.set_ylabel("Moyenne")
ax5.grid(alpha=0.2)
st.pyplot(fig5)

# =========================
# 🎓 FILIERE
# =========================
st.subheader("🎓 Performance par filière")

fig6, ax6 = plt.subplots()

df.groupby("filiere")["moyenne"].mean().plot(
    kind="bar",
    ax=ax6,
    color=["#FF5733", "#FFC300", "#28B463", "#3498DB", "#9B59B6"]
)

ax6.set_title("📊 Moyenne par filière")
ax6.set_ylabel("Moyenne")
ax6.grid(axis="y", alpha=0.2)

st.pyplot(fig6)