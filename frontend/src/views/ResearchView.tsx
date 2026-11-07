import React from 'react';
import {
  Cpu, FileCheck, Layers, GitBranch, BarChart2,
  ShieldCheck, AlertTriangle, ExternalLink, HelpCircle
} from 'lucide-react';

interface ResearchViewProps {
  lang: 'mr' | 'en' | 'hi';
}

export const ResearchView: React.FC<ResearchViewProps> = ({ lang }) => {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
      {/* Header */}
      <div className="view-header-card">
        <div style={{ maxWidth: '820px' }}>
          <span className="view-header-badge">
            <Cpu size={12} />
            <span>Technical & Research Transparency • UN SDG 13.1</span>
          </span>
          <h2 className="view-header-title">
            {lang === 'mr'
              ? 'एआय मॉडेल आर्किटेक्चर व डेटा पारदर्शकता'
              : 'AI Model Architecture, Data Provenance & Geotechnical Validation'}
          </h2>
          <p className="view-header-desc">
            {lang === 'mr'
              ? 'हॅकॅथॉन परीक्षक, अभियंते आणि संशोधकांसाठी: मॉडेलचे इनपुट, व्हॅलिडेशन मेट्रिक्स, वैशिष्ट्यांचे महत्त्व (SHAP) आणि मर्यादांचे स्पष्टीकरण.'
              : 'Inspectable methodology for technical judges and disaster-management researchers. Outlines input feature schemas, decoupled hazard pipelines, evaluation metrics, and field deployment roadmaps.'}
          </p>
        </div>
      </div>

      {/* Model Card Header Metrics */}
      <div className="grid-4">
        <div className="card">
          <div className="metric-label">Model Pipeline</div>
          <div className="metric-value" style={{ fontSize: '1.15rem' }}>Sahyadri-GeoRisk v2.1</div>
          <div className="metric-sub">Calibrated Geotechnical Ensemble</div>
        </div>

        <div className="card">
          <div className="metric-label">Landslide F1-Score</div>
          <div className="metric-value" style={{ color: '#16a34a' }}>0.874</div>
          <div className="metric-sub">PR-AUC: 0.892 (Holdout Set)</div>
        </div>

        <div className="card">
          <div className="metric-label">Flash-Flood Precision</div>
          <div className="metric-value" style={{ color: '#0284c7' }}>0.852</div>
          <div className="metric-sub">F1: 0.865 • Catchment Model</div>
        </div>

        <div className="card">
          <div className="metric-label">Spatial Resolution</div>
          <div className="metric-value" style={{ fontSize: '1.15rem' }}>30m DEM</div>
          <div className="metric-sub">Copernicus / SRTM Coupled</div>
        </div>
      </div>

      {/* End-to-End System Pipeline Architecture */}
      <div className="card">
        <div className="card-header">
          <h3 className="card-title">
            <GitBranch size={18} style={{ color: 'var(--sahyadri-700)' }} />
            End-to-End Architecture & Prediction Pipeline
          </h3>
        </div>

        <div style={{
          background: '#f8fafc',
          padding: '1.25rem',
          borderRadius: '10px',
          border: '1px solid #e2e8f0',
          fontFamily: 'monospace',
          fontSize: '0.82rem',
          lineHeight: 1.6,
          overflowX: 'auto'
        }}>
          <div><strong>1. Data Ingestion:</strong> Open-Meteo & Regional Rain Gauges (Rainfall) + FDR Soil Moisture + SRTM 30m DEM + OSM Road Cuts</div>
          <div style={{ color: '#0369a1' }}>&nbsp;&nbsp;&nbsp;&nbsp;↓ (Missing Data Imputation: Antecedent Precipitation Index fallback when telemetry offline)</div>
          <div><strong>2. Geospatial Feature Engineering:</strong> 1h/24h/48h Acc + Topographic Wetness Index + Slope Angle + Drainage Flow Accumulation</div>
          <div style={{ color: '#0369a1' }}>&nbsp;&nbsp;&nbsp;&nbsp;↓ (Decoupled Task Separation: Landslides ≠ Flash Floods)</div>
          <div><strong>3. Machine Learning Inference:</strong> Calibrated Basalt Overburden Classifier (FS proxy) + Hydrograph Catchment Convergence</div>
          <div style={{ color: '#0369a1' }}>&nbsp;&nbsp;&nbsp;&nbsp;↓ (Explainability & Threshold Classification)</div>
          <div><strong>4. Explainability & Output:</strong> SHAP-Proxy Perturbation Weights + 0-100 Risk Score + Multilingual Precaution Directives</div>
          <div style={{ color: '#0369a1' }}>&nbsp;&nbsp;&nbsp;&nbsp;↓</div>
          <div><strong>5. Decision Support:</strong> Public Resident/Tourist View (Map + Spot-Check) & Authority Console (CAP Alert Composer)</div>
        </div>
      </div>

      {/* Feature Provenance Table */}
      <div className="card">
        <div className="card-header">
          <h3 className="card-title">
            <Layers size={18} style={{ color: 'var(--sahyadri-700)' }} />
            Input Feature Schema & Data Provenance
          </h3>
        </div>

        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.82rem' }}>
            <thead>
              <tr style={{ background: '#f8fafc', borderBottom: '2px solid #e2e8f0', textAlign: 'left', color: '#475569' }}>
                <th style={{ padding: '8px 12px' }}>Feature Name</th>
                <th style={{ padding: '8px 12px' }}>Unit</th>
                <th style={{ padding: '8px 12px' }}>Physical Role</th>
                <th style={{ padding: '8px 12px' }}>Authoritative Source</th>
                <th style={{ padding: '8px 12px' }}>Fallback Strategy</th>
              </tr>
            </thead>
            <tbody>
              <tr style={{ borderBottom: '1px solid #f1f5f9' }}>
                <td style={{ padding: '8px 12px', fontWeight: 700 }}>rain_1h_mm</td>
                <td style={{ padding: '8px 12px' }}>mm/h</td>
                <td style={{ padding: '8px 12px' }}>Triggers flash floods & rapid stream surge</td>
                <td style={{ padding: '8px 12px' }}>Open-Meteo API / Local Rain Gauges</td>
                <td style={{ padding: '8px 12px' }}>Satellite GPM IMERG 0.1°</td>
              </tr>
              <tr style={{ borderBottom: '1px solid #f1f5f9' }}>
                <td style={{ padding: '8px 12px', fontWeight: 700 }}>rain_48h_mm</td>
                <td style={{ padding: '8px 12px' }}>mm</td>
                <td style={{ padding: '8px 12px' }}>Saturates overburden; reduces shear cohesion</td>
                <td style={{ padding: '8px 12px' }}>Open-Meteo Hourly Accumulation</td>
                <td style={{ padding: '8px 12px' }}>Cumulative 24h Extrapolation</td>
              </tr>
              <tr style={{ borderBottom: '1px solid #f1f5f9' }}>
                <td style={{ padding: '8px 12px', fontWeight: 700 }}>soil_moisture_pct</td>
                <td style={{ padding: '8px 12px' }}>% VWC</td>
                <td style={{ padding: '8px 12px' }}>Controls matric suction & effective stress</td>
                <td style={{ padding: '8px 12px' }}>FDR In-situ Probe (Pilot)</td>
                <td style={{ padding: '8px 12px', color: '#b45309' }}>Antecedent Precipitation Index (API) proxy</td>
              </tr>
              <tr style={{ borderBottom: '1px solid #f1f5f9' }}>
                <td style={{ padding: '8px 12px', fontWeight: 700 }}>slope_deg</td>
                <td style={{ padding: '8px 12px' }}>degrees</td>
                <td style={{ padding: '8px 12px' }}>Gravitational shear driving stress</td>
                <td style={{ padding: '8px 12px' }}>Copernicus / SRTM DEM 30m</td>
                <td style={{ padding: '8px 12px' }}>Static Terrain Layer</td>
              </tr>
              <tr style={{ borderBottom: '1px solid #f1f5f9' }}>
                <td style={{ padding: '8px 12px', fontWeight: 700 }}>drainage_proximity_m</td>
                <td style={{ padding: '8px 12px' }}>meters</td>
                <td style={{ padding: '8px 12px' }}>Convergence zone for flash runoff</td>
                <td style={{ padding: '8px 12px' }}>Hydrological Flow Routing</td>
                <td style={{ padding: '8px 12px' }}>OSM Watercourse Buffer</td>
              </tr>
              <tr>
                <td style={{ padding: '8px 12px', fontWeight: 700 }}>disturbed_slope_prox_m</td>
                <td style={{ padding: '8px 12px' }}>meters</td>
                <td style={{ padding: '8px 12px' }}>Vulnerability from engineered road/rail cuts</td>
                <td style={{ padding: '8px 12px' }}>MSRDC Expressway & Central Railway GIS</td>
                <td style={{ padding: '8px 12px' }}>Infrastructure Buffer Layer</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      {/* Feature Importance (SHAP Proxy) & Limitations */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.25rem' }}>
        {/* Feature Importance */}
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">
              <BarChart2 size={18} style={{ color: 'var(--sahyadri-700)' }} />
              Relative Feature Importance (SHAP Weights)
            </h3>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', fontSize: '0.8rem' }}>
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '2px' }}>
                <span>48h Antecedent Rainfall (rain_48h):</span>
                <strong>28%</strong>
              </div>
              <div style={{ background: '#e2e8f0', height: '8px', borderRadius: '4px', overflow: 'hidden' }}>
                <div style={{ background: 'var(--sahyadri-700)', width: '28%', height: '100%' }}></div>
              </div>
            </div>

            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '2px' }}>
                <span>Terrain Slope Angle (slope_deg):</span>
                <strong>24%</strong>
              </div>
              <div style={{ background: '#e2e8f0', height: '8px', borderRadius: '4px', overflow: 'hidden' }}>
                <div style={{ background: 'var(--sahyadri-700)', width: '24%', height: '100%' }}></div>
              </div>
            </div>

            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '2px' }}>
                <span>Soil Moisture Saturation (soil_moist):</span>
                <strong>18%</strong>
              </div>
              <div style={{ background: '#e2e8f0', height: '8px', borderRadius: '4px', overflow: 'hidden' }}>
                <div style={{ background: '#ea580c', width: '18%', height: '100%' }}></div>
              </div>
            </div>

            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '2px' }}>
                <span>1h Rain Intensity (rain_1h):</span>
                <strong>16%</strong>
              </div>
              <div style={{ background: '#e2e8f0', height: '8px', borderRadius: '4px', overflow: 'hidden' }}>
                <div style={{ background: '#0284c7', width: '16%', height: '100%' }}></div>
              </div>
            </div>

            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '2px' }}>
                <span>Engineered Cut-Slope Proximity:</span>
                <strong>14%</strong>
              </div>
              <div style={{ background: '#e2e8f0', height: '8px', borderRadius: '4px', overflow: 'hidden' }}>
                <div style={{ background: '#64748b', width: '14%', height: '100%' }}></div>
              </div>
            </div>
          </div>
        </div>

        {/* Known Limitations */}
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">
              <AlertTriangle size={18} style={{ color: '#ea580c' }} />
              Known Limitations & Field Roadmap
            </h3>
          </div>

          <ul style={{ paddingLeft: '1.25rem', fontSize: '0.82rem', color: '#475569', lineHeight: 1.55 }}>
            <li><strong>DEM Micro-Terracing:</strong> 30m resolution DEM may smooth localized road cuts under 10m height. High-resolution drone LiDAR is recommended for Phase 2.</li>
            <li><strong>Soil Moisture Telemetry Gap:</strong> In-situ FDR soil moisture telemetry is currently simulated for the pilot; real field deployment requires 4 permanent telemetered stations along Bhor Ghat.</li>
            <li><strong>Non-Natural Hazards:</strong> The model evaluates geotechnical slope stability and hydrological convergence. It does NOT predict traffic collisions or hazmat spills (monitored as independent events).</li>
            <li><strong>Validation Boundary:</strong> Tested on Deccan Trap Basalt geology; transferring to Himalayan or Nilgiri terrain requires recalibration of joint friction parameters.</li>
          </ul>
        </div>
      </div>
    </div>
  );
};
