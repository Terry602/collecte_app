import streamlit as st
import pandas as pd
import os
import time

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="SmartStudent Analytics", layout="centered")

st.markdown("""
<style>

/* ===== HEADER LIGHT SAAS ===== */
.form-header {
    background: linear-gradient(135deg, #F8FAFC, #EEF2FF);
    padding: 22px;
    border-radius: 14px;
    border: 1px solid #E5E7EB;
    text-align: center;
    box-shadow: 0 4px 14px rgba(0,0,0,0.05);
    margin-bottom: 10px;
}

/* TITLE */
.form-title {
    font-size: 28px;
    font-weight: 800;
    color: #0F172A;
    letter-spacing: -0.3px;
}

/* SUBTITLE */
.form-subtitle {
    font-size: 13px;
    color: #64748B;
    margin-top: 6px;
}
</style>

<div class="form-header">
    <div class="form-title"> SmartStudent Analytics Forms</div>
    <div class="form-subtitle">Data collection & intelligent student profiling system</div>
</div>
""", unsafe_allow_html=True)

st.divider()
st.subheader(" Formulaire de collecte des données étudiants")

DATA_FILE = "data_students.csv"

# =========================
# FORMULAIRE
# =========================
with st.form("student_form"):

    st.markdown("### 👤 Identité")

    prenom = st.text_input("Prénom")
    nom = st.text_input("Nom")

    st.markdown("### 🧾 Informations générales")
    age = st.number_input("Âge", min_value=15, max_value=60, step=1)
    sexe = st.selectbox("Sexe", ["Masculin", "Féminin"])

    filiere = st.selectbox(
        "Filière",
        ["Informatique", "Maths", "Économie", "Droit", "Médecine",
         "Physique", "Chimie", "Biologie", "Histoire", "Géographie",
         "Langue étrangère", "Géologie", "Philosophie"]
    )

    niveau = st.selectbox("Niveau", ["L1", "L2", "L3", "Master1", "Master2", "PhD"])

    st.markdown("### 📚 Habitudes d'étude")
    heures_etude = st.slider("Heures d'étude par jour", 0, 12, 2)
    methode = st.selectbox("Méthode d'apprentissage", ["Seul", "Groupe"])
    regularite = st.slider("Régularité (1 à 10)", 1, 10, 5)

    st.markdown("### 🍎 Mode de vie")
    sommeil = st.slider("Heures de sommeil", 0, 12, 6)
    sport = st.selectbox("Activité sportive", ["Oui", "Non"])
    telephone = st.slider("Temps téléphone (heures/jour)", 0, 12, 4)

    st.markdown("### 😰 Bien-être")
    stress = st.slider("Stress (1 à 10)", 1, 10, 5)
    concentration = st.slider("Concentration (1 à 10)", 1, 10, 5)
    motivation = st.slider("Motivation (1 à 10)", 1, 10, 5)

    st.markdown("### 🎓 Résultats")
    moyenne = st.number_input("Moyenne (/20)", 0.0, 20.0, 10.0)
    credits = st.number_input("Crédits validés", 0, 60, 20)

    submit = st.form_submit_button("💾 Enregistrer")

# =========================
# SAUVEGARDE SAFE + MESSAGES TEMPORAIRES
# =========================
if submit:

    nom_complet = f"{prenom} {nom}".strip()

    new_data = pd.DataFrame([{
        "nom": nom_complet,
        "age": age,
        "sexe": sexe,
        "filiere": filiere,
        "niveau": niveau,
        "heures_etude": heures_etude,
        "methode": methode,
        "regularite": regularite,
        "sommeil": sommeil,
        "sport": sport,
        "telephone": telephone,
        "stress": stress,
        "concentration": concentration,
        "motivation": motivation,
        "moyenne": moyenne,
        "credits": credits
    }])

    # =========================
    # COMPATIBILITÉ ANCIENNES DONNÉES
    # =========================
    if os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0:
        df = pd.read_csv(DATA_FILE)

        if "nom" not in df.columns:
            df["nom"] = "Inconnu"

        df = pd.concat([df, new_data], ignore_index=True)

    else:
        df = new_data

    df.to_csv(DATA_FILE, index=False)

    # =========================
    # MESSAGES TEMPORAIRES (2 secondes)
    # =========================
    placeholder = st.empty()

    placeholder.success(" Données enregistrées avec succès !")
    time.sleep(2)
    placeholder.empty()

    placeholder2 = st.empty()
    placeholder2.info(" Données ajoutées au système d'analyse")
    time.sleep(2)
    placeholder2.empty()