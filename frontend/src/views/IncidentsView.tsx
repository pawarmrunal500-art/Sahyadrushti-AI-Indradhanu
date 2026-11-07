import React, { useState } from 'react';
import { IncidentRecord } from '../types';
import {
  AlertTriangle, Shield, CheckCircle2, Clock,
  Send, ExternalLink, MapPin, User, FileText
} from 'lucide-react';
import { apiClient } from '../api';
import { SafeImage } from '../components/SafeImage';

function getIncidentImage(inc: IncidentRecord): string {
  if (inc.image_url) return inc.image_url;
  const text = (inc.location_name + ' ' + inc.title + ' ' + inc.id).toLowerCase();
  if (text.includes('bhushi')) return '/images/locations/bhushi_dam.jpg';
  if (text.includes('expressway') || text.includes('amrutanjan')) return '/images/locations/amrutanjan_bridge.jpg';
  if (text.includes('patan')) return '/images/locations/patan_village.jpg';
  if (text.includes('monkey') || text.includes('thakurwadi')) return '/images/locations/monkey_hill.jpg';
  if (text.includes('adoshi')) return '/images/locations/adoshi_tunnel.jpg';
  return '/images/features/feat_incidents.jpg';
}

interface IncidentsViewProps {
  incidents: IncidentRecord[];
  onIncidentSubmitted: () => void;
  lang: 'mr' | 'en' | 'hi';
}

