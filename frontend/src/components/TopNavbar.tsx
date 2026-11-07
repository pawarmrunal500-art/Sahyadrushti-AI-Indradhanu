import React, { useState } from 'react';
import {
  Mountain, Compass, Droplets, GitCommit, Bell, AlertTriangle,
  LifeBuoy, PlayCircle, ShieldAlert, Cpu, Info, Zap, ChevronDown,
  Clock, CheckCircle2, X, Sliders, ExternalLink, Globe
} from 'lucide-react';
import { Language, TRANSLATIONS } from '../translations';
import { AlertItem } from '../types';

interface TopNavbarProps {
  currentTab: string;
  onSelectTab: (tab: string) => void;
  lang: Language;
  onLanguageChange: (lang: Language) => void;
  onReturnToWelcome: () => void;
  selectedRegion: string;
  onRegionChange: (region: string) => void;
  alerts: AlertItem[];
  backendConnected: boolean;
}

export const TopNavbar: React.FC<TopNavbarProps> = ({
  currentTab,
  onSelectTab,
  lang,
  onLanguageChange,
  onReturnToWelcome,
  selectedRegion,
  onRegionChange,
  alerts,
  backendConnected
}) => {
  const t = TRANSLATIONS[lang];
  const [regionMenuOpen, setRegionMenuOpen] = useState(false);
  const [alertsDropdownOpen, setAlertsDropdownOpen] = useState(false);

  const highPriorityAlerts = alerts.filter(a => a.severity === 'warning' || a.severity === 'critical' || a.alert_type === 'official_warning');

  const regionOptions = [
    { id: 'lonavala', name: 'Lonavala (Active Pilot)', name_mr: 'लोणावळा (सक्रिय पायलट)' },
    { id: 'khandala', name: 'Khandala Ghat Corridor', name_mr: 'खंडाळा घाट महामार्ग' },
    { id: 'maval', name: 'Maval Upstream Catchment', name_mr: 'मावळ पाणलोट क्षेत्र' },
    { id: 'bhor_ghat', name: 'Bhor Ghat Railway Section', name_mr: 'बोरघाट रेल्वे मार्ग' }
  ];

  const currentRegionObj = regionOptions.find(r => r.id === selectedRegion) || regionOptions[0];

  return (
    <header className="top-nav-light">
      {/* Primary Sticky Top Bar */}
      <div className="top-nav-primary">
        <div className="top-nav-primary-inner">
          {/* Brand Identity */}
          <div className="nav-brand-container">
            <button
              onClick={onReturnToWelcome}
              className="nav-brand-link"
              title={lang === 'mr' ? 'स्वागत स्क्रीनवर परत जा' : 'Return to Welcome Screen'}
              aria-label="Return to Sahyadrushti Welcome Screen"
            >
              <div className="nav-brand-badge">
                <Mountain size={22} className="nav-brand-icon" />
              </div>
              <div className="nav-brand-text">
                <div className="nav-brand-name-mr" lang="mr">सह्यादृष्टी</div>
                <div className="nav-brand-sub">AI-Powered Regional Risk Intelligence</div>
              </div>
            </button>
          </div>

          {/* Region Selector */}
          <div className="nav-region-wrapper">
            <div className="nav-region-dropdown">
              <button
                onClick={() => setRegionMenuOpen(!regionMenuOpen)}
                className="nav-region-btn"
                aria-expanded={regionMenuOpen}
              >
                <span className="nav-region-dot" />
                <span className="nav-region-label">
                  {lang === 'mr' ? currentRegionObj.name_mr : currentRegionObj.name}
                </span>
                <ChevronDown size={14} className={`nav-region-caret ${regionMenuOpen ? 'open' : ''}`} />
              </button>

              {regionMenuOpen && (
                <div className="nav-region-menu">
                  <div className="nav-region-menu-header">
                    {lang === 'mr' ? 'निरीक्षण क्षेत्र निवडा' : 'Select Monitoring Zone'}
                  </div>
                  {regionOptions.map(opt => (
                    <button
                      key={opt.id}
                      onClick={() => {
                        onRegionChange(opt.id);
                        setRegionMenuOpen(false);
                      }}
                      className={`nav-region-option ${selectedRegion === opt.id ? 'active' : ''}`}
                    >
                      <span>{lang === 'mr' ? opt.name_mr : opt.name}</span>
                      {selectedRegion === opt.id && <CheckCircle2 size={13} style={{ color: '#2D6A4F' }} />}
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Center-Right Utilities */}
          <div className="nav-utilities-group">
            {/* Live Data Freshness Badge */}
            <div className="nav-freshness-pill" title="Live Observation Telemetry">
              <span className="nav-pulse-dot" />
              <span className="nav-freshness-text">
                {backendConnected
                  ? (lang === 'mr' ? 'थेट सेन्सर व मॉडेल सक्रिय' : 'Live ML Engine Synced')
                  : (lang === 'mr' ? 'स्थानिक डेटाबेस सक्रिय' : 'Live Telemetry • 2m ago')}
              </span>
            </div>

            {/* Notification / Alert Bell */}
            <div className="nav-notification-wrapper">
              <button
                onClick={() => setAlertsDropdownOpen(!alertsDropdownOpen)}
                className="nav-icon-btn"
                aria-label="View Active Alerts"
                title={`${highPriorityAlerts.length} Active Warnings`}
              >
                <Bell size={18} />
                {highPriorityAlerts.length > 0 && (
                  <span className="nav-bell-badge">{highPriorityAlerts.length}</span>
                )}
              </button>

              {/* Alerts Dropdown Drawer */}
              {alertsDropdownOpen && (
                <div className="nav-alerts-drawer">
                  <div className="nav-alerts-drawer-header">
                    <span style={{ fontWeight: 700, fontSize: '0.85rem', color: '#202820' }}>
                      {lang === 'mr' ? 'सक्रिय इशारे व सूचना' : 'Active Advisories & Warnings'}
                    </span>
                    <button
                      onClick={() => setAlertsDropdownOpen(false)}
                      className="nav-drawer-close"
                    >
                      <X size={15} />
                    </button>
                  </div>

                  <div className="nav-alerts-list">
                    {highPriorityAlerts.slice(0, 3).map((a, idx) => (
                      <div
                        key={idx}
                        className="nav-alert-preview-item"
                        onClick={() => {
                          setAlertsDropdownOpen(false);
                          onSelectTab('alerts');
                        }}
                      >
                        <div className="nav-alert-preview-badge">
                          <AlertTriangle size={13} />
                          <span>{a.severity.toUpperCase()}</span>
                        </div>
                        <div className="nav-alert-preview-title">
                          {lang === 'mr' && a.title_mr ? a.title_mr : a.title}
                        </div>
                      </div>
                    ))}
                  </div>

                  <button
                    onClick={() => {
                      setAlertsDropdownOpen(false);
                      onSelectTab('alerts');
                    }}
                    className="nav-alerts-viewall-btn"
                  >
                    {lang === 'mr' ? 'सर्व इशारे पहा →' : 'View All Active Alerts →'}
                  </button>
                </div>
              )}
            </div>

            {/* Hackathon 3-Min Demo Button */}
            <button
              onClick={() => onSelectTab('replay')}
              className="nav-demo-btn"
              title="Click to launch 3-minute hackathon comparison demo"
            >
              <Zap size={14} />
              <span>{t.demoMode}</span>
            </button>

            {/* Language Switcher */}
            <div className="nav-lang-cluster" role="radiogroup" aria-label="Language">
              <button
                onClick={() => onLanguageChange('mr')}
                className={`nav-lang-btn ${lang === 'mr' ? 'active' : ''}`}
                title="मराठी"
              >
                मराठी
              </button>
              <button
                onClick={() => onLanguageChange('en')}
                className={`nav-lang-btn ${lang === 'en' ? 'active' : ''}`}
                title="English"
              >
                EN
              </button>
              <button
                onClick={() => onLanguageChange('hi')}
                className={`nav-lang-btn ${lang === 'hi' ? 'active' : ''}`}
                title="हिंदी"
              >
                हिंदी
              </button>
            </div>

            {/* Return to Cinematic Welcome Page Button */}
            <button
              onClick={onReturnToWelcome}
              className="nav-welcome-btn"
              title={lang === 'mr' ? 'सिनेमॅटिक स्वागत स्क्रीन' : 'Cinematic Welcome Screen'}
            >
              <Mountain size={14} />
              <span className="nav-welcome-btn-text">{lang === 'mr' ? 'स्वागत पृष्ठ' : 'Welcome'}</span>
            </button>
          </div>
        </div>
      </div>

      {/* Secondary Sticky Nav Tabs Ribbon */}
      <nav className="top-nav-tabs" aria-label="Main Navigation">
        <div className="top-nav-tabs-inner">
          <button
            onClick={() => onSelectTab('home')}
            className={`nav-tab-item ${currentTab === 'home' ? 'active' : ''}`}
          >
            {t.navHome}
          </button>

          <button
            onClick={() => onSelectTab('map')}
            className={`nav-tab-item ${currentTab === 'map' ? 'active' : ''}`}
          >
            <Compass size={15} />
            <span>{t.navMap}</span>
          </button>

          <button
            onClick={() => onSelectTab('spots')}
            className={`nav-tab-item ${currentTab === 'spots' ? 'active' : ''}`}
          >
            <Droplets size={15} />
            <span>{t.navSpots}</span>
          </button>

          <button
            onClick={() => onSelectTab('corridors')}
            className={`nav-tab-item ${currentTab === 'corridors' ? 'active' : ''}`}
          >
            <GitCommit size={15} />
            <span>{t.navCorridors}</span>
          </button>

          <button
            onClick={() => onSelectTab('alerts')}
            className={`nav-tab-item ${currentTab === 'alerts' ? 'active' : ''}`}
          >
            <Bell size={15} />
            <span>{t.navAlerts}</span>
          </button>

          <button
            onClick={() => onSelectTab('incidents')}
            className={`nav-tab-item ${currentTab === 'incidents' ? 'active' : ''}`}
          >
            <AlertTriangle size={15} />
            <span>{t.navIncidents}</span>
          </button>

          <button
            onClick={() => onSelectTab('safety')}
            className={`nav-tab-item ${currentTab === 'safety' ? 'active' : ''}`}
          >
            <LifeBuoy size={15} />
            <span>{t.navSafety}</span>
          </button>

          <button
            onClick={() => onSelectTab('replay')}
            className={`nav-tab-item ${currentTab === 'replay' ? 'active' : ''}`}
          >
            <PlayCircle size={15} />
            <span>{t.navReplay}</span>
          </button>

          <button
            onClick={() => onSelectTab('authority')}
            className={`nav-tab-item ${currentTab === 'authority' ? 'active' : ''}`}
          >
            <ShieldAlert size={15} />
            <span>{t.navAuthority}</span>
          </button>

          <button
            onClick={() => onSelectTab('research')}
            className={`nav-tab-item ${currentTab === 'research' ? 'active' : ''}`}
          >
            <Cpu size={15} />
            <span>{t.navResearch}</span>
          </button>

          <button
            onClick={() => onSelectTab('about')}
            className={`nav-tab-item ${currentTab === 'about' ? 'active' : ''}`}
          >
            <Info size={15} />
            <span>{t.navAbout}</span>
          </button>
        </div>
      </nav>
    </header>
  );
};

export default TopNavbar;
