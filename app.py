 import streamlit as st
 import pandas as pd
 import streamlit.components.v1 as components

# ==========================================
# 1. CONFIGURATION DE LA PAGE
# ==========================================
st.set_page_config(
    page_title="Comparateur & Auto Import 3D",
    page_icon="🚘",
    layout="wide"
)

# ==========================================
# 2. BASE DE DONNÉES SIMULÉE (Pandas)
# ==========================================
# Dans le futur, tu pourras remplacer ceci par : df = pd.read_csv('voitures.csv')
data = {
    "Marque_Modele": [
        "Toyota Prado TXL", "Range Rover Sport", "Mercedes Classe G", 
        "Hyundai Tucson", "Lexus RX 350", "Porsche Cayenne"
    ],
    "Categorie": ["4x4", "Luxe", "Luxe", "SUV", "SUV", "Luxe"],
    "Prix_USD": [45000, 85000, 130000, 28000, 50000, 75000],
    "Avantages": [
        "Fiabilité extrême, Pièces disponibles partout",
        "Confort premium, Finitions luxueuses, Statut",
        "Design iconique, Capacités tout-terrain, Prestige",
        "Excellent rapport qualité/prix, Faible consommation",
        "Fiabilité japonaise, Confort silencieux, Revente facile",
        "Performances sportives, Tenue de route, Matériaux"
    ],
    "Inconvenients": [
        "Consommation élevée, Design vieillissant",
        "Coût d'entretien très cher, Décote rapide",
        "Prix d'achat exorbitant, Consommation énorme",
        "Moteur un peu faible chargé, Espace coffre moyen",
        "Design infodivertissement daté, Prix d'assurance",
        "Coût des options, Entretien hors de prix"
    ],
    "Vendeur_Officiel": [
        "CFAO Motors", "Tractafric Motors", "Silver Star Auto", 
        "CFAO Motors", "CFAO Motors", "Porsche Center"
    ],
    "Lien_Vendeur": [
        "https://www.cfaogroup.com", "https://www.tractafricmotors.com", 
        "https://www.mercedes-benz.com", "https://www.cfaogroup.com", 
        "https://www.lexus.com", "https://www.porsche.com"
    ],
    # URLs de modèles 3D (.glb). Ce sont des exemples, tu devras mettre tes propres liens
    "Modele_3D_URL": [
        "https://modelviewer.dev/shared-assets/models/Astronaut.glb", # Remplace par une URL de Prado 3D
        "https://modelviewer.dev/shared-assets/models/glTF-Sample-Models/2.0/DamagedHelmet/glTF-Binary/DamagedHelmet.glb", # Remplace par Range Rover
        "https://modelviewer.dev/shared-assets/models/RobotExpressive.glb", # Remplace par Classe G
        "https://modelviewer.dev/shared-assets/models/Astronaut.glb",
        "https://modelviewer.dev/shared-assets/models/Astronaut.glb",
        "https://modelviewer.dev/shared-assets/models/Astronaut.glb"
    ]
}

df = pd.DataFrame(data)

# ==========================================
# 3. EN-TÊTE ET FILTRES (UI)
# ==========================================
st.title("🚘 Plateforme Importation & Comparateur 3D")
st.markdown("Explorez les véhicules sous tous les angles, analysez les fiches techniques et calculez vos frais d'importation via SYDONIA World / GUCE.")
st.markdown("---")

st.sidebar.header("🔍 Filtres de recherche")
categorie_filtre = st.sidebar.multiselect(
    "Filtrer par catégorie :", 
    options=df["Categorie"].unique(), 
    default=df["Categorie"].unique()
)

# Filtrer la base de données selon les choix
df_filtre = df[df["Categorie"].isin(categorie_filtre)]

vehicule_choisi = st.sidebar.selectbox(
    "Sélectionnez le véhicule à inspecter :", 
    options=df_filtre["Marque_Modele"].tolist()
)

# Récupérer les infos du véhicule sélectionné
voiture_data = df_filtre[df_filtre["Marque_Modele"] == vehicule_choisi].iloc[0]

# ==========================================
# 4. VISUALISATION 3D (Style Need For Speed)
# ==========================================
st.header(f"Vue 360° : {voiture_data['Marque_Modele']} ({voiture_data['Categorie']})")

