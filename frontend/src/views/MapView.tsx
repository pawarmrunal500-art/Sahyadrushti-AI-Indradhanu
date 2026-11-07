import React, { useState } from 'react';
import { InteractiveMap } from '../components/InteractiveMap';
import { LocationDetailPanel } from '../components/LocationDetailPanel';
import { LocationItem, IncidentRecord, ShelterItem, CorridorItem, SensorNode } from '../types';
import { Compass, Filter, RefreshCw, AlertCircle } from 'lucide-react';

interface MapViewProps {
  locations: LocationItem[];
  incidents: IncidentRecord[];
  shelters: ShelterItem[];
  corridors: CorridorItem[];
  sensors: SensorNode[];
  selectedLocation: LocationItem | null;
  onSelectLocation: (loc: LocationItem) => void;
  lang: 'mr' | 'en' | 'hi';
}

export const MapView: React.FC<MapViewProps> = ({
  locations,
  incidents,
  shelters,
  corridors,
  sensors,
  selectedLocation,
  onSelectLocation,
  lang
}) => {
  const [categoryFilter, setCategoryFilter] = useState<string>('all');

  const filteredLocations = locations.filter((loc) => {
    if (categoryFilter === 'all') return true;
    if (categoryFilter === 'high_risk') return loc.status === 'high' || loc.status === 'very_high';
    return loc.category === categoryFilter;
  });

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', height: '100%' }}>
      {/* Top Filter and Region Context Bar */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        flexWrap: 'wrap',
        gap: '0.5rem',
        background: '#ffffff',
        padding: '0.65rem 1rem',
        borderRadius: '10px',
        border: '1px solid var(--border-subtle)'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Compass size={18} style={{ color: 'var(--accent-green-dark)' }} />
          <span style={{ fontWeight: 800, fontSize: '0.92rem', color: 'var(--text-main)' }}>
            {lang === 'mr' ? 'लोणावळा - खंडाळा हायपरलोकल धोका नकाशा' : 'Lonavala - Khandala Hyperlocal Risk Map'}
          </span>
          <span style={{
            fontSize: '0.72rem',
            background: 'var(--bg-surface)',
            color: 'var(--text-muted)',
            border: '1px solid var(--border-subtle)',
            padding: '2px 8px',
            borderRadius: 'var(--radius-full)'
          }}>
            18.70°N - 18.84°N • SRTM 30m DEM
          </span>
        </div>

        {/* Filter Pills */}
        <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
          <button
            onClick={() => setCategoryFilter('all')}
            className={`btn-secondary ${categoryFilter === 'all' ? 'active' : ''}`}
            style={{
              padding: '4px 12px',
              fontSize: '0.78rem',
              background: categoryFilter === 'all' ? 'var(--accent-yellow)' : '#ffffff',
              color: categoryFilter === 'all' ? '#202820' : 'var(--text-muted)',
              border: '1px solid var(--border-subtle)',
              fontWeight: categoryFilter === 'all' ? 700 : 500
            }}
          >
            {lang === 'mr' ? 'सर्व ठिकाणे' : 'All Points'} ({locations.length})
          </button>

          <button
            onClick={() => setCategoryFilter('high_risk')}
            className={`btn-secondary ${categoryFilter === 'high_risk' ? 'active' : ''}`}
            style={{
              padding: '4px 12px',
              fontSize: '0.78rem',
              background: categoryFilter === 'high_risk' ? 'var(--hazard-crit-bg)' : '#ffffff',
              color: categoryFilter === 'high_risk' ? 'var(--hazard-crit)' : 'var(--text-muted)',
              border: categoryFilter === 'high_risk' ? '1px solid var(--hazard-crit-border)' : '1px solid var(--border-subtle)',
              fontWeight: categoryFilter === 'high_risk' ? 700 : 500
            }}
          >
            {lang === 'mr' ? 'जास्त धोका' : 'High/Critical'}
          </button>

          <button
            onClick={() => setCategoryFilter('tourist_spot')}
            className={`btn-secondary ${categoryFilter === 'tourist_spot' ? 'active' : ''}`}
            style={{
              padding: '4px 12px',
              fontSize: '0.78rem',
              background: categoryFilter === 'tourist_spot' ? 'var(--accent-green-light)' : '#ffffff',
              color: categoryFilter === 'tourist_spot' ? 'var(--accent-green-dark)' : 'var(--text-muted)',
              border: categoryFilter === 'tourist_spot' ? '1px solid var(--accent-green)' : '1px solid var(--border-subtle)',
              fontWeight: categoryFilter === 'tourist_spot' ? 700 : 500
            }}
          >
            {lang === 'mr' ? 'पर्यटन स्थळे' : 'Tourist Spots'}
          </button>

          <button
            onClick={() => setCategoryFilter('corridor')}
            className={`btn-secondary ${categoryFilter === 'corridor' ? 'active' : ''}`}
            style={{
              padding: '4px 12px',
              fontSize: '0.78rem',
              background: categoryFilter === 'corridor' ? 'var(--accent-green-light)' : '#ffffff',
              color: categoryFilter === 'corridor' ? 'var(--accent-green-dark)' : 'var(--text-muted)',
              border: categoryFilter === 'corridor' ? '1px solid var(--accent-green)' : '1px solid var(--border-subtle)',
              fontWeight: categoryFilter === 'corridor' ? 700 : 500
            }}
          >
            {lang === 'mr' ? 'महामार्ग / रेल्वे' : 'Corridors'}
          </button>
        </div>
      </div>

      {/* Main Map + Intelligence Sidebar Grid */}
      <div className="map-view-container">
        <InteractiveMap
          locations={filteredLocations}
          incidents={incidents}
          shelters={shelters}
          corridors={corridors}
          sensors={sensors}
          selectedLocation={selectedLocation}
          onSelectLocation={onSelectLocation}
          lang={lang}
        />

        <LocationDetailPanel
          location={selectedLocation}
          lang={lang}
        />
      </div>
    </div>
  );
};
