import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components

st.set_page_config(page_title="Analyse par Niveau", layout="wide")


components.html("""
<div style="
    background: linear-gradient(135deg, #EFF6FF, #DBEAFE);
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #BFDBFE;
    text-align: center;
    margin-bottom: 12px;
    box-shadow: 0 8px 20px rgba(59,130,246,0.12);
    font-family: Arial, sans-serif;
">

    <!-- HEADER FLEX -->
    <div style="
        display:flex;
        align-items:center;
        justify-content:center;
        gap:12px;
    ">

        <!-- 🎓 + 📊 ICON (Academic level progression) -->
        <svg width="42" height="42" viewBox="0 0 24 24"
             fill="none"
             stroke="#0F172A"
             stroke-width="2.2"
             stroke-linecap="round"
             stroke-linejoin="round">

            <!-- graduation cap -->
            <path d="M3 9l9-4 9 4-9 4-9-4z"/>
            <path d="M7 12v4c0 1 2 3 5 3s5-2 5-3v-4"/>

            <!-- analytics bars -->
            <line x1="8" y1="20" x2="8" y2="16"/>
            <line x1="12" y1="20" x2="12" y2="14"/>
            <line x1="16" y1="20" x2="16" y2="10"/>

        </svg>

        <!-- TITLE -->
        <div style="
            font-size:25px;
            font-weight:800;
            color:#0F172A;
            letter-spacing:-0.4px;
        ">
            Analyse par Niveau Académique
        </div>

    </div>

    <!-- SUBTITLE -->
    <div style="
        font-size:13px;
        color:#1D4ED8;
        margin-top:6px;
    ">
        Étude des performances et évolutions selon les niveaux de formation
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
# FILTRE FILIÈRE
# =========================
st.subheader("📌 Sélection de la filière")

filiere_selected = st.selectbox(
    " Choisir une filière",
    df["filiere"].dropna().unique()
)

df_fil = df[df["filiere"] == filiere_selected]

# =========================
# CAS VIDE
# =========================
if df_fil.empty:
    st.warning(" Aucune donnée pour cette filière")
    st.stop()
st.divider()
# =========================
# KPI NIVEAU GLOBAL FILTRÉ
# =========================
st.subheader(f"🌍 Indicateurs - {filiere_selected}")

st.markdown("""
<style>

/* ===== KPI ANIMATED CARDS ===== */
.kpi-card {
    background: linear-gradient(135deg, #FFFFFF, #F8FAFC);
    border: 1px solid #E2E8F0;
    border-radius: 16px;
    padding: 10px 8px;
    text-align: center;
    box-shadow: 0 6px 18px rgba(15, 23, 42, 0.06);
    transition: all 0.3s ease;
}

/* hover glow + movement */
.kpi-card:hover {
    transform: translateY(-6px) scale(1.03);
    border: 1px solid #22D3EE;
    box-shadow:
        0 0 12px rgba(34, 211, 238, 0.6),
        0 12px 30px rgba(34, 211, 238, 0.25);
}

/* icon */
.kpi-icon {
    font-size: 12px;
    margin-bottom: 6px;
}

/* value */
.kpi-value {
    font-size: 16px;
    font-weight: 800;
    color: #0F172A;
}

/* label */
.kpi-label {
    font-size: 12.5px;
    color: #64748B;
    margin-top: 4px;
}

</style>
""", unsafe_allow_html=True)


niveau_group = df_fil.groupby("niveau").mean(numeric_only=True).reset_index()

col1, col2, col3 = st.columns(3)

col1.markdown(f"""
<div class="kpi-card">
    <div class="kpi-icon">🎓</div>
    <div class="kpi-value">{round(niveau_group["moyenne"].max(), 2)}</div>
    <div class="kpi-label">Meilleure moyenne</div>
</div>
""", unsafe_allow_html=True)

col2.markdown(f"""
<div class="kpi-card">
    <div class="kpi-icon">😰</div>
    <div class="kpi-value">{round(df_fil["stress"].mean(), 2)}</div>
    <div class="kpi-label">Stress moyen</div>
</div>
""", unsafe_allow_html=True)

col3.markdown(f"""
<div class="kpi-card">
    <div class="kpi-icon">📚</div>
    <div class="kpi-value">{len(df_fil)}</div>
    <div class="kpi-label">Étudiants</div>
</div>
""", unsafe_allow_html=True)

# =========================
# ANALYSE PAR NIVEAU
# =========================
st.subheader("🧠 Analyse par niveau dans la filière")

fig1 = px.bar(
    niveau_group,
    x="niveau",
    y="moyenne",
    color="niveau",
    title=f"🎓 Moyenne par niveau - {filiere_selected}",
    color_discrete_sequence=px.colors.qualitative.Set3
)

st.plotly_chart(fig1, use_container_width=True)

fig2 = px.bar(
    niveau_group,
    x="niveau",
    y="stress",
    color="niveau",
    title=f"😰 Stress par niveau - {filiere_selected}",
    color_discrete_sequence=px.colors.qualitative.Pastel
)

st.plotly_chart(fig2, use_container_width=True)

fig3 = px.bar(
    niveau_group,
    x="niveau",
    y="heures_etude",
    color="niveau",
    title=f"📚 Heures d'étude par niveau - {filiere_selected}",
    color_discrete_sequence=px.colors.qualitative.Bold
)

st.plotly_chart(fig3, use_container_width=True)

# =========================
# RÉPARTITION NIVEAU (FILTRÉE)
# =========================


fig4 = px.pie(
    df_fil,
    names="niveau",
    title=f"👨‍🎓 Répartition des niveaux - {filiere_selected}",
    color_discrete_sequence=px.colors.qualitative.Set3
)

st.plotly_chart(fig4, use_container_width=True)
