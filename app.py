import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# ==========================================
# 1. CONFIGURATION ET STYLE CSS (MODE SOMBRE)
# ==========================================
st.set_page_config(page_title="Comparateur & Auto Import 3D", layout="wide", page_icon="🚘")

st.markdown("""
    <style>
    /* Cartes de métriques en haut de page */
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
    /* Style du reçu de douane */
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
        st.error("⚠️ Fichier 'base_voitures.csv' introuvable sur GitHub. Assure-toi qu'il est bien à la racine de ton dépôpt.")
        st.stop()

df = load_data()

# ==========================================
# 3. BARRE LATÉRALE (SIDEBAR) & FILTRES
# ==========================================
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3204/3204005.png", width=80)
st.sidebar.title("Configuration")
st.sidebar.markdown("---")

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

voiture_data = df_filtre[df_filtre["Marque_Modele"] == vehicule_choisi].iloc[0]

# ==========================================
# 4. EN-TÊTE ET MÉTRIQUES CLÉS
# ==========================================
st.title(f"🚘 {voiture_data['Marque_Modele']}")
st.markdown("Plateforme d'inspection 3D et d'estimation d'importation douanière.")

col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    st.markdown(f"<div class='metric-card'><b>Prix d'achat (FOB)</b><h2>${voiture_data['Prix_USD']:,.0f}</h2></div>", unsafe_allow_html=True)
with col_m2:
    st.markdown(f"<div class='metric-card'><b>Catégorie</b><h2>{voiture_data['Categorie']}</h2></div>", unsafe_allow_html=True)
with col_m3:
    st.markdown(f"<div class='metric-card'><b>Vendeur Officiel</b><h2>{voiture_data['Vendeur_Officiel']}</h2></div>", unsafe_allow_html=True)

st.write("") 

# ==========================================
# 5. ONGLETS DE NAVIGATION
# ==========================================
tab1, tab2 = st.tabs(["🏎️ Vue 360° & Fiche Technique", "🛃 Simulateur Douane (SYDONIA / GUCE)"])

# --- ONGLET 1 : INSPECTION 3D ---
with tab1:
    col_3d, col_specs = st.columns([3, 2])
    
    with col_3d:
        st.subheader("Inspection 3D Interactive")
        
        # Modèle 3D de secours automatique
        default_model = "https://modelviewer.dev/shared-assets/models/ToyCar.glb"
        
        raw_url = str(voiture_data['Modele_3D_URL']).strip()
        if raw_url == "" or raw_url.lower() == "nan":
            model_url = default_model
            st.caption("ℹ️ Affichage d'une voiture test 3D (ajoute un lien .glb dans ton CSV pour changer).")
        else:
            model_url = raw_url

        # Intégration 3D avec cadre sombre (#1a1a24)
        model_viewer_html = f"""
            <script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.4.0/model-viewer.min.js"></script>
            <model-viewer 
                src="{model_url}" 
                environment-image="neutral"
                auto-rotate 
                auto-rotate-delay="1000"
                camera-controls 
                interaction-prompt="auto"
                style="width: 100%; height: 500px; background-color: #1a1a24; border-radius: 12px; border: 1px solid #333333;">
            </model-viewer>
        """
        components.html(model_viewer_html, height=520)
        st.caption("Faites glisser pour tourner. Utilisez la molette pour zoomer.")

    with col_specs:
        st.subheader("Analyse du véhicule")
        
        with st.expander("✅ Points Forts", expanded=True):
            for av in str(voiture_data['Avantages']).split(','): 
                st.write(f"✔️ {av.strip()}")
                
        with st.expander("❌ Points Faibles", expanded=True):
            for inc in str(voiture_data['Inconvenients']).split(','): 
                st.write(f"⚠️ {inc.strip()}")
                
        st.markdown("---")
        st.write("Intéressé par ce modèle en concession ?")
        st.link_button(f"🌐 Visiter {voiture_data['Vendeur_Officiel']}", voiture_data['Lien_Vendeur'], use_container_width=True)

# --- ONGLET 2 : CALCULATEUR DOUANE ---
with tab2:
    st.subheader("Calculateur d'Importation Détaillé")
    
    col_param, col_result = st.columns([1, 1.5])
    
    with col_param:
        st.write("**1. Paramètres de l'importation**")
        taux_change = st.number_input("Taux de change (1 USD en XOF)", value=605.0, step=5.0)
        fret_maritime_usd = st.slider("Frais de transport maritime (Fret) en $", 500, 3000, 1200)
        annee_vehicule = st.selectbox("Année de mise en circulation", list(range(2026, 2005, -1)))
        
        prix_fob_xof = voiture_data['Prix_USD'] * taux_change
        fret_xof = fret_maritime_usd * taux_change
        assurance_xof = prix_fob_xof * 0.01
        valeur_caf = prix_fob_xof + fret_xof + assurance_xof

    with col_result:
        st.write("**2. Décomposition des Taxes**")
        droits_douane = valeur_caf * 0.20
        redevance_stat = valeur_caf * 0.01
        prelevement_com = valeur_caf * 0.008
        base_tva = valeur_caf + droits_douane + redevance_stat + prelevement_com
        tva = base_tva * 0.18
        frais_guce = 35000
        taxe_age = 150000 if annee_vehicule < 2016 else 0
        
        total_taxes = droits_douane + redevance_stat + prelevement_com + tva + frais_guce + taxe_age
        cout_total_final = prix_fob_xof + fret_xof + total_taxes

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
        
        st.info(f"**💡 BUDGET TOTAL PRÉVU : {cout_total_final:,.0f} FCFA**")