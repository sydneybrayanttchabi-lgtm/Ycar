import streamlit as st
import requests

# Configuration de la page
st.set_page_config(
    page_title="YKR.com",
    page_icon="🚗",
    layout="wide"
)

# --- 1. FONCTION DE CONVERSION EN TEMPS RÉEL (API GRATUITE) ---
@st.cache_data(ttl=3600)  # Cache de 1 heure pour garder le site fluide et rapide
def obtenir_taux_devises(devise_base="EUR"):
    """
    Interroge une API gratuite pour obtenir les taux de change actualisés.
    En cas de problème réseau, bascule automatiquement sur des taux par défaut.
    """
    try:
        url = f"https://open.er-api.com/v6/latest/{devise_base}"
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            data = res.json()
            if data.get("result") == "success":
                return data.get("rates", {}), True
    except Exception:
        pass
    
    # Taux de secours (hors-ligne)
    taux_secours = {
        "EUR": 1.0,
        "XOF": 655.957,  # Franc CFA BCEAO
        "USD": 1.09,
        "GBP": 0.85,
        "CAD": 1.48,
        "JPY": 165.0
    }
    return taux_secours, False

# Chargement des taux
taux_dict, api_succes = obtenir_taux_devises("EUR")

# --- TITRE & EN-TÊTE ---
st.title("Ycar")
st.write("Comparez des véhicules, simulez les frais de douane et convertissez les prix en temps réel.")

# Témoin d'état du réseau
if api_succes:
    st.caption("🟢 **Taux de change :** En direct du marché financier (Mis à jour)")
else:
    st.caption("🟠 **Taux de change :** Mode secours (Hors-ligne)")

# --- ONGLETS PRINCIPAUX ---
tab1, tab2 = st.tabs(["📊 Comparateur & Simulateur Import", "🔀 Convertisseur de Devises Universel"])

# --- BASE DE DONNÉES TEMPORAIRE ---
vehicules = {
    "Toyota RAV4 Hybride 2022": {
        "prix_export_eur": 25000,
        "moteur": "Hybride 2.5L",
        "avantages": "Fiabilité extrême, faible conso, revente facile.",
        "inconvenients": "Prix d'achat élevé, assurance plus chère.",
        "lien_affiliation": "https://vendeur-officiel.com/rav4",
        "image_url": "https://images.unsplash.com/photo-1621007947382-df31b1e4e6b6?auto=format&fit=crop&w=800"
    },
    "Hyundai Tucson 2021": {
        "prix_export_eur": 21000,
        "moteur": "Diesel 1.6 CRDi",
        "avantages": "Design moderne, beaucoup d'options, pièces accessibles.",
        "inconvenients": "Consommation urbaine, décote plus rapide.",
        "lien_affiliation": "https://vendeur-officiel.com/tucson",
        "image_url": "https://images.unsplash.com/photo-1633511090164-b4bf3ccaa01b?auto=format&fit=crop&w=800"
    }
}

# === ONGLET 1 : COMPARATEUR & SIMULATEUR ===
with tab1:
    modele_choisi = st.selectbox("Choisissez un véhicule à analyser :", list(vehicules.keys()))
    voiture = vehicules[modele_choisi]

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"Fiche Technique : {modele_choisi}")
        st.image(voiture['image_url'], use_container_width=True)
        st.write(f"**Motorisation :** {voiture['moteur']}")
        st.success(f"**Avantages :** {voiture['avantages']}")
        st.warning(f"**Inconvénients :** {voiture['inconvenients']}")
        
        # Conversion du prix d'origine en FCFA (XOF)
        prix_eur = voiture['prix_export_eur']
        taux_xof = taux_dict.get("XOF", 655.957)
        prix_xof = prix_eur * taux_xof
        
        st.info(f"**Prix Export :** {prix_eur:,.0f} € (~ **{prix_xof:,.0f} FCFA**)")
        st.link_button("Voir chez le vendeur certifié", voiture['lien_affiliation'])

    with col2:
        st.subheader("🚢 Simulateur de Frais de Douane")
        frais_fret = st.number_input("Frais de transport maritime (€)", min_value=500, max_value=3000, value=1200, step=100)
        taux_douane = st.slider("Taux de dédouanement estimé (%)", min_value=10, max_value=80, value=40)
        
        valeur_caf = voiture['prix_export_eur'] + frais_fret
        montant_douane = valeur_caf * (taux_douane / 100)
        prix_total_eur = valeur_caf + montant_douane
        prix_total_xof = prix_total_eur * taux_xof
        
        st.divider()
        st.metric(label="Valeur CAF (Prix + Fret)", value=f"{valeur_caf:,.0f} €")
        st.metric(label="Taxes douanières estimées", value=f"{montant_douane:,.0f} €")
        
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.metric(label="💰 Total Estimé (Euros)", value=f"{prix_total_eur:,.0f} €")
        with col_m2:
            st.metric(label="🌍 Total Estimé (Franc CFA)", value=f"{prix_total_xof:,.0f} FCFA")

# === ONGLET 2 : CONVERTISSEUR UNIVERSEL ===
with tab2:
    st.subheader("🔀 Convertisseur de Devises en Temps Réel")
    st.write("Convertissez n'importe quelle monnaie mondiale pour vos opérations d'importation.")
    
    col_a, col_b, col_c = st.columns(3)
    
    devises_disponibles = sorted(list(taux_dict.keys()))
    
    with col_a:
        montant_saisi = st.number_input("Montant à convertir :", min_value=1.0, value=1000.0, step=50.0)
    
    with col_b:
        idx_eur = devises_disponibles.index("EUR") if "EUR" in devises_disponibles else 0
        devise_depart = st.selectbox("Monnaie de départ :", devises_disponibles, index=idx_eur)
        
    with col_c:
        idx_xof = devises_disponibles.index("XOF") if "XOF" in devises_disponibles else 0
        devise_arrivee = st.selectbox("Monnaie de destination :", devises_disponibles, index=idx_xof)
    
    # Calcul dynamique de la conversion
    taux_dep = taux_dict.get(devise_depart, 1.0)
    taux_arr = taux_dict.get(devise_arrivee, 1.0)
    
    montant_en_eur = montant_saisi / taux_dep
    resultat = montant_en_eur * taux_arr
    taux_direct = taux_arr / taux_dep
    
    st.divider()
    st.success(f"### 💵 Résultat : {montant_saisi:,.2f} {devise_depart} = **{resultat:,.2f} {devise_arrivee}**")
    st.caption(f"Taux appliqué : 1 {devise_depart} = {taux_direct:,.4f} {devise_arrivee}")