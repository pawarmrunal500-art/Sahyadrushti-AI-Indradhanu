import { LocationItem, HazardType, RiskLevel } from '../types';

export interface RegionalPlace {
  id: string;
  name: string;
  name_mr: string;
  name_hi: string;
  region: string;
  coordinates: [number, number]; // [lat, lon]
  elevation_m: number;
  slope_deg: number;
  category: 'tourist_spot' | 'corridor' | 'settlement' | 'water_body';
  display_name: string;
  hazard_type: HazardType;
  status: RiskLevel;
  status_label: string;
  risk_score: number;
  upstream_catchment_km2?: number;
  drainage_proximity_m?: number;
  guidance: string;
  guidance_mr: string;
  guidance_hi: string;
}

export const REGIONAL_GAZETTEER: RegionalPlace[] = [
  {
    id: 'kamshet_region',
    name: 'Kamshet',
    name_mr: 'कामशेत',
    name_hi: 'कामशेत',
    region: 'Maval Taluka, Pune District (Western Ghats Basin)',
    coordinates: [18.7669, 73.5524],
    elevation_m: 625.0,
    slope_deg: 6.5,
    category: 'settlement',
    display_name: 'Kamshet, Maval, Pune District, Maharashtra',
    hazard_type: 'flash_flood',
    status: 'moderate',
    status_label: 'Riverine Basin Caution',
    risk_score: 38,
    upstream_catchment_km2: 18.4,
    drainage_proximity_m: 80.0,
    guidance: 'Indrayani river basin; check river crossings, low bridges, and railway underpasses during heavy rain.',
    guidance_mr: 'इंद्रायणी नदीचे खोरे; मुसळधार पावसात नदीकाठचे रस्ते, जुने पूल आणि रेल्वे भुयारी मार्गांवर सावधगिरी बाळगा.',
    guidance_hi: 'इंद्रािणी नदी बेसिन; भारी बारिश में नदी तट, पुराने पुलों और अंडरपास पर सतर्क रहें।'
  },
  {
    id: 'karla_region',
    name: 'Karla Caves & Ekvira',
    name_mr: 'कार्ला / एकवीरा देवी / कार्ले लेणी',
    name_hi: 'कार्ला / एकवीरा देवी / कार्ले गुफाएं',
    region: 'Maval Taluka, Pune District',
    coordinates: [18.7820, 73.4700],
    elevation_m: 650.0,
    slope_deg: 18.0,
    category: 'tourist_spot',
    display_name: 'Karla, Maval, Pune District, Maharashtra',
    hazard_type: 'landslide',
    status: 'moderate',
    status_label: 'Moderate Slope Caution',
    risk_score: 45,
    upstream_catchment_km2: 3.5,
    drainage_proximity_m: 45.0,
    guidance: 'Hillside approach to ancient rock caves. Watch for loose rocks on temple steps during rain.',
    guidance_mr: 'प्राचीन लेण्यांकडे जाणारा डोंगर मार्ग. पावसाळ्यात पायऱ्यांवर निसरडेपणा व दगड पडण्यापासून सावध राहा.',
    guidance_hi: 'गुफाओं का पहाड़ी मार्ग। बारिश में सीढ़ियों पर सतर्क रहें।'
  },
  {
    id: 'malavli_region',
    name: 'Malavli',
    name_mr: 'मळवली',
    name_hi: 'मलवडी',
    region: 'Maval Taluka, Pune District',
    coordinates: [18.7490, 73.4680],
    elevation_m: 615.0,
    slope_deg: 8.0,
    category: 'settlement',
    display_name: 'Malavli, Maval, Pune District, Maharashtra',
    hazard_type: 'flash_flood',
    status: 'low',
    status_label: 'Low Terrain Risk',
    risk_score: 28,
    upstream_catchment_km2: 5.2,
    drainage_proximity_m: 60.0,
    guidance: 'Gateway to Lohagad & Visapur forts. Check stream crossings along fort base roads.',
    guidance_mr: 'लोहगड-विसापूरचे प्रवेशद्वार. किल्ल्याच्या पायथ्याशी नाल्यांच्या प्रवाहात सावधगिरी बाळगा.',
    guidance_hi: 'लोहगढ़ का आधार। नालों के बहाव पर सतर्क रहें।'
  },
  {
    id: 'pawna_lake',
    name: 'Pawna Lake & Dam',
    name_mr: 'पवना धरण व जलाशय',
    name_hi: 'पवना बांध और झील',
    region: 'Maval Taluka, Pune District',
    coordinates: [18.6730, 73.4970],
    elevation_m: 640.0,
    slope_deg: 12.0,
    category: 'water_body',
    display_name: 'Pawna Dam, Maval, Pune District, Maharashtra',
    hazard_type: 'flash_flood',
    status: 'moderate',
    status_label: 'Reservoir Perimeter Alert',
    risk_score: 52,
    upstream_catchment_km2: 112.0,
    drainage_proximity_m: 20.0,
    guidance: 'Major catchment dam. Avoid camping near submerged shoreline during spillway discharge.',
    guidance_mr: 'प्रमुख धरण क्षेत्र. सांडव्यातून पाण्याचा विसर्ग सुरू असताना पाणथळ किनारी जाणे टाळा.',
    guidance_hi: 'प्रमुख बांध क्षेत्र। जल निकासी के समय तट के पास न जाएं।'
  },
  {
    id: 'lohagad_fort',
    name: 'Lohagad Fort',
    name_mr: 'लोहगड किल्ला',
    name_hi: 'लोहगढ़ किला',
    region: 'Western Ghats Escarpment',
    coordinates: [18.7000, 73.4790],
    elevation_m: 1033.0,
    slope_deg: 42.0,
    category: 'tourist_spot',
    display_name: 'Lohagad Fort, Maval, Pune District, Maharashtra',
    hazard_type: 'landslide',
    status: 'high',
    status_label: 'High Escarpment Risk',
    risk_score: 72,
    upstream_catchment_km2: 1.5,
    drainage_proximity_m: 150.0,
    guidance: 'Steep escarpment and Vinchu Kata spur. Severe gale winds and slippery steps during monsoon.',
    guidance_mr: 'उंच कडा आणि विंचूकडा. मुसळधार पावसात पायऱ्या निसरड्या होतात आणि वेगाने वाहणाऱ्या वाऱ्यांपासून सावध राहा.',
    guidance_hi: 'खड़ी चट्टान और तेज हवाएं। बारिश में संभलकर चलें।'
  },
  {
    id: 'visapur_fort',
    name: 'Visapur Fort',
    name_mr: 'विसापूर किल्ला',
    name_hi: 'विसापुर किला',
    region: 'Western Ghats Escarpment',
    coordinates: [18.7240, 73.4900],
    elevation_m: 1084.0,
    slope_deg: 44.0,
    category: 'tourist_spot',
    display_name: 'Visapur Fort, Maval, Pune District, Maharashtra',
    hazard_type: 'landslide',
    status: 'high',
    status_label: 'Waterfall Trail Warning',
    risk_score: 76,
    upstream_catchment_km2: 1.8,
    drainage_proximity_m: 10.0,
    guidance: 'Waterfall trek trail up stone stairs. Risk of rapid water cascades and rock rolls.',
    guidance_mr: 'दगडी पायऱ्यांवरून वाहणारा धबधबा मार्ग. अचानक पाण्याचा जोर वाढण्याची व घसरण्याची शक्यता.',
    guidance_hi: 'सीढ़ियों पर तेज बहाव। पत्थरों के गिरने का जोखिम।'
  },
  {
    id: 'khopoli_town',
    name: 'Khopoli',
    name_mr: 'खोपोली',
    name_hi: 'खोपोली',
    region: 'Khalapur Taluka, Raigad District',
    coordinates: [18.7890, 73.3440],
    elevation_m: 85.0,
    slope_deg: 5.0,
    category: 'settlement',
    display_name: 'Khopoli, Khalapur, Raigad District, Maharashtra',
    hazard_type: 'flash_flood',
    status: 'moderate',
    status_label: 'Bhor Ghat Base Caution',
    risk_score: 42,
    upstream_catchment_km2: 45.0,
    drainage_proximity_m: 35.0,
    guidance: 'Bhor Ghat base corridor and Patalganga river. Watch for tailrace surges and urban waterlogging.',
    guidance_mr: 'बोरघाटाचा पायथा आणि पाताळगंगा नदी. सखल भागात पाणी साचणे व घाटातून येणाऱ्या पाण्याच्या प्रवाहावर लक्ष ठेवा.',
    guidance_hi: 'बोरघाट की तलहटी। निचले इलाकों में जलभराव पर नजर रखें।'
  },
  {
    id: 'talegaon_dabhade',
    name: 'Talegaon Dabhade',
    name_mr: 'तळेगाव दाभाडे',
    name_hi: 'तलेगांव दाभाड़े',
    region: 'Maval Taluka, Pune District',
    coordinates: [18.7300, 73.6800],
    elevation_m: 610.0,
    slope_deg: 4.0,
    category: 'settlement',
    display_name: 'Talegaon Dabhade, Pune District, Maharashtra',
    hazard_type: 'flash_flood',
    status: 'low',
    status_label: 'Low Plateau Risk',
    risk_score: 22,
    upstream_catchment_km2: 8.0,
    drainage_proximity_m: 120.0,
    guidance: 'Plateau plain urban area. Normal monsoon drainage precautions.',
    guidance_mr: 'सपाट पठारी भाग. सामान्य पावसाळी निचरा दक्षता.',
    guidance_hi: 'मैदानी क्षेत्र। सामान्य जल निकासी सावधानियां।'
  },
  {
    id: 'wadgaon_maval',
    name: 'Wadgaon Maval',
    name_mr: 'वडगाव मावळ',
    name_hi: 'वडगांव मावल',
    region: 'Maval Taluka Administrative Center, Pune',
    coordinates: [18.7420, 73.6450],
    elevation_m: 615.0,
    slope_deg: 4.5,
    category: 'settlement',
    display_name: 'Wadgaon Maval, Pune District, Maharashtra',
    hazard_type: 'flash_flood',
    status: 'low',
    status_label: 'Administrative Hub Clear',
    risk_score: 24,
    upstream_catchment_km2: 6.5,
    drainage_proximity_m: 110.0,
    guidance: 'Taluka administrative headquarters. Emergency operations hub for Maval region.',
    guidance_mr: 'मावळ तालुका प्रशासकीय केंद्र व आपत्ती व्यवस्थापन संपर्क केंद्र.',
    guidance_hi: 'मावल तालुका प्रशासनिक केंद्र।'
  },
  {
    id: 'somatane_phata',
    name: 'Somatane Phata / Toll',
    name_mr: 'सोमाटणे फाटा',
    name_hi: 'सोमाटने फाटा',
    region: 'Mumbai-Pune Expressway / Maval',
    coordinates: [18.7180, 73.6850],
    elevation_m: 605.0,
    slope_deg: 3.5,
    category: 'corridor',
    display_name: 'Somatane Phata, Pune District, Maharashtra',
    hazard_type: 'corridor_disruption',
    status: 'low',
    status_label: 'Highway Junction Clear',
    risk_score: 20,
    upstream_catchment_km2: 4.0,
    drainage_proximity_m: 200.0,
    guidance: 'Expressway entry junction. Highway transit clear.',
    guidance_mr: 'द्रुतगती मार्ग जंक्शन. वाहतूक सुरळीत.',
    guidance_hi: 'एक्सप्रेसवे जंक्शन। यातायात सुचारू।'
  },
  {
    id: 'rajmachi_plateau',
    name: 'Rajmachi Fort & Plateau',
    name_mr: 'राजमाची किल्ला व पठार',
    name_hi: 'राजमाची किला',
    region: 'Western Ghats Crestline',
    coordinates: [18.8280, 73.3980],
    elevation_m: 825.0,
    slope_deg: 45.0,
    category: 'tourist_spot',
    display_name: 'Rajmachi Fort, Pune/Raigad Border, Maharashtra',
    hazard_type: 'landslide',
    status: 'very_high',
    status_label: 'Critical Escarpment Risk',
    risk_score: 85,
    upstream_catchment_km2: 2.0,
    drainage_proximity_m: 30.0,
    guidance: 'Extremely rugged cliffline. Mudslides and rock detachment on unpaved 14km forest approach.',
    guidance_mr: 'अतिदुर्गम कडा. पावसाळ्यात पायवाट व जंगलातील रस्त्यावर चिखल व दरड कोसळण्याचा मोठा धोका.',
    guidance_hi: 'अत्यंत दुर्गम कगार। भूस्खलन का उच्च जोखिम।'
  },
  {
    id: 'tungarli_lake',
    name: 'Tungarli Lake & Hills',
    name_mr: 'तुंगार्ली तलाव व टेकड्या',
    name_hi: 'तुंगार्ली झील',
    region: 'Lonavala North, Pune District',
    coordinates: [18.7640, 73.4150],
    elevation_m: 660.0,
    slope_deg: 15.0,
    category: 'water_body',
    display_name: 'Tungarli Lake, Lonavala, Maharashtra',
    hazard_type: 'flash_flood',
    status: 'low',
    status_label: 'Low Dam Spill Risk',
    risk_score: 26,
    upstream_catchment_km2: 2.8,
    drainage_proximity_m: 25.0,
    guidance: 'Scenic small dam and resort hill slope. Controlled overflow during monsoon.',
    guidance_mr: 'निसर्गरम्य लहान धरण व टेकडी. पावसाळ्यात नियंत्रित विसर्ग.',
    guidance_hi: 'छोटी झील और पहाड़ी। नियंत्रित जल बहाव।'
  },
  {
    id: 'kurvande_village',
    name: 'Kurvande Village',
    name_mr: 'कुर्वांडे गाव',
    name_hi: 'कुर्वांडे गांव',
    region: 'Lonavala South / Tiger Point Base',
    coordinates: [18.7330, 73.3980],
    elevation_m: 670.0,
    slope_deg: 16.0,
    category: 'settlement',
    display_name: 'Kurvande, Lonavala, Pune District, Maharashtra',
    hazard_type: 'landslide',
    status: 'moderate',
    status_label: 'Hill Valley Caution',
    risk_score: 48,
    upstream_catchment_km2: 3.2,
    drainage_proximity_m: 40.0,
    guidance: 'Base village along INS Shivaji - Tiger Point corridor. Watch for hill slope soil saturation.',
    guidance_mr: 'आयएनएस शिवाजी - टायगर पॉईंट मार्गावरील गाव. डोंगरावरील पाण्याच्या प्रवाहांवर लक्ष ठेवा.',
    guidance_hi: 'पहाड़ी मार्ग का गांव। मिट्टी के कटाव पर नजर रखें।'
  },
  {
    id: 'aamby_valley',
    name: 'Aamby Valley Corridor',
    name_mr: 'अ‍ॅम्बी व्हॅली मार्ग',
    name_hi: 'एम्बी वैली मार्ग',
    region: 'Western Ghats Plateau, Pune',
    coordinates: [18.6650, 73.3850],
    elevation_m: 820.0,
    slope_deg: 22.0,
    category: 'corridor',
    display_name: 'Aamby Valley Road, Maharashtra',
    hazard_type: 'landslide',
    status: 'moderate',
    status_label: 'Mountain Road Fog & Wet Alert',
    risk_score: 54,
    upstream_catchment_km2: 12.0,
    drainage_proximity_m: 50.0,
    guidance: 'High altitude ghat road. Dense monsoon fog, low visibility, and minor gravel slips.',
    guidance_mr: 'उंच घाट रस्ता. दाट धुके, कमी दृश्यमानता आणि किरकोळ खडी घसरण्यापासून सावध राहा.',
    guidance_hi: 'पहाड़ी सड़क। घना कोहरा और फिसलन।'
  },
  {
    id: 'bedse_caves',
    name: 'Bedse Caves',
    name_mr: 'बेडसे लेणी',
    name_hi: 'बेडसे गुफाएं',
    region: 'Maval Taluka, Pune District',
    coordinates: [18.7110, 73.5350],
    elevation_m: 720.0,
    slope_deg: 28.0,
    category: 'tourist_spot',
    display_name: 'Bedse Caves, Maval, Pune District, Maharashtra',
    hazard_type: 'landslide',
    status: 'moderate',
    status_label: 'Cliff Trail Caution',
    risk_score: 46,
    upstream_catchment_km2: 1.8,
    drainage_proximity_m: 80.0,
    guidance: 'Ancient Buddhist rock-cut caves. Steep stairway approach with slippery moss during rain.',
    guidance_mr: 'प्राचीन बौद्ध लेणी. पावसाळ्यात पायऱ्यांवर शेवाळ असल्याने घसरण्याचा धोका.',
    guidance_hi: 'प्राचीन शैलकृत गुफाएं। बारिश में सीढ़ियों पर संभलकर चलें।'
  }
];

