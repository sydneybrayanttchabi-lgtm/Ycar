import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# ==========================================
# 1. CONFIGURATION
# ==========================================
st.set_page_config(page_title="Comparateur Auto 3D", layout="wide")

# ==========================================
# 2. CHARGEMENT DE LA BASE DE DONNÉES
# ==========================================
@st.cache_data  # Optimisation pour charger le fichier une seule fois
def load_data():
    # Streamlit lira ton fichier base_voitures.csv depuis GitHub
    return pd.read_csv("base_voitures.csv")

try:
    df = load_data()
except Exception as e:
    st.error(f"Erreur lors du chargement du fichier CSV : {e}")
    st.stop()

# ==========================================
# 3. INTERFACE UTILISATEUR
# ==========================================
st.title("🚘 Comparateur Auto & Importation")
st.sidebar.header("🔍 Filtres")

categorie_filtre = st.sidebar.multiselect("Catégorie :", options=df["Categorie"].unique(), default=df["Categorie"].unique())
df_filtre = df[df["Categorie"].isin(categorie_filtre)]

vehicule_choisi = st.sidebar.selectbox("Sélectionnez le véhicule :", options=df_filtre["Marque_Modele"].tolist())
voiture_data = df_filtre[df_filtre["Marque_Modele"] == vehicule_choisi].iloc[0]

# ==========================================
# 4. VISUALISATION 3D
# ==========================================
st.header(f"Vue 360° : {voiture_data['Marque_Modele']}")
model_url = voiture_data['Modele_3D_URL']

model_viewer_html = f"""
    <script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.1.1/model-viewer.min.js"></script>
    <model-viewer src="{model_url}" auto-rotate camera-controls style="width:100%; height:500px; background:#f4f4f4; border-radius:10px;"></model-viewer>
"""
components.html(model_viewer_html, height=520)

# ==========================================
# 5. FICHE DÉTAILLÉE
# ==========================================
col1, col2 = st.columns(2)
with col1:
    st.success("### ✅ Points Forts")
    for av in str(voiture_data['Avantages']).split(','): st.write(f"- {av.strip()}")
with col2:
    st.warning("### ❌ Points Faibles")
    for inc in str(voiture_data['Inconvenients']).split(','): st.write(f"- {inc.strip()}")

# ==========================================
# 6. CALCULATEUR DOUANE
# ==========================================
st.markdown("---")
st.header("🛃 Estimateur de Frais de Douane")
prix_xof = voiture_data['Prix_USD'] * 605
st.write(f"**Prix véhicule :** {prix_xof:,.0f} XOF")
st.success(f"**Total Taxes estimées (DD + TVA + GUCE) :** {(prix_xof * 0.45):,.0f} XOF (Estimation 45%)")

# ==========================================
# 7. LIEN VENDEUR
# ==========================================
st.link_button(f"🌐 Visiter le site de {voiture_data['Vendeur_Officiel']}", voiture_data['Lien_Vendeur'])