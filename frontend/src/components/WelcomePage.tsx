import React from 'react';
import { Mountain, Compass, Shield, ArrowRight, Droplets, Activity, Globe, Zap, AlertTriangle } from 'lucide-react';
import { Language, TRANSLATIONS } from '../translations';

interface WelcomePageProps {
  onExplore: () => void;
  lang: Language;
  onLanguageChange: (lang: Language) => void;
  rainfall24h?: number;
  alertCount?: number;
}

export const WelcomePage: React.FC<WelcomePageProps> = ({
  onExplore,
  lang,
  onLanguageChange,
  rainfall24h = 138.0,
  alertCount = 3
}) => {
  const t = TRANSLATIONS[lang];

  return (
    <div className="welcome-screen">
      {/* Cinematic Sahyadri Landscape Background with Layered Depth */}
      <div className="welcome-backdrop">
        <img
          src="/sahyadri_landscape.jpg"
          alt="Sahyadri Lonavala Khandala Landscape"
          className="welcome-bg-image"
        />
        {/* Subtle Ethereal Drifting Mist Layer */}
        <div className="welcome-mist-layer" />
        {/* Atmospheric Gradient for Crystal Clear Legibility */}
        <div className="welcome-overlay-scrim" />
      </div>

      {/* Floating Header */}
      <header className="welcome-header">
        <div className="welcome-header-inner">
          <div className="welcome-badge-cluster">
            <span className="welcome-geo-pill">
              <Mountain size={14} className="welcome-pill-icon" />
              <span>{lang === 'mr' ? 'सह्याद्री पर्वतमाला • लोणावळा-खंडाळा पायलट' : 'Sahyadri Range • Lonavala-Khandala Pilot'}</span>
            </span>

            <span className="welcome-status-pill">
              <span className="welcome-live-dot" />
              <span>{lang === 'mr' ? 'थेट सेन्सर व आयएमडी डेटा सक्रिय' : 'IMD Telemetry Synced'}</span>
            </span>
          </div>

          {/* Language Switcher */}
          <div className="welcome-lang-switcher" role="radiogroup" aria-label="Language selection">
            <button
              onClick={() => onLanguageChange('mr')}
              className={`welcome-lang-btn ${lang === 'mr' ? 'active' : ''}`}
              title="मराठी मध्ये पहा"
            >
              मराठी
            </button>
            <button
              onClick={() => onLanguageChange('en')}
              className={`welcome-lang-btn ${lang === 'en' ? 'active' : ''}`}
              title="Switch to English"
            >
              English
            </button>
            <button
              onClick={() => onLanguageChange('hi')}
              className={`welcome-lang-btn ${lang === 'hi' ? 'active' : ''}`}
              title="हिंदी में देखें"
            >
              हिंदी
            </button>
          </div>
        </div>
      </header>

      {/* Hero Centerpiece */}
      <main className="welcome-main">
        <div className="welcome-centerpiece">
          {/* Subtle Project Category Pill */}
          <div className="welcome-category-tag">
            <Shield size={14} style={{ color: '#F4D35E' }} />
            <span>AI-POWERED DISASTER INTELLIGENCE PLATFORM</span>
          </div>

          {/* 1. Prominent Marathi Brand Name: सह्यादृष्टी */}
          <h1 className="welcome-marathi-title" lang="mr">
            सह्यादृष्टी
          </h1>

          {/* 2. English Sub-brand: SAHYADRUSHTI AI */}
          <div className="welcome-subbrand">
            SAHYADRUSHTI AI
          </div>

          {/* 3. Authentic Tagline: “पावसाआधी नव्हे, धोक्याआधी सावध!” */}
          <p className="welcome-tagline">
            {lang === 'mr'
              ? '“पावसाआधी नव्हे, धोक्याआधी सावध!”'
              : lang === 'hi'
              ? '“बारिश से पहले नहीं, खतरे से पहले सावधान!”'
              : '“Know the risk before the slope or stream turns dangerous.”'}
          </p>

          {/* Concise Supporting Description */}
          <p className="welcome-description">
            {lang === 'mr'
              ? 'लोणावळा, खंडाळा आणि बोरघाट परिसरासाठी हायपरलोकल दरड व अचानक पूर पूर्वसूचना प्रणाली. स्थानिक भूपृष्ठ उतार, पाणलोट क्षेत्र आणि रिअल-टाइम पर्जन्यमानाचे भौतिक एआय विश्लेषण.'
              : 'Hyperlocal landslide & flash-flood risk monitoring platform for Lonavala, Khandala, and the surrounding Western Ghats. Physics-grounded terrain hydrology and AI decision-support for citizen safety and municipal resilience.'}
          </p>

          {/* Core Feature Badges */}
          <div className="welcome-features-strip">
            <div className="welcome-feature-item">
              <Mountain size={16} style={{ color: '#A8D5A2' }} />
              <span>30m SRTM DEM Slope Physics</span>
            </div>
            <div className="welcome-feature-item">
              <Droplets size={16} style={{ color: '#F4D35E' }} />
              <span>Upstream Catchment Hydrology</span>
            </div>
            <div className="welcome-feature-item">
              <Activity size={16} style={{ color: '#A8D5A2' }} />
              <span>Real-Time Hazard Early Warning</span>
            </div>
          </div>

          {/* 4. Prominent Start Button: Explore Dashboard → */}
          <div className="welcome-cta-container">
            <button
              onClick={onExplore}
              className="welcome-explore-btn"
              id="btn-explore-dashboard"
              aria-label="Explore Lonavala Risk Dashboard"
            >
              <span>{lang === 'mr' ? 'डॅशबोर्ड उघडा' : 'Explore Dashboard'}</span>
              <ArrowRight size={20} className="welcome-arrow-icon" />
            </button>

            <div className="welcome-quick-telemetry">
              <span>📍 Lonavala: <strong>{rainfall24h} mm</strong> (24h Rain)</span>
              <span className="welcome-separator">•</span>
              <span>⚠️ <strong>{alertCount}</strong> {lang === 'mr' ? 'सक्रिय पूर्वसूचना' : 'Active Hotspots'}</span>
            </div>
          </div>
        </div>
      </main>

      {/* Discreet Footer */}
      <footer className="welcome-footer">
        <div className="welcome-footer-inner">
          <div className="welcome-sdg-label">
            <Globe size={13} style={{ color: '#A8D5A2' }} />
            <span>Aligned with UN SDG 13.1 Climate Resilience & National Disaster Management Guidelines</span>
          </div>
          <div className="welcome-pilot-meta">
            Pilot Geography: Lonavala Municipal Council • Bhor Ghat Expressway • Khandala Crestline
          </div>
        </div>
      </footer>
    </div>
  );
};

export default WelcomePage;
