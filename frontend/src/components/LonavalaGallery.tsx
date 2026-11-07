import React, { useState } from 'react';
import { LocationItem } from '../types';
import { SafeImage } from './SafeImage';
import { getLocationImage } from '../utils/imageHelpers';
import {
  MapPin, Compass, Mountain, Droplets, AlertTriangle,
  ArrowRight, ShieldCheck, Eye, Sparkles, Filter
} from 'lucide-react';
import { Language } from '../translations';

interface LonavalaGalleryProps {
  locations: LocationItem[];
  onSelectLocation: (loc: LocationItem) => void;
  onNavigate: (tab: string) => void;
  lang: Language;
}

interface GalleryItemDef {
  keyId: string;
  matchedId: string;
  nameEn: string;
  nameMr: string;
  nameHi: string;
  subtitleEn: string;
  subtitleMr: string;
  descEn: string;
  descMr: string;
  image: string;
  categoryTag: string;
  slope: number;
  elevation: number;
  riskScore: number;
  riskStatus: 'low' | 'moderate' | 'high' | 'very_high';
}

export const LonavalaGallery: React.FC<LonavalaGalleryProps> = ({
  locations,
  onSelectLocation,
  onNavigate,
  lang
}) => {
  const [selectedFilter, setSelectedFilter] = useState<'all' | 'water' | 'cliffs' | 'corridors'>('all');

  // Explicitly curating the 7 required Lonavala locations with authentic attributes
  const galleryItems: GalleryItemDef[] = [
    {
      keyId: 'bhushi_dam',
      matchedId: 'bhushi_dam',
      nameEn: 'Bhushi Dam & Waterfall Rapids',
      nameMr: 'भुशी धरण व पायऱ्यांचा धबधबा',
      nameHi: 'भुशी बांध और झरना',
      subtitleEn: '4.8 km² Tiger Valley Upstream Catchment',
      subtitleMr: 'टायगर व्हॅली ४.८ चौ.किमी वरचा पाणलोट',
      descEn: 'Iconic masonry weir overflow where sudden torrential runoff from Tiger Hill causes rapid water level surges across cascading steps within 10 minutes.',
      descMr: 'मुसळधार पावसात टायगर व्हॅलीतून येणाऱ्या पाण्यामुळे पायऱ्यांवर अत्यंत वेगाने पाण्याच्या लाटा येतात. पर्यटकांना पाण्यात न उतरण्याचा इशारा.',
      image: '/images/locations/bhushi_dam.jpg',
      categoryTag: 'Water Surge Hotspot',
      slope: 24.5,
      elevation: 638,
      riskScore: 74,
      riskStatus: 'high'
    },
    {
      keyId: 'tiger_point',
      matchedId: 'tiger_point',
      nameEn: "Tiger's Leap (Waghai) Escarpment",
      nameMr: 'वाघदरी / टायगर पॉईंट कडा',
      nameHi: 'टाइगर पॉइंट कगार',
      subtitleEn: '650m Sheer Cliff Drop to Konkan Valley',
      subtitleMr: 'कोकण दरीकडे ६५० मीटर खोल उभा कडा',
      descEn: 'Sheer vertical basalt precipice experiencing heavy monsoon updrafts, thick dense fog, and severe gust windshear during active squall lines.',
      descMr: 'सह्याद्रीचा ६५० मीटर खोल उभा कडा. जोरदार वारे व दाट धुक्यामुळे कड्याच्या कठड्यावरून तोल जाण्याचा मोठा धोका.',
      image: '/images/locations/tiger_point.jpg',
      categoryTag: 'Sheer Escarpment',
      slope: 46.0,
      elevation: 725,
      riskScore: 71,
      riskStatus: 'high'
    },
    {
      keyId: 'lions_point',
      matchedId: 'lions_point',
      nameEn: "Lion's Point Panoramic Ridge",
      nameMr: 'लायन्स पॉईंट विहंगम डोंगररांग',
      nameHi: 'लायंस पॉइंट पर्वतमाला',
      subtitleEn: 'High Wind Ridge & Valley Watershed',
      subtitleMr: 'दोन दऱ्यांमधील उघडी डोंगररांग',
      descEn: 'Exposed high-altitude viewpoint between Lonavala and Aamby Valley road, vulnerable to surface sheet erosion and unpaved shoulder slippage.',
      descMr: 'उघड्या डोंगरउतारावर मुसळधार पावसामुळे मातीची धूप होते आणि रस्त्यालगत चिखल साचतो. दृश्यमानता कमी असताना सावधगिरी आवश्यक.',
      image: '/images/locations/lions_point.jpg',
      categoryTag: 'Mountain Ridge',
      slope: 41.0,
      elevation: 718,
      riskScore: 48,
      riskStatus: 'moderate'
    },
    {
      keyId: 'kune_falls',
      matchedId: 'kune_falls',
      nameEn: 'Kune Falls & Valley Escarpment',
      nameMr: 'कुणे धबधबा व खंडाळा दरी',
      nameHi: 'कुणे जलप्रपात एवं घाटी',
      subtitleEn: '200m 3-Tiered Basalt Waterfall Cascade',
      subtitleMr: '३ टप्प्यांचा २०० मीटर उंच धबधबा',
      descEn: 'Dramatic multi-tiered waterfall cascading down sheer basalt cliffs near Khandala. High moisture creates treacherous slippery rock surfaces and minor scree drops.',
      descMr: 'खंडाळ्याजवळील २०० मीटर खोल कड्यावरून कोसळणारा धबधबा. सततच्या पाण्यामुळे कातळ अत्यंत निसरडा होतो आणि कडे निसटण्याची भीती असते.',
      image: '/images/locations/kune_falls.jpg',
      categoryTag: 'Waterfall Cascade',
      slope: 38.0,
      elevation: 622,
      riskScore: 52,
      riskStatus: 'moderate'
    },
    {
      keyId: 'rajmachi',
      matchedId: 'rajmachi_route',
      nameEn: 'Rajmachi Fort & Trek Route (Udhewadi)',
      nameMr: 'राजमाची किल्ला व उढेवाडी ट्रेक मार्ग',
      nameHi: 'राजमाची किला व ट्रेक',
      subtitleEn: 'High-Altitude Forest Stream Crossings',
      subtitleMr: 'जंगल मार्ग व चार डोंगरी ओढ्यांचा प्रवाह',
      descEn: 'Ancient Sahyadri mountain bastion accessed via a 15km remote jungle trail crossing 4 swollen seasonal streams with severe mud-track washout risk.',
      descMr: 'जंगल रस्ता चिखलामुळे अत्यंत निसरडा असून डोंगर ओढ्यांना पूर आल्यास पायी वाट वाहून जाण्याची शक्यता असते. रेड अलर्टमध्ये ट्रेकिंग टाळावी.',
      image: '/images/locations/rajmachi.jpg',
      categoryTag: 'Wilderness Trail',
      slope: 32.0,
      elevation: 780,
      riskScore: 88,
      riskStatus: 'very_high'
    },
    {
      keyId: 'amrutanjan_bridge',
      matchedId: 'khandala_expressway',
      nameEn: 'Amrutanjan Bridge / Bhor Ghat Cut Slope',
      nameMr: 'अमृतांजन पूल / बोरघाट द्रुतगती महामार्ग',
      nameHi: 'अमृतांजन ब्रिज / भोर घाट',
      subtitleEn: 'Engineered Basalt Rock Cut & Safety Mesh',
      subtitleMr: 'द्रुतगती मार्गावरील धोकादायक डोंगर कटिंग',
      descEn: 'Critical 6-lane transport artery cut deep into Western Ghats basalt terraces. Overburden saturation exceeding 85% induces risk of rolling boulders onto lanes.',
      descMr: 'मुंबई-पुणे द्रुतगती मार्गाचा सर्वात संवेदनशील घाट खंड. अतिवृष्टीत डोंगरावरील जाळी भेदून मोठे दगड रस्त्यावर येण्याचा गंभीर धोका असतो.',
      image: '/images/locations/amrutanjan_bridge.jpg',
      categoryTag: 'Transit Lifeline',
      slope: 36.5,
      elevation: 585,
      riskScore: 79,
      riskStatus: 'high'
    },
    {
      keyId: 'lonavala_valleys',
      matchedId: 'lonavala_town',
      nameEn: 'Khandala Valleys & Duke’s Nose (Nagphani)',
      nameMr: 'खंडाळा दरी व नागफणी कडा (ड्यूक्स नोज)',
      nameHi: 'खंडाला घाटी एवं ड्यूक्स नोज',
      subtitleEn: 'Natural Sahyadri Catchment & Forest Slopes',
      subtitleMr: 'सह्याद्रीच्या नैसर्गिक दऱ्या व दाट जंगले',
      descEn: 'Breathtaking Sahyadri mountain crestline flanking Khandala and Lonavala. Natural watershed drains massive monsoon volumes westward toward the Konkan plain.',
      descMr: 'लोणावळा-खंडाळ्याच्या कुशीतील विस्तीर्ण दऱ्या आणि पावसाळी ढगांची हिरवीगार चादर. कोकणात उतरणाऱ्या ओढ्यांचे मुख्य उगमस्थान.',
      image: '/images/locations/lonavala_valleys.jpg',
      categoryTag: 'Sahyadri Valleys',
      slope: 30.0,
      elevation: 650,
      riskScore: 35,
      riskStatus: 'low'
    }
  ];

  const filteredItems = galleryItems.filter(item => {
    if (selectedFilter === 'all') return true;
    if (selectedFilter === 'water') return item.keyId === 'bhushi_dam' || item.keyId === 'kune_falls';
    if (selectedFilter === 'cliffs') return item.keyId === 'tiger_point' || item.keyId === 'lions_point' || item.keyId === 'lonavala_valleys';
    if (selectedFilter === 'corridors') return item.keyId === 'amrutanjan_bridge' || item.keyId === 'rajmachi';
    return true;
  });

  const handleCardClick = (item: GalleryItemDef, targetTab: 'map' | 'spots') => {
    // Locate the actual location object from data
    const matched = locations.find(l => l.id === item.matchedId) || locations.find(l => l.id === item.keyId) || locations[0];
    if (matched) {
      onSelectLocation(matched);
    }
    onNavigate(targetTab);
  };

  const getStatusBadgeClass = (status: string) => {
    switch (status) {
      case 'low': return 'status-badge-low';
      case 'moderate': return 'status-badge-mod';
      case 'high': return 'status-badge-high';
      case 'very_high': return 'status-badge-crit';
      default: return 'status-badge-mod';
    }
  };

  return (
    <section className="location-gallery-section" aria-label="Lonavala Location Gallery">
      {/* Section Header */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'flex-end',
        flexWrap: 'wrap',
        gap: '0.75rem',
        marginBottom: '1rem',
        borderBottom: '2px solid var(--border-subtle)',
        paddingBottom: '0.75rem'
      }}>
        <div>
          <div style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '6px',
            background: 'var(--accent-yellow-light)',
            color: '#854d0e',
            border: '1px solid #fde68a',
            borderRadius: 'var(--radius-full)',
            padding: '2px 10px',
            fontSize: '0.72rem',
            fontWeight: 700,
            marginBottom: '4px'
          }}>
            <Sparkles size={13} style={{ color: '#d97706' }} />
            <span>{lang === 'mr' ? 'लोणावळा परिसरातील मुख्य भौगोलिक ठिकाणे' : 'Lonavala Western Ghats Geographic Showcase'}</span>
          </div>
          <h2 style={{ fontSize: '1.35rem', fontWeight: 800, color: 'var(--text-main)', letterSpacing: '-0.01em' }}>
            {lang === 'mr' ? 'लोणावळा-खंडाळा प्रमुख स्थळ गॅलरी व धोका निरीक्षण' : 'Lonavala & Ghats Photographic Location Gallery'}
          </h2>
          <p style={{ fontSize: '0.84rem', color: 'var(--text-muted)', marginTop: '2px' }}>
            {lang === 'mr'
              ? 'पर्यटन, वाहतूक आणि आपत्कालीन तयारीसाठी प्रत्यक्ष सत्य छायाचित्रे आणि एआय धोका विश्लेषण.'
              : 'Authentic high-resolution photographs paired with terrain slope physics, catchment metrics, and live hazard ratings.'}
          </p>
        </div>

        {/* Filter Chips */}
        <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
          <button
            onClick={() => setSelectedFilter('all')}
            className={`btn-secondary ${selectedFilter === 'all' ? 'active-filter' : ''}`}
            style={{
              padding: '4px 10px',
              fontSize: '0.75rem',
              borderRadius: 'var(--radius-full)',
              background: selectedFilter === 'all' ? 'var(--accent-green-dark)' : '#ffffff',
              color: selectedFilter === 'all' ? '#ffffff' : 'var(--text-muted)',
              border: '1px solid var(--border-subtle)'
            }}
          >
            {lang === 'mr' ? 'सर्व स्थळे (७)' : 'All Locations (7)'}
          </button>
          <button
            onClick={() => setSelectedFilter('water')}
            className={`btn-secondary ${selectedFilter === 'water' ? 'active-filter' : ''}`}
            style={{
              padding: '4px 10px',
              fontSize: '0.75rem',
              borderRadius: 'var(--radius-full)',
              background: selectedFilter === 'water' ? '#0284c7' : '#ffffff',
              color: selectedFilter === 'water' ? '#ffffff' : 'var(--text-muted)',
              border: '1px solid var(--border-subtle)'
            }}
          >
            <Droplets size={12} style={{ display: 'inline', marginRight: '3px' }} />
            {lang === 'mr' ? 'धरण व धबधबे' : 'Dams & Falls'}
          </button>
          <button
            onClick={() => setSelectedFilter('cliffs')}
            className={`btn-secondary ${selectedFilter === 'cliffs' ? 'active-filter' : ''}`}
            style={{
              padding: '4px 10px',
              fontSize: '0.75rem',
              borderRadius: 'var(--radius-full)',
              background: selectedFilter === 'cliffs' ? '#d97706' : '#ffffff',
              color: selectedFilter === 'cliffs' ? '#ffffff' : 'var(--text-muted)',
              border: '1px solid var(--border-subtle)'
            }}
          >
            <Mountain size={12} style={{ display: 'inline', marginRight: '3px' }} />
            {lang === 'mr' ? 'उंच कडे व व्ह्यूपॉईंट' : 'Cliffs & Ridges'}
          </button>
          <button
            onClick={() => setSelectedFilter('corridors')}
            className={`btn-secondary ${selectedFilter === 'corridors' ? 'active-filter' : ''}`}
            style={{
              padding: '4px 10px',
              fontSize: '0.75rem',
              borderRadius: 'var(--radius-full)',
              background: selectedFilter === 'corridors' ? '#b91c1c' : '#ffffff',
              color: selectedFilter === 'corridors' ? '#ffffff' : 'var(--text-muted)',
              border: '1px solid var(--border-subtle)'
            }}
          >
            <Compass size={12} style={{ display: 'inline', marginRight: '3px' }} />
            {lang === 'mr' ? 'महामार्ग व ट्रेक' : 'Corridors & Trails'}
          </button>
        </div>
      </div>

      {/* Responsive Location Cards Grid */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))',
        gap: '1.25rem'
      }}>
        {filteredItems.map((item) => {
          const title = lang === 'mr' ? item.nameMr : (lang === 'hi' ? item.nameHi : item.nameEn);
          const subtitle = lang === 'mr' ? item.subtitleMr : item.subtitleEn;
          const description = lang === 'mr' ? item.descMr : item.descEn;

          return (
            <div
              key={item.keyId}
              className="gallery-card"
              style={{
                background: '#ffffff',
                border: '1px solid var(--border-subtle)',
                borderRadius: 'var(--radius-md)',
                overflow: 'hidden',
                display: 'flex',
                flexDirection: 'column',
                boxShadow: 'var(--shadow-xs)',
                transition: 'transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform = 'translateY(-4px)';
                e.currentTarget.style.boxShadow = 'var(--shadow-md)';
                e.currentTarget.style.borderColor = 'var(--accent-green)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = 'none';
                e.currentTarget.style.boxShadow = 'var(--shadow-xs)';
                e.currentTarget.style.borderColor = 'var(--border-subtle)';
              }}
            >
              {/* Image Frame with Aspect Ratio 16:10 */}
              <div style={{
                position: 'relative',
                width: '100%',
                height: '190px',
                background: '#e2e8f0',
                overflow: 'hidden'
              }}>
                <SafeImage
                  src={item.image}
                  alt={item.nameEn}
                  badge={item.categoryTag}
                />

                {/* Subtle gradient overlay at bottom of image for readability */}
                <div style={{
                  position: 'absolute',
                  inset: 0,
                  background: 'linear-gradient(to top, rgba(15, 23, 42, 0.45) 0%, transparent 60%)',
                  pointerEvents: 'none'
                }} />

                {/* Top Right Floating Risk Pill */}
                <div style={{
                  position: 'absolute',
                  top: '10px',
                  right: '10px',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '4px',
                  background: item.riskStatus === 'very_high' ? '#dc2626' : (item.riskStatus === 'high' ? '#ea580c' : (item.riskStatus === 'moderate' ? '#d97706' : '#16a34a')),
                  color: '#ffffff',
                  fontSize: '0.72rem',
                  fontWeight: 800,
                  padding: '3px 9px',
                  borderRadius: 'var(--radius-full)',
                  boxShadow: '0 2px 6px rgba(0,0,0,0.25)'
                }}>
                  <span>Risk: {item.riskScore}/100</span>
                </div>
              </div>

              {/* Card Body */}
              <div style={{ padding: '1rem', display: 'flex', flexDirection: 'column', flex: 1, justifyContent: 'space-between' }}>
                <div>
                  <div style={{
                    fontSize: '0.72rem',
                    color: 'var(--text-muted)',
                    fontWeight: 600,
                    textTransform: 'uppercase',
                    letterSpacing: '0.04em'
                  }}>
                    {subtitle}
                  </div>

                  <h3 style={{
                    fontSize: '1.08rem',
                    fontWeight: 800,
                    color: 'var(--text-main)',
                    marginTop: '2px',
                    lineHeight: 1.3
                  }}>
                    {title}
                  </h3>

                  <p style={{
                    fontSize: '0.82rem',
                    color: '#475569',
                    marginTop: '6px',
                    lineHeight: 1.45,
                    display: '-webkit-box',
                    WebkitLineClamp: 3,
                    WebkitBoxOrient: 'vertical',
                    overflow: 'hidden'
                  }}>
                    {description}
                  </p>

                  {/* Geotechnical Quick Chips */}
                  <div style={{
                    display: 'flex',
                    gap: '6px',
                    flexWrap: 'wrap',
                    marginTop: '10px',
                    fontSize: '0.72rem'
                  }}>
                    <span style={{
                      background: '#f1f5f9',
                      padding: '2px 8px',
                      borderRadius: '4px',
                      color: '#334155',
                      fontWeight: 600
                    }}>
                      Slope: <strong>{item.slope}°</strong>
                    </span>
                    <span style={{
                      background: '#f1f5f9',
                      padding: '2px 8px',
                      borderRadius: '4px',
                      color: '#334155',
                      fontWeight: 600
                    }}>
                      Elevation: <strong>{item.elevation}m</strong>
                    </span>
                    <span style={{
                      background: 'var(--accent-green-light)',
                      padding: '2px 8px',
                      borderRadius: '4px',
                      color: 'var(--accent-green-dark)',
                      fontWeight: 600
                    }}>
                      Verified Sahyadri Spot
                    </span>
                  </div>
                </div>

                {/* Working Action Buttons */}
                <div style={{
                  display: 'flex',
                  gap: '8px',
                  marginTop: '1rem',
                  borderTop: '1px solid var(--border-subtle)',
                  paddingTop: '0.75rem'
                }}>
                  <button
                    onClick={() => handleCardClick(item, 'map')}
                    className="btn-accent-yellow"
                    style={{ flex: 1, padding: '6px 10px', fontSize: '0.78rem', justifyContent: 'center' }}
                    title={lang === 'mr' ? 'नकाशावर पहा' : 'Explore on Interactive Map'}
                  >
                    <MapPin size={13} />
                    <span>{lang === 'mr' ? 'नकाशावर पहा' : 'View on Map'}</span>
                  </button>

                  <button
                    onClick={() => handleCardClick(item, 'spots')}
                    className="btn-secondary"
                    style={{ flex: 1, padding: '6px 10px', fontSize: '0.78rem', justifyContent: 'center' }}
                    title={lang === 'mr' ? 'तपशील तपासा' : 'Inspect Spot Details'}
                  >
                    <Eye size={13} />
                    <span>{lang === 'mr' ? 'सविस्तर तपशील' : 'Spot Details'}</span>
                  </button>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
};

export default LonavalaGallery;

