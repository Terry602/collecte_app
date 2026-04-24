import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit.components.v1 as components

st.set_page_config(page_title="Analyse par Filière", layout="wide")

components.html("""
<div style="
    background: linear-gradient(135deg, #FFFBEB, #FEF3C7);
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #FDE68A;
    text-align: center;
    margin-bottom: 12px;
    box-shadow: 0 8px 20px rgba(245,158,11,0.10);
    font-family: Arial, sans-serif;
">

    <!-- HEADER FLEX -->
    <div style="
        display:flex;
        align-items:center;
        justify-content:center;
        gap:12px;
    ">

        <!-- 📚 + 📊 ICON (Filière / Academic track analysis) -->
        <svg width="42" height="42" viewBox="0 0 24 24"
             fill="none"
             stroke="#7C2D12"
             stroke-width="2.2"
             stroke-linecap="round"
             stroke-linejoin="round">

            <!-- book -->
            <path d="M4 19c0-2 2-3 5-3h11"/>
            <path d="M4 5c0-2 2-3 5-3h11v16"/>
            <path d="M9 2v14"/>

            <!-- analytics bars -->
            <line x1="14" y1="18" x2="14" y2="14"/>
            <line x1="16.5" y1="18" x2="16.5" y2="12"/>
            <line x1="19" y1="18" x2="19" y2="10"/>

        </svg>

        <!-- TITLE -->
        <div style="
            font-size:30px;
            font-weight:800;
            color:#7C2D12;
            letter-spacing:-0.4px;
        ">
            Analyse par Filière
        </div>

    </div>

    <!-- SUBTITLE -->
    <div style="
        font-size:13px;
        color:#92400E;
        margin-top:6px;
    ">
        Comparaison des performances, comportements et tendances par spécialisation
    </div>

</div>
""", height=150)

DATA_FILE = "data_students.csv"

# =========================
# CHARGEMENT DONNÉES
# =========================
@st.cache_data
def load_data():
    return pd.read_csv(DATA_FILE)


try:
    df = load_data()
except:
    st.error(" Aucune donnée disponible.")
    st.stop()
st.divider()

# =========================
# FILTRES
# =========================
filiere_selected = st.selectbox(
    "📌 Choisir une filière",
    df["filiere"].dropna().unique()
)

df_fil = df[df["filiere"] == filiere_selected]


# =========================
# KPI FILIERE + SEXE (SEMI CIRCLE)
# =========================
st.subheader(f"🌍 Indicateurs de la filiere - {filiere_selected}")

