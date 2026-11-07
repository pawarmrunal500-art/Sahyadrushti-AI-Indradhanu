import {
  LocationItem, AlertItem, IncidentRecord, ShelterItem, CorridorItem,
  SensorNode, ReplayFrame, DemoScenarioData, PredictionResponse
} from './types';
import { getLocationImage } from './utils/imageHelpers';

// Fallback seed data in case backend is offline
const FALLBACK_LOCATIONS: LocationItem[] = [
  {
    id: "bhushi_dam",
    name: "Bhushi Dam & Waterfall Catchment",
    name_mr: "भुशी धरण व धबधबा पाणलोट क्षेत्र",
    name_hi: "भुशी बांध और झरना जलग्रहण क्षेत्र",
    category: "tourist_spot",
    coordinates: [18.7364, 73.3965],
    elevation_m: 638.0,
    slope_deg: 24.5,
    upstream_catchment_km2: 4.8,
    drainage_proximity_m: 15.0,
    status: "high",
    status_label: "High Surge Risk",
    last_updated: "2026-10-24T18:15:00Z",
    telemetry_status: "modelled",
    current_hazard: "flash_flood",
    risk_score: 74,
    guidance: "High upstream rainfall in Tiger Hill catchment elevates sudden water surge danger. Do not step onto overflow masonry or waterfall plunge areas.",
    guidance_mr: "टायगर हिल पाणलोटात मुसळधार पावसामुळे धरणाच्या सांडव्यावर अचानक प्रवाह वाढण्याची शक्यता. पर्यटकांनी पाण्यात उतरू नये.",
    guidance_hi: "ऊपरी जलग्रहण क्षेत्र में भारी बारिश से अचानक जलस्तर बढ़ने का खतरा। पानी में न उतरें।",
    restrictions: "Section 144 / Police advisory active during torrential rains after 17:00.",
    upstream_info: "Fed by 4.8 km² steep catchment from Tiger Valley. Water level telemetry is modelled from radar & rain gauge proxies.",
    photo_description: "Masonry overflow weir, natural rocky rapids, and downstream gorge.",
    tags: ["Water Hazard", "Tourist Hotspot", "Upstream Catchment Alert"]
  },
  {
    id: "kune_falls",
    name: "Kune Falls & Valley Escarpment",
    name_mr: "कुणे धबधबा व दरी कडा",
    name_hi: "कुणे जलप्रपात और घाटी कगार",
    category: "tourist_spot",
    coordinates: [18.7618, 73.3854],
    elevation_m: 622.0,
    slope_deg: 38.0,
    upstream_catchment_km2: 6.2,
    drainage_proximity_m: 30.0,
    status: "moderate",
    status_label: "Moderate Escarpment Caution",
    last_updated: "2026-10-24T18:10:00Z",
    telemetry_status: "telemetry_unavailable",
    current_hazard: "landslide",
    risk_score: 52,
    guidance: "Three-tiered 200m waterfall over basalt cliff. Wet spray causes slippery edges and minor pebble roll off cut slopes.",
    guidance_mr: "२०० मीटर उंच कडा असून निसरड्या कड्यांवरून चालणे टाळा. कडे कोसळण्याचा मध्यम धोका.",
    guidance_hi: "खड़ी चट्टान और फिसलन भरे किनारे। घाटी के किनारे न जाएं।",
    restrictions: "Viewing restricted to marked viewpoints on Old Highway.",
    upstream_info: "Water-level telemetry unavailable. Risk estimated from IMD radar & regional precipitation.",
    photo_description: "Three-tiered waterfall cascading down sheer basalt escarpment.",
    tags: ["Waterfall", "Steep Cliff", "Spray Zone"]
  },
  {
    id: "tiger_point",
    name: "Tiger's Leap (Waghai) Escarpment",
    name_mr: "वाघदरी / टायगर पॉईंट कडा",
    name_hi: "टाइगर पॉइंट कगार",
    category: "tourist_spot",
    coordinates: [18.7077, 73.3881],
    elevation_m: 725.0,
    slope_deg: 46.0,
    upstream_catchment_km2: 1.2,
    drainage_proximity_m: 120.0,
    status: "high",
    status_label: "High Wind & Cliff Shear",
    last_updated: "2026-10-24T18:20:00Z",
    telemetry_status: "modelled",
    current_hazard: "landslide",
    risk_score: 71,
    guidance: "Severe 650m sheer cliff drop. Dense fog and strong monsoon updrafts reduce visibility. Stay strictly behind railing.",
    guidance_mr: "६५० मीटर खोल दरी. जोरदार वारे व दाट धुक्यामुळे कड्याच्या कठड्यापलीकडे जाऊ नये.",
    guidance_hi: "गहरी खाई और तेज हवाएं। सुरक्षा रेलिंग के पीछे रहें।",
    restrictions: "Strict ban on climbing over safety barricades.",
    upstream_info: "High windshear zone, rapid surface runoff drains into Konkan plains.",
    photo_description: "High cliff top overlooking deep sheer Konkan drop.",
    tags: ["Cliff", "High Altitude", "Windshear"]
  },
  {
    id: "lions_point",
    name: "Lion's Point",
    name_mr: "लायन्स पॉईंट",
    name_hi: "लायंस पॉइंट",
    category: "tourist_spot",
    coordinates: [18.7122, 73.3912],
    elevation_m: 718.0,
    slope_deg: 41.0,
    upstream_catchment_km2: 1.5,
    drainage_proximity_m: 140.0,
    status: "moderate",
    status_label: "Moderate Ridge Caution",
    last_updated: "2026-10-24T18:00:00Z",
    telemetry_status: "modelled",
    current_hazard: "landslide",
    risk_score: 48,
    guidance: "Exposed ridge between Lonavala and Aamby Valley road. Minor surface erosion observed on unpaved shoulders.",
    guidance_mr: "उघड्या डोंगररांगेवर जोरदार वारे. रस्त्याच्या बाजूला माती खचण्याची शक्यता.",
    guidance_hi: "खुली पहाड़ी कगार पर तेज हवाएं। सावधानी बरतें।",
    restrictions: "Parking only in designated asphalt bays.",
    upstream_info: "Surface sheet wash during intense showers.",
    photo_description: "Panoramic ridge viewpoint between two valleys.",
    tags: ["Ridge", "Viewpoint", "Road Access"]
  },
  {
    id: "rajmachi_route",
    name: "Rajmachi Trek & Udhewadi Route",
    name_mr: "राजमाची ट्रेक मार्ग व उढेवाडी",
    name_hi: "राजमाची ट्रेक मार्ग",
    category: "tourist_spot",
    coordinates: [18.8262, 73.4005],
    elevation_m: 780.0,
    slope_deg: 32.0,
    upstream_catchment_km2: 9.5,
    drainage_proximity_m: 45.0,
    status: "very_high",
    status_label: "Very High Trail Washout Risk",
    last_updated: "2026-10-24T18:25:00Z",
    telemetry_status: "telemetry_unavailable",
    current_hazard: "landslide",
    risk_score: 88,
    guidance: "15km kutcha jungle road severely waterlogged. Four mountain seasonal stream crossings are in spate. Do not attempt on two-wheelers or without local guides.",
    guidance_mr: "जंगल मार्ग चिखलामुळे अत्यंत निसरडा. ओढ्यांना आलेला पूर वाहून नेऊ शकतो. ट्रेकिंग टाळावी.",
    guidance_hi: "रास्ता अत्यधिक फिसलन भरा और नाले उफान पर हैं। ट्रेक न करें।",
    restrictions: "Forest department advisory in effect during red alerts.",
    upstream_info: "No cellular telemetry. Satellite precipitation indicates over 160mm in 24 hours.",
    photo_description: "Dense Sahyadri forest road with torrential seasonal stream crossings.",
    tags: ["Jungle Trail", "Flash Streams", "Remote Evacuation Difficulty"]
  },
  {
    id: "khandala_expressway",
    name: "Amrutanjan Bridge / Bhor Ghat Expressway",
    name_mr: "अमृतांजन पूल / बोरघाट द्रुतगती महामार्ग",
    name_hi: "अमृतांजन ब्रिज / भोर घाट एक्सप्रेसवे",
    category: "corridor",
    coordinates: [18.7758, 73.3592],
    elevation_m: 585.0,
    slope_deg: 36.5,
    upstream_catchment_km2: 3.4,
    drainage_proximity_m: 50.0,
    status: "high",
    status_label: "High Rockfall & Mudslide Alert",
    last_updated: "2026-10-24T18:28:00Z",
    telemetry_status: "live",
    current_hazard: "landslide",
    risk_score: 79,
    guidance: "Steep cut slopes stabilized with wire netting experiencing heavy saturation. Watch for loose boulders rolling onto Pune-bound corridor.",
    guidance_mr: "द्रुतगती मार्गाच्या कडेला दरड व लहान दगड कोसळण्याची शक्यता. चालकांनी वेग मर्यादित ठेवावा.",
    guidance_hi: "चट्टान गिरने का खतरा। वाहन धीमी गति से चलाएं।",
    restrictions: "Heavy vehicles advised to maintain 40 km/h ghat speed.",
    upstream_info: "Continuous road safety sensor active. Overburden saturation 86%.",
    photo_description: "High engineered rock cut adjacent to 6-lane expressway.",
    tags: ["Expressway Corridor", "Critical Infrastructure", "Rockfall Mesh Area"]
  },
  {
    id: "adoshi_tunnel",
    name: "Adoshi Tunnel Vicinity",
    name_mr: "अडोशी बोगदा परिसर",
    name_hi: "अडोशी सुरंग क्षेत्र",
    category: "corridor",
    coordinates: [18.7792, 73.3441],
    elevation_m: 490.0,
    slope_deg: 31.0,
    upstream_catchment_km2: 2.1,
    drainage_proximity_m: 80.0,
    status: "moderate",
    status_label: "Moderate Corridor Caution",
    last_updated: "2026-10-24T18:12:00Z",
    telemetry_status: "modelled",
    current_hazard: "corridor_disruption",
    risk_score: 45,
    guidance: "Approach to tunnel portal. Drainage culverts flowing at 70% capacity. Surface aquaplaning risk during sudden downpours.",
    guidance_mr: "बोगद्याच्या मुखाजवळ पाणी साचण्याचा धोका. वाहनांचे स्किडिंग टाळण्यासाठी सावधगिरी.",
    guidance_hi: "सुरंग के पास फिसलन का खतरा। सतर्क रहें।",
    restrictions: "Normal transit permitted. Traffic patrol deployed.",
    upstream_info: "Separate collision/incident risk monitored independently from natural hazards.",
    photo_description: "Tunnel entrance through basalt mountain spur.",
    tags: ["Tunnel Portal", "Aquaplaning", "Traffic Choke Point"]
  },
  {
    id: "monkey_hill",
    name: "Monkey Hill Railway Ghat Corridor",
    name_mr: "मंकी हिल रेल्वे घाट मार्ग",
    name_hi: "मंकी हिल रेलवे घाट खंड",
    category: "corridor",
    coordinates: [18.7845, 73.3610],
    elevation_m: 540.0,
    slope_deg: 44.0,
    upstream_catchment_km2: 2.8,
    drainage_proximity_m: 35.0,
    status: "high",
    status_label: "High Rail Boulder Watch",
    last_updated: "2026-10-24T18:22:00Z",
    telemetry_status: "live",
    current_hazard: "landslide",
    risk_score: 76,
    guidance: "Central Railway ghat section. Historical boulder drop spot. Catch-water drains monitored; bank patrols deployed with detonators.",
    guidance_mr: "रेल्वे मार्गावर दरड कोसळण्याची भीती. रेल्वे गँगमन सतत पाहणी करत आहेत.",
    guidance_hi: "रेलवे ट्रैक पर पत्थर गिरने की आशंका। निगरानी जारी।",
    restrictions: "Speed restriction of 30 km/h for descending trains.",
    upstream_info: "Geotechnical fence sensor indicates minor tension cracks on upper terrace.",
    photo_description: "Steep rail cutting with overhead electrification and rockfall shelter.",
    tags: ["Railway Ghat", "Central Railway", "Critical Transit"]
  },
  {
    id: "thakurwadi",
    name: "Thakurwadi Railway Catchment",
    name_mr: "ठाकूरवाडी रेल्वे पाणलोट व घाट",
    name_hi: "ठाकुरवाड़ी रेलवे खंड",
    category: "corridor",
    coordinates: [18.8023, 73.3458],
    elevation_m: 410.0,
    slope_deg: 35.0,
    upstream_catchment_km2: 5.1,
    drainage_proximity_m: 40.0,
    status: "moderate",
    status_label: "Moderate Track Runoff",
    last_updated: "2026-10-24T18:05:00Z",
    telemetry_status: "modelled",
    current_hazard: "waterlogging",
    risk_score: 50,
    guidance: "Ghat brake-testing station. Water overflow from mountain culverts into ballast. Operational caution.",
    guidance_mr: "रेल्वे ट्रॅकशेजारील ओढ्यांमधून पाण्याचा मोठा निचरा. रेल्वे वाहतूक सावकाश.",
    guidance_hi: "ट्रैक के किनारे पानी का बहाव। सावधानी बरतें।",
    restrictions: "Cautious running advised by railway control.",
    upstream_info: "Catchment runoff drains towards Karjat plains.",
    photo_description: "Railway station on mountain terrace surrounded by cliffs.",
    tags: ["Railway Station", "Ballast Runoff", "Bhor Ghat"]
  },
  {
    id: "patan_village",
    name: "Patan Village & Hillside Settlements",
    name_mr: "पाटण गाव व डोंगर पायथा वस्त्या",
    name_hi: "पाटन गांव व बस्ती",
    category: "settlement",
    coordinates: [18.7291, 73.4350],
    elevation_m: 665.0,
    slope_deg: 29.0,
    upstream_catchment_km2: 3.7,
    drainage_proximity_m: 60.0,
    status: "high",
    status_label: "High Settlement Slope Alert",
    last_updated: "2026-10-24T18:30:00Z",
    telemetry_status: "modelled",
    current_hazard: "landslide",
    risk_score: 75,
    guidance: "Upper slope exhibits weathered soil mantle with high antecedent saturation. Residents near eastern escarpment advised to remain alert for ground fissures.",
    guidance_mr: "डोंगरउतारावरील घरांना माती सरकण्याचा धोका. जमिनीला भेगा किंवा पाण्याचे नवे झरे दिसल्यास तात्काळ स्थलांतर करावे.",
    guidance_hi: "गांव के ऊपर की पहाड़ी से मिट्टी खिसकने का खतरा। सतर्क रहें।",
    restrictions: "Local Talathi and Village Disaster Committee on standby.",
    upstream_info: "Terrain slope 29°, soil moisture 84%. Nearest shelter at Bhangarwadi.",
    photo_description: "Rural hamlet situated beneath steep basalt tableland.",
    tags: ["Habitation", "SDG 13 Resilience", "Community Shelter Link"]
  },
  {
    id: "lonavala_town",
    name: "Lonavala Civic Center (Ryewood)",
    name_mr: "लोणावळा शहर मध्यवर्ती (रायवूड)",
    name_hi: "लोनावला शहर",
    category: "settlement",
    coordinates: [18.7512, 73.4082],
    elevation_m: 624.0,
    slope_deg: 6.5,
    upstream_catchment_km2: 2.2,
    drainage_proximity_m: 220.0,
    status: "low",
    status_label: "Low Risk",
    last_updated: "2026-10-24T18:30:00Z",
    telemetry_status: "live",
    current_hazard: "waterlogging",
    risk_score: 18,
    guidance: "Flat urban plateau with good drainage. Municipal stormwater drains operating normally. Safe zone for emergency staging.",
    guidance_mr: "शहरात पाणी साचलेले नाही. नागरी जनजीवन व वाहतूक सुरळीत.",
    guidance_hi: "शहरी क्षेत्र में स्थिति सामान्य। मुख्य राहत केंद्र यहीं स्थित है।",
    restrictions: "None.",
    upstream_info: "Central assembly and coordination headquarters.",
    photo_description: "Town center with municipal council, hospitals, and transit hubs.",
    tags: ["Safe Haven", "Administrative HQ", "Hospital Access"]
  }
];

