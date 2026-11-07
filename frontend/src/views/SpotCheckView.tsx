import React from 'react';
import { LocationItem } from '../types';
import {
  Droplets, AlertTriangle, ShieldCheck, MapPin, Eye,
  Compass, ExternalLink, ShieldAlert, Mountain, Clock
} from 'lucide-react';
import { SafeImage } from '../components/SafeImage';
import { getLocationImage } from '../utils/imageHelpers';

interface SpotCheckViewProps {
  locations: LocationItem[];
  onSelectLocation: (loc: LocationItem) => void;
  onNavigate: (tab: string) => void;
  lang: 'mr' | 'en' | 'hi';
}

export const SpotCheckView: React.FC<SpotCheckViewProps> = ({
  locations,
  onSelectLocation,
  onNavigate,
  lang
}) => {
  const touristSpots = locations.filter(l => l.category === 'tourist_spot');

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
      {/* Introduction Card */}
      <div className="view-header-card">
        <div style={{ maxWidth: '820px' }}>
          <span className="view-header-badge">
            <Droplets size={12} />
            <span>{lang === 'mr' ? 'पर्यटक सुरक्षितता पूर्वसूचना' : 'Visitor Hazard Pre-Check'}</span>
          </span>
          <h2 className="view-header-title">
            {lang === 'mr'
              ? 'पर्यटन स्थळ तपासणी — पाण्याआधी धोका ओळखा'
              : 'Tourist Spot-Check — Upstream Water & Escarpment Intelligence'}
          </h2>
          <p className="view-header-desc">
            {lang === 'mr'
              ? 'धबधबा किंवा धरणावर जाताना केवळ खालील पाणी पाहू नका. वरच्या डोंगररांगांमधील पाऊस व ओढ्यांचे पाणी अचानक पूर किंवा दरड निर्माण करू शकते. खालील माहिती प्रत्यक्ष तपासा.'
              : 'Mountain waterfalls and streams react to rainfall kilometers upstream. A gentle cascade can transform into a lethal surge within minutes. Always verify upstream catchment conditions and official advisories before visiting.'}
          </p>
        </div>
      </div>

      {/* Directory Grid */}
      <div className="grid-2">
        {touristSpots.map((spot) => {
          const name = lang === 'mr' ? spot.name_mr : (lang === 'hi' ? spot.name_hi : spot.name);
          const guidance = lang === 'mr' ? spot.guidance_mr : (lang === 'hi' ? spot.guidance_hi : spot.guidance);

          const imgUrl = spot.image_url || getLocationImage(spot.id);

          return (
            <div key={spot.id} className="card" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between', padding: '0', overflow: 'hidden' }}>
              {/* Authentic Location Image Frame */}
              <div style={{ position: 'relative', width: '100%', height: '170px', background: '#e2e8f0' }}>
                <SafeImage
                  src={imgUrl}
                  alt={spot.name}
                  badge={`${spot.elevation_m}m MSL • ${spot.slope_deg}° Slope`}
                />
                <span
                  className={`hazard-badge ${spot.status}`}
                  style={{
                    position: 'absolute',
                    top: '10px',
                    right: '10px',
                    boxShadow: '0 2px 6px rgba(0,0,0,0.2)'
                  }}
                >
                  {spot.status_label}
                </span>
              </div>

              <div style={{ padding: '1.25rem' }}>
                {/* Header status */}
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '8px' }}>
                  <span style={{ fontSize: '0.74rem', color: '#64748b', display: 'flex', alignItems: 'center', gap: '3px' }}>
                    <Clock size={12} /> {spot.last_updated.replace('T', ' ').slice(0, 16)} UTC
                  </span>
                  <span style={{ fontSize: '0.78rem', fontWeight: 800, color: 'var(--text-main)' }}>
                    Risk: {spot.risk_score}/100
                  </span>
                </div>

                <h3 style={{ fontSize: '1.2rem', fontWeight: 800, color: '#092415', marginBottom: '4px' }}>
                  {name}
                </h3>

                <div style={{ fontSize: '0.75rem', color: '#475569', marginBottom: '10px' }}>
                  📍 {spot.coordinates[0].toFixed(4)}°N, {spot.coordinates[1].toFixed(4)}°E • Elevation: {spot.elevation_m}m MSL
                </div>

                {/* Key Metrics Chips */}
                <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap', marginBottom: '12px' }}>
                  <span style={{
                    background: '#f1f5f9',
                    fontSize: '0.72rem',
                    fontWeight: 600,
                    padding: '3px 8px',
                    borderRadius: '4px',
                    color: '#334155'
                  }}>
                    Slope: {spot.slope_deg}°
                  </span>

                  {spot.upstream_catchment_km2 && (
                    <span style={{
                      background: '#e0f2fe',
                      fontSize: '0.72rem',
                      fontWeight: 600,
                      padding: '3px 8px',
                      borderRadius: '4px',
                      color: '#0369a1'
                    }}>
                      Upstream Catchment: {spot.upstream_catchment_km2} km²
                    </span>
                  )}

                  <span style={{
                    background: spot.telemetry_status === 'live' ? '#dcfce7' : '#fef3c7',
                    fontSize: '0.72rem',
                    fontWeight: 600,
                    padding: '3px 8px',
                    borderRadius: '4px',
                    color: spot.telemetry_status === 'live' ? '#15803d' : '#b45309'
                  }}>
                    {spot.telemetry_status === 'live' ? '🟢 Live Sensor' : '📡 Modelled Estimate'}
                  </span>
                </div>

                {/* Upstream Catchment Info Box */}
                {spot.upstream_info && (
                  <div style={{
                    background: '#eff6ff',
                    border: '1px solid #bfdbfe',
                    borderRadius: '8px',
                    padding: '8px 10px',
                    fontSize: '0.78rem',
                    color: '#1e40af',
                    marginBottom: '10px',
                    lineHeight: 1.35
                  }}>
                    <strong>⚠️ {lang === 'mr' ? 'पाणलोट माहिती:' : 'Upstream Catchment Hazard:'}</strong> {spot.upstream_info}
                  </div>
                )}

                {/* Official Restrictions Box */}
                {spot.restrictions && (
                  <div style={{
                    background: '#fef2f2',
                    border: '1px solid #fecaca',
                    borderRadius: '8px',
                    padding: '8px 10px',
                    fontSize: '0.78rem',
                    color: '#991b1b',
                    marginBottom: '10px',
                    lineHeight: 1.35
                  }}>
                    <strong>🛑 {lang === 'mr' ? 'प्रशासकीय निर्बंध:' : 'Official Restriction:'}</strong> {spot.restrictions}
                  </div>
                )}

                {/* Precaution Guidance */}
                <div style={{
                  background: '#f8fafc',
                  padding: '10px',
                  borderRadius: '8px',
                  border: '1px solid #e2e8f0',
                  fontSize: '0.8rem',
                  color: '#334155',
                  lineHeight: 1.4
                }}>
                  <strong style={{ color: '#092415', display: 'block', marginBottom: '2px' }}>
                    {lang === 'mr' ? 'पर्यटकांनी काय करावे:' : 'Safety Guidance:'}
                  </strong>
                  {guidance}
                </div>
              </div>

              {/* Action Buttons */}
              <div style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                marginTop: '1rem',
                borderTop: '1px solid #e2e8f0',
                paddingTop: '0.75rem'
              }}>
                <span style={{ fontSize: '0.74rem', color: '#64748b' }}>
                  Risk Score: <strong>{spot.risk_score} / 100</strong>
                </span>

                <button
                  onClick={() => {
                    onSelectLocation(spot);
                    onNavigate('map');
                  }}
                  className="btn-primary"
                  style={{ fontSize: '0.78rem', padding: '5px 12px' }}
                >
                  <MapPin size={13} /> {lang === 'mr' ? 'नकाशावर पहा' : 'View on Map'}
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
