import React, { useState, useEffect } from 'react';
import { LocationItem, AlertItem, IncidentRecord, SensorNode } from '../types';
import {
  ShieldAlert, Activity, CheckCircle2, XCircle, Send,
  FileSpreadsheet, Printer, Clock, Bell, UserCheck, AlertTriangle,
  Lock, LogIn, LogOut, ShieldCheck
} from 'lucide-react';
import { apiClient } from '../api';

interface AuthorityViewProps {
  locations: LocationItem[];
  alerts: AlertItem[];
  incidents: IncidentRecord[];
  sensors: SensorNode[];
  onRefreshData: () => void;
  lang: 'mr' | 'en' | 'hi';
}

export const AuthorityView: React.FC<AuthorityViewProps> = ({
  locations,
  alerts,
  incidents,
  sensors,
  onRefreshData,
  lang
}) => {
  // Auth state
  const [currentUser, setCurrentUser] = useState(apiClient.getCurrentUser());
  const [usernameInput, setUsernameInput] = useState('');
  const [passwordInput, setPasswordInput] = useState('');
  const [loginError, setLoginError] = useState<string | null>(null);
  const [loggingIn, setLoggingIn] = useState(false);

  // Authority Queue state
  const [actionQueue, setActionQueue] = useState<any[]>([]);
  const [queueCount, setQueueCount] = useState<number>(0);

  // Composer state
  const [draftTitle, setDraftTitle] = useState('');
  const [draftTitleMr, setDraftTitleMr] = useState('');
  const [draftMessage, setDraftMessage] = useState('');
  const [draftSeverity, setDraftSeverity] = useState('advisory');
  const [coverageArea, setCoverageArea] = useState('Lonavala Ghat Region');
  const [drafting, setDrafting] = useState(false);
  const [composerSuccess, setComposerSuccess] = useState<string | null>(null);
  const [actionError, setActionError] = useState<string | null>(null);

  const pendingIncidents = incidents.filter(i => i.verification_status === 'Unverified report');
  const escalatingHotspots = locations.filter(l => l.status === 'high' || l.status === 'very_high');

  const fetchQueue = async () => {
    if (!currentUser) return;
    const res = await apiClient.getAuthorityQueue();
    if (res.ok) {
      setActionQueue(res.queue);
      setQueueCount(res.count);
    } else if (res.error === 'Session expired') {
      setCurrentUser(null);
      setLoginError('Your session has expired. Please log in again.');
    }
  };

  useEffect(() => {
    if (currentUser) {
      fetchQueue();
    }
  }, [currentUser]);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!usernameInput || !passwordInput) return;
    setLoggingIn(true);
    setLoginError(null);

    const res = await apiClient.login(usernameInput, passwordInput);
    setLoggingIn(false);
    if (res.ok) {
      setCurrentUser(apiClient.getCurrentUser());
      setUsernameInput('');
      setPasswordInput('');
    } else {
      setLoginError(res.error || 'Authentication failed.');
    }
  };

  const handleLogout = async () => {
    await apiClient.logout();
    setCurrentUser(null);
    setActionQueue([]);
  };

  const handleDraftAlert = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!draftTitle || !draftMessage) return;

    setDrafting(true);
    setActionError(null);
    setComposerSuccess(null);

    const res = await apiClient.draftAlert({
      title: draftTitle,
      title_mr: draftTitleMr || draftTitle,
      message: draftMessage,
      message_mr: draftMessage,
      severity: draftSeverity,
      geographic_coverage: coverageArea,
      target_locations: ['bhushi_dam', 'khandala_expressway']
    });

    setDrafting(false);
    if (res.ok) {
      setComposerSuccess(`Draft advisory ${res.alert_id || ''} created and placed into approval queue.`);
      setDraftTitle('');
      setDraftTitleMr('');
      setDraftMessage('');
      onRefreshData();
      fetchQueue();
    } else {
      if (res.status === 401) {
        setCurrentUser(null);
        setLoginError('Session expired. Please log in again.');
      } else {
        setActionError(res.error || 'Failed to create draft advisory.');
      }
    }
  };

  const handleApproveAlert = async (alertId: string) => {
    setActionError(null);
    setComposerSuccess(null);
    const res = await apiClient.approveAlert(alertId);
    if (res.ok) {
      setComposerSuccess(`Alert ${alertId} approved and broadcast to public feeds.`);
      onRefreshData();
      fetchQueue();
    } else {
      if (res.status === 409) {
        setActionError(`Four-Eyes Principle: You drafted this alert and cannot approve your own advisory.`);
      } else if (res.status === 401) {
        setCurrentUser(null);
        setLoginError('Session expired. Please log in again.');
      } else {
        setActionError(res.error || 'Approval failed.');
      }
    }
  };

  const handlePrintSitRep = () => {
    window.print();
  };

  // If not logged in, render authenticated gate
  if (!currentUser) {
    return (
      <div style={{ maxWidth: '480px', margin: '3rem auto', padding: '0 1rem' }}>
        <div className="card" style={{ padding: '2rem', textAlign: 'center' }}>
          <div style={{
            background: 'rgba(9, 36, 21, 0.08)',
            width: '56px',
            height: '56px',
            borderRadius: '50%',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            margin: '0 auto 1rem auto',
            color: 'var(--accent-green-dark)'
          }}>
            <Lock size={28} />
          </div>

          <h2 style={{ fontSize: '1.25rem', fontWeight: 800, color: 'var(--text-main)', marginBottom: '0.25rem' }}>
            {lang === 'mr' ? 'अधिकारी नियंत्रण कक्ष प्रवेश' : 'Authority Console Authentication'}
          </h2>
          <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '1.5rem' }}>
            {lang === 'mr'
              ? 'आपत्ती व्यवस्थापन अधिकारी, ऑपरेटर व अनुमोदक यांच्यासाठी आरक्षित.'
              : 'Restricted to verified Maval Taluka Emergency Operators & Approvers.'}
          </p>

          {loginError && (
            <div style={{
              background: '#fef2f2',
              border: '1px solid #fecaca',
              color: '#b91c1c',
              fontSize: '0.8rem',
              padding: '10px 12px',
              borderRadius: '6px',
              marginBottom: '1rem',
              textAlign: 'left',
              display: 'flex',
              alignItems: 'center',
              gap: '8px'
            }}>
              <AlertTriangle size={16} />
              <span>{loginError}</span>
            </div>
          )}

          <form onSubmit={handleLogin} style={{ display: 'flex', flexDirection: 'column', gap: '1rem', textAlign: 'left' }}>
            <div>
              <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 700, color: '#334155', marginBottom: '4px' }}>
                Username / युझरनेम
              </label>
              <input
                type="text"
                className="input-field"
                placeholder="e.g. test_operator"
                value={usernameInput}
                onChange={(e) => setUsernameInput(e.target.value)}
                required
                style={{ width: '100%', padding: '8px 12px', fontSize: '0.85rem' }}
              />
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 700, color: '#334155', marginBottom: '4px' }}>
                Password / पासवर्ड
              </label>
              <input
                type="password"
                className="input-field"
                placeholder="Enter password"
                value={passwordInput}
                onChange={(e) => setPasswordInput(e.target.value)}
                required
                style={{ width: '100%', padding: '8px 12px', fontSize: '0.85rem' }}
              />
            </div>

            <button
              type="submit"
              disabled={loggingIn}
              className="btn-primary"
              style={{ width: '100%', padding: '10px', marginTop: '0.5rem', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px' }}
            >
              <LogIn size={16} />
              {loggingIn ? 'Authenticating...' : 'Sign In to Operations Console'}
            </button>
          </form>

          <div style={{ marginTop: '1.25rem', fontSize: '0.72rem', color: '#64748b', borderTop: '1px solid #e2e8f0', paddingTop: '1rem' }}>
            Account provisioning CLI: <code>python -m app.cli create-user --username &lt;name&gt; --role &lt;operator|approver|admin&gt;</code>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
      {/* Control Room Top Status Bar */}
      <div className="view-header-card">
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span style={{
              background: '#16a34a',
              width: '10px',
              height: '10px',
              borderRadius: '50%',
              display: 'inline-block'
            }}></span>
            <span style={{ fontSize: '0.75rem', fontWeight: 800, letterSpacing: '0.05em', color: 'var(--accent-green-dark)' }}>
              INCIDENT COMMAND OPERATIONS CONSOLE
            </span>
          </div>
          <h2 className="view-header-title" style={{ marginTop: '4px' }}>
            {lang === 'mr' ? 'मावळ आपत्ती नियंत्रण व पूर्वसूचना कक्ष' : 'Maval Taluka Disaster Operations Center'}
          </h2>
          <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: '2px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span>Officer: <strong>{currentUser.username}</strong></span>
            <span style={{
              textTransform: 'uppercase',
              fontSize: '0.68rem',
              fontWeight: 800,
              background: currentUser.role === 'admin' ? '#fef3c7' : currentUser.role === 'approver' ? '#e0f2fe' : '#dcfce7',
              color: currentUser.role === 'admin' ? '#b45309' : currentUser.role === 'approver' ? '#0369a1' : '#15803d',
              padding: '2px 6px',
              borderRadius: '4px'
            }}>
              {currentUser.role}
            </span>
            <span>• Pilot: Lonavala–Khandala</span>
          </div>
        </div>

        <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
          <button
            onClick={handlePrintSitRep}
            className="btn-secondary"
            style={{ fontSize: '0.78rem', background: 'rgba(255,255,255,0.1)', color: '#ffffff', border: '1px solid rgba(255,255,255,0.2)' }}
          >
            <Printer size={14} /> Export / Print SitRep
          </button>
          <button
            onClick={handleLogout}
            className="btn-secondary"
            style={{ fontSize: '0.78rem', background: 'rgba(239, 68, 68, 0.2)', color: '#ffffff', border: '1px solid rgba(239, 68, 68, 0.4)' }}
            title="Sign out"
          >
            <LogOut size={14} /> Logout
          </button>
        </div>
      </div>

      {actionError && (
        <div style={{
          background: '#fef2f2',
          border: '1px solid #fecaca',
          color: '#b91c1c',
          fontSize: '0.85rem',
          padding: '12px 16px',
          borderRadius: '8px',
          display: 'flex',
          alignItems: 'center',
          gap: '10px'
        }}>
          <AlertTriangle size={18} />
          <span>{actionError}</span>
        </div>
      )}

      {composerSuccess && (
        <div style={{
          background: '#f0fdf4',
          border: '1px solid #bbf7d0',
          color: '#15803d',
          fontSize: '0.85rem',
          padding: '12px 16px',
          borderRadius: '8px',
          display: 'flex',
          alignItems: 'center',
          gap: '10px'
        }}>
          <CheckCircle2 size={18} />
          <span>{composerSuccess}</span>
        </div>
      )}

      {/* High-Risk Action Queue (Additive Endpoint) */}
      {actionQueue.length > 0 && (
        <div className="card" style={{ borderLeft: '4px solid #ea580c' }}>
          <div className="card-header">
            <h3 className="card-title">
              <ShieldAlert size={18} style={{ color: '#ea580c' }} />
              {lang === 'mr' ? 'तातडीने कारवाई आवश्यक ठिकाणे (Action Queue)' : 'Active High-Risk Action Queue'}
            </h3>
            <span style={{ fontSize: '0.75rem', fontWeight: 700, color: '#ea580c', background: '#ffedd5', padding: '2px 8px', borderRadius: '4px' }}>
              {actionQueue.filter(q => q.requires_action).length} Unaddressed Hotspots (Risk ≥ 70)
            </span>
          </div>
          <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.82rem' }}>
              <thead>
                <tr style={{ background: '#f8fafc', borderBottom: '2px solid #e2e8f0', textAlign: 'left', color: '#475569' }}>
                  <th style={{ padding: '8px 12px' }}>Location</th>
                  <th style={{ padding: '8px 12px' }}>Hazard</th>
                  <th style={{ padding: '8px 12px' }}>Current Risk</th>
                  <th style={{ padding: '8px 12px' }}>Slope</th>
                  <th style={{ padding: '8px 12px' }}>Recommended Protocol</th>
                </tr>
              </thead>
              <tbody>
                {actionQueue.map((item) => (
                  <tr key={item.location_id} style={{ borderBottom: '1px solid #f1f5f9' }}>
                    <td style={{ padding: '8px 12px', fontWeight: 700, color: '#092415' }}>
                      {lang === 'mr' ? item.name_mr : item.name}
                    </td>
                    <td style={{ padding: '8px 12px', textTransform: 'capitalize' }}>
                      {item.hazard_type?.replace('_', ' ')}
                    </td>
                    <td style={{ padding: '8px 12px' }}>
                      <span className="hazard-badge high">{item.risk_score} / 100{(item.score_capped || item.risk_score >= 96) ? ` (Capped at ${item.current_hazard === 'landslide' ? 98 : 96})` : ''}</span>
                    </td>
                    <td style={{ padding: '8px 12px' }}>{item.slope_deg}°</td>
                    <td style={{ padding: '8px 12px', color: item.requires_action ? '#c2410c' : '#15803d', fontWeight: 600 }}>
                      {item.recommended_action}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Escalating Hotspots Panel */}
      <div className="card">
        <div className="card-header">
          <h3 className="card-title">
            <ShieldAlert size={18} style={{ color: '#ea580c' }} />
            {lang === 'mr' ? 'अतिदक्षता व धोक्यातील ठिकाणे' : 'Highest-Priority Escalating Hotspots'}
          </h3>
          <span style={{ fontSize: '0.75rem', color: '#64748b' }}>
            {escalatingHotspots.length} Locations Flagged
          </span>
        </div>

        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.82rem' }}>
            <thead>
              <tr style={{ background: '#f8fafc', borderBottom: '2px solid #e2e8f0', textAlign: 'left', color: '#475569' }}>
                <th style={{ padding: '8px 12px' }}>Location</th>
                <th style={{ padding: '8px 12px' }}>Hazard</th>
                <th style={{ padding: '8px 12px' }}>Risk Score</th>
                <th style={{ padding: '8px 12px' }}>Slope</th>
                <th style={{ padding: '8px 12px' }}>Telemetry</th>
                <th style={{ padding: '8px 12px' }}>Primary Action</th>
              </tr>
            </thead>
            <tbody>
              {escalatingHotspots.map((loc) => (
                <tr key={loc.id} style={{ borderBottom: '1px solid #f1f5f9' }}>
                  <td style={{ padding: '8px 12px', fontWeight: 700, color: '#092415' }}>
                    {lang === 'mr' ? loc.name_mr : loc.name}
                  </td>
                  <td style={{ padding: '8px 12px' }}>
                    <span style={{ textTransform: 'capitalize' }}>{loc.current_hazard.replace('_', ' ')}</span>
                  </td>
                  <td style={{ padding: '8px 12px' }}>
                    <span className={`hazard-badge ${loc.status}`}>
                      {loc.risk_score} / 100{(loc.score_capped || loc.risk_score >= 96) ? ` (Capped at ${loc.current_hazard === 'landslide' ? 98 : 96})` : ''}
                    </span>
                  </td>
                  <td style={{ padding: '8px 12px' }}>{loc.slope_deg}°</td>
                  <td style={{ padding: '8px 12px', color: loc.telemetry_status === 'live' ? '#16a34a' : '#b45309' }}>
                    {loc.telemetry_status === 'live' ? '🟢 Live Sensor' : '📡 Modelled'}
                  </td>
                  <td style={{ padding: '8px 12px', fontSize: '0.78rem', color: '#334155' }}>
                    {loc.guidance.slice(0, 60)}...
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 1fr', gap: '1.25rem' }}>
        {/* Incident Moderation Queue */}
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">
              <UserCheck size={18} style={{ color: 'var(--sahyadri-700)' }} />
              {lang === 'mr' ? 'नागरी नोंदणी पडताळणी कक्ष' : 'Crowdsourced Incident Moderation Queue'}
            </h3>
            <span style={{ fontSize: '0.75rem', color: '#ea580c', fontWeight: 700 }}>
              {pendingIncidents.length} Pending Verification
            </span>
          </div>

          {pendingIncidents.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '2rem 1rem', color: '#64748b', fontSize: '0.85rem' }}>
              <CheckCircle2 size={32} style={{ color: '#16a34a', margin: '0 auto 8px auto' }} />
              All submitted ground reports have been verified or resolved.
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
              {pendingIncidents.map((p) => (
                <div key={p.id} style={{
                  background: '#f8fafc',
                  border: '1px solid #e2e8f0',
                  borderRadius: '8px',
                  padding: '12px',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '6px'
                }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <span style={{ fontSize: '0.72rem', fontWeight: 700, color: '#ea580c' }}>
                      {p.hazard_type.toUpperCase()} • {p.date_time.slice(11, 16)} UTC
                    </span>
                    <span style={{ fontSize: '0.72rem', color: '#64748b' }}>
                      {p.source_name}
                    </span>
                  </div>

                  <h4 style={{ fontSize: '0.92rem', fontWeight: 700, color: '#0f172a' }}>
                    {p.title}
                  </h4>

                  <p style={{ fontSize: '0.8rem', color: '#475569' }}>
                    {p.description}
                  </p>

                  <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '8px', marginTop: '6px' }}>
                    <button
                      onClick={() => alert(`Report ${p.id} marked verified. Logged in audit registry.`)}
                      className="btn-primary"
                      style={{ padding: '3px 10px', fontSize: '0.72rem', background: '#16a34a' }}
                    >
                      <CheckCircle2 size={12} /> Verify & Broadcast
                    </button>
                    <button
                      onClick={() => alert(`Report ${p.id} rejected due to lack of corroboration.`)}
                      className="btn-secondary"
                      style={{ padding: '3px 10px', fontSize: '0.72rem', color: '#dc2626' }}
                    >
                      <XCircle size={12} /> Reject
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Authority Advisory Composer */}
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">
              <Bell size={18} style={{ color: 'var(--sahyadri-700)' }} />
              {lang === 'mr' ? 'पूर्वसूचना तयार करा' : 'Draft Platform Risk Advisory'}
            </h3>
          </div>

          {composerSuccess && (
            <div style={{
              background: '#dcfce7',
              border: '1px solid #86efac',
              color: '#15803d',
              padding: '8px 10px',
              borderRadius: '6px',
              fontSize: '0.78rem',
              marginBottom: '10px'
            }}>
              {composerSuccess}
            </div>
          )}

          <form onSubmit={handleDraftAlert}>
            <div className="form-group">
              <label className="form-label">Advisory Title (English)</label>
              <input
                type="text"
                className="form-input"
                placeholder="e.g. Flash Surge Watch for Bhushi Overburden"
                value={draftTitle}
                onChange={(e) => setDraftTitle(e.target.value)}
                required
              />
            </div>

            <div className="form-group">
              <label className="form-label">Advisory Title (मराठी)</label>
              <input
                type="text"
                className="form-input"
                placeholder="उदा. भुशी धरण परिसरात अचानक पाण्याचा वेग वाढण्याचा धोका"
                value={draftTitleMr}
                onChange={(e) => setDraftTitleMr(e.target.value)}
              />
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px' }}>
              <div className="form-group">
                <label className="form-label">Severity Level</label>
                <select
                  className="form-select"
                  value={draftSeverity}
                  onChange={(e) => setDraftSeverity(e.target.value)}
                >
                  <option value="advisory">Advisory (सल्लागार)</option>
                  <option value="watch">Watch (दक्षता)</option>
                  <option value="warning">Warning (इशारा)</option>
                  <option value="critical">Critical (अतिधोका)</option>
                </select>
              </div>

              <div className="form-group">
                <label className="form-label">Target Zone</label>
                <input
                  type="text"
                  className="form-input"
                  value={coverageArea}
                  onChange={(e) => setCoverageArea(e.target.value)}
                />
              </div>
            </div>

            <div className="form-group">
              <label className="form-label">Detailed Precaution Instructions</label>
              <textarea
                className="form-textarea"
                rows={3}
                placeholder="Actionable steps for tourists, village committees, or police chowkis..."
                value={draftMessage}
                onChange={(e) => setDraftMessage(e.target.value)}
                required
              />
            </div>

            <button
              type="submit"
              disabled={drafting}
              className="btn-primary"
              style={{ width: '100%', marginTop: '6px' }}
            >
              <Send size={14} /> {drafting ? 'Drafting...' : 'Save Advisory Draft'}
            </button>
          </form>
        </div>
      </div>

      {/* IoT Sensor Health Diagnostic Grid */}
      <div className="card">
        <div className="card-header">
          <h3 className="card-title">
            <Activity size={18} style={{ color: 'var(--sahyadri-700)' }} />
            {lang === 'mr' ? 'IoT सेन्सर नेटवर्क आरोग्य स्थिती (सिम्युलेटेड प्रायोगिक सेन्सर)' : 'IoT Field Monitoring Network Health Diagnostics'}
          </h3>
          <span style={{
            fontSize: '0.72rem',
            background: '#e0f2fe',
            color: '#0369a1',
            padding: '2px 8px',
            borderRadius: '4px',
            fontWeight: 700
          }}>
            SIMULATED PROTOTYPE FEEDS
          </span>
        </div>

        <div className="grid-4">
          {sensors.map((sn) => (
            <div key={sn.sensor_id} style={{
              background: '#f8fafc',
              border: `1px solid ${sn.health_status === 'HEALTHY' ? '#cbd5e1' : '#fcd34d'}`,
              borderRadius: '8px',
              padding: '12px'
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ fontSize: '0.72rem', fontWeight: 700, color: '#0f172a' }}>
                  {sn.sensor_id}
                </span>
                <span style={{
                  fontSize: '0.68rem',
                  fontWeight: 700,
                  padding: '2px 6px',
                  borderRadius: '4px',
                  background: sn.health_status === 'HEALTHY' ? '#dcfce7' : '#fef3c7',
                  color: sn.health_status === 'HEALTHY' ? '#15803d' : '#b45309'
                }}>
                  {sn.health_status}
                </span>
              </div>

              <div style={{ fontSize: '0.8rem', fontWeight: 600, color: '#334155', marginTop: '4px' }}>
                {sn.station_name}
              </div>

              <div style={{ fontSize: '1.2rem', fontWeight: 800, color: '#092415', marginTop: '4px' }}>
                {sn.latest_value} <span style={{ fontSize: '0.75rem', fontWeight: 500, color: '#64748b' }}>{sn.unit}</span>
              </div>

              <div style={{ fontSize: '0.7rem', color: '#64748b', marginTop: '6px', display: 'flex', justifyContent: 'space-between' }}>
                <span>Battery: <strong>{sn.battery_pct}%</strong></span>
                <span>Flag: <strong>{sn.quality_flag}</strong></span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