export interface NearestStationInfo {
  station: LocationItem;
  distanceKm: number;
}

export function findNearestStation(
  coords: [number, number],
  monitoredLocations: LocationItem[]
): NearestStationInfo | null {
  if (!monitoredLocations || monitoredLocations.length === 0) return null;

  let nearest: LocationItem | null = null;
  let minDistance = Infinity;

  const [lat1, lon1] = coords;

  for (const loc of monitoredLocations) {
    const [lat2, lon2] = loc.coordinates;
    const dLat = (lat2 - lat1) * 111.0;
    const dLon = (lon2 - lon1) * 111.0 * Math.cos((lat1 * Math.PI) / 180);
    const dist = Math.sqrt(dLat * dLat + dLon * dLon);
    if (dist < minDistance) {
      minDistance = dist;
      nearest = loc;
    }
  }

  return nearest ? { station: nearest, distanceKm: minDistance } : null;
}

export function searchLocalGazetteer(
  query: string,
  monitoredLocations: LocationItem[]
): Array<RegionalPlace | (LocationItem & { region: string; display_name: string })> {
  const cleanQ = query.trim().toLowerCase();
  if (!cleanQ) return [];

  const results: Array<RegionalPlace | (LocationItem & { region: string; display_name: string })> = [];

  // 1. Check monitored locations
  for (const loc of monitoredLocations) {
    if (
      loc.name.toLowerCase().includes(cleanQ) ||
      loc.name_mr.includes(cleanQ) ||
      loc.name_hi.includes(cleanQ) ||
      loc.id.toLowerCase().includes(cleanQ)
    ) {
      results.push({
        ...loc,
        region: 'Lonavala-Khandala Monitored Grid',
        display_name: `${loc.name} (Monitored Instrument Point)`
      });
    }
  }

  // 2. Check regional gazetteer (Kamshet, Karla, Pawna, etc.)
  for (const place of REGIONAL_GAZETTEER) {
    if (
      place.name.toLowerCase().includes(cleanQ) ||
      place.name_mr.includes(cleanQ) ||
      place.name_hi.includes(cleanQ) ||
      place.id.toLowerCase().includes(cleanQ) ||
      place.region.toLowerCase().includes(cleanQ)
    ) {
      // Avoid duplicate if same id exists
      if (!results.some((r) => r.id === place.id)) {
        results.push(place);
      }
    }
  }

  return results;
}

