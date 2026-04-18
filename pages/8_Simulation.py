import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestRegressor

st.set_page_config(page_title="IA Simulation Pro", layout="wide")

st.title("🧠 Simulation IA Avancée (What-If Pro)")

# =========================
# DATA
# =========================
@st.cache_data
def load_data():
    return pd.read_csv("data_students.csv")

df = load_data()

# =========================
# ENCODAGE (IMPORTANT 🔥)
# =========================
df_model = pd.get_dummies(df, columns=["filiere", "sexe"], drop_first=True)

# =========================
# FEATURES
# =========================
features = [
    "heures_etude", "stress", "sommeil",
    "motivation", "concentration", "telephone"
] + [col for col in df_model.columns if "filiere_" in col or "sexe_" in col]

X = df_model[features]
y = df_model["moyenne"]

# =========================
# MODEL
# =========================
model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X, y)

# =========================
# INPUT USER
# =========================
st.subheader("🎯 Paramètres étudiant")

col1, col2, col3 = st.columns(3)

with col1:
    heures = st.slider("📚 Heures d'étude", 0, 12, 4)
    sommeil = st.slider("😴 Sommeil", 0, 12, 6)

with col2:
    stress = st.slider("😰 Stress", 1, 10, 5)
    motivation = st.slider("🔥 Motivation", 1, 10, 6)

with col3:
    concentration = st.slider("🧠 Concentration", 1, 10, 6)
    telephone = st.slider("📱 Téléphone", 0, 12, 4)

# =========================
# FILIERE + SEXE
# =========================
st.subheader("🎓 Profil étudiant")

filiere_input = st.selectbox("📚 Filière", df["filiere"].unique())
sexe_input = st.selectbox("👤 Sexe", df["sexe"].unique())

# =========================
# MOYENNE ACTUELLE
# =========================
st.subheader("🎯 Ta situation actuelle")

moyenne_actuelle = st.number_input(
    "🎓 Entre ta moyenne actuelle (/20)",
    0.0, 20.0, 10.0
)

# =========================
# CONSTRUCTION INPUT
# =========================
input_dict = {
    "heures_etude": heures,
    "stress": stress,
    "sommeil": sommeil,
    "motivation": motivation,
    "concentration": concentration,
    "telephone": telephone
}

# Ajouter colonnes encodées
for col in features:
    if "filiere_" in col:
        input_dict[col] = 1 if col == f"filiere_{filiere_input}" else 0
    elif "sexe_" in col:
        input_dict[col] = 1 if col == f"sexe_{sexe_input}" else 0

input_data = pd.DataFrame([input_dict])

# =========================
# PREDICTION
# =========================
pred = model.predict(input_data)[0]

diff = pred - moyenne_actuelle
percent = (diff / moyenne_actuelle) * 100 if moyenne_actuelle != 0 else 0

# =========================
# RESULTATS
# =========================
st.subheader("📊 Résultats de simulation")

col1, col2, col3 = st.columns(3)

col1.metric("🎓 Moyenne prédite", round(pred, 2))
col2.metric("🎯 Ta moyenne actuelle", round(moyenne_actuelle, 2))
col3.metric("📈 Impact", f"{percent:.1f}%")

# =========================
# GRAPH
# =========================
st.subheader("📊 Avant vs Après")

fig = go.Figure()

fig.add_trace(go.Bar(
    x=["Avant", "Après IA"],
    y=[moyenne_actuelle, pred],
    marker_color=["#FF9F1C", "#2EC4B6"]
))

fig.update_layout(
    title="Impact des habitudes + filière",
    yaxis_title="Moyenne /20"
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# EXPLICATION IA
# =========================
st.subheader("🧠 Diagnostic IA")

if diff > 2:
    st.success("🚀 Très forte amélioration possible")
elif diff > 0:
    st.info("📈 Amélioration détectée")
elif diff > -2:
    st.warning("⚠️ Légère baisse possible")
else:
    st.error("❌ Forte baisse de performance")

# =========================
# FOOTER
# =========================
st.divider()
st.info("🧠 Simulation IA avec prise en compte de la filière + sexe + note actuelle")