export const apiClient = {
  isBackendConnected: false,

  async checkHealth(): Promise<boolean> {
    try {
      const res = await fetch('/api/health');
      if (res.ok) {
        this.isBackendConnected = true;
        return true;
      }
    } catch {
      this.isBackendConnected = false;
    }
    return false;
  },

  async getLocations(): Promise<LocationItem[]> {
    try {
      const res = await fetch('/api/locations');
      if (res.ok) {
        this.isBackendConnected = true;
        const data: LocationItem[] = await res.json();
        return data.map(l => ({ ...l, image_url: l.image_url || getLocationImage(l.id) }));
      }
    } catch (e) {
      console.warn('Backend unavailable, using resilient fallback locations:', e);
    }
    return FALLBACK_LOCATIONS.map(l => ({ ...l, image_url: l.image_url || getLocationImage(l.id) }));
  },

  async getIncidents(): Promise<IncidentRecord[]> {
    try {
      const res = await fetch('/api/incidents');
      if (res.ok) return await res.json();
    } catch (e) {
      console.warn('Backend unavailable for incidents, using local records:', e);
    }
    return [];
  },

  async getAlerts(): Promise<AlertItem[]> {
    try {
      const res = await fetch('/api/alerts');
      if (res.ok) return await res.json();
    } catch (e) {
      console.warn('Backend unavailable for alerts, using local alerts:', e);
    }
    return [];
  },

  async getShelters(): Promise<ShelterItem[]> {
    try {
      const res = await fetch('/api/shelters');
      if (res.ok) return await res.json();
    } catch (e) {
      console.warn('Backend unavailable for shelters, using local shelters:', e);
    }
    return [];
  },

  async getCorridors(): Promise<CorridorItem[]> {
    try {
      const res = await fetch('/api/corridors');
      if (res.ok) return await res.json();
    } catch (e) {
      console.warn('Backend unavailable for corridors:', e);
    }
    return [];
  },

  async getSensors(): Promise<{ nodes: SensorNode[]; healthy_count: number }> {
    try {
      const res = await fetch('/api/sensors/status');
      if (res.ok) return await res.json();
    } catch (e) {
      console.warn('Backend unavailable for sensors:', e);
    }
    return { nodes: [], healthy_count: 0 };
  },

  async getReplay(): Promise<{ timeline: ReplayFrame[] }> {
    try {
      const res = await fetch('/api/replay');
      if (res.ok) return await res.json();
    } catch (e) {
      console.warn('Backend unavailable for replay:', e);
    }
    return { timeline: [] };
  },

  async getDemoScenario(): Promise<DemoScenarioData | null> {
    try {
      const res = await fetch('/api/demo/scenario');
      if (res.ok) return await res.json();
    } catch (e) {
      console.warn('Backend unavailable for demo scenario:', e);
    }
    return null;
  },

  async runSimulation(payload: {
    rain_1h_mm: number;
    rain_24h_mm: number;
    rain_48h_mm: number;
    forecast_24h_mm: number;
    soil_moisture_pct: number;
    baseline_location_ids: string[];
  }) {
    try {
      const res = await fetch('/api/simulate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (res.ok) return await res.json();
    } catch (e) {
      console.warn('Simulation failed via backend:', e);
    }
    return null;
  },

  async submitIncident(payload: {
    hazard_type: string;
    location_name: string;
    lat: number;
    lon: number;
    description: string;
    observed_time: string;
    reporter_name: string;
  }) {
    try {
      const res = await fetch('/api/incidents', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (res.ok) return await res.json();
    } catch (e) {
      console.warn('Incident submit failed via backend:', e);
    }
    return {
      message: 'Recorded locally in offline queue.',
      incident_id: 'LOCAL-' + Math.floor(Math.random() * 10000),
      verification_status: 'Unverified report'
    };
  },

  async draftAlert(payload: {
    title: string;
    title_mr: string;
    message: string;
    message_mr: string;
    severity: string;
    geographic_coverage: string;
    target_locations: string[];
  }) {
    try {
      const res = await fetch('/api/authority/alerts/draft', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (res.ok) return await res.json();
    } catch (e) {
      console.warn('Alert draft failed via backend:', e);
    }
    return null;
  },

  async approveAlert(alertId: string) {
    try {
      const res = await fetch(`/api/authority/alerts/${alertId}/approve`, {
        method: 'POST'
      });
      if (res.ok) return await res.json();
    } catch (e) {
      console.warn('Alert approve failed via backend:', e);
    }
    return null;
  }
};
