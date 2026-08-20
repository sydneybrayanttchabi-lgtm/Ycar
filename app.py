import React, { useState, useEffect, useMemo, useRef } from 'react';
import Papa from 'papaparse';
import '@google/model-viewer';

// ============================================================================
// TYPES ET INTERFACES
// ============================================================================

interface CarData {
  Marque_Modele: string;
  Categorie: string;
  Prix_USD: number;
  Avantages: string;
  Inconvenients: string;
  Vendeur_Officiel: string;
  Lien_Vendeur: string;
  Modele_3D_URL: string;
}

interface CustomsCalculation {
  prixFOB_FCFA: number;
  fret_FCFA: number;
  assurance: number;
  valeurCAF: number;
  droitsDouane: number;
  redevanceStatistique: number;
  pcs: number;
  tva: number;
  fraisGUCE: number;
  penaliteAge: number;
  totalDouane: number;
  budgetTotal: number;
}

// ============================================================================
// CONSTANTES ET CONFIGURATION
// ============================================================================

const CATEGORIES = ['SUV', '4x4', 'Berline', 'Hybride/Électrique', 'Luxe'];
const DEFAULT_EXCHANGE_RATE = 605;
const DEFAULT_FREIGHT_USD = 1200;
const MIN_YEAR = 2006;
const MAX_YEAR = 2026;
const AGE_THRESHOLD = 2016;
const AGE_PENALTY = 150000;
const GUCE_FEE = 35000;

// Taux douaniers (Barème Afrique de l'Ouest / Bénin)
const CUSTOMS_RATES = {
  droitsDouane: 0.20,      // 20% de CAF
  redevanceStatistique: 0.01, // 1% de CAF
  pcs: 0.008,              // 0.8% de CAF
  tva: 0.18,               // 18% de (CAF + DD + RS + PCS)
  assurance: 0.01,         // 1% de FOB
};

const FALLBACK_3D_MODEL = 'https://modelviewer.dev/shared-assets/models/ToyCar.glb';

// ============================================================================
// COMPOSANTS UTILITAIRES
// ============================================================================

/**
 * Formattage des nombres en format monétaire FCFA
 */
const formatFCFA = (value: number): string => {
  return new Intl.NumberFormat('fr-FR').format(Math.round(value)) + ' FCFA';
};

/**
 * Formattage des nombres en format monétaire USD
 */
const formatUSD = (value: number): string => {
  return '$' + new Intl.NumberFormat('en-US').format(Math.round(value));
};

/**
 * Composant de carte métrica stylisée
 */
const MetricCard: React.FC<{
  label: string;
  value: string;
  accentColor?: string;
}> = ({ label, value, accentColor = '#ff4b4b' }) => (
  <div 
    className="p-4 rounded-lg border-l-4 backdrop-blur-sm"
    style={{ 
      backgroundColor: 'rgba(26, 26, 36, 0.8)',
      borderColor: accentColor,
      borderLeftWidth: '4px'
    }}
  >
    <p className="text-gray-400 text-xs uppercase tracking-wider mb-1">{label}</p>
    <p className="text-white font-bold text-lg">{value}</p>
  </div>
);

/**
 * Composant de reçu douanier style terminal
 */
