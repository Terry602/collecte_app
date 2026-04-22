import streamlit as st
import pandas as pd
import plotly.express as px

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

st.set_page_config(page_title="Clustering Étudiants", layout="wide")

st.markdown("""
<style>

/* ===== CLUSTERING HEADER (AI / PURPLE SCIENCE STYLE) ===== */
.clustering-header {
    background: linear-gradient(135deg, #F5F3FF, #EDE9FE);
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #DDD6FE;
    text-align: center;
    margin-bottom: 12px;
    box-shadow: 0 10px 25px rgba(139,92,246,0.12);
}

/* TITLE */
.clustering-title {
    font-size: 30px;
    font-weight: 800;
    color: #1E1B4B;
    letter-spacing: -0.4px;
}

/* SUBTITLE */
.clustering-subtitle {
    font-size: 13px;
    color: #6D28D9;
    margin-top: 6px;
}
</style>

<div class="clustering-header">
    <div class="clustering-title">🧠 Segmentation Intelligente des Étudiants</div>
    <div class="clustering-subtitle">Machine Learning • K-Means • AI-driven Student Profiling</div>
</div>
""", unsafe_allow_html=True)

# =========================
# DATA
# =========================
@st.cache_data
def load_data():
    return pd.read_csv("data_students.csv")

try:
    df = load_data()
except:
    st.error("❌ Aucune donnée disponible")
    st.stop()

# =========================
# FEATURES POUR CLUSTERING
# =========================
features = [
    "moyenne",
    "stress",
    "heures_etude",
    "sommeil",
    "motivation",
    "concentration"
]

X = df[features]

# =========================
# NORMALISATION (IMPORTANT 🔥)
# =========================
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# =========================
# KMEANS MODEL
# =========================
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df["cluster"] = kmeans.fit_predict(X_scaled)

# =========================
# LABELS INTELLIGENTS
# =========================
cluster_map = {}

for c in df["cluster"].unique():
    avg_score = df[df["cluster"] == c]["moyenne"].mean()

    if avg_score >= 13:
        cluster_map[c] = "🟢 Performants"
    elif avg_score >= 10:
        cluster_map[c] = "🟡 Moyens"
    else:
        cluster_map[c] = "🔴 À risque"

df["profil"] = df["cluster"].map(cluster_map)
st.divider()
# =========================
# DISPLAY KPI
# =========================
st.subheader("📊 Répartition des profils")

col1, col2, col3 = st.columns(3)

col1.metric("🟢 Performants", (df["profil"] == "🟢 Performants").sum())
col2.metric("🟡 Moyens", (df["profil"] == "🟡 Moyens").sum())
col3.metric("🔴 À risque", (df["profil"] == "🔴 À risque").sum())
st.divider()
# =========================
# VISUALISATION 2D
# =========================
st.subheader("📉 Visualisation des clusters")

fig = px.scatter(
    df,
    x="heures_etude",
    y="moyenne",
    color="profil",
    color_discrete_map={
        "🟢 Performants": "green",
        "🟡 Moyens": "orange",
        "🔴 À risque": "red"
    },
    title="Segmentation des étudiants"
)

st.plotly_chart(fig, use_container_width=True)
st.divider()
# =========================
# PROFILS EXPLIQUÉS
# =========================
st.subheader("🧠 Analyse des groupes")

for profil in df["profil"].unique():
    st.markdown(f"### {profil}")

    subset = df[df["profil"] == profil]

    st.write("📊 Moyenne :", round(subset["moyenne"].mean(), 2))
    st.write("😰 Stress :", round(subset["stress"].mean(), 2))
    st.write("📚 Étude :", round(subset["heures_etude"].mean(), 2))
    st.write("👥 Effectif :", len(subset))

st.divider()