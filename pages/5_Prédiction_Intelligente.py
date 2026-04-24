import streamlit as st
import pandas as pd
import numpy as np
import streamlit.components.v1 as components

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_absolute_error, accuracy_score

st.set_page_config(page_title="Prédiction IA", layout="wide")

components.html("""
<div style="
    background: linear-gradient(135deg, #0F172A, #111827);
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #1F2937;
    text-align: center;
    box-shadow: 0 10px 25px rgba(0,0,0,0.25);
    margin-bottom: 10px;
    font-family: Arial, sans-serif;
">

    <!-- HEADER FLEX -->
    <div style="
        display:flex;
        align-items:center;
        justify-content:center;
        gap:12px;
    ">

        <!-- 🧠 + 📈 AI PREDICTION ICON -->
        <svg width="44" height="44" viewBox="0 0 24 24"
             fill="none"
             stroke="#A78BFA"
             stroke-width="2.2"
             stroke-linecap="round"
             stroke-linejoin="round">

            <!-- brain / AI core -->
            <path d="M9 3c-2 0-3.5 1.5-3.5 3.5S7 10 7 10"/>
            <path d="M15 3c2 0 3.5 1.5 3.5 3.5S17 10 17 10"/>
            <path d="M7 10c-1.5 0-2.5 1-2.5 2.5S6 15 7 15"/>
            <path d="M17 10c1.5 0 2.5 1 2.5 2.5S18 15 17 15"/>

            <!-- upward trend (prediction) -->
            <polyline points="6 18 10 14 13 16 18 9"/>

        </svg>

        <!-- TITLE -->
        <div style="
            font-size:25px;
            font-weight:800;
            color:#F8FAFC;
            letter-spacing:-0.5px;
        ">
            Module de Prédiction Intelligente
        </div>

    </div>

    <!-- SUBTITLE -->
    <div style="
        margin-top:6px;
        font-size:13px;
        color:#94A3B8;
    ">
        AI-powered Academic Performance Prediction System
    </div>

</div>
""", height=150)

st.divider()
# =========================
# DATA
# =========================
@st.cache_data
def load_data():
    return pd.read_csv("data_students.csv")

df = load_data()

# =========================
#  ENTRAINEMENT MULTI-MODELES (PAR FILIERE)
# =========================
@st.cache_resource
def train_models(df):

    models = {}
    encodings = {}

    for filiere in df["filiere"].dropna().unique():

        df_fil = df[df["filiere"] == filiere].copy()

        if len(df_fil) < 5:
            continue

        # encodage
        df_fil["sexe"] = df_fil["sexe"].map({"Masculin": 0, "Féminin": 1})
        df_fil["sport"] = df_fil["sport"].map({"Non": 0, "Oui": 1})
        df_fil["methode"] = df_fil["methode"].map({"Seul": 0, "Groupe": 1})

        df_fil = pd.get_dummies(df_fil, columns=["niveau"], drop_first=True)

        features = [
            "heures_etude",
            "regularite",
            "sommeil",
            "stress",
            "concentration",
            "motivation",
            "telephone",
            "sexe",
            "sport",
            "methode"
        ] + [col for col in df_fil.columns if col.startswith("niveau_")]

        X = df_fil[features]
        y = df_fil["moyenne"]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        model_reg = RandomForestRegressor(
            n_estimators=120,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )

        model_reg.fit(X_train, y_train)

        y_pred = model_reg.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)

        # classification
        df_fil["reussite"] = (df_fil["moyenne"] >= 10).astype(int)

        model_clf = RandomForestClassifier(
            n_estimators=120,
            max_depth=8,
            random_state=42,
            n_jobs=-1
        )

        model_clf.fit(X, df_fil["reussite"])

        acc = accuracy_score(df_fil["reussite"], model_clf.predict(X))

        # stockage
        models[filiere] = {
            "reg": model_reg,
            "clf": model_clf,
            "features": features,
            "mae": mae,
            "acc": acc
        }

    return models


models = train_models(df)

# =========================
# EXPLICATION PÉDAGOGIQUE
# =========================

st.subheader("📖 Explication du modèle")

st.components.v1.html("""
<style>

/* ===== CONTAINER GLOBAL ===== */
.scroll-wrapper {
    height: 60px;
    overflow: hidden;
    width: 100%;
    position: relative;
}

/* ===== CONTENT ===== */
.scroll-content {
    display: flex;
    flex-direction: column;
    animation: scrollStep 32s infinite;
}

/* ===== LINE ===== */
.line {
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 15px;
    color: #64748B;
    transition: all 0.4s ease;
}

/* ===== ACTIVE LINE ===== */
.line.active {
    font-size: 17px;
    font-weight: 700;
    color:#3B82F6;
    transform: scale(1.05);
}

/* ===== ANIMATION ===== */
@keyframes scrollStep {

    0%   { transform: translateY(0%); }
    10%  { transform: translateY(0%); }

    12.5% { transform: translateY(-60px); }
    22.5% { transform: translateY(-60px); }

    25%  { transform: translateY(-120px); }
    35%  { transform: translateY(-120px); }

    37.5% { transform: translateY(-180px); }
    47.5% { transform: translateY(-180px); }

    50%  { transform: translateY(-240px); }
    60%  { transform: translateY(-240px); }

    62.5% { transform: translateY(-300px); }
    72.5% { transform: translateY(-300px); }

    75%  { transform: translateY(-360px); }
    85%  { transform: translateY(-360px); }

    87.5% { transform: translateY(-420px); }
    97.5% { transform: translateY(-420px); }

    100% { transform: translateY(0%); }
}

</style>

<div class="scroll-wrapper">
    <div class="scroll-content">

        <div class="line active"> Le modèle analyse et exploite toutes les variables de la filière choisie </div>
        <div class="line"> Ceci étant, les variables exploitées sont entre autres : </div>

        <div class="line">- Habitudes d’étude : heures et régularité</div>

        <div class="line">- Mode de vie : sommeil, téléphone, sport</div>

        <div class="line">- Bien-être : stress, motivation, concentration</div>

        <div class="line">- Profil académique : filière, niveau, sexe, méthode</div>

        <div class="line"> Objectif : </div>

        <div class="line">- prédire la moyenne académique</div> 

        <div class="line">- prédire la réussite ou l’échec</div>


        <div class="line"> Algorithme utilisée : Random Forest (robuste et performant)</div>

    </div>
</div>
""", height=90)
# =========================
#  SELECTION FILIERE
# =========================
st.subheader("📌 Choisir une filière")

