import React from 'react';
import { SafeImage } from './SafeImage';
import { FEATURE_IMAGES } from '../utils/imageHelpers';
import {
  AlertTriangle, Droplets, CloudRain, Mountain, Clock,
  LifeBuoy, MapPin, PhoneCall, ArrowRight, ShieldCheck, Activity
} from 'lucide-react';
import { Language } from '../translations';

interface FeatureIntelligenceGridProps {
  onNavigate: (tab: string) => void;
  lang: Language;
}

interface FeatureCardItem {
  id: string;
  titleEn: string;
  titleMr: string;
  categoryEn: string;
  categoryMr: string;
  descEn: string;
  descMr: string;
  image: string;
  badgeText: string;
  badgeColor: string;
  targetTab: string;
  actionTextEn: string;
  actionTextMr: string;
  icon: React.ReactNode;
}

export const FeatureIntelligenceGrid: React.FC<FeatureIntelligenceGridProps> = ({
  onNavigate,
  lang
}) => {
  const features: FeatureCardItem[] = [
    {
      id: 'landslide',
      titleEn: 'Landslide & Escarpment Monitoring',
      titleMr: 'दरड व कडा घसरण संनियंत्रण',
      categoryEn: 'Geotechnical Physics',
      categoryMr: 'भूभौतिकीय विश्लेषण',
      descEn: 'Continuous monitoring of steep basalt cut slopes along Bhor Ghat. Calculates shear plane detachment risk from 84.5% soil moisture and slope angles up to 46°.',
      descMr: 'बोरघाटातील तीव्र उतारांच्या कड्यांचे निरीक्षण. ८४.५% माती संपृक्तता आणि ४६° पर्यंतच्या उतारांवरील कातळ घसरणीचा धोका मोजला जातो.',
      image: FEATURE_IMAGES.landslide,
      badgeText: '36.5° Basalt Shear Plane',
      badgeColor: '#c2410c',
      targetTab: 'corridors',
      actionTextEn: 'Inspect Slopes & Corridors →',
      actionTextMr: 'उतार व महामार्ग पहा →',
      icon: <AlertTriangle size={15} style={{ color: '#ea580c' }} />
    },
    {
      id: 'flashflood',
      titleEn: 'Flash-Flood & Waterfall Surges',
      titleMr: 'अचानक पूर व धबधबा प्रवाह इशारा',
      categoryEn: 'Catchment Hydrology',
      categoryMr: 'पाणलोट जलविज्ञान',
      descEn: 'Monitors upstream mountain convergence for Bhushi Dam, Kune Falls, and Rajmachi streams. Predicts water surges before runoff reaches tourist areas.',
      descMr: 'भुशी धरण, कुणे आणि राजमाचीच्या वरच्या डोंगररांगांमधील पावसाचे संकलन. खाली पर्यटकांपर्यंत पाणी पोहोचण्याआधीच लाटांची पूर्वसूचना दिली जाते.',
      image: FEATURE_IMAGES.flashflood,
      badgeText: '4.8 km² Catchment Surge Watch',
      badgeColor: '#0284c7',
      targetTab: 'spots',
      actionTextEn: 'Check Tourist Waterfalls →',
      actionTextMr: 'पर्यटक धबधबे तपासा →',
      icon: <Droplets size={15} style={{ color: '#0284c7' }} />
    },
    {
      id: 'weather',
      titleEn: 'Rainfall & Weather Telemetry',
      titleMr: 'पर्जन्यमान व ढग संनियंत्रण',
      categoryEn: 'Open-Meteo & Weather Telemetry',
      categoryMr: 'हवामान व पर्जन्य संनियंत्रण',
      descEn: 'Real-time telemetry tracking heavy convective cloud bands across Maval and Lonavala. 138mm recorded in 24 hours with peak intensity of 24.5 mm/hr.',
      descMr: 'मावळ व लोणावळा घाटमाथ्यावरील अतिवृष्टीचे थेट रडार मोजमाप. २४ तासांत १३८ मिमी पाऊस आणि प्रतितास २४.५ मिमी तीव्रतेची नोंद.',
      image: FEATURE_IMAGES.weather,
      badgeText: '138.0 mm (24h Accumulation)',
      badgeColor: '#0369a1',
      targetTab: 'replay',
      actionTextEn: 'Explore Storm Progression →',
      actionTextMr: 'वादळाची प्रगती पहा →',
      icon: <CloudRain size={15} style={{ color: '#0369a1' }} />
    },
    {
      id: 'terrain',
      titleEn: 'Terrain & Topographic Analysis',
      titleMr: 'भूपृष्ठ व डिजिटल उंची मॉडेल',
      categoryEn: 'SRTM 30m & Copernicus DEM',
      categoryMr: '३० मीटर एसआरटीएम डीईएम',
      descEn: 'High-resolution digital elevation modeling mapping elevation contours (410m to 780m MSL), slope aspects, drainage density, and runoff convergence vectors.',
      descMr: '४१० ते ७८० मीटर उंचीचे सह्याद्रीचे डिजिटल मॉडेल. डोंगरउतार, खोऱ्यांची दिशा आणि पाण्याच्या प्रवाहाचे अचूक नकाशांकन.',
      image: FEATURE_IMAGES.terrain,
      badgeText: '30m Resolution DEM Grid',
      badgeColor: '#2d6a4f',
      targetTab: 'map',
      actionTextEn: 'Open 3D Relief Map →',
      actionTextMr: 'सखोल नकाशा उघडा →',
      icon: <Mountain size={15} style={{ color: '#2d6a4f' }} />
    },
    {
      id: 'incidents',
      titleEn: 'Historical Incidents & Ground Logs',
      titleMr: 'ऐतिहासिक दुर्घटना व प्रत्यक्ष नोंदी',
      categoryEn: 'Sourced Disaster Archives',
      categoryMr: 'प्रमाणित आपत्ती इतिहास',
      descEn: 'Catalog of verified historical landslides, expressway boulder blockages, and the June 2024 Bhushi Dam tragedy with crowdsourced field incident verification.',
      descMr: 'जून २०२४ मधील भुशी धरणातील दुर्दैवी घटना, महामार्गावरील दरड आणि गावठाण भेगांचा प्रमाणित इतिहास व नागरिक नोंदणी कक्ष.',
      image: FEATURE_IMAGES.incidents,
      badgeText: 'Verified Police & DDMA Log',
      badgeColor: '#7c3aed',
      targetTab: 'incidents',
      actionTextEn: 'View Incident Archive →',
      actionTextMr: 'दुर्घटना इतिहास पहा →',
      icon: <Clock size={15} style={{ color: '#7c3aed' }} />
    },
    {
      id: 'safety',
      titleEn: 'Safety Guidelines & Evacuation',
      titleMr: 'सुरक्षा मार्गदर्शक व निवारा केंद्र',
      categoryEn: 'Community Preparedness',
      categoryMr: 'नागरी बचाव मार्गदर्शक',
      descEn: 'Practical geotechnical warning signs (tension cracks, muddy springs) and verified relief shelters including Khandala ZP School and Lonavala Civic Hall.',
      descMr: 'दरड कोसळण्याची पूर्वलक्षणे (जमिनीला भेगा, नवे झरे) ओळखणे आणि लोणावळा-खंडाळा परिसरातील प्रमाणित निवारा केंद्रांची माहिती.',
      image: FEATURE_IMAGES.safety,
      badgeText: '3 Verified Civic Shelters',
      badgeColor: '#15803d',
      targetTab: 'safety',
      actionTextEn: 'Read Safety Rules & Shelters →',
      actionTextMr: 'सुरक्षा नियम व निवारे →',
      icon: <LifeBuoy size={15} style={{ color: '#15803d' }} />
    },
    {
      id: 'spotcheck',
      titleEn: 'Tourist Spot-Check Directory',
      titleMr: 'पर्यटन स्थळ सुरक्षा तपासणी',
      categoryEn: 'Visitor Advisory Matrix',
      categoryMr: 'पर्यटक मार्गदर्शक',
      descEn: 'Interactive safety directory for Tiger Point, Lion’s Point, Bhushi Dam, Kune Falls, and Rajmachi with Section 144 police notices and rain advisories.',
      descMr: 'टायगर पॉईंट, लायन्स पॉईंट, भुशी धरण आणि राजमाची या प्रसिद्ध पर्यटन स्थळांचे सध्याचे नियम, पोलीस निर्बंध व सुरक्षा सूचना.',
      image: '/images/locations/tiger_point.jpg',
      badgeText: '5 Major Tourist Hubs',
      badgeColor: '#d97706',
      targetTab: 'spots',
      actionTextEn: 'Spot-Check Locations →',
      actionTextMr: 'स्थळनिहाय सुरक्षा तपासा →',
      icon: <MapPin size={15} style={{ color: '#d97706' }} />
    },
    {
      id: 'rescue',
      titleEn: 'Emergency Resources & First Responders',
      titleMr: 'आपत्कालीन प्रतिसाद व मदत दल',
      categoryEn: '24x7 Coordinated Response',
      categoryMr: '२४ तास मदत यंत्रणा',
      descEn: 'Direct integration with Pune District Disaster Control (1077), Lonavala City Police (02114-273033), Highway Safety Patrol, and regional NDRF teams.',
      descMr: 'पुणे जिल्हा आपत्ती नियंत्रण कक्ष (१०७७), लोणावळा पोलीस ठाणे (०२११४-२७३०३३) आणि महामार्ग सुरक्षा पथकांचे थेट संपर्क क्रमांक.',
      image: FEATURE_IMAGES.rescue,
      badgeText: 'Helpline: 1077 / 112',
      badgeColor: '#b91c1c',
      targetTab: 'safety',
      actionTextEn: 'Call Official Helplines →',
      actionTextMr: 'मदत कक्ष संपर्क पहा →',
      icon: <PhoneCall size={15} style={{ color: '#b91c1c' }} />
    }
  ];

  return (
    <section className="feature-intelligence-section" aria-label="Geospatial Intelligence Features">
      {/* Section Header */}
      <div style={{ marginBottom: '1rem', borderBottom: '2px solid var(--border-subtle)', paddingBottom: '0.65rem' }}>
        <div style={{
          display: 'inline-flex',
          alignItems: 'center',
          gap: '6px',
          background: 'var(--accent-green-light)',
          color: 'var(--accent-green-dark)',
          border: '1px solid var(--accent-green)',
          borderRadius: 'var(--radius-full)',
          padding: '2px 10px',
          fontSize: '0.72rem',
          fontWeight: 700,
          marginBottom: '4px'
        }}>
          <Activity size={13} />
          <span>{lang === 'mr' ? 'हायपरलोकल एआय वैशिष्ट्ये व संनियंत्रण' : 'Hyperlocal AI Features & Environmental Monitoring'}</span>
        </div>
        <h2 style={{ fontSize: '1.35rem', fontWeight: 800, color: 'var(--text-main)', letterSpacing: '-0.01em' }}>
          {lang === 'mr' ? 'आपत्ती पूर्वसूचना व भूपृष्ठ विश्लेषण प्रणाली' : 'Comprehensive Hazard Intelligence Modules'}
        </h2>
        <p style={{ fontSize: '0.84rem', color: 'var(--text-muted)', marginTop: '2px' }}>
          {lang === 'mr'
            ? 'प्रत्येक मोड्युलमध्ये सत्य छायाचित्रे, शास्त्रीय भूपृष्ठ विश्लेषण आणि उपयुक्त कृती तत्काळ उपलब्ध आहेत.'
            : 'Each feature pairs authentic Western Ghats visual imagery with uncalibrated geotechnical metrics and actionable emergency tools.'}
        </p>
      </div>

      {/* Grid of 8 Distinct Feature Cards */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))',
        gap: '1.15rem'
      }}>
        {features.map((feat) => {
          const title = lang === 'mr' ? feat.titleMr : feat.titleEn;
          const category = lang === 'mr' ? feat.categoryMr : feat.categoryEn;
          const desc = lang === 'mr' ? feat.descMr : feat.descEn;
          const actionText = lang === 'mr' ? feat.actionTextMr : feat.actionTextEn;

          return (
            <div
              key={feat.id}
              className="feature-card"
              onClick={() => onNavigate(feat.targetTab)}
              style={{
                background: '#ffffff',
                border: '1px solid var(--border-subtle)',
                borderRadius: 'var(--radius-md)',
                overflow: 'hidden',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between',
                boxShadow: 'var(--shadow-xs)',
                cursor: 'pointer',
                transition: 'transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform = 'translateY(-3px)';
                e.currentTarget.style.boxShadow = 'var(--shadow-md)';
                e.currentTarget.style.borderColor = 'var(--accent-yellow)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = 'none';
                e.currentTarget.style.boxShadow = 'var(--shadow-xs)';
                e.currentTarget.style.borderColor = 'var(--border-subtle)';
              }}
            >
              {/* Feature Visual Thumbnail Frame */}
              <div style={{
                position: 'relative',
                width: '100%',
                height: '145px',
                background: '#f1f5f9',
                overflow: 'hidden'
              }}>
                <SafeImage
                  src={feat.image}
                  alt={feat.titleEn}
                  badge={category}
                />

                {/* Status Pill on Top */}
                <span style={{
                  position: 'absolute',
                  top: '8px',
                  right: '8px',
                  background: 'rgba(255, 255, 255, 0.95)',
                  backdropFilter: 'blur(4px)',
                  color: feat.badgeColor,
                  border: `1px solid ${feat.badgeColor}40`,
                  fontSize: '0.68rem',
                  fontWeight: 700,
                  padding: '2px 8px',
                  borderRadius: 'var(--radius-full)',
                  boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
                }}>
                  {feat.badgeText}
                </span>
              </div>

              {/* Feature Content */}
              <div style={{ padding: '0.9rem', display: 'flex', flexDirection: 'column', flex: 1, justifyContent: 'space-between' }}>
                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '4px' }}>
                    {feat.icon}
                    <h3 style={{ fontSize: '0.96rem', fontWeight: 800, color: 'var(--text-main)', lineHeight: 1.3 }}>
                      {title}
                    </h3>
                  </div>

                  <p style={{
                    fontSize: '0.78rem',
                    color: '#475569',
                    lineHeight: 1.45,
                    display: '-webkit-box',
                    WebkitLineClamp: 3,
                    WebkitBoxOrient: 'vertical',
                    overflow: 'hidden',
                    marginTop: '4px'
                  }}>
                    {desc}
                  </p>
                </div>

                {/* Action Link Row */}
                <div style={{
                  marginTop: '0.75rem',
                  borderTop: '1px solid var(--border-subtle)',
                  paddingTop: '0.5rem',
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  fontSize: '0.76rem',
                  fontWeight: 700,
                  color: 'var(--accent-green-dark)'
                }}>
                  <span>{actionText}</span>
                  <ArrowRight size={13} />
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
};

export default FeatureIntelligenceGrid;

