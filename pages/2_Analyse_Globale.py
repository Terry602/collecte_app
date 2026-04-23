import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px


st.set_page_config(page_title="Analyse Globale", layout="wide")

st.markdown("""
<style>

/* ===== ANALYTICS HEADER GREEN STYLE ===== */
.analytics-header {
    background: linear-gradient(135deg, #ECFDF5, #D1FAE5);
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #A7F3D0;
    text-align: center;
    margin-bottom: 12px;
    box-shadow: 0 6px 18px rgba(16,185,129,0.08);
}

/* TITLE */
.analytics-title {
    font-size: 30px;
    font-weight: 800;
    color: #064E3B;
    letter-spacing: -0.4px;
}

/* SUBTITLE */
.analytics-subtitle {
    font-size: 13px;
    color: #065F46;
    margin-top: 6px;
}
</style>

<div class="analytics-header">
    <div class="analytics-title"> Analyse Globale des Données Étudiantes</div>
    <div class="analytics-subtitle">Exploration complète des tendances, performances et corrélations académiques</div>
</div>
""", unsafe_allow_html=True)

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
    st.error(" Aucune donnée disponible.")
    st.stop()

numeric_df = df.select_dtypes(include=['int64', 'float64'])
st.divider()

# =========================
# KPIs
# =========================
st.markdown("""
<h3 style="color:#92400E;">
 Indicateurs clés
</h3>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

col1.metric("🎓 Moyenne générale", round(df["moyenne"].mean(), 2))
col2.metric("😰 Stress moyen", round(df["stress"].mean(), 2))
col3.metric("📚 Heures d'étude", round(df["heures_etude"].mean(), 2))

st.divider()

# =========================
#  HISTOGRAMMES
# =========================
st.markdown("""
<h3 style="color:#64748B;">
 Distributions des variables
</h3>
""", unsafe_allow_html=True)

fig1 = px.histogram(
    df,
    x="moyenne",
    nbins=12,
    title=" Moyennes des étudiants",
    color_discrete_sequence=["#4CAF50"]
)
st.plotly_chart(fig1, use_container_width=True)

fig2 = px.histogram(
    df,
    x="stress",
    nbins=12,
    title=" Niveau de stress",
    color_discrete_sequence=["#F44336"]
)
st.plotly_chart(fig2, use_container_width=True)

fig3 = px.histogram(
    df,
    x="heures_etude",
    nbins=12,
    title=" Heures d'étude",
    color_discrete_sequence=["#2196F3"]
)
st.plotly_chart(fig3, use_container_width=True)

st.divider()

# =========================
#  PIE CHARTS MODERNES
# =========================
st.markdown("""
<h3 style="color:#64748B;">
 Répartitions
</h3>
""", unsafe_allow_html=True)

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
    ax1.set_title(" Répartition par filière")
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
    ax2.set_title(" Répartition par sexe")
    st.pyplot(fig5)


st.divider()

# =========================
#  CORRELATION
# =========================
st.markdown("""
<h3 style="color:#64748B;">
 Corrélation
</h3>
""", unsafe_allow_html=True)

fig6, ax3 = plt.subplots(figsize=(10,6))
sns.heatmap(
    numeric_df.corr(),
    annot=True,
    cmap="coolwarm",
    fmt=".2f",
    ax=ax3
)
ax3.set_title(" Matrice de corrélation")
st.pyplot(fig6)

st.divider()

# =========================
#  RELATIONS IMPORTANTES (MODERNISÉ PLOTLY)
# =========================
st.markdown("""
<h3 style="color:#64748B;">
Relations clés
</h3>
""", unsafe_allow_html=True)

fig7 = px.scatter(
    df,
    x="heures_etude",
    y="moyenne",
    color="heures_etude",
    color_continuous_scale="Purples",
    title=" Étude vs Performance",
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
    title=" Stress vs Performance",
    trendline="ols"
)

fig8.update_traces(marker=dict(size=10, opacity=0.7))
fig8.update_layout(template="plotly_dark")

st.plotly_chart(fig8, use_container_width=True)

st.divider()

# =========================
# BOXPLOT (INTOUCHABLE)
# =========================
st.markdown("""
<h3 style="color:#64748B;">
 Distribution des notes par filière
</h3>
""", unsafe_allow_html=True)

fig4, ax4 = plt.subplots(figsize=(10,6))
sns.boxplot(data=df, x="filiere", y="moyenne", ax=ax4, palette="Set2")

ax4.set_title("Répartition des moyennes par filière")
ax4.set_xlabel("Filière")
ax4.set_ylabel("Moyenne")

plt.xticks(rotation=45)

st.pyplot(fig4)

st.divider()
# =========================
# EXPORT CSV + AFFICHAGE DONNÉES
# =========================
col1, col2 = st.columns(2)

# =========================
# BOUTON 1 : DOWNLOAD CSV
# =========================
csv = df.to_csv(index=False).encode("utf-8")

with col1:
    st.download_button(
        label="📥 Télécharger les données CSV",
        data=csv,
        file_name="donnees_etudiants.csv",
        mime="text/csv"
    )

# =========================
# BOUTON 2 : AFFICHER DATA
# =========================
with col2:
    show_data = st.button("👁️ Voir tous les étudiants")

# =========================
# AFFICHAGE CONDITIONNEL
# =========================
if show_data:
    st.subheader("📚 Liste complète des étudiants")

    st.dataframe(
        df,
        use_container_width=True
    )