filiere_selected = st.selectbox(
    "Filière",
    sorted(models.keys())
)

model_data = models[filiere_selected]

model_reg = model_data["reg"]
model_clf = model_data["clf"]
features = model_data["features"]
mae = model_data["mae"]
acc = model_data["acc"]

# =========================
# RESULTATS
# =========================
st.subheader("⚡ Performances du modèle")

col1, col2 = st.columns(2)

col1.metric(" MAE(Erreur Moyenne)", round(mae, 2))
col2.metric(" Accuracy", round(acc, 2))

if mae < 1.5:
    st.success(" Prédiction très fiable (faible erreur)")
elif mae < 3:
    st.warning(" Précision moyenne mais acceptable")
else:
    st.error(" Modèle peu précis → données insuffisantes ou bruit élevé")

if acc > 0.85:
    st.success(" Excellent modèle de classification")
elif acc > 0.7:
    st.warning(" Modèle correct mais améliorable")
else:
    st.error(" Modèle faible")


st.divider()
# =========================
# IMPORTANCE
# =========================
st.subheader("🌫️ Facteurs les plus influents")

importance = pd.Series(model_reg.feature_importances_, index=features)
importance = importance.sort_values()

st.bar_chart(importance)
st.divider()
# =========================
#  SIMULATION
# =========================
st.subheader("🧪 Tester ton profil")

col1, col2 = st.columns(2)

with col1:
    heures = st.slider("📚 Heures d'étude", 0, 12, 3)
    regularite = st.slider("📖 Régularité", 1, 10, 5)
    sommeil = st.slider("😴 Sommeil", 0, 12, 6)
    stress = st.slider("😰 Stress", 1, 10, 5)
    concentration = st.slider("🧠 Concentration", 1, 10, 5)
    motivation = st.slider("🔥 Motivation", 1, 10, 5)

with col2:
    telephone = st.slider("📱 Téléphone", 0, 12, 4)
    sexe = st.selectbox("Sexe", ["Masculin", "Féminin"])
    sport = st.selectbox("Sport", ["Oui", "Non"])
    methode = st.selectbox("Méthode", ["Seul", "Groupe"])

    niveau = st.selectbox(
        "Niveau",
        [f.replace("niveau_", "") for f in features if "niveau_" in f]
    )

# =========================
# INPUT
# =========================
input_dict = {
    "heures_etude": heures,
    "regularite": regularite,
    "sommeil": sommeil,
    "stress": stress,
    "concentration": concentration,
    "motivation": motivation,
    "telephone": telephone,
    "sexe": 0 if sexe == "Masculin" else 1,
    "sport": 1 if sport == "Oui" else 0,
    "methode": 0 if methode == "Seul" else 1
}

for col in features:
    if col.startswith("niveau_"):
        input_dict[col] = 0

col_niveau = f"niveau_{niveau}"
if col_niveau in input_dict:
    input_dict[col_niveau] = 1

input_data = pd.DataFrame([input_dict])

# =========================
# PREDICTION
# =========================
pred_moyenne = model_reg.predict(input_data)[0]
pred_reussite = model_clf.predict(input_data)[0]

# =========================
# RESULTATS
# =========================
st.subheader(" Résultat")

color = "#16A34A" if pred_moyenne >= 10 else "#DC2626"

st.markdown(f"""
<div style="
    background: #FFFFFF;
    padding: 16px;
    border-radius: 12px;
    border: 1px solid #E5E7EB;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
">
    <div style="font-size:14px; color:#64748B;">🎓 Moyenne prédite</div>
    <div style="font-size:28px; font-weight:800; color:{color};">
        {round(pred_moyenne, 2)} / 20
    </div>
</div>
""", unsafe_allow_html=True)

if pred_reussite == 1:
    st.success("🎉 Réussite probable")
else:
    st.error("⚠ Risque d'échec")

st.divider()
# =========================
# ANALYSE
# =========================
st.subheader(" Analyse personnalisée")

if pred_moyenne < 10:
    st.warning("Profil à risque, augmente tes heures d'étude et réduit le (stress + telephone + sommeil)")
elif pred_moyenne < 13:
    st.info("Profil moyen, amélioration possible")
else:
    st.success("Excellent profil ")







  
