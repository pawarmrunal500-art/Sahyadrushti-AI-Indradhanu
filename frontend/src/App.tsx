import React, { useState, useEffect } from 'react';
import {
  LocationItem, AlertItem, IncidentRecord, ShelterItem,
  CorridorItem, SensorNode, ReplayFrame, DemoScenarioData
} from './types';
import { TRANSLATIONS, Language } from './translations';
import { apiClient } from './api';

import { WelcomePage } from './components/WelcomePage';
import { TopNavbar } from './components/TopNavbar';

import { HomeView } from './views/HomeView';
import { MapView } from './views/MapView';
import { SpotCheckView } from './views/SpotCheckView';
import { CorridorsView } from './views/CorridorsView';
import { AlertsView } from './views/AlertsView';
import { IncidentsView } from './views/IncidentsView';
import { SafetyView } from './views/SafetyView';
import { ReplayView } from './views/ReplayView';
import { AuthorityView } from './views/AuthorityView';
import { ResearchView } from './views/ResearchView';
import { AboutView } from './views/AboutView';

import { Mountain } from 'lucide-react';

export const App: React.FC = () => {
  // Opening screen is the cinematic welcome page by default
  const [welcomeActive, setWelcomeActive] = useState<boolean>(true);
  const [currentTab, setCurrentTab] = useState<string>('home');
  const [lang, setLang] = useState<Language>('mr');
  const [selectedRegion, setSelectedRegion] = useState<string>('lonavala');

  const [locations, setLocations] = useState<LocationItem[]>([]);
  const [incidents, setIncidents] = useState<IncidentRecord[]>([]);
  const [alerts, setAlerts] = useState<AlertItem[]>([]);
  const [shelters, setShelters] = useState<ShelterItem[]>([]);
  const [corridors, setCorridors] = useState<CorridorItem[]>([]);
  const [sensors, setSensors] = useState<SensorNode[]>([]);
  const [replayTimeline, setReplayTimeline] = useState<ReplayFrame[]>([]);
  const [demoScenario, setDemoScenario] = useState<DemoScenarioData | null>(null);
  const [selectedLocation, setSelectedLocation] = useState<LocationItem | null>(null);
  const [backendConnected, setBackendConnected] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);

  const t = TRANSLATIONS[lang];

  const loadData = async () => {
    try {
      const isHealthy = await apiClient.checkHealth();
      setBackendConnected(isHealthy);

      const [locs, incs, alrts, shelts, corrs, sens, rep, demo] = await Promise.all([
        apiClient.getLocations(),
        apiClient.getIncidents(),
        apiClient.getAlerts(),
        apiClient.getShelters(),
        apiClient.getCorridors(),
        apiClient.getSensors(),
        apiClient.getReplay(),
        apiClient.getDemoScenario()
      ]);

      setLocations(locs);
      setIncidents(incs);
      setAlerts(alrts);
      setShelters(shelts);
      setCorridors(corrs);
      setSensors(sens.nodes);
      setReplayTimeline(rep.timeline);
      setDemoScenario(demo);

      // Default selected location: Bhushi Dam
      if (locs.length > 0 && !selectedLocation) {
        setSelectedLocation(locs[0]);
      }
    } catch (err) {
      console.error('Initialization error, resilient fallback applied:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  // 1. If welcome screen is active, show the immersive Welcome Page first!
  if (welcomeActive) {
    return (
      <WelcomePage
        onExplore={() => setWelcomeActive(false)}
        lang={lang}
        onLanguageChange={setLang}
        rainfall24h={138.0}
        alertCount={alerts.filter(a => a.severity === 'warning' || a.severity === 'critical').length || 3}
      />
    );
  }

  // 2. Otherwise, show the Light Theme Dashboard
  return (
    <div className="dashboard-shell">
      {/* 3.A Top Navigation Bar */}
      <TopNavbar
        currentTab={currentTab}
        onSelectTab={(tab) => setCurrentTab(tab)}
        lang={lang}
        onLanguageChange={setLang}
        onReturnToWelcome={() => setWelcomeActive(true)}
        selectedRegion={selectedRegion}
        onRegionChange={setSelectedRegion}
        alerts={alerts}
        backendConnected={backendConnected}
      />

      {/* Main Tab Content */}
      <main className="main-content">
        {loading ? (
          <div style={{ textAlign: 'center', padding: '4rem 1rem', color: 'var(--text-muted)' }}>
            <Mountain size={48} style={{ opacity: 0.35, margin: '0 auto 12px auto', color: 'var(--accent-green-dark)' }} />
            <h3 style={{ color: 'var(--text-main)', fontWeight: 700 }}>
              {lang === 'mr' ? 'सह्यादृष्टी भू-स्थानिक माहिती लोड होत आहे...' : 'Loading SAHYADRUSHTI AI Geodata...'}
            </h3>
          </div>
        ) : (
          <>
            {currentTab === 'home' && (
              <HomeView
                locations={locations}
                alerts={alerts}
                onNavigate={(tab) => setCurrentTab(tab)}
                onSelectLocation={(loc) => setSelectedLocation(loc)}
                lang={lang}
              />
            )}

            {currentTab === 'map' && (
              <MapView
                locations={locations}
                incidents={incidents}
                shelters={shelters}
                corridors={corridors}
                sensors={sensors}
                selectedLocation={selectedLocation}
                onSelectLocation={(loc) => setSelectedLocation(loc)}
                lang={lang}
              />
            )}

            {currentTab === 'spots' && (
              <SpotCheckView
                locations={locations}
                onSelectLocation={(loc) => setSelectedLocation(loc)}
                onNavigate={(tab) => setCurrentTab(tab)}
                lang={lang}
              />
            )}

            {currentTab === 'corridors' && (
              <CorridorsView
                corridors={corridors}
                incidents={incidents}
                onNavigate={(tab) => setCurrentTab(tab)}
                lang={lang}
              />
            )}

            {currentTab === 'alerts' && (
              <AlertsView
                alerts={alerts}
                lang={lang}
              />
            )}

            {currentTab === 'incidents' && (
              <IncidentsView
                incidents={incidents}
                onIncidentSubmitted={loadData}
                lang={lang}
              />
            )}

            {currentTab === 'safety' && (
              <SafetyView
                shelters={shelters}
                lang={lang}
              />
            )}

            {currentTab === 'replay' && (
              <ReplayView
                replayTimeline={replayTimeline}
                demoScenario={demoScenario}
                locations={locations}
                lang={lang}
              />
            )}

            {currentTab === 'authority' && (
              <AuthorityView
                locations={locations}
                alerts={alerts}
                incidents={incidents}
                sensors={sensors}
                onRefreshData={loadData}
                lang={lang}
              />
            )}

            {currentTab === 'research' && (
              <ResearchView
                lang={lang}
              />
            )}

            {currentTab === 'about' && (
              <AboutView
                lang={lang}
              />
            )}
          </>
        )}
      </main>

      {/* Professional Light-Theme Footer */}
      <footer className="app-footer">
        <div className="footer-inner">
          <div>
            <strong style={{ color: 'var(--text-main)' }}>सह्यादृष्टी | SAHYADRUSHTI AI</strong> — Hyperlocal Climate-Risk Intelligence & Disaster Early-Warning Platform.
            <div style={{ color: 'var(--text-muted)', fontSize: '0.75rem', marginTop: '3px' }}>
              Built for AI-for-Climate-Change Hackathon aligned with UN Sustainable Development Goal 13.1.
            </div>
          </div>

          <div style={{ textAlign: 'right', fontSize: '0.74rem', color: 'var(--text-muted)' }}>
            <div>Basemap: © OpenStreetMap contributors, OpenTopoMap, NASA SRTM 30m DEM</div>
            <div>Weather & Warnings: India Meteorological Department (IMD) Pilot Integration</div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default App;
