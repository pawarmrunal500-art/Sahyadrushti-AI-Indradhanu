import React from 'react';
import { CorridorItem, IncidentRecord } from '../types';
import {
  GitCommit, AlertTriangle, ShieldCheck, Clock,
  ExternalLink, Car, Train, ShieldAlert, CheckCircle2
} from 'lucide-react';
import { SafeImage } from '../components/SafeImage';

function getCorridorImage(c: CorridorItem): string {
  const text = (c.corridor_name + ' ' + c.segment_name).toLowerCase();
  if (text.includes('amrutanjan')) return '/images/locations/amrutanjan_bridge.jpg';
  if (text.includes('adoshi') || text.includes('tunnel')) return '/images/locations/adoshi_tunnel.jpg';
  if (text.includes('monkey hill')) return '/images/locations/monkey_hill.jpg';
  if (text.includes('thakurwadi')) return '/images/locations/thakurwadi.jpg';
  return '/images/features/feat_corridor.jpg';
}

interface CorridorsViewProps {
  corridors: CorridorItem[];
  incidents: IncidentRecord[];
  onNavigate: (tab: string) => void;
  lang: 'mr' | 'en' | 'hi';
}

export const CorridorsView: React.FC<CorridorsViewProps> = ({
  corridors,
  incidents,
  onNavigate,
  lang
}) => {
  // Separate corridor-related incidents
  const transportIncidents = incidents.filter(i =>
    i.hazard_type === 'corridor_disruption' ||
    i.location_name.toLowerCase().includes('expressway') ||
    i.location_name.toLowerCase().includes('railway')
  );

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
      {/* Intro Header */}
      <div className="view-header-card">
        <div style={{ maxWidth: '820px' }}>
          <span className="view-header-badge">
            <GitCommit size={12} />
            <span>{lang === 'mr' ? 'घाट वाहतूक व पायाभूत सुविधा संनियंत्रण' : 'Ghat Transport Corridor Intelligence'}</span>
          </span>
          <h2 className="view-header-title">
            {lang === 'mr'
              ? 'बोरघाट द्रुतगती महामार्ग व रेल्वे मार्ग निरीक्षण'
              : 'Bhor Ghat Highway & Railway Corridor Monitoring'}
          </h2>
          <p className="view-header-desc">
            {lang === 'mr'
              ? 'मुंबई-पुणे द्रुतगती मार्ग, जुना महामार्ग व मध्य रेल्वेचा बोरघाट खंड — दरड, निसरडे रस्ते व हवामान प्रवृत्त वाहतूक अडथळ्यांचे स्वतंत्र विश्लेषण.'
              : 'Continuous geotechnical & weather monitoring along the critical Mumbai–Pune transportation lifeline. Explicitly distinguishes rainfall-triggered slope failures from vehicular traffic & hazardous-cargo accidents.'}
          </p>
        </div>
      </div>

      {/* Corridors Grid */}
      <div className="grid-3">
        {corridors.map((c) => {
          const statusBg = c.current_status === 'CLOSED' ? '#fee2e2' : (c.current_status === 'CAUTION' ? '#ffedd5' : '#dcfce7');
          const statusColor = c.current_status === 'CLOSED' ? '#991b1b' : (c.current_status === 'CAUTION' ? '#9a3412' : '#166534');
          const corridorImg = getCorridorImage(c);

          return (
            <div key={c.id} className="card" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between', padding: 0, overflow: 'hidden' }}>
              {/* Corridor Visual Frame */}
              <div style={{ position: 'relative', width: '100%', height: '145px', background: '#e2e8f0' }}>
                <SafeImage
                  src={corridorImg}
                  alt={c.corridor_name}
                  badge={c.segment_name}
                />
                <span style={{
                  position: 'absolute',
                  top: '10px',
                  right: '10px',
                  background: statusBg,
                  color: statusColor,
                  padding: '3px 10px',
                  borderRadius: '9999px',
                  fontSize: '0.75rem',
                  fontWeight: 700,
                  boxShadow: '0 2px 4px rgba(0,0,0,0.15)'
                }}>
                  {c.current_status}
                </span>
              </div>

              <div style={{ padding: '1.25rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
                  <span style={{ fontSize: '0.72rem', color: '#64748b', display: 'flex', alignItems: 'center', gap: '3px' }}>
                    <Clock size={11} /> {c.latest_report_time.slice(11, 16)} UTC
                  </span>
                  <span style={{ fontSize: '0.74rem', fontWeight: 700, color: '#334155' }}>
                    {c.slope_susceptibility} Susceptibility
                  </span>
                </div>

                <h3 style={{ fontSize: '1.05rem', fontWeight: 800, color: '#092415' }}>
                  {c.corridor_name}
                </h3>
                <h4 style={{ fontSize: '0.82rem', fontWeight: 600, color: '#475569', marginTop: '2px', marginBottom: '12px' }}>
                  {c.segment_name}
                </h4>

                {/* Attributes */}
                <div style={{ display: 'flex', flexDirection: 'column', gap: '6px', fontSize: '0.8rem' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid #f1f5f9', paddingBottom: '4px' }}>
                    <span style={{ color: '#64748b' }}>Slope Susceptibility:</span>
                    <strong style={{ color: '#0f172a' }}>{c.slope_susceptibility}</strong>
                  </div>

                  <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid #f1f5f9', paddingBottom: '4px' }}>
                    <span style={{ color: '#64748b' }}>Trigger Status:</span>
                    <strong style={{ color: '#b45309' }}>{c.rainfall_trigger_status}</strong>
                  </div>

                  <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid #f1f5f9', paddingBottom: '4px' }}>
                    <span style={{ color: '#64748b' }}>Disruption Reported:</span>
                    <strong style={{ color: c.verified_disruption ? '#dc2626' : '#16a34a' }}>
                      {c.verified_disruption ? 'Yes - Clearance Active' : 'No Active Blockage'}
                    </strong>
                  </div>
                </div>

                {/* Traffic Notes */}
                {c.traffic_notes && (
                  <div style={{
                    marginTop: '10px',
                    background: '#f8fafc',
                    padding: '8px 10px',
                    borderRadius: '6px',
                    fontSize: '0.78rem',
                    color: '#334155',
                    border: '1px solid #e2e8f0'
                  }}>
                    <strong>Traffic Advisory:</strong> {c.traffic_notes}
                  </div>
                )}
              </div>

              {/* Source attribution */}
              <div style={{
                marginTop: '12px',
                borderTop: '1px solid #e2e8f0',
                paddingTop: '8px',
                fontSize: '0.72rem',
                color: '#64748b'
              }}>
                <div>Source: <strong>{c.source}</strong></div>
                <div style={{ color: '#0284c7', marginTop: '2px' }}>Official Helpline: {c.official_channel}</div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Corridor Incident History & Freight Accident Separation Banner */}
      <div className="card">
        <div className="card-header">
          <h3 className="card-title">
            <AlertTriangle size={18} style={{ color: '#ea580c' }} />
            {lang === 'mr' ? 'महामार्ग व रेल्वे घटनांची नोंद (नैसर्गिक वि. वाहतूक अपघात)' : 'Corridor Incident Log — Natural Hazards vs Freight Accidents'}
          </h3>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
          {transportIncidents.map((inc) => (
            <div key={inc.id} style={{
              background: '#f8fafc',
              border: '1px solid var(--border-subtle)',
              borderRadius: '8px',
              padding: '12px',
              display: 'flex',
              flexDirection: 'column',
              gap: '4px'
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{
                  fontSize: '0.72rem',
                  fontWeight: 700,
                  background: inc.hazard_type === 'corridor_disruption' ? '#e0f2fe' : '#fee2e2',
                  color: inc.hazard_type === 'corridor_disruption' ? '#0369a1' : '#991b1b',
                  padding: '2px 8px',
                  borderRadius: '4px'
                }}>
                  {inc.hazard_type === 'corridor_disruption' ? 'Traffic / Tanker Accident' : 'Natural Rockfall / Mudslide'}
                </span>
                <span style={{ fontSize: '0.72rem', color: '#64748b' }}>
                  {inc.date_time.slice(0, 10)} • {inc.verification_status}
                </span>
              </div>

              <h4 style={{ fontSize: '0.92rem', fontWeight: 700, color: '#0f172a' }}>
                {lang === 'mr' ? inc.title_mr : inc.title}
              </h4>

              <p style={{ fontSize: '0.8rem', color: '#475569', lineHeight: 1.4 }}>
                {inc.description}
              </p>

              <div style={{ fontSize: '0.72rem', color: '#64748b', display: 'flex', justifyContent: 'space-between', marginTop: '4px' }}>
                <span>Impact: {inc.impact_summary}</span>
                <span>Source: {inc.source_name}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
