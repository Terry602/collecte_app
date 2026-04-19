






import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go  # ✅ CORRECTION ICI

from sklearn.ensemble import RandomForestRegressor

st.set_page_config(page_title="IA Simulation Pro", layout="wide")

st.title("🧠 Simulation IA (What-If Pro)")
st.divider()

# =========================
# DATA
# =========================
@st.cache_data
def load_data():
    return pd.read_csv("data_students.csv")

df = load_data()

# =========================
# 🔥 TRAIN MODELS PAR FILIERE
# =========================
@st.cache_resource
def train_models(df):

    models = {}

    for filiere in df["filiere"].dropna().unique():

        df_fil = df[df["filiere"] == filiere].copy()

        if len(df_fil) < 5:
            continue

        df_enc = pd.get_dummies(df_fil, columns=["sexe"], drop_first=True)

        features = [
            "heures_etude", "stress", "sommeil",
            "motivation", "concentration", "telephone"
        ] + [col for col in df_enc.columns if col.startswith("sexe_")]

        X = df_enc[features]
        y = df_enc["moyenne"]

        model = RandomForestRegressor(
            n_estimators=120,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )

        model.fit(X, y)

        models[filiere] = {
            "model": model,
            "features": features,
            "data": df_fil
        }

    return models


models = train_models(df)

# =========================
# CHOIX FILIERE
# =========================
st.subheader("🎓 Profil étudiant")

filiere_input = st.selectbox("📚 Filière", list(models.keys()))
model_data = models[filiere_input]

model = model_data["model"]
features = model_data["features"]
df_fil = model_data["data"]

sexe_input = st.selectbox("👤 Sexe", df_fil["sexe"].unique())

# =========================
# MOYENNE ACTUELLE
# =========================
st.subheader("🎯 Ta situation actuelle")

moyenne_actuelle = st.number_input(
    "🎓 Entre ta moyenne actuelle (/20)",
    0.0, 20.0, 10.0
)

# =========================
# 🔥 INITIALISATION INTELLIGENTE
# =========================
df_fil["diff"] = abs(df_fil["moyenne"] - moyenne_actuelle)
closest = df_fil.sort_values("diff").iloc[0]

# =========================
# INPUT USER
# =========================
st.subheader("🎯 Paramètres étudiant (modifiables)")

col1, col2, col3 = st.columns(3)

with col1:
    heures = st.slider("📚 Heures d'étude", 0, 12, int(closest["heures_etude"]))
    sommeil = st.slider("😴 Sommeil", 0, 12, int(closest["sommeil"]))

with col2:
    stress = st.slider("😰 Stress", 1, 10, int(closest["stress"]))
    motivation = st.slider("🔥 Motivation", 1, 10, int(closest["motivation"]))

with col3:
    concentration = st.slider("🧠 Concentration", 1, 10, int(closest["concentration"]))
    telephone = st.slider("📱 Téléphone", 0, 12, int(closest["telephone"]))

# =========================
# 🔥 FONCTION BUILD INPUT (MANQUANTE AVANT ❌)
# =========================
def build_input(h, s, sl, m, c, t):
    d = {
        "heures_etude": h,
        "stress": s,
        "sommeil": sl,
        "motivation": m,
        "concentration": c,
        "telephone": t
    }

    for col in features:
        if col.startswith("sexe_"):
            d[col] = 1 if col == f"sexe_{sexe_input}" else 0

    return pd.DataFrame([d])

# =========================
# INPUT MODEL
# =========================
input_data = build_input(
    heures, stress, sommeil,
    motivation, concentration, telephone
)

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
col2.metric("🎯 Moyenne actuelle", round(moyenne_actuelle, 2))
col3.metric("📈 Impact", f"{percent:.1f}%")
st.divider()
# =========================
# 🔥 RADAR CHART
# =========================
st.subheader("📡 Profil étudiant")

radar = go.Figure()

radar.add_trace(go.Scatterpolar(
    r=[heures, sommeil, 10-stress, motivation, concentration],
    theta=["Étude", "Sommeil", "Anti-stress", "Motivation", "Concentration"],
    fill='toself'
))

st.plotly_chart(radar, use_container_width=True)

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
    title="Impact des habitudes (par filière)",
    yaxis_title="Moyenne /20"
)

st.plotly_chart(fig, use_container_width=True)
st.divider()
# =========================
# 🔥 OPTIMISATION AUTO
# =========================
st.subheader("🚀 Optimisation automatique")

best_score = pred

for _ in range(100):
    test = build_input(
        np.random.randint(2, 10),
        np.random.randint(1, 6),
        np.random.randint(5, 10),
        np.random.randint(6, 10),
        np.random.randint(6, 10),
        np.random.randint(0, 6)
    )

    score = model.predict(test)[0]

    if score > best_score:
        best_score = score

st.metric("🎯 Meilleure moyenne possible", round(best_score, 2))

# =========================
# RECOMMANDATIONS IA
# =========================
st.subheader("💡 Recommandations IA")

if heures < 4:
    st.warning("📚 Augmente ton temps d'étude")

if stress > 6:
    st.warning("😰 Réduis ton stress")

if sommeil < 6:
    st.warning("😴 Dors plus")

if motivation < 5:
    st.warning("🔥 Travaille ta motivation")

if concentration < 5:
    st.warning("🧠 Améliore ta concentration")

if telephone > 6:
    st.warning("📱 Réduis le téléphone")

# =========================
# DIAGNOSTIC IA
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
st.info("🧠 IA par filière + simulation intelligente basée sur données réelles")