const CustomsReceipt: React.FC<{ calculation: CustomsCalculation }> = ({ calculation }) => {
  const receiptItems = [
    { label: 'Prix FOB (FCFA)', value: calculation.prixFOB_FCFA },
    { label: 'Fret Maritime (FCFA)', value: calculation.fret_FCFA },
    { label: 'Assurance (1%)', value: calculation.assurance },
    { label: '─'.repeat(40), value: null, isSeparator: true },
    { label: 'VALEUR C.A.F.', value: calculation.valeurCAF, isBold: true },
    { label: '─'.repeat(40), value: null, isSeparator: true },
    { label: 'Droits de Douane (20%)', value: calculation.droitsDouane },
    { label: 'Redevance Statistique (1%)', value: calculation.redevanceStatistique },
    { label: 'Prélèvement Communautaire (0.8%)', value: calculation.pcs },
    { label: 'TVA (18%)', value: calculation.tva },
    { label: 'Frais GUCE', value: calculation.fraisGUCE },
    { label: `Pénalité d'âge (${AGE_THRESHOLD})`, value: calculation.penaliteAge },
    { label: '─'.repeat(40), value: null, isSeparator: true },
    { label: 'TOTAL DOUANE', value: calculation.totalDouane, isBold: true, isHighlight: true },
  ];

  return (
    <div 
      className="p-6 rounded-lg font-mono text-sm"
      style={{ 
        backgroundColor: '#000000',
        border: '1px solid #00ff00',
        boxShadow: '0 0 20px rgba(0, 255, 0, 0.3)'
      }}
    >
      <div className="text-center mb-4 pb-2 border-b border-green-900">
        <p className="text-green-500 text-xs">RÉPUBLIQUE DU BÉNIN</p>
        <p className="text-green-400 text-sm font-bold">DOUANE - SYDONIA / GUCE</p>
        <p className="text-green-600 text-xs">SIMULATEUR DE CALCUL</p>
      </div>
      
      <div className="space-y-1">
        {receiptItems.map((item, index) => (
          <div 
            key={index} 
            className={`flex justify-between ${item.isSeparator ? 'text-green-700' : 'text-green-400'}`}
            style={item.isBold ? { fontWeight: 'bold' } : {}}
          >
            <span className={item.isHighlight ? 'text-green-300' : ''}>{item.label}</span>
            {item.value !== null && (
              <span className={item.isHighlight ? 'text-green-300 font-bold' : ''}>
                {formatFCFA(item.value)}
              </span>
            )}
          </div>
        ))}
      </div>

      <div className="mt-4 pt-4 border-t-2 border-green-500">
        <div className="flex justify-between items-center">
          <span className="text-green-300 font-bold text-base">BUDGET TOTAL GLOBAL</span>
          <span className="text-green-300 font-bold text-xl">{formatFCFA(calculation.budgetTotal)}</span>
        </div>
        <p className="text-green-700 text-xs mt-2 text-center">
          *Estimation non contractuelle - Sous réserve de vérification
        </p>
      </div>
    </div>
  );
};

/**
 * Composant ModelViewer encapsulant l'élément custom
 */
const ModelViewerComponent: React.FC<{
  src: string;
  alt: string;
  className?: string;
  style?: React.CSSProperties;
}> = ({ src, alt, className, style }) => {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (containerRef.current) {
      containerRef.current.innerHTML = `
        <model-viewer
          src="${src}"
          alt="${alt}"
          auto-rotate
          camera-controls
          zoom-progress
          shadow-intensity="1"
          environment-image="neutral"
          exposure="1"
          interaction-prompt="none"
          class="${className || ''}"
          style="--poster-color: #1a1a24; width: 100%; height: 100%;"
        ></model-viewer>
      `;
    }
  }, [src, alt, className]);

  return <div ref={containerRef} className="w-full h-full" style={style} />;
};

// ============================================================================
// COMPOSANT PRINCIPAL
// ============================================================================

