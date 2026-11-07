import React from 'react';
import { ShelterItem } from '../types';
import {
  Shield, AlertTriangle, PhoneCall, Home, CheckCircle2,
  AlertOctagon, LifeBuoy, MapPin, ExternalLink
} from 'lucide-react';
import { SafeImage } from '../components/SafeImage';
import { FEATURE_IMAGES } from '../utils/imageHelpers';

interface SafetyViewProps {
  shelters: ShelterItem[];
  lang: 'mr' | 'en' | 'hi';
}

export const SafetyView: React.FC<SafetyViewProps> = ({ shelters, lang }) => {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
      {/* Header */}
      <div className="view-header-card">
        <div style={{ maxWidth: '820px' }}>
          <span className="view-header-badge">
            <LifeBuoy size={12} />
            <span>{lang === 'mr' ? 'आपत्ती निवारण व सुरक्षा मार्गदर्शक' : 'Community Preparedness & Shelter Registry'}</span>
          </span>
          <h2 className="view-header-title">
            {lang === 'mr'
              ? 'जीव वाचवणारी सावधगिरी व सुरक्षित निवारा'
              : 'Actionable Safety Protocols & Verified Shelters'}
          </h2>
          <p className="view-header-desc">
            {lang === 'mr'
              ? 'सह्याद्री घाटमाथ्यावरील दरड व पुरातून सुरक्षित राहण्यासाठी वैज्ञानिक मार्गदर्शक तत्त्वे आणि अधिकृत मदत केंद्रांची यादी.'
              : 'Scientifically validated disaster survival guidance for residents, trekkers, and commuters in the Western Ghats. All shelters and helplines are verified with official district authorities.'}
          </p>
        </div>
      </div>

      {/* Emergency Phone Helplines Directory */}
      <div className="card" style={{ background: '#f8fafc', borderLeft: '5px solid #2d6a4f', overflow: 'hidden' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '10px', marginBottom: '8px' }}>
          <h3 style={{ fontSize: '1.1rem', fontWeight: 800, color: '#092415', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <PhoneCall size={20} style={{ color: '#2d6a4f' }} />
            {lang === 'mr' ? 'अधिकृत आपत्कालीन हेल्पलाईन क्रमांक' : 'Verified Official Emergency Helplines (Lonavala / Maval)'}
          </h3>
          <span style={{ fontSize: '0.72rem', background: '#dcfce7', color: '#15803d', padding: '3px 8px', borderRadius: '4px', fontWeight: 700 }}>
            24x7 Control Room Active
          </span>
        </div>

        <div className="grid-3" style={{ marginTop: '12px' }}>
          <div style={{ background: '#ffffff', padding: '12px', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
            <div style={{ fontSize: '0.75rem', color: '#64748b' }}>Pune District Disaster Control</div>
            <div style={{ fontSize: '1.2rem', fontWeight: 800, color: '#0f172a', marginTop: '2px' }}>1077 / 020-26123371</div>
            <div style={{ fontSize: '0.72rem', color: '#16a34a', marginTop: '2px' }}>24x7 Emergency Operations</div>
          </div>

          <div style={{ background: '#ffffff', padding: '12px', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
            <div style={{ fontSize: '0.75rem', color: '#64748b' }}>Lonavala City Police Station</div>
            <div style={{ fontSize: '1.2rem', fontWeight: 800, color: '#0f172a', marginTop: '2px' }}>02114-273033 / 112</div>
            <div style={{ fontSize: '0.72rem', color: '#16a34a', marginTop: '2px' }}>Local Law & Order / Rescue</div>
          </div>

          <div style={{ background: '#ffffff', padding: '12px', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
            <div style={{ fontSize: '0.75rem', color: '#64748b' }}>Expressway Highway Safety Patrol</div>
            <div style={{ fontSize: '1.2rem', fontWeight: 800, color: '#0f172a', marginTop: '2px' }}>9822498224</div>
            <div style={{ fontSize: '0.72rem', color: '#16a34a', marginTop: '2px' }}>Bhor Ghat Breakdown & Clearance</div>
          </div>
        </div>
      </div>

      {/* Safety Protocol Cards with Visual Context Headers */}
      <div className="grid-2">
        {/* Landslide Warning Signs */}
        <div className="card" style={{ padding: 0, overflow: 'hidden' }}>
          <div style={{ position: 'relative', width: '100%', height: '130px', background: '#e2e8f0' }}>
            <SafeImage
              src={FEATURE_IMAGES.landslide}
              alt="Landslide slope warning signs"
              badge="Escarpment & Slope Physics"
            />
          </div>
          <div style={{ padding: '1.25rem' }}>
            <div className="card-header" style={{ marginBottom: '8px' }}>
              <h3 className="card-title">
                <AlertTriangle size={18} style={{ color: '#ea580c' }} />
                {lang === 'mr' ? 'दरड कोसळण्याची पूर्वलक्षणे' : 'Pre-Landslide Physical Warning Signs'}
              </h3>
            </div>
            <ul style={{ paddingLeft: '1.25rem', fontSize: '0.85rem', color: '#334155', lineHeight: 1.6 }}>
              <li><strong>Tension Cracks:</strong> Appearance of new ground cracks or fissures on slopes, road cuts, or retaining walls.</li>
              <li><strong>Tilted Trees or Utility Poles:</strong> Trees or electricity poles leaning progressively downslope.</li>
              <li><strong>Sudden Water Emergence:</strong> New springs or sudden muddy water seeping from slope joints.</li>
              <li><strong>Rumbling Sounds:</strong> Deep rumbling or popping trees indicating shear plane detachment.</li>
              <li><strong>Immediate Action:</strong> Evacuate downslope residences laterally (perpendicular to the slide path). Never remain inside lower ground floors.</li>
            </ul>
          </div>
        </div>

        {/* Waterfall & Flash-Flood Precautions */}
        <div className="card" style={{ padding: 0, overflow: 'hidden' }}>
          <div style={{ position: 'relative', width: '100%', height: '130px', background: '#e2e8f0' }}>
            <SafeImage
              src={FEATURE_IMAGES.flashflood}
              alt="Waterfall flash flood precautions"
              badge="Upstream Catchment Surge"
            />
          </div>
          <div style={{ padding: '1.25rem' }}>
            <div className="card-header" style={{ marginBottom: '8px' }}>
              <h3 className="card-title">
                <LifeBuoy size={18} style={{ color: '#0284c7' }} />
                {lang === 'mr' ? 'धबधबा व अचानक पूर सुरक्षा' : 'Waterfall & Flash-Surge Survival Rules'}
              </h3>
            </div>
            <ul style={{ paddingLeft: '1.25rem', fontSize: '0.85rem', color: '#334155', lineHeight: 1.6 }}>
              <li><strong>Water Discoloration:</strong> Clear mountain water turning muddy or carrying floating debris means an upstream surge is arriving.</li>
              <li><strong>Listen for Roaring:</strong> A sudden increase in water roar indicates a flash flood wave. Exit the stream bed immediately.</li>
              <li><strong>Do Not Stand on Overflow Masonry:</strong> Algae-covered basalt weirs at Bhushi Dam become treacherous instantly when water speed rises.</li>
              <li><strong>Alcohol Ban:</strong> Strict zero-tolerance for drinking near waterfalls or dam spillways.</li>
              <li><strong>Never Drive Through Flowing Water:</strong> Just 30cm of moving water can float a passenger car off a causeway.</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Verified Shelters Registry */}
      <div className="card">
        <div className="card-header">
          <h3 className="card-title">
            <Home size={18} style={{ color: 'var(--sahyadri-700)' }} />
            {lang === 'mr' ? 'प्रमाणित आपत्ती निवारा केंद्र (लोणावळा / मावळ)' : 'Verified Disaster Relief Shelters'}
          </h3>
          <span style={{ fontSize: '0.75rem', color: '#64748b' }}>
            Civic Centers Approved by DDMA
          </span>
        </div>

        <div className="grid-3">
          {shelters.map((s) => {
            const name = lang === 'mr' ? s.name_mr : (lang === 'hi' ? s.name_hi : s.name);
            return (
              <div key={s.id} style={{
                background: '#ffffff',
                border: '1px solid #cbd5e1',
                borderRadius: '10px',
                padding: '14px',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between'
              }}>
                <div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <span style={{
                      background: s.status === 'ACTIVE_OPEN' ? '#dcfce7' : '#f1f5f9',
                      color: s.status === 'ACTIVE_OPEN' ? '#15803d' : '#475569',
                      padding: '2px 8px',
                      borderRadius: '4px',
                      fontSize: '0.72rem',
                      fontWeight: 700
                    }}>
                      {s.status}
                    </span>
                    {s.data_origin === 'demo_seed' && (
                      <span style={{
                        background: '#f1f5f9',
                        color: '#64748b',
                        border: '1px solid #cbd5e1',
                        padding: '2px 6px',
                        borderRadius: '4px',
                        fontSize: '0.68rem',
                        fontWeight: 600,
                        marginLeft: '4px'
                      }}>
                        Demo data
                      </span>
                    )}
                    <span style={{ fontSize: '0.72rem', color: '#64748b' }}>
                      Cap: <strong>{s.capacity_persons}</strong> persons
                    </span>
                  </div>

                  <h4 style={{ fontSize: '1rem', fontWeight: 700, color: '#092415', marginTop: '6px' }}>
                    {name}
                  </h4>
                  <div style={{ fontSize: '0.75rem', color: '#64748b', marginTop: '2px' }}>
                    📍 {s.location_name}
                  </div>

                  <div style={{ marginTop: '8px' }}>
                    <div style={{ fontSize: '0.72rem', fontWeight: 600, color: '#334155', marginBottom: '3px' }}>Facilities:</div>
                    <ul style={{ fontSize: '0.74rem', color: '#475569', paddingLeft: '1rem', lineHeight: 1.4 }}>
                      {s.facilities.map((f, idx) => (
                        <li key={idx}>{f}</li>
                      ))}
                    </ul>
                  </div>
                </div>

                <div style={{
                  marginTop: '10px',
                  borderTop: '1px solid #f1f5f9',
                  paddingTop: '6px',
                  fontSize: '0.72rem',
                  color: '#64748b'
                }}>
                  <div>Desk: <strong>{s.official_contact}</strong></div>
                  <div>Managed by: {s.managed_by}</div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
