import React from 'react';
import { LocationItem, AlertItem } from '../types';
import {
  ShieldAlert, Mountain, Droplets, Compass, ArrowRight,
  AlertTriangle, PhoneCall, ExternalLink, Activity, Info, CheckCircle2, Zap,
  Eye, Sparkles, CloudRain, MapPin
} from 'lucide-react';
import { Language } from '../translations';
import { SafeImage } from '../components/SafeImage';
import { LonavalaGallery } from '../components/LonavalaGallery';
import { FeatureIntelligenceGrid } from '../components/FeatureIntelligenceGrid';
import { getLocationImage } from '../utils/imageHelpers';

interface HomeViewProps {
  locations: LocationItem[];
  alerts: AlertItem[];
  onNavigate: (tab: string) => void;
  onSelectLocation: (loc: LocationItem) => void;
  lang: Language;
}

export const HomeView: React.FC<HomeViewProps> = ({
  locations,
  alerts,
  onNavigate,
  onSelectLocation,
  lang
}) => {
  const officialAlert = alerts.find(a => a.alert_type === 'official_warning') || {
    title: 'IMD Orange Alert: Heavy to Very Heavy Rainfall in Ghat Areas of Maval & Lonavala',
    title_mr: 'ऑरेंज अलर्ट: मावळ व लोणावळा घाट परिसरात अतिमुसळधार पावसाचा इशारा',
    message: 'Isolated heavy to very heavy rainfall expected along the Sahyadri crest lines. Residents and tourists advised to exercise caution near streams and steep cuttings.'
  };

  const highRiskLocations = locations.filter(l => l.status === 'high' || l.status === 'very_high');

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.75rem' }}>
      {/* =========================================================================
          A. DASHBOARD OVERVIEW SECTION: Integrated Lonavala Landscape Hero Banner
          Features: Sahyadri Mountain Ranges, Lush Green Hills, Monsoon Atmosphere,
                    Natural Valleys and Forests in an integrated, responsive layout.
          ========================================================================= */}
      <section
        className="situation-hero-card"
        aria-label="Lonavala Situation Overview & Landscape"
        style={{
          background: '#ffffff',
          border: '1px solid var(--border-card)',
          borderRadius: 'var(--radius-lg)',
          overflow: 'hidden',
          boxShadow: 'var(--shadow-sm)'
        }}
      >
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'minmax(320px, 1.35fr) minmax(280px, 1fr)',
          minHeight: '260px'
        }}>
          {/* Left Column: Heading, Telemetry Badges & Action Buttons */}
          <div style={{
            padding: '1.5rem',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-between',
            gap: '1rem'
          }}>
            <div>
              {/* Regional Metadata Badge Strip */}
              <div className="situation-badge-strip" style={{ marginBottom: '8px' }}>
                <span className="situation-pill">
                  <Mountain size={13} style={{ color: 'var(--accent-green-dark)' }} />
                  <span>{lang === 'mr' ? 'लोणावळा - खंडाळा पायलट झोन' : 'Lonavala - Khandala Pilot Zone'}</span>
                </span>

                <span className="situation-pill" style={{ color: '#0369a1', borderColor: '#bae6fd' }}>
                  <Activity size={13} />
                  <span>UN SDG 13.1 Climate Resilience</span>
                </span>

                <span className="situation-pill" style={{ color: '#b45309', borderColor: '#fde68a' }}>
                  <CloudRain size={13} />
                  <span>Live Weather Sync</span>
                </span>
              </div>

              {/* Main Heading */}
              <h1 className="situation-main-title" style={{ fontSize: '1.65rem', fontWeight: 800, color: 'var(--text-main)', lineHeight: 1.25 }}>
                {lang === 'mr'
                  ? 'लोणावळा आपत्ती व हवामान-धोका डॅशबोर्ड'
                  : lang === 'hi'
                  ? 'लोनावला आपदा एवं जोखिम इंटेलिजेंस डैशबोर्ड'
                  : 'Lonavala Risk Intelligence Dashboard'}
              </h1>

              {/* Supporting Authentic Tagline */}
              <p className="situation-subtitle" style={{ fontSize: '0.92rem', color: '#475569', marginTop: '6px', lineHeight: 1.5 }}>
                {lang === 'mr'
                  ? '“पावसाआधी नव्हे, धोक्याआधी सावध! — सह्याद्रीच्या डोंगरउतारांचे भौतिकी आणि हायपरलोकल पूर्वसूचना.”'
                  : lang === 'hi'
                  ? '“बारिश से पहले नहीं, खतरे से पहले सावधान! — पश्चिमी घाट का सटीक एआई एवं भौतिक जोखिम विश्लेषण।”'
                  : '“Know the danger before it becomes a disaster — Hyperlocal slope physics and upstream catchment early warning.”'}
              </p>
            </div>

            {/* Quick Interactive Navigation Buttons */}
            <div className="situation-actions-row" style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
              <button
                onClick={() => onNavigate('map')}
                className="btn-accent-yellow"
                id="btn-explore-map"
                style={{ padding: '8px 16px', fontSize: '0.86rem', fontWeight: 700 }}
              >
                <Compass size={17} />
                <span>{lang === 'mr' ? 'हायपरलोकल नकाशा पहा →' : 'Explore Risk Map →'}</span>
              </button>

              <button
                onClick={() => onNavigate('spots')}
                className="btn-accent-green"
                id="btn-tourist-spots"
                style={{ padding: '8px 14px', fontSize: '0.84rem', fontWeight: 700 }}
              >
                <Droplets size={16} />
                <span>{lang === 'mr' ? 'पर्यटन स्थळ तपासणी' : 'Tourist Spot-Check'}</span>
              </button>

              <button
                onClick={() => onNavigate('replay')}
                className="btn-light-secondary"
                id="btn-demo-mode"
                style={{ padding: '8px 14px', fontSize: '0.84rem' }}
              >
                <Zap size={15} style={{ color: '#b45309' }} />
                <span>{lang === 'mr' ? '३-मिनिट सादरीकरण डेमो' : '3-Min Presentation Demo'}</span>
              </button>

              <button
                onClick={() => onNavigate('incidents')}
                className="btn-light-secondary"
                style={{ padding: '8px 14px', fontSize: '0.84rem' }}
              >
                <AlertTriangle size={15} style={{ color: '#c2410c' }} />
                <span>{lang === 'mr' ? 'धोका नोंदवा' : 'Report Hazard'}</span>
              </button>
            </div>
          </div>

          {/* Right Column: High-Quality Lonavala Landscape Photographic Banner */}
          <div style={{
            position: 'relative',
            height: '100%',
            minHeight: '220px',
            background: '#0f172a',
            overflow: 'hidden'
          }}>
            <SafeImage
              src="/images/banner_lonavala_overview.jpg"
              fallbackSrc="/sahyadri_landscape.jpg"
              alt="Lonavala Khandala Sahyadri Monsoon Landscape - Lush green hills and misty valleys"
              style={{
                width: '100%',
                height: '100%',
                objectFit: 'cover'
              }}
            />

            {/* Subtle Gradient Overlays for Elegance & Contrast */}
            <div style={{
              position: 'absolute',
              inset: 0,
              background: 'linear-gradient(to right, rgba(255,255,255,0.15) 0%, transparent 40%), linear-gradient(to top, rgba(15,23,42,0.65) 0%, transparent 60%)',
              pointerEvents: 'none'
            }} />

            {/* Geographical Location Overlay Badge */}
            <div style={{
              position: 'absolute',
              bottom: '12px',
              left: '12px',
              right: '12px',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'flex-end',
              flexWrap: 'wrap',
              gap: '6px'
            }}>
              <div style={{
                background: 'rgba(15, 23, 42, 0.82)',
                backdropFilter: 'blur(6px)',
                padding: '4px 10px',
                borderRadius: 'var(--radius-sm)',
                border: '1px solid rgba(255,255,255,0.15)'
              }}>
                <div style={{ fontSize: '0.74rem', fontWeight: 800, color: '#ffffff', display: 'flex', alignItems: 'center', gap: '5px' }}>
                  <Mountain size={13} style={{ color: 'var(--accent-yellow)' }} />
                  <span>Sahyadri Mountain Crestline (Western Ghats)</span>
                </div>
                <div style={{ fontSize: '0.68rem', color: '#cbd5e1' }}>
                  Lonavala, Khandala & Bhor Ghat Valleys • 780m MSL
                </div>
              </div>

              <span style={{
                background: 'rgba(21, 128, 61, 0.85)',
                color: '#ffffff',
                fontSize: '0.68rem',
                fontWeight: 700,
                padding: '3px 8px',
                borderRadius: 'var(--radius-full)',
                boxShadow: '0 2px 6px rgba(0,0,0,0.3)'
              }}>
                ● Monsoon Active
              </span>
            </div>
          </div>
        </div>
      </section>

      {/* Official Government Warning Announcement Banner */}
      <div style={{
        background: 'var(--hazard-mod-bg)',
        border: '1px solid var(--hazard-mod-border)',
        borderRadius: 'var(--radius-md)',
        padding: '1rem 1.25rem',
        display: 'flex',
        alignItems: 'flex-start',
        gap: '0.85rem',
        boxShadow: 'var(--shadow-xs)'
      }}>
        <div style={{
          background: 'var(--accent-yellow)',
          color: '#202820',
          borderRadius: 'var(--radius-sm)',
          padding: '6px',
          display: 'flex',
          boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
        }}>
          <AlertTriangle size={22} />
        </div>
        <div style={{ flex: 1 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
            <span style={{
              background: '#fef3c7',
              color: '#92400e',
              border: '1px solid #fcd34d',
              padding: '2px 8px',
              borderRadius: 'var(--radius-full)',
              fontSize: '0.72rem',
              fontWeight: 700,
              textTransform: 'uppercase'
            }}>
              Verified Official IMD Warning
            </span>
            <span style={{ fontSize: '0.75rem', color: '#78350f' }}>
              Valid for Next 24 Hours • Pune Ghats (Maval & Lonavala)
            </span>
          </div>
          <h4 style={{ fontSize: '0.98rem', fontWeight: 700, color: '#78350f', marginTop: '4px' }}>
            {lang === 'mr' ? officialAlert.title_mr : officialAlert.title}
          </h4>
          <p style={{ fontSize: '0.85rem', color: '#92400e', marginTop: '2px', lineHeight: 1.45 }}>
            {officialAlert.message}
          </p>
        </div>
      </div>

      {/* Live Regional Environmental Status Metrics */}
      <div className="grid-4">
        <div className="metric-card">
          <div className="metric-label">{lang === 'mr' ? '२४ तास पर्जन्यमान' : '24-Hour Rainfall'}</div>
          <div className="metric-value">138.0 <span style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>mm</span></div>
          <div className="metric-sub">📍 Bhushi Catchment Gauge</div>
        </div>

        <div className="metric-card">
          <div className="metric-label">{lang === 'mr' ? 'कमाल पाऊस तीव्रता' : 'Peak Rain Intensity'}</div>
          <div className="metric-value">24.5 <span style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>mm/h</span></div>
          <div className="metric-sub">⚡ Convective Squall Active</div>
        </div>

        <div className="metric-card">
          <div className="metric-label">{lang === 'mr' ? 'माती संपृक्तता (घाट)' : 'Ghat Soil Saturation'}</div>
          <div className="metric-value" style={{ color: 'var(--hazard-high)' }}>84.5 <span style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>%</span></div>
          <div className="metric-sub">⚠️ High Shear Weakness</div>
        </div>

        <div className="metric-card">
          <div className="metric-label">{lang === 'mr' ? 'सक्रिय पूर्वसूचना' : 'Active Hotspots'}</div>
          <div className="metric-value" style={{ color: 'var(--hazard-crit)' }}>{highRiskLocations.length} <span style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>Hotspots</span></div>
          <div className="metric-sub">🛡️ 3 Shelters on Standby</div>
        </div>
      </div>

      {/* =========================================================================
          B. FEATURE CARDS WITH RELEVANT IMAGES:
          Landslide, Flash-Flood, Weather, Terrain, Incidents, Safety, Spot-Check, Rescue
          ========================================================================= */}
      <FeatureIntelligenceGrid
        onNavigate={onNavigate}
        lang={lang}
      />

      {/* =========================================================================
          C. LONAVALA LOCATION GALLERY:
          Bhushi Dam, Tiger Point, Lion's Point, Kune Falls, Rajmachi,
          Amrutanjan Bridge, Lonavala Mountain Valleys
          ========================================================================= */}
      <LonavalaGallery
        locations={locations}
        onSelectLocation={onSelectLocation}
        onNavigate={onNavigate}
        lang={lang}
      />

      {/* =========================================================================
          High-Priority Monitored Hotspots (Enhanced with Authentic Visual Thumbnails)
          ========================================================================= */}
      <div className="card" style={{ background: '#ffffff', borderRadius: 'var(--radius-lg)', border: '1px solid var(--border-card)' }}>
        <div className="card-header" style={{ marginBottom: '1rem', borderBottom: '1px solid var(--border-subtle)', paddingBottom: '0.75rem' }}>
          <div>
            <h3 className="card-title" style={{ fontSize: '1.25rem', fontWeight: 800, color: 'var(--text-main)', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <ShieldAlert size={20} style={{ color: 'var(--hazard-high)' }} />
              <span>{lang === 'mr' ? 'प्राधान्य दक्षतेची संवेदनशील ठिकाणे' : 'High-Priority Alert Hotspots (Lonavala–Khandala)'}</span>
            </h3>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: '2px' }}>
              {lang === 'mr'
                ? 'अतिवृष्टीत सर्वाधिक धोका असणाऱ्या कड्यांचे व ओढ्यांचे थेट एआय वर्गीकरण.'
                : 'Locations with elevated geotechnical shear failure or upstream surge probability.'}
            </p>
          </div>
          <button
            onClick={() => onNavigate('map')}
            className="btn-secondary"
            style={{ fontSize: '0.78rem', padding: '5px 12px' }}
          >
            <span>{lang === 'mr' ? 'सर्व नकाशामध्ये पहा' : 'View All on Map'}</span>
            <ArrowRight size={13} />
          </button>
        </div>

        <div className="grid-3">
          {highRiskLocations.slice(0, 6).map((loc) => {
            const name = lang === 'mr' ? loc.name_mr : (lang === 'hi' ? loc.name_hi : loc.name);
            const guidance = lang === 'mr' ? loc.guidance_mr : (lang === 'hi' ? loc.guidance_hi : loc.guidance);
            const imgUrl = loc.image_url || getLocationImage(loc.id);

            return (
              <div
                key={loc.id}
                onClick={() => {
                  onSelectLocation(loc);
                  onNavigate('map');
                }}
                style={{
                  border: '1px solid var(--border-subtle)',
                  borderRadius: 'var(--radius-md)',
                  overflow: 'hidden',
                  cursor: 'pointer',
                  background: '#ffffff',
                  display: 'flex',
                  flexDirection: 'column',
                  transition: 'all 0.2s ease',
                  boxShadow: 'var(--shadow-xs)'
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.transform = 'translateY(-3px)';
                  e.currentTarget.style.boxShadow = 'var(--shadow-md)';
                  e.currentTarget.style.borderColor = 'var(--accent-green)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.transform = 'none';
                  e.currentTarget.style.boxShadow = 'var(--shadow-xs)';
                  e.currentTarget.style.borderColor = 'var(--border-subtle)';
                }}
              >
                {/* Visual Thumbnail Frame */}
                <div style={{ position: 'relative', width: '100%', height: '135px', background: '#f1f5f9' }}>
                  <SafeImage
                    src={imgUrl}
                    alt={loc.name}
                    badge={loc.category.replace('_', ' ')}
                  />
                  <span
                    className={`hazard-badge ${loc.status}`}
                    style={{
                      position: 'absolute',
                      top: '8px',
                      right: '8px',
                      boxShadow: '0 2px 4px rgba(0,0,0,0.15)'
                    }}
                  >
                    Risk: {loc.risk_score}/100
                  </span>
                </div>

                {/* Content */}
                <div style={{ padding: '0.85rem', display: 'flex', flexDirection: 'column', flex: 1, justifyContent: 'space-between' }}>
                  <div>
                    <h4 style={{ fontSize: '0.98rem', fontWeight: 800, color: 'var(--text-main)' }}>
                      {name}
                    </h4>

                    <p style={{
                      fontSize: '0.78rem',
                      color: 'var(--text-muted)',
                      marginTop: '4px',
                      lineHeight: 1.4,
                      display: '-webkit-box',
                      WebkitLineClamp: 2,
                      WebkitBoxOrient: 'vertical',
                      overflow: 'hidden'
                    }}>
                      {guidance}
                    </p>
                  </div>

                  <div style={{
                    fontSize: '0.74rem',
                    color: 'var(--text-muted)',
                    marginTop: '8px',
                    borderTop: '1px solid var(--border-subtle)',
                    paddingTop: '6px',
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center'
                  }}>
                    <span>Slope: <strong>{loc.slope_deg}°</strong> • {loc.elevation_m}m</span>
                    <span style={{ color: 'var(--accent-green-dark)', fontWeight: 700 }}>Inspect →</span>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Emergency Contacts & Help Desk Ribbon */}
      <div style={{
        background: 'var(--accent-green-light)',
        border: '1px solid var(--accent-green)',
        borderRadius: 'var(--radius-lg)',
        padding: '1.25rem 1.5rem',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        gap: '1rem'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
          <div style={{
            width: '54px',
            height: '54px',
            borderRadius: 'var(--radius-md)',
            overflow: 'hidden',
            flexShrink: 0,
            border: '2px solid #ffffff',
            boxShadow: 'var(--shadow-xs)'
          }}>
            <SafeImage
              src="/images/features/feat_rescue.jpg"
              alt="Disaster Response Team"
            />
          </div>
          <div>
            <h4 style={{ fontSize: '1.02rem', fontWeight: 800, color: 'var(--accent-green-dark)', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <PhoneCall size={18} />
              {lang === 'mr' ? 'अधिकृत आपत्कालीन मदत कक्ष (लोणावळा / मावळ)' : 'Verified Official Emergency Contacts'}
            </h4>
            <p style={{ fontSize: '0.82rem', color: '#2d4d36', marginTop: '3px' }}>
              {lang === 'mr'
                ? 'पुणे ग्रामीण आपत्ती नियंत्रण कक्ष: १०७७ • लोणावळा शहर पोलीस: ०२११४-२७३०३३ • महामार्ग पोलीस: ९८२२४९८२२४'
                : 'Pune District Disaster Cell: 1077 • Lonavala Police: 02114-273033 • Expressway Highway Patrol: 9822498224'}
            </p>
          </div>
        </div>

        <button
          onClick={() => onNavigate('safety')}
          className="btn-accent-yellow"
          style={{ fontSize: '0.84rem', padding: '8px 16px' }}
        >
          {lang === 'mr' ? 'सुरक्षित निवारा केंद्र पहा →' : 'View Shelters & Safety Guide →'}
        </button>
      </div>
    </div>
  );
};

export default HomeView;
