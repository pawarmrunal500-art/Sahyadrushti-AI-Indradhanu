import React from 'react';
import { LocationItem } from '../types';
import {
  AlertTriangle, Shield, Droplets, Mountain, Compass, Info,
  ExternalLink, Clock, AlertOctagon, Activity, ChevronRight
} from 'lucide-react';
import { SafeImage } from './SafeImage';
import { getLocationImage } from '../utils/imageHelpers';

interface LocationDetailPanelProps {
  location: LocationItem | null;
  onClose?: () => void;
  lang: 'mr' | 'en' | 'hi';
}

export const LocationDetailPanel: React.FC<LocationDetailPanelProps> = ({
  location,
  onClose,
  lang
}) => {
  if (!location) {
    return (
      <div className="map-sidebar-panel" style={{ justifyContent: 'center', alignItems: 'center', textAlign: 'center', color: '#64748b' }}>
        <Compass size={40} style={{ opacity: 0.5, marginBottom: '12px' }} />
        <h4 style={{ fontWeight: 600, color: '#334155' }}>
          {lang === 'mr' ? 'नकाशावरील ठिकाण निवडा' : 'Select a Location on Map'}
        </h4>
        <p style={{ fontSize: '0.8rem', marginTop: '6px', maxWidth: '240px' }}>
          {lang === 'mr'
            ? 'भुशी धरण, कुणे धबधबा, अमृतांजन पूल किंवा पाटण गावाची सविस्तर माहिती पाहण्यासाठी क्लिक करा.'
            : 'Click on Bhushi Dam, Kune Falls, Expressway, or Patan village for detailed terrain & risk intelligence.'}
        </p>
      </div>
    );
  }

  const name = lang === 'mr' ? location.name_mr : (lang === 'hi' ? location.name_hi : location.name);
  const guidance = lang === 'mr' ? location.guidance_mr : (lang === 'hi' ? location.guidance_hi : location.guidance);

  const imgUrl = location.image_url || getLocationImage(location.id);

  return (
    <div className="map-sidebar-panel">
      {/* Authentic Location Photograph Preview */}
      <div style={{
        position: 'relative',
        width: '100%',
        height: '140px',
        borderRadius: 'var(--radius-sm)',
        overflow: 'hidden',
        background: '#e2e8f0',
        marginBottom: '4px',
        boxShadow: 'var(--shadow-xs)'
      }}>
        <SafeImage
          src={imgUrl}
          alt={location.name}
          badge={`${location.elevation_m}m MSL • ${location.slope_deg}° Slope`}
        />
        <div style={{
          position: 'absolute',
          inset: 0,
          background: 'linear-gradient(to top, rgba(15, 23, 42, 0.45) 0%, transparent 60%)',
          pointerEvents: 'none'
        }} />
      </div>

      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div>
          <span className={`hazard-badge ${location.status}`}>
            {location.status_label}
          </span>
          <h3 style={{ fontSize: '1.15rem', fontWeight: 800, color: '#092415', marginTop: '4px' }}>
            {name}
          </h3>
          <div style={{ fontSize: '0.74rem', color: '#64748b', display: 'flex', alignItems: 'center', gap: '4px' }}>
            <Clock size={12} /> {location.last_updated.replace('T', ' ').slice(0, 16)} UTC
          </div>
        </div>
      </div>

      {/* Model Risk Score Gauge */}
      <div className="metric-box" style={{ background: '#f8fafc', borderLeft: `4px solid ${getBorderColor(location.status)}` }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <div className="metric-label">{lang === 'mr' ? 'एआय धोका निर्देशांक' : 'Risk Index (0-100)'}</div>
            <div className="metric-value">
              {location.risk_score} <span style={{ fontSize: '0.85rem', fontWeight: 500, color: '#64748b' }}>/ 100</span>
              {(location.score_capped || location.risk_score === 96) && (
                <span title="Score capped at hydrological model ceiling (96) to reflect uncalibrated overflow limits" style={{ marginLeft: '6px', fontSize: '0.65rem', background: '#fef3c7', color: '#b45309', border: '1px solid #fde68a', padding: '1px 5px', borderRadius: '4px', fontWeight: 600 }}>
                  Capped at 96
                </span>
              )}
            </div>
          </div>
          <div style={{ textAlign: 'right' }}>
            <span style={{ fontSize: '0.75rem', fontWeight: 700, textTransform: 'uppercase', color: getBorderColor(location.status) }}>
              {location.current_hazard.replace('_', ' ')}
            </span>
            <div style={{ fontSize: '0.7rem', color: '#64748b' }}>
              {location.telemetry_status === 'live' ? '🟢 Live Sensor Feed' : '📡 Modelled Estimate'}
            </div>
          </div>
        </div>
      </div>

      {/* Terrain & Catchment Attributes */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px' }}>
        <div className="metric-box" style={{ padding: '8px' }}>
          <div className="metric-label" style={{ fontSize: '0.68rem', display: 'flex', alignItems: 'center', gap: '3px' }}>
            <Mountain size={11} /> {lang === 'mr' ? 'उतार' : 'Slope'}
          </div>
          <div style={{ fontSize: '1.05rem', fontWeight: 700, color: '#1e293b' }}>
            {location.slope_deg}°
          </div>
          <div style={{ fontSize: '0.68rem', color: '#64748b' }}>
            {location.slope_deg > 30 ? 'Steep Escarpment' : 'Moderate Relief'}
          </div>
        </div>

        <div className="metric-box" style={{ padding: '8px' }}>
          <div className="metric-label" style={{ fontSize: '0.68rem', display: 'flex', alignItems: 'center', gap: '3px' }}>
            <Compass size={11} /> {lang === 'mr' ? 'उंची' : 'Elevation'}
          </div>
          <div style={{ fontSize: '1.05rem', fontWeight: 700, color: '#1e293b' }}>
            {location.elevation_m}m
          </div>
          <div style={{ fontSize: '0.68rem', color: '#64748b' }}>MSL Orthometric</div>
        </div>

        <div className="metric-box" style={{ padding: '8px' }}>
          <div className="metric-label" style={{ fontSize: '0.68rem', display: 'flex', alignItems: 'center', gap: '3px' }}>
            <Droplets size={11} /> {lang === 'mr' ? 'पाणलोट' : 'Catchment'}
          </div>
          <div style={{ fontSize: '1.05rem', fontWeight: 700, color: '#1e293b' }}>
            {location.upstream_catchment_km2 ? `${location.upstream_catchment_km2} km²` : 'Localized'}
          </div>
          <div style={{ fontSize: '0.68rem', color: '#64748b' }}>Upstream Basin</div>
        </div>

        <div className="metric-box" style={{ padding: '8px' }}>
          <div className="metric-label" style={{ fontSize: '0.68rem', display: 'flex', alignItems: 'center', gap: '3px' }}>
            <Activity size={11} /> {lang === 'mr' ? 'जलमार्ग अंतर' : 'Drainage'}
          </div>
          <div style={{ fontSize: '1.05rem', fontWeight: 700, color: '#1e293b' }}>
            {location.drainage_proximity_m}m
          </div>
          <div style={{ fontSize: '0.68rem', color: '#64748b' }}>To Active Channel</div>
        </div>
      </div>

      {/* Upstream Catchment Notice (Bhushi / Waterfalls) */}
      {location.upstream_info && (
        <div style={{
          background: '#eff6ff',
          border: '1px solid #bfdbfe',
          borderRadius: '8px',
          padding: '8px 10px',
          fontSize: '0.78rem',
          color: '#1e40af'
        }}>
          <strong>⚠️ {lang === 'mr' ? 'पाणलोट व प्रवाह माहिती:' : 'Upstream Catchment Context:'}</strong>
          <p style={{ marginTop: '3px', lineHeight: 1.35 }}>{location.upstream_info}</p>
        </div>
      )}

      {/* Official Restrictions Banner */}
      {location.restrictions && (
        <div style={{
          background: '#fef2f2',
          border: '1px solid #fecaca',
          borderRadius: '8px',
          padding: '8px 10px',
          fontSize: '0.78rem',
          color: '#991b1b'
        }}>
          <strong>🛑 {lang === 'mr' ? 'प्रशासकीय निर्बंध:' : 'Official Restrictions:'}</strong>
          <p style={{ marginTop: '2px', lineHeight: 1.35 }}>{location.restrictions}</p>
        </div>
      )}

      {/* Precautionary Guidance */}
      <div>
        <div style={{ fontWeight: 700, fontSize: '0.82rem', color: '#092415', marginBottom: '4px' }}>
          {lang === 'mr' ? 'शिफारस केलेल्या उपाययोजना' : 'Recommended Precautions'}
        </div>
        <p style={{ fontSize: '0.8rem', color: '#334155', lineHeight: 1.4, background: '#f1f5f9', padding: '8px 10px', borderRadius: '6px' }}>
          {guidance}
        </p>
      </div>

      {/* Telemetry Status Note */}
      <div style={{ fontSize: '0.72rem', color: '#64748b', borderTop: '1px solid #e2e8f0', paddingTop: '8px' }}>
        <strong>{lang === 'mr' ? 'डेटा स्रोत:' : 'Data Integrity:'}</strong>{' '}
        {location.telemetry_status === 'telemetry_unavailable'
          ? 'Direct stream water-depth telemetry is currently unavailable for this cascade; hazard estimation utilizes regional radar & upstream precipitation indices.'
          : 'Integrated via Open-Meteo meso-scale grid & geotechnical terrain inputs. Geotechnical model based on Western Ghats basalt failure criteria.'}
      </div>
    </div>
  );
};

function getBorderColor(status: string): string {
  switch (status) {
    case 'low': return '#16a34a';
    case 'moderate': return '#d97706';
    case 'high': return '#ea580c';
    case 'very_high': return '#dc2626';
    default: return '#64748b';
  }
}