# Code HTML/JS pour intégrer Google Model-Viewer
# Cela permet de tourner, zoomer et interagir avec la voiture
model_viewer_html = f"""
    <script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.1.1/model-viewer.min.js"></script>
    <style>
        model-viewer {{
            width: 100%;
            height: 500px;
            background-color: #f4f4f4;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}
    </style>
    <model-viewer 
        src="{voiture_data['Modele_3D_URL']}" 
        alt="Modèle 3D de {voiture_data['Marque_Modele']}" 
        auto-rotate 
        camera-controls 
        shadow-intensity="1"
        exposure="1.2">
    </model-viewer>
"""
# Injection du code HTML dans Streamlit
components.html(model_viewer_html, height=520)
st.caption("🖱️ *Astuce : Utilisez votre souris ou votre doigt pour faire tourner le véhicule et zoomer sur les détails.*")

# ==========================================
# 5. FICHE DÉTAILLÉE : AVANTAGES / INCONVÉNIENTS
# ==========================================
st.markdown("---")
st.header("📋 Fiche Technique & Analyse")

col_avantages, col_inconvenients = st.columns(2)

with col_avantages:
    st.success("### ✅ Points Forts")
    # Séparer les avantages par des virgules pour créer une liste à puces
    avantages_liste = voiture_data['Avantages'].split(',')
    for av in avantages_liste:
        st.write(f"- {av.strip()}")

with col_inconvenients:
    st.warning("### ❌ Points Faibles")
    # Séparer les inconvénients
    inconvenients_liste = voiture_data['Inconvenients'].split(',')
    for inc in inconvenients_liste:
        st.write(f"- {inc.strip()}")

# ==========================================
# 6. CALCULATEUR D'IMPORTATION (GUCE & SYDONIA)
# ==========================================
st.markdown("---")
st.header("🛃 Estimateur de Frais de Douane & Importation")

col_calc1, col_calc2 = st.columns([1, 2])

with col_calc1:
    st.subheader("Paramètres financiers")
    taux_usd_xof = st.number_input("Taux de change (USD vers XOF)", value=605.0, step=5.0)
    annee_fab = st.slider("Année de fabrication (Impacte la vétusté)", 2010, 2024, 2020)
    
    prix_vehicule_xof = voiture_data['Prix_USD'] * taux_usd_xof
    st.metric(label="Prix d'achat estimé (Hors Taxes)", value=f"{prix_vehicule_xof:,.0f} XOF")

with col_calc2:
    st.subheader("Détails des taxes (Estimation)")
    
    # Logique d'estimation des douanes
    fret_maritime = 800000  # Estimation forfaitaire du transport
    valeur_en_douane = prix_vehicule_xof + fret_maritime
    
    # Calcul des taux standards (Exemple simplifié)
    droits_douane = valeur_en_douane * 0.20  # 20% DD
    tva = (valeur_en_douane + droits_douane) * 0.18  # 18% TVA
    frais_guce = 30000  # Frais de guichet unique
    taxe_vetuste = 0
    
    if annee_fab < 2015:
        taxe_vetuste = 250000  # Pénalité vieux véhicules
        st.error(f"⚠️ Pénalité de vétusté appliquée : {taxe_vetuste:,.0f} XOF")
        
    total_taxes = droits_douane + tva + frais_guce + taxe_vetuste
    prix_final_cle_en_main = prix_vehicule_xof + total_taxes + fret_maritime
    
    # Affichage du bordereau
    st.text(f"Valeur FOB (Véhicule)      : {prix_vehicule_xof:,.0f} XOF")
    st.text(f"Fret Maritime estimé       : {fret_maritime:,.0f} XOF")
    st.text(f"Valeur en Douane (CAF)     : {valeur_en_douane:,.0f} XOF")
    st.markdown("---")
    st.text(f"+ Droits de Douane (20%)   : {droits_douane:,.0f} XOF")
    st.text(f"+ TVA (18%)                : {tva:,.0f} XOF")
    st.text(f"+ Frais GUCE               : {frais_guce:,.0f} XOF")
    st.markdown("---")
    st.success(f"💰 PRIX FINAL CLÉ EN MAIN : {prix_final_cle_en_main:,.0f} XOF")

# ==========================================
# 7. RÉSEAU OFFICIEL / AFFILIATION
# ==========================================
st.markdown("---")
st.header("🤝 Acheter via un Réseau Officiel")
st.info(f"Ce véhicule est distribué officiellement par **{voiture_data['Vendeur_Officiel']}**.")
st.link_button(f"🌐 Visiter le site de {voiture_data['Vendeur_Officiel']} pour un devis officiel", voiture_data['Lien_Vendeur'])

st.markdown("""
<div style="text-align: center; margin-top: 50px; color: gray;">
    <small>Application développée avec Python, Streamlit et la technologie Model-Viewer.</small>
</div>
""", unsafe_allow_html=True)