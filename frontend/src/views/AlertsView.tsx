import React, { useState } from 'react';
import { AlertItem } from '../types';
import {
  Bell, AlertTriangle, ShieldCheck, Download, Code,
  ExternalLink, Filter, CheckCircle2, ShieldAlert
} from 'lucide-react';

interface AlertsViewProps {
  alerts: AlertItem[];
  lang: 'mr' | 'en' | 'hi';
}

export const AlertsView: React.FC<AlertsViewProps> = ({ alerts, lang }) => {
  const [selectedSeverity, setSelectedSeverity] = useState<string>('all');
  const [selectedType, setSelectedType] = useState<string>('all');
  const [viewingCapAlert, setViewingCapAlert] = useState<AlertItem | null>(null);

  const filteredAlerts = alerts.filter((a) => {
    if (selectedSeverity !== 'all' && a.severity !== selectedSeverity) return false;
    if (selectedType !== 'all' && a.alert_type !== selectedType) return false;
    return true;
  });

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
      {/* Header Banner */}
      <div className="view-header-card">
        <div style={{ maxWidth: '820px' }}>
          <span className="view-header-badge">
            <Bell size={12} />
            <span>{lang === 'mr' ? 'आपत्ती पूर्वसूचना व सीएपी प्रोटोकॉल' : 'Common Alerting Protocol (CAP 1.2)'}</span>
          </span>
          <h2 className="view-header-title">
            {lang === 'mr'
              ? 'अधिकृत इशारे व एआय सल्लागार सूचना'
              : 'Official Warnings & AI Platform Advisories'}
          </h2>
          <p className="view-header-desc">
            {lang === 'mr'
              ? 'प्रशासकीय कायदेशीर इशारे (IMD/NDMA) आणि सह्यादृष्टी एआयच्या स्वयंचलित विश्लेषणात्मक सूचना यांमध्ये पारदर्शक फरक केला आहे.'
              : 'Strictly distinguishes statutory official warnings from model-generated hyperlocal advisories. Supports standardized Common Alerting Protocol (CAP) exports.'}
          </p>
        </div>
      </div>

      {/* Filter Ribbon */}
      <div className="card" style={{ padding: '0.85rem 1.25rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.75rem' }}>
          {/* Type Filter */}
          <div style={{ display: 'flex', gap: '6px', alignItems: 'center', flexWrap: 'wrap' }}>
            <span style={{ fontSize: '0.78rem', fontWeight: 700, color: '#475569', marginRight: '4px' }}>
              Type:
            </span>
            <button
              onClick={() => setSelectedType('all')}
              className={`btn-secondary ${selectedType === 'all' ? 'active' : ''}`}
              style={{ padding: '3px 10px', fontSize: '0.75rem' }}
            >
              All Types
            </button>
            <button
              onClick={() => setSelectedType('official_warning')}
              className={`btn-secondary ${selectedType === 'official_warning' ? 'active' : ''}`}
              style={{
                padding: '3px 10px',
                fontSize: '0.75rem',
                background: selectedType === 'official_warning' ? '#f59e0b' : '#fffbeb',
                color: selectedType === 'official_warning' ? '#ffffff' : '#92400e',
                border: '1px solid #fcd34d'
              }}
            >
              🏛️ Official Warnings
            </button>
            <button
              onClick={() => setSelectedType('ai_advisory')}
              className={`btn-secondary ${selectedType === 'ai_advisory' ? 'active' : ''}`}
              style={{
                padding: '3px 10px',
                fontSize: '0.75rem',
                background: selectedType === 'ai_advisory' ? '#2563eb' : '#eff6ff',
                color: selectedType === 'ai_advisory' ? '#ffffff' : '#1e40af',
                border: '1px solid #bfdbfe'
              }}
            >
              ⚡ AI Advisories
            </button>
          </div>

          {/* Severity Filter */}
          <div style={{ display: 'flex', gap: '6px', alignItems: 'center' }}>
            <span style={{ fontSize: '0.78rem', fontWeight: 700, color: '#475569', marginRight: '4px' }}>
              Severity:
            </span>
            {['all', 'critical', 'warning', 'advisory'].map((sev) => (
              <button
                key={sev}
                onClick={() => setSelectedSeverity(sev)}
                className={`btn-secondary ${selectedSeverity === sev ? 'active' : ''}`}
                style={{ padding: '3px 8px', fontSize: '0.75rem', textTransform: 'capitalize' }}
              >
                {sev}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Alerts Feed */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        {filteredAlerts.map((alert) => {
          const isOfficial = alert.alert_type === 'official_warning';
          const isCritical = alert.severity === 'critical';
          const title = lang === 'mr' ? alert.title_mr : (lang === 'hi' ? alert.title_hi : alert.title);
          const msg = lang === 'mr' ? alert.message_mr : (lang === 'hi' ? alert.message_hi : alert.message);

          return (
            <div
              key={alert.id}
              className="card"
              style={{
                borderLeft: `5px solid ${isOfficial ? '#f59e0b' : (isCritical ? '#dc2626' : '#2563eb')}`,
                background: isCritical ? '#fff5f5' : '#ffffff'
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '0.5rem' }}>
                <div style={{ display: 'flex', gap: '8px', alignItems: 'center', flexWrap: 'wrap' }}>
                  <span style={{
                    background: isOfficial ? '#fef3c7' : '#eff6ff',
                    color: isOfficial ? '#92400e' : '#1e40af',
                    border: `1px solid ${isOfficial ? '#fcd34d' : '#bfdbfe'}`,
                    padding: '2px 8px',
                    borderRadius: '4px',
                    fontSize: '0.72rem',
                    fontWeight: 700,
                    textTransform: 'uppercase'
                  }}>
                    {isOfficial ? 'Verified Official Warning (IMD/Govt)' : 'AI-Generated Hyperlocal Advisory'}
                  </span>

                  <span style={{
                    background: isCritical ? '#fee2e2' : '#f1f5f9',
                    color: isCritical ? '#991b1b' : '#475569',
                    padding: '2px 8px',
                    borderRadius: '4px',
                    fontSize: '0.72rem',
                    fontWeight: 700,
                    textTransform: 'uppercase'
                  }}>
                    Severity: {alert.severity}
                  </span>
                </div>

                <span style={{ fontSize: '0.72rem', color: '#64748b' }}>
                  Issued: {alert.issue_time.slice(0, 16).replace('T', ' ')} UTC
                </span>
              </div>

              <h3 style={{ fontSize: '1.1rem', fontWeight: 800, color: '#092415', marginTop: '8px' }}>
                {title}
              </h3>

              <p style={{ fontSize: '0.86rem', color: '#334155', marginTop: '6px', lineHeight: 1.45 }}>
                {msg}
              </p>

              <div style={{
                marginTop: '10px',
                paddingTop: '8px',
                borderTop: '1px solid #e2e8f0',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                flexWrap: 'wrap',
                gap: '0.5rem',
                fontSize: '0.75rem',
                color: '#64748b'
              }}>
                <div>
                  Issuer: <strong>{alert.issuer}</strong> • Coverage: <strong>{alert.geographic_coverage}</strong>
                </div>

                <div style={{ display: 'flex', gap: '8px' }}>
                  {alert.cap_format && (
                    <button
                      onClick={() => setViewingCapAlert(alert)}
                      className="btn-secondary"
                      style={{ padding: '3px 8px', fontSize: '0.72rem' }}
                    >
                      <Code size={12} /> View CAP XML
                    </button>
                  )}

                  {alert.source_url && (
                    <a
                      href={alert.source_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="btn-secondary"
                      style={{ padding: '3px 8px', fontSize: '0.72rem' }}
                    >
                      <ExternalLink size={12} /> Source Bulletin
                    </a>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* CAP Format Viewer Modal */}
      {viewingCapAlert && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'rgba(0,0,0,0.6)',
          zIndex: 2000,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          padding: '1rem'
        }}>
          <div style={{
            background: '#ffffff',
            borderRadius: '12px',
            maxWidth: '720px',
            width: '100%',
            maxHeight: '85vh',
            overflowY: 'auto',
            padding: '1.5rem',
            boxShadow: '0 20px 25px -5px rgba(0,0,0,0.3)'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
              <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#092415' }}>
                Common Alerting Protocol (CAP v1.2) XML Payload
              </h3>
              <button onClick={() => setViewingCapAlert(null)} style={{ background: 'none', border: 'none', fontSize: '1.2rem', cursor: 'pointer' }}>
                ✕
              </button>
            </div>

            <div style={{
              background: '#fef3c7',
              border: '1px solid #fde68a',
              borderRadius: '6px',
              padding: '8px 10px',
              fontSize: '0.78rem',
              color: '#92400e',
              marginBottom: '1rem'
            }}>
              <strong>Notice:</strong> Exporting or generating a CAP format XML alert does NOT constitute transmission through statutory government broadcasting channels (e.g. NDMA SACHET / CAP-India). It is formatted for standards compliance.
            </div>

            <pre style={{
              background: '#0f172a',
              color: '#38bdf8',
              padding: '1rem',
              borderRadius: '8px',
              fontSize: '0.78rem',
              overflowX: 'auto',
              fontFamily: 'monospace',
              lineHeight: 1.4
            }}>
              {viewingCapAlert.cap_format}
            </pre>

            <div style={{ marginTop: '1rem', display: 'flex', justifyContent: 'flex-end', gap: '8px' }}>
              <button onClick={() => setViewingCapAlert(null)} className="btn-secondary">
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
