import streamlit as st
import pandas as pd
import os
import time

st.set_page_config(page_title="Gestion des étudiants", layout="wide")

st.title("🗑️ Gestion des étudiants")

DATA_FILE = "data_students.csv"

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_FILE)

    if "nom" not in df.columns:
        df["nom"] = "Inconnu"

    if "filiere" not in df.columns:
        df["filiere"] = "Non défini"

    if "niveau" not in df.columns:
        df["niveau"] = "Non défini"

    return df

df = load_data()

# =========================
# FILTRES
# =========================
st.subheader("🎓 Sélection de l'étudiant")

filiere = st.selectbox(
    "📚 Choisir la filière",
    sorted(df["filiere"].dropna().unique())
)

df_f = df[df["filiere"] == filiere]

niveau = st.selectbox(
    "🎓 Choisir le niveau",
    sorted(df_f["niveau"].dropna().unique())
)

df_n = df_f[df_f["niveau"] == niveau]

if df_n.empty:
    st.warning("⚠️ Aucun étudiant trouvé.")
    st.stop()

df_n = df_n.copy()
df_n["nom"] = df_n["nom"].fillna("Inconnu")
df_n = df_n.sort_values("nom")

nom = st.selectbox("👤 Choisir l'étudiant", df_n["nom"].unique())

student = df_n[df_n["nom"] == nom].iloc[0]

# =========================
# PROFIL
# =========================
st.subheader("📊 Informations étudiant")

st.write("👤 Nom :", student["nom"])
st.write("🎓 Niveau :", student["niveau"])
st.write("📚 Filière :", student["filiere"])

# =========================
# CONFIRMATION
# =========================
st.subheader("⚠️ Confirmation")

confirm = st.checkbox("Je confirme vouloir supprimer cet étudiant")

if confirm:
    if st.button("🗑️ Supprimer définitivement"):

        try:
            # 🔥 fermer cache avant écriture
            st.cache_data.clear()

            # suppression
            df_new = df[df["nom"] != nom]

            # 🔥 écriture sécurisée
            temp_file = "temp_students.csv"
            df_new.to_csv(temp_file, index=False)

            # remplacer fichier original
            os.replace(temp_file, DATA_FILE)

            st.success("✅ Étudiant supprimé avec succès")

            time.sleep(1)
            st.rerun()

        except PermissionError:
            st.error("❌ Erreur : le fichier est ouvert ailleurs (Excel ?). Ferme-le puis réessaie.")

        except Exception as e:
            st.error(f"❌ Erreur inattendue : {e}")

# =========================
# FOOTER
# =========================
st.divider()
st.info("🧠 Suppression sécurisée avec gestion d'erreur avancée")