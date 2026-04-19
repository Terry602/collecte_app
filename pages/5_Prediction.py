import streamlit as st
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_absolute_error, accuracy_score

st.set_page_config(page_title="Prédiction IA", layout="wide")

st.title("🤖 Module de Prédiction Intelligente (ML Avancé)")

# =========================
# DATA
# =========================
@st.cache_data
def load_data():
    return pd.read_csv("data_students.csv")

df = load_data()

# =========================
# 🔥 ENTRAINEMENT MULTI-MODELES (PAR FILIERE)
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
# 🎯 SELECTION FILIERE
# =========================
st.subheader("🎓 Choisir une filière")

filiere_selected = st.selectbox(
    "📚 Filière",
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
st.subheader("📊 Performances du modèle")

col1, col2 = st.columns(2)

col1.metric("📉 MAE", round(mae, 2))
col2.metric("🎯 Accuracy", round(acc, 2))

# Interprétation MAE
if mae < 1.5:
    st.success("✔ Prédiction très fiable (faible erreur)")
elif mae < 3:
    st.warning("⚠ Précision moyenne mais acceptable")
else:
    st.error("❌ Modèle peu précis → données insuffisantes ou bruit élevé")

# Interprétation accuracy
if acc > 0.85:
    st.success("✔ Excellent modèle de classification")
elif acc > 0.7:
    st.warning("⚠ Modèle correct mais améliorable")
else:
    st.error("❌ Modèle faible")

# =========================
# EXPLICATION PÉDAGOGIQUE (IMPORTANT 🔥)
# =========================
st.subheader("🧠 Explication du modèle")

st.markdown("""
 Le modèle utilise **toutes les variables collectées** :

- habitudes d’étude (heures, régularité)
- mode de vie (sommeil, téléphone, sport)
- bien-être (stress, motivation, concentration)
- profil étudiant (filière, niveau, sexe, méthode)

📌 Objectif :
- prédire la moyenne académique
- prédire la réussite ou l’échec

📊 Algorithme utilisé :
 Random Forest (modèle robuste et performant)
""")

# =========================
# IMPORTANCE
# =========================
st.subheader("📊 Facteurs les plus influents")

importance = pd.Series(model_reg.feature_importances_, index=features)
importance = importance.sort_values()

st.bar_chart(importance)

# =========================
# 🎯 SIMULATION
# =========================
st.subheader("🎯 Tester ton profil")

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

# gérer OneHot niveau
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
st.subheader("📌 Résultat")

st.metric("🎓 Moyenne prédite", round(pred_moyenne, 2))

if pred_reussite == 1:
    st.success("🎉 Réussite probable")
else:
    st.error("⚠ Risque d'échec")

# =========================
# ANALYSE
# =========================
st.subheader("💡 Analyse personnalisée")

if pred_moyenne < 10:
    st.warning("Profil à risque → augmente étude + réduit stress")
elif pred_moyenne < 13:
    st.info("Profil moyen → amélioration possible")
else:
    st.success("Excellent profil 🎯")







  