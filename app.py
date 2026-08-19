import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# ==========================================
# 1. CONFIGURATION ET STYLE CSS 
# ==========================================
st.set_page_config(page_title="Comparateur & Auto Import 3D", layout="wide", page_icon="🚘")

st.markdown("""
    <style>
    .metric-card {
        background-color: #262730;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
        border-left: 5px solid #ff4b4b;
    }
    .metric-card b {
        color: #b0b0b0 !important;
        font-size: 0.95rem;
    }
    .metric-card h2 {
        color: #ffffff !important;
        margin-top: 5px;
        margin-bottom: 0px;
        font-weight: 600;
    }
    .customs-receipt {
        background-color: #1e1e1e;
        color: #00ff00;
        padding: 20px;
        border-radius: 5px;
        font-family: 'Courier New', Courier, monospace;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. CHARGEMENT DE LA BASE DE DONNÉES (CSV)
# ==========================================
@st.cache_data
def load_data():
    try:
        return pd.read_csv("base_voitures.csv")
    except Exception as e:
        st.error("⚠️ Fichier 'base_voitures.csv' introuvable ou mal formaté. Assure-toi qu'il est bien sur GitHub.")
        st.stop()

df = load_data()

# ==========================================
# 3. BARRE LATÉRALE (SIDEBAR) & FILTRES
# ==========================================
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3204/3204005.png", width=80)
st.sidebar.title("Configuration")
st.sidebar.markdown("---")

# Filtres interactifs
categorie_filtre = st.sidebar.multiselect(
    "1. Catégorie de véhicule :", 
    options=df["Categorie"].unique(), 
    default=df["Categorie"].unique()
)
df_filtre = df[df["Categorie"].isin(categorie_filtre)]

vehicule_choisi = st.sidebar.selectbox(
    "2. Sélectionnez le modèle :", 
    options=df_filtre["Marque_Modele"].tolist()
)

# Extraction des données du véhicule sélectionné
voiture_data = df_filtre[df_filtre["Marque_Modele"] == vehicule_choisi].iloc[0]

# ==========================================
# 4. EN-TÊTE PRINCIPAL
# ==========================================
st.title(f"🚘 {voiture_data['Marque_Modele']}")
st.markdown("Plateforme d'inspection 3D et d'estimation d'importation douanière.")

# Affichage des métriques clés en haut de page
col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    st.markdown(f"<div class='metric-card'><b>Prix d'achat (FOB)</b><h2>${voiture_data['Prix_USD']:,.0f}</h2></div>", unsafe_allow_html=True)
with col_m2:
    st.markdown(f"<div class='metric-card'><b>Catégorie</b><h2>{voiture_data['Categorie']}</h2></div>", unsafe_allow_html=True)
with col_m3:
    st.markdown(f"<div class='metric-card'><b>Vendeur Officiel</b><h2>{voiture_data['Vendeur_Officiel']}</h2></div>", unsafe_allow_html=True)

st.write("") # Espace

# Création de deux onglets pour structurer l'application
tab1, tab2 = st.tabs(["🏎️ Vue 360° & Fiche Technique", "🛃 Simulateur Douane (SYDONIA / GUCE)"])

# ==========================================
# ONGLET 1 : VISUALISATION 3D ET SPECS
# ==========================================
with tab1:
    col_3d, col_specs = st.columns([3, 2])
    
    # Colonne de gauche : Le modèle 3D
    with col_3d:
        st.subheader("Inspection 3D Interactive")
        model_url = voiture_data['Modele_3D_URL']
        
        # Ajout d'attributs avancés (environment-image) pour des reflets réalistes sur la carrosserie
        model_viewer_html = f"""
            <script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.1.1/model-viewer.min.js"></script>
            <model-viewer 
                src="{model_url}" 
                environment-image="neutral"
                auto-rotate 
                auto-rotate-delay="1000"
                camera-controls 
                interaction-prompt="auto"
                style="width: 100%; height: 500px; background-color: #e0e5ec; border-radius: 12px; box-shadow: inset 0px 0px 10px rgba(0,0,0,0.1);">
            </model-viewer>
        """
        components.html(model_viewer_html, height=520)
        st.caption("Faites glisser pour tourner. Utilisez la molette pour zoomer.")

    # Colonne de droite : Avantages / Inconvénients et Affiliation
    with col_specs:
        st.subheader("Analyse du véhicule")
        
        with st.expander("✅ Points Forts (Déplier)", expanded=True):
            for av in str(voiture_data['Avantages']).split(','): 
                st.write(f"✔️ {av.strip()}")
                
        with st.expander("❌ Points Faibles (Déplier)", expanded=True):
            for inc in str(voiture_data['Inconvenients']).split(','): 
                st.write(f"⚠️ {inc.strip()}")
                
        st.markdown("---")
        st.write("Intéressé par ce modèle en concession ?")
        st.link_button(f"🌐 Visiter {voiture_data['Vendeur_Officiel']}", voiture_data['Lien_Vendeur'], use_container_width=True)

# ==========================================
# ONGLET 2 : CALCULATEUR SYDONIA / GUCE
# ==========================================
with tab2:
    st.subheader("Calculateur d'Importation Détaillé")
    st.markdown("Simulez les frais réels selon les barèmes douaniers.")
    
    col_param, col_result = st.columns([1, 1.5])
    
    with col_param:
        st.write("**1. Paramètres de l'importation**")
        taux_change = st.number_input("Taux de change (1 USD en XOF)", value=605.0, step=5.0)
        fret_maritime_usd = st.slider("Frais de transport maritime (Fret) en $", 500, 3000, 1200)
        annee_vehicule = st.selectbox("Année de mise en circulation", list(range(2024, 2004, -1)))
        
        # Base de calcul
        prix_fob_xof = voiture_data['Prix_USD'] * taux_change
        fret_xof = fret_maritime_usd * taux_change
        assurance_xof = prix_fob_xof * 0.01 # L'assurance douanière est souvent estimée à 1% du FOB
        
        valeur_caf = prix_fob_xof + fret_xof + assurance_xof

    with col_result:
        st.write("**2. Décomposition des Taxes (Bordereau)**")
        
        # Logique douanière (Valeurs d'exemple très proches de la réalité)
        droits_douane = valeur_caf * 0.20        # 20% DD
        redevance_stat = valeur_caf * 0.01       # 1% RS
        prelevement_com = valeur_caf * 0.008     # 0.8% PCS/PC
        
        base_tva = valeur_caf + droits_douane + redevance_stat + prelevement_com
        tva = base_tva * 0.18                    # 18% TVA
        
        frais_guce = 35000                       # Frais de dossier fixes
        
        # Vétusté ou taxe environnementale
        taxe_age = 0
        if annee_vehicule < 2014:
            taxe_age = 150000
            
        total_taxes = droits_douane + redevance_stat + prelevement_com + tva + frais_guce + taxe_age
        cout_total_final = prix_fob_xof + fret_xof + total_taxes

        # Affichage style "Terminal / Reçu de douane"
        st.markdown(f"""
        <div class="customs-receipt">
            > VALEUR FOB (Véhicule) : {prix_fob_xof:,.0f} FCFA<br>
            > FRET MARITIME         : {fret_xof:,.0f} FCFA<br>
            > ASSURANCE (1%)        : {assurance_xof:,.0f} FCFA<br>
            ------------------------------------------<br>
            <b>= VALEUR C.A.F.           : {valeur_caf:,.0f} FCFA</b><br>
            <br>
            > Droits de Douane (20%) : {droits_douane:,.0f} FCFA<br>
            > RS & PCS (1.8%)        : {(redevance_stat+prelevement_com):,.0f} FCFA<br>
            > T.V.A. (18%)           : {tva:,.0f} FCFA<br>
            > Frais GUCE             : {frais_guce:,.0f} FCFA<br>
            > Pénalité d'âge         : {taxe_age:,.0f} FCFA<br>
            ------------------------------------------<br>
            <b>= TOTAL TAXES A PAYER     : {total_taxes:,.0f} FCFA</b>
        </div>
        """, unsafe_allow_html=True)
        
        st.info(f"**💡 BUDGET TOTAL PRÉVU (Véhicule + Transport + Douane) : {cout_total_final:,.0f} FCFA**")