st.markdown("""
<style>

/* ===== ANIMATED KPI CARDS ===== */
.kpi-card {
    background: linear-gradient(135deg, #FFFFFF, #F8FAFC);
    border: 1px solid #E2E8F0;
    border-radius: 16px;
    padding: 18px 14px;
    text-align: center;
    box-shadow: 0 6px 18px rgba(15, 23, 42, 0.06);
    transition: all 0.3s ease;
}

/* hover effect + glow border */
.kpi-card:hover {
    transform: translateY(-6px) scale(1.03);
    border: 1px solid #60A5FA;
    box-shadow:
        0 0 10px rgba(96, 165, 250, 0.6),
        0 10px 25px rgba(96, 165, 250, 0.25);
}

/* title icon */
.kpi-icon {
    font-size: 20px;
    margin-bottom: 6px;
}

/* value */
.kpi-value {
    font-size: 24px;
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


col1, col2, col3, col4 = st.columns(4)

col1.markdown(f"""
<div class="kpi-card">
    <div class="kpi-icon">🎓</div>
    <div class="kpi-value">{round(df_fil["moyenne"].mean(), 2)}</div>
    <div class="kpi-label">Moyenne</div>
</div>
""", unsafe_allow_html=True)

col2.markdown(f"""
<div class="kpi-card">
    <div class="kpi-icon">😰</div>
    <div class="kpi-value">{round(df_fil["stress"].mean(), 2)}</div>
    <div class="kpi-label">Stress</div>
</div>
""", unsafe_allow_html=True)

col3.markdown(f"""
<div class="kpi-card">
    <div class="kpi-icon">📚</div>
    <div class="kpi-value">{round(df_fil["heures_etude"].mean(), 2)}</div>
    <div class="kpi-label">Heures étude</div>
</div>
""", unsafe_allow_html=True)

col4.markdown(f"""
<div class="kpi-card">
    <div class="kpi-icon">👨‍🎓</div>
    <div class="kpi-value">{len(df_fil)}</div>
    <div class="kpi-label">Total étudiants</div>
</div>
""", unsafe_allow_html=True)

st.divider()

# =========================
#  SEMI-CIRCLE SEXE
# =========================
st.subheader(f"🔬 Analyse de la filiere - {filiere_selected}")

st.subheader("")

sex_counts = df_fil["sexe"].value_counts().reset_index()
sex_counts.columns = ["sexe", "count"]

fig_sex = px.pie(
    sex_counts,
    names="sexe",
    values="count",
    hole=0.5,
    title=" Répartition du sexe",
    color_discrete_sequence=["#FF9F1C", "#2EC4B6"]
)

fig_sex.update_traces(textinfo="percent+label")

fig_sex.update_layout(
    showlegend=True,
    height=400,
    annotations=[dict(text="Sexe", x=0.5, y=0.5, showarrow=False)],
    margin=dict(t=40, b=0)
)

st.plotly_chart(fig_sex, use_container_width=True)



# =========================
# MATRICE DE CORRELATION
# =========================

numeric_df = df_fil.select_dtypes(include=["int64", "float64"])

fig_corr = px.imshow(
    numeric_df.corr(),
    text_auto=True,
    color_continuous_scale="RdBu",
    title=" Corrélation des variables"
)

st.plotly_chart(fig_corr, use_container_width=True)
st.divider()
# =========================
# NUAGES DE POINTS FUSIONNÉS
# =========================
st.subheader("📊 Relations clés avec la performance")

# transformer les données (format long)
df_long = df_fil.melt(
    id_vars=["moyenne"],
    value_vars=["heures_etude", "concentration", "motivation", "regularite"],
    var_name="Variable",
    value_name="Valeur"
)

# mapping noms propres
labels_map = {
    "heures_etude": "📚 Étude",
    "concentration": "🧠 Concentration",
    "motivation": "🔥 Motivation",
    "regularite": "📅 Régularité"
}
df_long["Variable"] = df_long["Variable"].map(labels_map)

# création du graphe
fig = px.scatter(
    df_long,
    x="Valeur",
    y="moyenne",
    facet_col="Variable",
    facet_col_wrap=2,
    trendline="ols",
    color="Variable",
    title="🎯 Impact des facteurs clés sur la performance académique"
)

# amélioration visuelle
fig.update_layout(
    showlegend=False,
    margin=dict(t=60, l=30, r=30, b=30)
)

st.plotly_chart(fig, use_container_width=True)

st.divider()
# =========================
# COMPARAISONS
# =========================
st.subheader("⚖️ Comparaison des filières")

moyenne_filiere = df.groupby("filiere")["moyenne"].mean().reset_index()

fig1 = px.bar(
    moyenne_filiere,
    x="filiere",
    y="moyenne",
    color="filiere",
    title=" Moyenne académique par filière",
    color_discrete_sequence=px.colors.qualitative.Set3
)

st.plotly_chart(fig1, use_container_width=True)



stress_filiere = df.groupby("filiere")["stress"].mean().reset_index()

fig2 = px.bar(
    stress_filiere,
    x="filiere",
    y="stress",
    color="filiere",
    title=" Stress moyen par filière",
    color_discrete_sequence=px.colors.qualitative.Pastel
)

st.plotly_chart(fig2, use_container_width=True)



study_filiere = df.groupby("filiere")["heures_etude"].mean().reset_index()

fig3 = px.bar(
    study_filiere,
    x="filiere",
    y="heures_etude",
    color="filiere",
    title=" Heures d'étude moyennes par filière",
    color_discrete_sequence=px.colors.qualitative.Bold
)

st.plotly_chart(fig3, use_container_width=True)
st.divider()

# =========================
# INSIGHTS
# =========================
st.subheader("🔁 Analyse intelligente")

# Moyenne
best_filiere = df.groupby("filiere")["moyenne"].mean().idxmax()
worst_filiere = df.groupby("filiere")["moyenne"].mean().idxmin()

# Stress
stress_high = df.groupby("filiere")["stress"].mean().idxmax()
stress_low = df.groupby("filiere")["stress"].mean().idxmin()

concentration_high = df.groupby("filiere")["concentration"].mean().idxmax()
motivation_high = df.groupby("filiere")["motivation"].mean().idxmax()
regularite_high = df.groupby("filiere")["regularite"].mean().idxmax()

age_high = None
credits_high = None

if "age" in df.columns:
    age_high = df.groupby("filiere")["age"].mean().idxmax()

if "credits" in df.columns:
    credits_high = df.groupby("filiere")["credits"].mean().idxmax()

# =========================
# AFFICHAGE
# =========================
st.success(f" Filière la plus performante : {best_filiere}")
st.error(f" Filière la moins performante : {worst_filiere}")

st.warning(f" Filière la plus stressée : {stress_high}")
st.info(f" Filière la moins stressée : {stress_low}")

st.success(f" Filière la plus concentrée : {concentration_high}")
st.success(f" Filière la plus motivée : {motivation_high}")
st.success(f" Filière la plus régulière : {regularite_high}")

if age_high:
    st.info(f" Filière avec étudiants les plus âgés : {age_high}")



niveau_group = df_fil.groupby("niveau").mean(numeric_only=True).reset_index()
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


if credits_high:
    st.info(f" Filière avec le plus de crédits validés : {credits_high}")
