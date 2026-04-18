import streamlit as st
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_absolute_error, accuracy_score
from sklearn.preprocessing import LabelEncoder

st.set_page_config(page_title="Prédiction IA", layout="wide")

st.title("🤖 Module de Prédiction Intelligente (ML Avancé)")

# =========================
# CHARGEMENT DATA
# =========================
@st.cache_data
def load_data():
    return pd.read_csv("data_students.csv")

try:
    df = load_data()
except:
    st.error("❌ Aucune donnée disponible.")
    st.stop()

# =========================
# NETTOYAGE / ENCODAGE
# =========================
df_ml = df.copy()

# Encodage binaire
df_ml["sexe"] = df_ml["sexe"].map({"Masculin": 0, "Féminin": 1})
df_ml["sport"] = df_ml["sport"].map({"Non": 0, "Oui": 1})
df_ml["methode"] = df_ml["methode"].map({"Seul": 0, "Groupe": 1})

# Encodage catégoriel (important 🔥)
le_filiere = LabelEncoder()
le_niveau = LabelEncoder()

df_ml["filiere"] = le_filiere.fit_transform(df_ml["filiere"])
df_ml["niveau"] = le_niveau.fit_transform(df_ml["niveau"])

# =========================
# FEATURES (TOUTES LES DONNÉES UTILISÉES)
# =========================
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
    "methode",
    "filiere",
    "niveau"
]

X = df_ml[features]

# =========================
# TARGET 1 : RÉGRESSION (MOYENNE)
# =========================
y_reg = df_ml["moyenne"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y_reg, test_size=0.2, random_state=42
)

model_reg = RandomForestRegressor(
    n_estimators=200,
    random_state=42,
    max_depth=10
)

model_reg.fit(X_train, y_train)
y_pred = model_reg.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)

# =========================
# TARGET 2 : CLASSIFICATION (RÉUSSITE)
# =========================
df_ml["reussite"] = (df_ml["moyenne"] >= 10).astype(int)

y_clf = df_ml["reussite"]

X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(
    X, y_clf, test_size=0.2, random_state=42
)

model_clf = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    max_depth=10
)

model_clf.fit(X_train_c, y_train_c)
y_pred_c = model_clf.predict(X_test_c)

acc = accuracy_score(y_test_c, y_pred_c)

# =========================
# RÉSULTATS
# =========================
st.subheader("📊 Performances du modèle")

col1, col2 = st.columns(2)

col1.metric("📉 Erreur moyenne (MAE)", round(mae, 2))
col2.metric("🎯 Accuracy", round(acc, 2))

# =========================
# EXPLICATION PÉDAGOGIQUE (IMPORTANT 🔥)
# =========================
st.subheader("🧠 Explication du modèle (pour le jury)")

st.markdown("""
👉 Le modèle utilise **toutes les variables collectées** :

- habitudes d’étude (heures, régularité)
- mode de vie (sommeil, téléphone, sport)
- bien-être (stress, motivation, concentration)
- profil étudiant (filière, niveau, sexe, méthode)

📌 Objectif :
- prédire la moyenne académique
- prédire la réussite ou l’échec

📊 Algorithme utilisé :
👉 Random Forest (modèle robuste et performant)
""")

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
# IMPORTANCE DES VARIABLES
# =========================
st.subheader("📊 Facteurs les plus influents")

importance = pd.Series(model_reg.feature_importances_, index=features)
importance = importance.sort_values()

st.bar_chart(importance)

st.write("""
👉 Interprétation :
Les variables les plus importantes sont celles qui influencent le plus la moyenne académique.
""")

# =========================
# PRÉDICTION UTILISATEUR
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
    filiere = st.selectbox("Filière", df["filiere"].unique())
    niveau = st.selectbox("Niveau", df["niveau"].unique())

# encodage input
input_data = pd.DataFrame([[
    heures,
    regularite,
    sommeil,
    stress,
    concentration,
    motivation,
    telephone,
    0 if sexe == "Masculin" else 1,
    1 if sport == "Oui" else 0,
    0 if methode == "Seul" else 1,
    le_filiere.transform([filiere])[0],
    le_niveau.transform([niveau])[0]
]], columns=features)

# prédictions
pred_moyenne = model_reg.predict(input_data)[0]
pred_reussite = model_clf.predict(input_data)[0]

# =========================
# RÉSULTATS
# =========================
st.subheader("📌 Résultat")

st.metric("🎓 Moyenne prédite", round(pred_moyenne, 2))

if pred_reussite == 1:
    st.success("🎉 Prédiction : RÉUSSITE probable")
else:
    st.error("⚠ Prédiction : RISQUE D'ÉCHEC")

# =========================
# EXPLICATION PERSONNALISÉE
# =========================
st.subheader("💡 Analyse personnalisée")

if pred_moyenne < 10:
    st.write("👉 Le modèle prédit une moyenne faible (<10). Risque d’échec élevé.")
    st.write("💡 Conseils : augmenter le temps d’étude et réduire le stress.")

elif pred_moyenne < 13:
    st.write("👉 Profil moyen. Résultats corrects mais instables.")
    st.write("💡 Conseils : améliorer la régularité et la concentration.")

else:
    st.write("👉 Excellent profil académique.")
    st.write("💡 Continue tes bonnes habitudes.")

# =========================
# BONUS SCIENTIFIQUE
# =========================
st.subheader("📚 Note méthodologique")

st.info("""
👉 Le modèle utilise Random Forest car :
- il gère bien les données mixtes
- il est robuste au bruit
- il permet d’évaluer l’importance des variables

⚠ Limite :
- dépend de la qualité des données collectées
""")