export const IncidentsView: React.FC<IncidentsViewProps> = ({
  incidents,
  onIncidentSubmitted,
  lang
}) => {
  const [hazardType, setHazardType] = useState('landslide');
  const [locationName, setLocationName] = useState('');
  const [description, setDescription] = useState('');
  const [reporterName, setReporterName] = useState('');
  const [lat, setLat] = useState('18.755');
  const [lon, setLon] = useState('73.395');
  const [submitting, setSubmitting] = useState(false);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!locationName || !description) return;

    setSubmitting(true);
    const payload = {
      hazard_type: hazardType,
      location_name: locationName,
      lat: parseFloat(lat) || 18.755,
      lon: parseFloat(lon) || 73.395,
      description,
      observed_time: new Date().toISOString(),
      reporter_name: reporterName || 'Anonymous Citizen'
    };

    const res = await apiClient.submitIncident(payload);
    setSubmitting(false);
    setSuccessMessage(
      lang === 'mr'
        ? 'तुमची नोंद यशस्वीरित्या पाठवली गेली आहे. प्रशासकीय पडताळणीनंतर ती नकाशावर अपडेट होईल.'
        : 'Report submitted successfully. Placed into moderation queue for field verification before public broadcast.'
    );

    // Reset form
    setLocationName('');
    setDescription('');
    setReporterName('');
    onIncidentSubmitted();
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
      {/* Header */}
      <div className="view-header-card">
        <div style={{ maxWidth: '820px' }}>
          <span className="view-header-badge">
            <AlertTriangle size={12} />
            <span>{lang === 'mr' ? 'नागरी सहभाग व पडताळणी कक्ष' : 'Citizen Reporting & Verification Workflow'}</span>
          </span>
          <h2 className="view-header-title">
            {lang === 'mr'
              ? 'स्थानिक आपत्ती घटना नोंद व इतिहास'
              : 'Crowdsourced Incident Reporting & Historical Log'}
          </h2>
          <p className="view-header-desc">
            {lang === 'mr'
              ? 'रस्त्यावर दरड, ओढ्याला अचानक पूर किंवा पाणी साचल्याचे दिसल्यास त्वरित कळवा. खोटी भीती पसरू नये म्हणून सर्व नोंदींची पडताळणी केली जाते.'
              : 'Residents and commuters can submit ground observations. To prevent misinformation, reports enter an audit queue (Under Review → Corroborated → Verified) before influencing risk levels.'}
          </p>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1.3fr', gap: '1.25rem' }}>
        {/* Submission Form */}
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">
              <FileText size={18} style={{ color: 'var(--sahyadri-700)' }} />
              {lang === 'mr' ? 'नवीन घटना नोंदवा' : 'Submit Ground Hazard Observation'}
            </h3>
          </div>

          {successMessage && (
            <div style={{
              background: '#dcfce7',
              border: '1px solid #86efac',
              color: '#15803d',
              borderRadius: '8px',
              padding: '10px 12px',
              fontSize: '0.82rem',
              marginBottom: '1rem',
              display: 'flex',
              alignItems: 'center',
              gap: '6px'
            }}>
              <CheckCircle2 size={16} /> {successMessage}
            </div>
          )}

          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label className="form-label">{lang === 'mr' ? 'धोक्याचा प्रकार' : 'Hazard Category'}</label>
              <select
                className="form-select"
                value={hazardType}
                onChange={(e) => setHazardType(e.target.value)}
              >
                <option value="landslide">Rockfall / Landslide (दरड कोसळणे)</option>
                <option value="flash_flood">Flash Flood / Stream Surge (अचानक पाण्याचा लोंढा)</option>
                <option value="waterlogging">Waterlogging (पाणी साचणे)</option>
                <option value="corridor_disruption">Road / Rail Obstruction (वाहतूक अडथळा)</option>
                <option value="dangerous_tourist_spot">Dangerous Waterfall Condition (धोकादायक धबधबा)</option>
              </select>
            </div>

            <div className="form-group">
              <label className="form-label">{lang === 'mr' ? 'स्थान / परिसर नाव' : 'Location Name / Landmark'}</label>
              <input
                type="text"
                className="form-input"
                placeholder={lang === 'mr' ? 'उदा. अमृतांजन पुलाजवळ, वळवण नाका, इ.' : 'e.g., Near Adoshi Tunnel, Bhushi road...'}
                value={locationName}
                onChange={(e) => setLocationName(e.target.value)}
                required
              />
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px' }}>
              <div className="form-group">
                <label className="form-label">Approx Lat</label>
                <input
                  type="text"
                  className="form-input"
                  value={lat}
                  onChange={(e) => setLat(e.target.value)}
                />
              </div>
              <div className="form-group">
                <label className="form-label">Approx Lon</label>
                <input
                  type="text"
                  className="form-input"
                  value={lon}
                  onChange={(e) => setLon(e.target.value)}
                />
              </div>
            </div>

            <div className="form-group">
              <label className="form-label">{lang === 'mr' ? 'तपशील' : 'Description of What You Observed'}</label>
              <textarea
                className="form-textarea"
                rows={3}
                placeholder={lang === 'mr' ? 'दगडी दरड पडली आहे, पाणी रस्त्यावरून वाहत आहे, इ.' : 'Describe current conditions, water depth, debris size...'}
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                required
              />
            </div>

            <div className="form-group">
              <label className="form-label">{lang === 'mr' ? 'तुमचे नाव (ऐच्छिक)' : 'Reporter Name (Optional)'}</label>
              <input
                type="text"
                className="form-input"
                placeholder="Anonymous Citizen"
                value={reporterName}
                onChange={(e) => setReporterName(e.target.value)}
              />
            </div>

            <button
              type="submit"
              disabled={submitting}
              className="btn-primary"
              style={{ width: '100%', marginTop: '6px' }}
            >
              <Send size={15} /> {submitting ? 'Submitting...' : (lang === 'mr' ? 'नोंद पाठवा' : 'Submit for Moderation')}
            </button>
          </form>
        </div>

        {/* Incidents Feed */}
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">
              <AlertTriangle size={18} style={{ color: '#ea580c' }} />
              {lang === 'mr' ? 'नोंदवलेल्या घटनांची यादी' : 'Verified Records & Incident Feed'}
            </h3>
            <span style={{ fontSize: '0.75rem', color: '#64748b' }}>
              {incidents.length} Records
            </span>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', maxHeight: '550px', overflowY: 'auto' }}>
            {incidents.map((inc) => {
              const isVerified = inc.verification_status === 'Verified official record';
              const title = lang === 'mr' ? inc.title_mr : inc.title;
              const incImg = getIncidentImage(inc);

              return (
                <div key={inc.id} style={{
                  background: '#f8fafc',
                  border: '1px solid #e2e8f0',
                  borderRadius: '8px',
                  overflow: 'hidden',
                  display: 'flex',
                  gap: '12px'
                }}>
                  {/* Incident Location Thumbnail */}
                  <div style={{ width: '100px', minHeight: '90px', flexShrink: 0, position: 'relative' }}>
                    <SafeImage
                      src={incImg}
                      alt={inc.location_name}
                    />
                  </div>

                  <div style={{ padding: '8px 10px 8px 0', flex: 1, display: 'flex', flexDirection: 'column', gap: '4px' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <span style={{
                        fontSize: '0.68rem',
                        fontWeight: 700,
                        background: isVerified ? '#dcfce7' : '#fef3c7',
                        color: isVerified ? '#15803d' : '#b45309',
                        padding: '2px 6px',
                        borderRadius: '4px',
                        textTransform: 'uppercase'
                      }}>
                        {inc.verification_status}
                      </span>
                      <span style={{ fontSize: '0.7rem', color: '#64748b' }}>
                        {inc.date_time.slice(0, 10)}
                      </span>
                    </div>

                    <h4 style={{ fontSize: '0.88rem', fontWeight: 700, color: '#0f172a' }}>
                      {title}
                    </h4>

                    <p style={{ fontSize: '0.76rem', color: '#475569', lineHeight: 1.35 }}>
                      {inc.description}
                    </p>

                    <div style={{ fontSize: '0.7rem', color: '#64748b', display: 'flex', justifyContent: 'space-between', borderTop: '1px solid #f1f5f9', paddingTop: '4px', marginTop: 'auto' }}>
                      <span>📍 {inc.location_name}</span>
                      <span>Source: <strong>{inc.source_name}</strong></span>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
};