export default function App() {
  // États pour les données
  const [carData, setCarData] = useState<CarData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // États pour les filtres
  const [selectedCategories, setSelectedCategories] = useState<string[]>([]);
  const [selectedCar, setSelectedCar] = useState<CarData | null>(null);

  // États pour le simulateur douanier
  const [exchangeRate, setExchangeRate] = useState(DEFAULT_EXCHANGE_RATE);
  const [freightUSD, setFreightUSD] = useState(DEFAULT_FREIGHT_USD);
  const [vehicleYear, setVehicleYear] = useState(2020);

  // État pour l'onglet actif
  const [activeTab, setActiveTab] = useState<'3d' | 'customs'>('3d');

  // ============================================================================
  // CHARGEMENT DES DONNÉES CSV
  // ============================================================================

  useEffect(() => {
    const loadCSVData = async () => {
      try {
        setLoading(true);
        setError(null);

        const response = await fetch('/data/b.v.O.csv');
        if (!response.ok) {
          throw new Error('Impossible de charger le fichier CSV');
        }

        const csvText = await response.text();

        const parseResults = Papa.parse<CarData>(csvText, {
          header: true,
          skipEmptyLines: true,
        });

        if (parseResults.errors.length > 0) {
          throw new Error(`Erreur de parsing CSV: ${parseResults.errors[0].message}`);
        }

        const parsedData = parseResults.data
          .filter((row) => {
            const marqueModele = row.Marque_Modele as string | undefined;
            return marqueModele && marqueModele.trim() !== '';
          })
          .map(row => ({
            Marque_Modele: (row.Marque_Modele as string) || '',
            Categorie: (row.Categorie as string) || '',
            Prix_USD: parseFloat(row.Prix_USD as unknown as string) || 0,
            Avantages: (row.Avantages as string) || '',
            Inconvenients: (row.Inconvenients as string) || '',
            Vendeur_Officiel: (row.Vendeur_Officiel as string) || '',
            Lien_Vendeur: (row.Lien_Vendeur as string) || '',
            Modele_3D_URL: (row.Modele_3D_URL as string) || '',
          }));
        setCarData(parsedData);
        if (parsedData.length > 0) {
          setSelectedCar(parsedData[0]);
        }
        setLoading(false);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Erreur inconnue lors du chargement');
        setLoading(false);
      }
    };

    loadCSVData();
  }, []);

  // ============================================================================
  // FILTRAGE DES VÉHICULES
  // ============================================================================

  const filteredCars = useMemo(() => {
    if (selectedCategories.length === 0) {
      return carData;
    }
    return carData.filter(car => selectedCategories.includes(car.Categorie));
  }, [carData, selectedCategories]);

  // Mettre à jour la voiture sélectionnée si elle n'est plus dans les filtres
  useEffect(() => {
    if (selectedCar && !filteredCars.find(c => c.Marque_Modele === selectedCar.Marque_Modele)) {
      setSelectedCar(filteredCars[0] || null);
    }
  }, [filteredCars, selectedCar]);

  // ============================================================================
  // CALCUL DOUANIER
  // ============================================================================

  const customsCalculation = useMemo<CustomsCalculation | null>(() => {
    if (!selectedCar) return null;

    const prixFOB_FCFA = selectedCar.Prix_USD * exchangeRate;
    const fret_FCFA = freightUSD * exchangeRate;
    const assurance = prixFOB_FCFA * CUSTOMS_RATES.assurance;
    const valeurCAF = prixFOB_FCFA + fret_FCFA + assurance;

    const droitsDouane = valeurCAF * CUSTOMS_RATES.droitsDouane;
    const redevanceStatistique = valeurCAF * CUSTOMS_RATES.redevanceStatistique;
    const pcs = valeurCAF * CUSTOMS_RATES.pcs;
    const tva = (valeurCAF + droitsDouane + redevanceStatistique + pcs) * CUSTOMS_RATES.tva;
    const fraisGUCE = GUCE_FEE;
    const penaliteAge = vehicleYear < AGE_THRESHOLD ? AGE_PENALTY : 0;

    const totalDouane = droitsDouane + redevanceStatistique + pcs + tva + fraisGUCE + penaliteAge;
    const budgetTotal = prixFOB_FCFA + fret_FCFA + assurance + totalDouane;

    return {
      prixFOB_FCFA,
      fret_FCFA,
      assurance,
      valeurCAF,
      droitsDouane,
      redevanceStatistique,
      pcs,
      tva,
      fraisGUCE,
      penaliteAge,
      totalDouane,
      budgetTotal,
    };
  }, [selectedCar, exchangeRate, freightUSD, vehicleYear]);

  // ============================================================================
  // GESTIONNAIRES D'ÉVÉNEMENTS
  // ============================================================================

  const toggleCategory = (category: string) => {
    setSelectedCategories(prev =>
      prev.includes(category)
        ? prev.filter(c => c !== category)
        : [...prev, category]
    );
  };

  const get3DModelUrl = (car: CarData): string => {
    if (!car.Modele_3D_URL || car.Modele_3D_URL.trim() === '' || car.Modele_3D_URL === 'NaN') {
      return FALLBACK_3D_MODEL;
    }
    return car.Modele_3D_URL;
  };

  // ============================================================================
  // RENDU
  // ============================================================================

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center" style={{ backgroundColor: '#0e1117' }}>
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-red-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-400">Chargement des données...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center" style={{ backgroundColor: '#0e1117' }}>
        <div className="text-center p-8 rounded-lg" style={{ backgroundColor: '#1a1a24' }}>
          <p className="text-red-500 text-xl mb-4">⚠️ Erreur</p>
          <p className="text-gray-400">{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen" style={{ backgroundColor: '#0e1117' }}>
      {/* En-tête */}
      <header 
        className="p-6 border-b"
        style={{ 
          backgroundColor: '#1a1a24',
          borderColor: '#ff4b4b'
        }}
      >
        <div className="max-w-7xl mx-auto">
          <h1 className="text-3xl font-bold text-white mb-2">
            🚗 Comparateur Auto & Simulateur de Douane
          </h1>
          <p className="text-gray-400 text-sm">
            Plateforme intelligente d'importation de véhicules - Barème Bénin / Afrique de l'Ouest
          </p>
        </div>
      </header>

      <div className="flex">
        {/* Barre latérale - Filtres */}
        <aside 
          className="w-72 p-6 border-r flex-shrink-0"
          style={{ 
            backgroundColor: '#1a1a24',
            borderColor: '#2a2a3a'
          }}
        >
          <h2 className="text-white font-semibold mb-4 flex items-center">
            <span className="mr-2">🔍</span> Filtres
          </h2>

          {/* Filtres par catégorie */}
          <div className="mb-6">
            <p className="text-gray-400 text-xs uppercase tracking-wider mb-3">Catégories</p>
            <div className="space-y-2">
              {CATEGORIES.map(category => (
                <label 
                  key={category}
                  className="flex items-center cursor-pointer group"
                >
                  <input
                    type="checkbox"
                    checked={selectedCategories.includes(category)}
                    onChange={() => toggleCategory(category)}
                    className="w-4 h-4 rounded border-gray-600 text-red-500 focus:ring-red-500 focus:ring-offset-gray-900"
                  />
                  <span className="ml-3 text-gray-300 group-hover:text-white transition-colors">
                    {category}
                  </span>
                </label>
              ))}
            </div>
          </div>

          {/* Sélecteur de véhicule */}
          <div>
            <p className="text-gray-400 text-xs uppercase tracking-wider mb-3">Véhicule</p>
            <select
              value={selectedCar?.Marque_Modele || ''}
              onChange={(e) => {
                const car = filteredCars.find(c => c.Marque_Modele === e.target.value);
                if (car) setSelectedCar(car);
              }}
              className="w-full p-3 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-red-500 transition-all"
              style={{ backgroundColor: '#0e1117', border: '1px solid #2a2a3a' }}
            >
              {filteredCars.map(car => (
                <option key={car.Marque_Modele} value={car.Marque_Modele}>
                  {car.Marque_Modele}
                </option>
              ))}
            </select>
            <p className="text-gray-500 text-xs mt-2">
              {filteredCars.length} véhicule(s) disponible(s)
            </p>
          </div>
        </aside>

        {/* Contenu principal */}
        <main className="flex-1 p-6">
          {selectedCar ? (
            <>
              {/* Cartes de métriques */}
              <div className="grid grid-cols-3 gap-4 mb-6">
                <MetricCard
                  label="Prix FOB"
                  value={formatUSD(selectedCar.Prix_USD)}
                  accentColor="#ff4b4b"
                />
                <MetricCard
                  label="Catégorie"
                  value={selectedCar.Categorie}
                  accentColor="#4b8bff"
                />
                <MetricCard
                  label="Concessionnaire"
                  value={selectedCar.Vendeur_Officiel}
                  accentColor="#4bff8b"
                />
              </div>

              {/* Onglets */}
              <div className="mb-6">
                <div className="flex border-b" style={{ borderColor: '#2a2a3a' }}>
                  <button
                    onClick={() => setActiveTab('3d')}
                    className={`px-6 py-3 font-medium transition-colors ${
                      activeTab === '3d' 
                        ? 'text-white border-b-2' 
                        : 'text-gray-400 hover:text-white'
                    }`}
                    style={{ borderColor: activeTab === '3d' ? '#ff4b4b' : 'transparent' }}
                  >
                    🏎️ Vue 360° & Fiche Technique
                  </button>
                  <button
                    onClick={() => setActiveTab('customs')}
                    className={`px-6 py-3 font-medium transition-colors ${
                      activeTab === 'customs' 
                        ? 'text-white border-b-2' 
                        : 'text-gray-400 hover:text-white'
                    }`}
                    style={{ borderColor: activeTab === 'customs' ? '#ff4b4b' : 'transparent' }}
                  >
                    🛃 Simulateur Douane (SYDONIA / GUCE)
                  </button>
                </div>
              </div>

              {/* Contenu des onglets */}
              {activeTab === '3d' && (
                <div className="grid grid-cols-2 gap-6">
                  {/* Visualisation 3D */}
                  <div 
                    className="rounded-lg overflow-hidden"
                    style={{ backgroundColor: '#1a1a24' }}
                  >
                    <div className="p-4 border-b" style={{ borderColor: '#2a2a3a' }}>
                      <h3 className="text-white font-semibold">🔮 Inspection 3D</h3>
                      <p className="text-gray-500 text-xs">Rotation automatique • Zoom • Contrôle caméra</p>
                    </div>
                    <div className="h-96">
                      <ModelViewerComponent
                        src={get3DModelUrl(selectedCar)}
                        alt={`Modèle 3D de ${selectedCar.Marque_Modele}`}
                        className="w-full h-full"
                      />
                    </div>
                  </div>

                  {/* Fiche technique */}
                  <div 
                    className="rounded-lg p-6"
                    style={{ backgroundColor: '#1a1a24' }}
                  >
                    <h3 className="text-white font-semibold mb-4">📋 Fiche Technique</h3>
                    
                    <div className="mb-6">
                      <h4 className="text-green-400 text-sm font-medium mb-2 flex items-center">
                        <span className="mr-2">✓</span> Points Forts
                      </h4>
                      <ul className="space-y-2">
                        {selectedCar.Avantages.split(';').map((avantage, index) => (
                          <li key={index} className="text-gray-300 text-sm flex items-start">
                            <span className="text-green-500 mr-2">•</span>
                            {avantage.trim()}
                          </li>
                        ))}
                      </ul>
                    </div>

                    <div className="mb-6">
                      <h4 className="text-red-400 text-sm font-medium mb-2 flex items-center">
                        <span className="mr-2">⚠</span> Points Faibles
                      </h4>
                      <ul className="space-y-2">
                        {selectedCar.Inconvenients.split(';').map((inconvenient, index) => (
                          <li key={index} className="text-gray-300 text-sm flex items-start">
                            <span className="text-red-500 mr-2">•</span>
                            {inconvenient.trim()}
                          </li>
                        ))}
                      </ul>
                    </div>

                    <a
                      href={selectedCar.Lien_Vendeur}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="block w-full py-3 px-4 rounded-lg text-center font-medium transition-all hover:opacity-90"
                      style={{ 
                        backgroundColor: '#ff4b4b',
                        color: 'white'
                      }}
                    >
                      🏪 Visiter la concession officielle
                    </a>
                  </div>
                </div>
              )}

              {activeTab === 'customs' && (
                <div className="grid grid-cols-2 gap-6">
                  {/* Paramètres du simulateur */}
                  <div 
                    className="rounded-lg p-6"
                    style={{ backgroundColor: '#1a1a24' }}
                  >
                    <h3 className="text-white font-semibold mb-6">⚙️ Paramètres</h3>

                    {/* Taux de change */}
                    <div className="mb-6">
                      <label className="block text-gray-400 text-sm mb-2">
                        Taux de change (USD → FCFA)
                      </label>
                      <input
                        type="number"
                        value={exchangeRate}
                        onChange={(e) => setExchangeRate(parseFloat(e.target.value) || DEFAULT_EXCHANGE_RATE)}
                        className="w-full p-3 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-red-500 transition-all"
                        style={{ backgroundColor: '#0e1117', border: '1px solid #2a2a3a' }}
                        min="1"
                        step="1"
                      />
                      <p className="text-gray-500 text-xs mt-1">Défaut: {DEFAULT_EXCHANGE_RATE} FCFA</p>
                    </div>

                    {/* Fret maritime */}
                    <div className="mb-6">
                      <label className="block text-gray-400 text-sm mb-2">
                        Fret maritime: {formatUSD(freightUSD)}
                      </label>
                      <input
                        type="range"
                        value={freightUSD}
                        onChange={(e) => setFreightUSD(parseFloat(e.target.value))}
                        className="w-full h-2 rounded-lg appearance-none cursor-pointer"
                        style={{ backgroundColor: '#2a2a3a' }}
                        min="500"
                        max="3000"
                        step="50"
                      />
                      <div className="flex justify-between text-gray-500 text-xs mt-1">
                        <span>$500</span>
                        <span>$3,000</span>
                      </div>
                    </div>

                    {/* Année du véhicule */}
                    <div className="mb-6">
                      <label className="block text-gray-400 text-sm mb-2">
                        Année du véhicule
                      </label>
                      <select
                        value={vehicleYear}
                        onChange={(e) => setVehicleYear(parseInt(e.target.value))}
                        className="w-full p-3 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-red-500 transition-all"
                        style={{ backgroundColor: '#0e1117', border: '1px solid #2a2a3a' }}
                      >
                        {Array.from({ length: MAX_YEAR - MIN_YEAR + 1 }, (_, i) => MAX_YEAR - i).map(year => (
                          <option key={year} value={year}>{year}</option>
                        ))}
                      </select>
                      {vehicleYear < AGE_THRESHOLD && (
                        <p className="text-red-400 text-xs mt-1">
                          ⚠️ Pénalité d'âge appliquée ({formatFCFA(AGE_PENALTY)})
                        </p>
                      )}
                    </div>

                    {/* Résumé rapide */}
                    <div 
                      className="p-4 rounded-lg"
                      style={{ backgroundColor: '#0e1117' }}
                    >
                      <p className="text-gray-400 text-xs mb-2">Véhicule sélectionné</p>
                      <p className="text-white font-medium">{selectedCar.Marque_Modele}</p>
                      <p className="text-gray-500 text-sm">{selectedCar.Categorie} • {formatUSD(selectedCar.Prix_USD)}</p>
                    </div>
                  </div>

                  {/* Résultat du calcul */}
                  <div>
                    <h3 className="text-white font-semibold mb-4">📊 Estimation Douanière</h3>
                    {customsCalculation && (
                      <CustomsReceipt calculation={customsCalculation} />
                    )}
                  </div>
                </div>
              )}
            </>
          ) : (
            <div className="flex items-center justify-center h-96">
              <div className="text-center">
                <p className="text-gray-400 text-xl mb-4">🚗</p>
                <p className="text-gray-500">Aucun véhicule disponible avec les filtres sélectionnés</p>
                <button
                  onClick={() => setSelectedCategories([])}
                  className="mt-4 px-6 py-2 rounded-lg font-medium transition-all hover:opacity-90"
                  style={{ backgroundColor: '#ff4b4b', color: 'white' }}
                >
                  Réinitialiser les filtres
                </button>
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}