export function toLocationItem(
  place: RegionalPlace | any,
  monitoredLocations: LocationItem[]
): LocationItem {
  // If it's already a full LocationItem with tags, return it
  if ('tags' in place && Array.isArray(place.tags) && place.tags.length > 0) {
    return place as LocationItem;
  }

  const nearest = findNearestStation(place.coordinates, monitoredLocations);
  const nearestNote = nearest
    ? `Nearest sensor: ${nearest.station.name} (${nearest.distanceKm.toFixed(1)} km away, Risk Score: ${nearest.station.risk_score}/100)`
    : '';

  return {
    id: place.id || `search_${Date.now()}`,
    name: place.name,
    name_mr: place.name_mr || place.name,
    name_hi: place.name_hi || place.name,
    category: place.category || 'settlement',
    coordinates: place.coordinates,
    elevation_m: place.elevation_m || 625.0,
    slope_deg: place.slope_deg || 6.5,
    upstream_catchment_km2: place.upstream_catchment_km2 || 15.0,
    drainage_proximity_m: place.drainage_proximity_m || 80.0,
    status: (place.status as RiskLevel) || 'moderate',
    status_label: place.status_label || 'Regional Zone',
    last_updated: new Date().toISOString(),
    telemetry_status: 'modelled',
    current_hazard: (place.hazard_type as HazardType) || 'flash_flood',
    risk_score: place.risk_score || 35,
    guidance: place.guidance || `Regional monitoring area for ${place.name}. Exercise caution on stream crossings and valley ghat roads during heavy downpours.`,
    guidance_mr: place.guidance_mr || `${place.name_mr || place.name} परिसर. मुसळधार पावसात नदी-नाल्यांचे प्रवाह व घाटातील सखल रस्त्यांवर सावधगिरी बाळगा.`,
    guidance_hi: place.guidance_hi || `${place.name_hi || place.name} क्षेत्र। भारी बारिश में नदी तट और घाटी मार्गों पर सतर्क रहें।`,
    upstream_info: `${place.region || 'Western Ghats / Maval Belt'}. ${nearestNote}`,
    photo_description: `Regional landscape perspective of ${place.name}.`,
    tags: ['Regional Search', 'Maval Basin', 'Western Ghats']
  };
}

