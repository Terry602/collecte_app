import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

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
st.divider()

# =========================
# KPIs
# =========================
st.subheader("📈 Indicateurs clés")

col1, col2, col3 = st.columns(3)

col1.metric("🎓 Moyenne générale", round(df["moyenne"].mean(), 2))
col2.metric("😰 Stress moyen", round(df["stress"].mean(), 2))
col3.metric("📚 Heures d'étude", round(df["heures_etude"].mean(), 2))

st.divider()

# =========================
# 🎨 HISTOGRAMMES PREMIUM (MODERNISÉS)
# =========================
st.subheader("📊 Distributions (version améliorée)")

fig1 = px.histogram(
    df,
    x="moyenne",
    nbins=12,
    title="📊 Moyennes des étudiants",
    color_discrete_sequence=["#4CAF50"]
)
st.plotly_chart(fig1, use_container_width=True)

fig2 = px.histogram(
    df,
    x="stress",
    nbins=12,
    title="😰 Niveau de stress",
    color_discrete_sequence=["#F44336"]
)
st.plotly_chart(fig2, use_container_width=True)

fig3 = px.histogram(
    df,
    x="heures_etude",
    nbins=12,
    title="📚 Heures d'étude",
    color_discrete_sequence=["#2196F3"]
)
st.plotly_chart(fig3, use_container_width=True)

st.divider()

# =========================
# 🥧 PIE CHARTS MODERNES
# =========================
st.subheader("🥧 Répartitions")

col1, col2 = st.columns(2)

with col1:
    fig4, ax1 = plt.subplots()
    df["filiere"].value_counts().plot(
        kind="pie",
        autopct="%1.1f%%",
        startangle=90,
        colors=["#FF5733", "#FFC300", "#28B463", "#3498DB", "#9B59B6"],
        ax=ax1
    )
    ax1.set_ylabel("")
    ax1.set_title("🎓 Répartition par filière")
    st.pyplot(fig4)

with col2:
    fig5, ax2 = plt.subplots()
    df["sexe"].value_counts().plot(
        kind="pie",
        autopct="%1.1f%%",
        startangle=90,
        colors=["#FF9F1C", "#2EC4B6"],
        ax=ax2
    )
    ax2.set_ylabel("")
    ax2.set_title("👤 Répartition par sexe")
    st.pyplot(fig5)


    st.divider()

# =========================
# 🔥 CORRELATION
# =========================
st.subheader("🔥 Corrélation")

fig6, ax3 = plt.subplots(figsize=(10,6))
sns.heatmap(
    numeric_df.corr(),
    annot=True,
    cmap="coolwarm",
    fmt=".2f",
    ax=ax3
)
ax3.set_title("📊 Matrice de corrélation")
st.pyplot(fig6)

st.divider()

# =========================
# 📉 RELATIONS IMPORTANTES (MODERNISÉ PLOTLY)
# =========================
st.subheader("📉 Relations clés")

fig7 = px.scatter(
    df,
    x="heures_etude",
    y="moyenne",
    color="heures_etude",
    color_continuous_scale="Purples",
    title="📚 Étude vs Performance",
    trendline="ols"
)

fig7.update_traces(marker=dict(size=10, opacity=0.7))
fig7.update_layout(template="plotly_dark")

st.plotly_chart(fig7, use_container_width=True)


fig8 = px.scatter(
    df,
    x="stress",
    y="moyenne",
    color="stress",
    color_continuous_scale="Oranges",
    title="😰 Stress vs Performance",
    trendline="ols"
)

fig8.update_traces(marker=dict(size=10, opacity=0.7))
fig8.update_layout(template="plotly_dark")

st.plotly_chart(fig8, use_container_width=True)