import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit.components.v1 as components

st.set_page_config(page_title="Analyse Globale", layout="wide")

components.html("""
<div style="
    background: linear-gradient(135deg, #ECFDF5, #D1FAE5);
    padding: 25px;
    border-radius: 18px;
    border: 1px solid #A7F3D0;
    text-align: center;
    margin-bottom: 20px;
    box-shadow: 0 8px 24px rgba(16,185,129,0.12);
    font-family: Arial;
">

    <div style="
        display:flex;
        align-items:center;
        justify-content:center;
        gap:12px;
    ">

        <svg width="40" height="40" viewBox="0 0 24 24"
             fill="none" stroke="#059669" stroke-width="2.5">

            <circle cx="11" cy="11" r="7"/>
            <line x1="21" y1="21" x2="16.65" y2="16.65"/>
            <polyline points="8 11 10 13 14 9"/>

        </svg>

        <div style="
            font-size:20px;
            font-weight:800;
            color:#064E3B;
        ">
            Analyse Globale des Données Étudiantes
        </div>

    </div>

    <div style="
        font-size:14px;
        color:#065F46;
        margin-top:8px;
    ">
        Exploration complète des tendances, performances et corrélations académiques
    </div>

</div>
""", height=180)

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
### 🌍  Indicateurs clés
</h3>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

col1.metric("🎓 Moyenne générale", round(df["moyenne"].mean(), 2))
col2.metric("😰 Stress moyen", round(df["stress"].mean(), 2))
col3.metric("📚 Heures d'étude moyenne", round(df["heures_etude"].mean(), 2))

st.divider()

# =========================
#  HISTOGRAMMES (inchangé)
# =========================
st.markdown("""
<h3 style="color:#3B82F6;">
### 📦 Distributions des variables
</h3>
""", unsafe_allow_html=True)

fig_hist = px.histogram(
    df,
    x="moyenne",
    nbins=20,
    title="Distribution des moyennes",
    marginal="box"
)

st.plotly_chart(fig_hist, use_container_width=True)

fig2 = px.histogram(df, x="stress", nbins=12, title=" Niveau de stress",
                    color_discrete_sequence=["#F44336"])
st.plotly_chart(fig2, use_container_width=True)

fig3 = px.histogram(df, x="heures_etude", nbins=12, title=" Heures d'étude",
                    color_discrete_sequence=["#2196F3"])
st.plotly_chart(fig3, use_container_width=True)

st.divider()

# =========================
#  PIE CHARTS 
# =========================
st.markdown("""
<h3 style="color:#059669;">
### 🔀 Répartitions
</h3>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    fig4 = px.pie(
        df,
        names="filiere",
        title=" Répartition par filière",
        color_discrete_sequence=["#FF5733", "#FFC300", "#28B463", "#3498DB", "#9B59B6"]
    )
    st.plotly_chart(fig4, use_container_width=True)

with col2:
    fig5 = px.pie(
        df,
        names="sexe",
        title=" Répartition par sexe",
        color_discrete_sequence=["#FF9F1C", "#2EC4B6"]
    )
    st.plotly_chart(fig5, use_container_width=True)

st.divider()

# =========================
#  CORRELATION 
# =========================
st.markdown("""
<h3 style="color:#92400E;">
### 🔗 Corrélation
</h3>
""", unsafe_allow_html=True)

corr_matrix = numeric_df.corr()

fig6 = px.imshow(
    corr_matrix,
    text_auto=True,
    color_continuous_scale="RdBu_r",
    title=" Matrice de corrélation"
)

st.plotly_chart(fig6, use_container_width=True)

st.divider()

# =========================
#  RELATIONS IMPORTANTES (inchangé)
# =========================
st.markdown("""
<h3 style="color:#EAB308;">
### 🔑 Relations clés
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
# BOXPLOT 
# =========================
st.markdown("""
<h3 style="color:#94A3B8;">
### 📊 Distribution des notes par filière
</h3>
""", unsafe_allow_html=True)

fig9 = px.box(
    df,
    x="filiere",
    y="moyenne",
    color="filiere",
    title="Répartition des moyennes par filière",
    color_discrete_sequence=px.colors.qualitative.Set2
)

fig9.update_layout(xaxis_tickangle=45)

st.plotly_chart(fig9, use_container_width=True)

st.divider()
# ==========================================================
#  TENDANCES
# ==========================================================
st.subheader("📈 Tendances globales")

trend = df.groupby("niveau")["moyenne"].mean().reset_index()

fig_trend = px.line(
    trend,
    x="niveau",
    y="moyenne",
    markers=True,
    title="Évolution des performances par niveau"
)

st.plotly_chart(fig_trend, use_container_width=True)

st.divider()

# =========================
# EXPORT CSV + AFFICHAGE DONNÉES (inchangé)
# =========================
st.subheader("📁 Export & Visualisation de données")
col1, col2 = st.columns(2)

csv = df.to_csv(index=False).encode("utf-8")

with col1:
    st.download_button(
        label="📥 Télécharger les données CSV",
        data=csv,
        file_name="donnees_etudiants.csv",
        mime="text/csv"
    )

with col2:
    show_data = st.button("👁️ Voir les données brutes")

if show_data:
    st.subheader("📚 Liste complète des étudiants")

    st.dataframe(
        df,
        use_container_width=True
    )
