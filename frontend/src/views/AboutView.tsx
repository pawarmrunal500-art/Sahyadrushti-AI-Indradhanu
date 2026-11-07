import React from 'react';
import { Mountain, Shield, Globe, Award, Target, Compass, CheckCircle2 } from 'lucide-react';

interface AboutViewProps {
  lang: 'mr' | 'en' | 'hi';
}

export const AboutView: React.FC<AboutViewProps> = ({ lang }) => {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
      {/* Hero Header */}
      <div className="view-header-card" style={{ borderLeft: '4px solid var(--accent-yellow)' }}>
        <div style={{ maxWidth: '820px' }}>
          <span className="view-header-badge" style={{ background: 'var(--accent-yellow-light)', color: '#92400e', borderColor: 'var(--accent-yellow)' }}>
            <Target size={12} />
            <span>Mission & Hackathon Scope • UN SDG 13</span>
          </span>
          <h2 className="view-header-title">
            सह्यादृष्टी | SAHYADRUSHTI AI
          </h2>
          <p style={{ fontSize: '1rem', color: 'var(--accent-green-dark)', fontWeight: 700, marginTop: '2px' }}>
            पावसाआधी नव्हे, धोक्याआधी सावध! • See the danger before it becomes a disaster.
          </p>
          <p className="view-header-desc">
            {lang === 'mr'
              ? 'सह्यादृष्टी एआय हे लोणावळा, खंडाळा आणि मावळ परिसरातील तीव्र उतारांवरील दरडी आणि ओढ्यांच्या अचानक पुराची पूर्वसूचना देणारे हायपरलोकल तंत्रज्ञान व्यासपीठ आहे.'
              : 'SAHYADRUSHTI AI is a hyperlocal climate-risk intelligence and disaster early-warning decision-support platform designed specifically for the complex escarpments of Lonavala, Khandala, and surrounding Maval, Maharashtra, India.'}
          </p>
        </div>
      </div>

      {/* Core Hackathon Questions & Answers for Judges */}
      <div className="grid-2">
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">
              <Target size={18} style={{ color: 'var(--sahyadri-700)' }} />
              1. What Core Problem Does It Solve?
            </h3>
          </div>
          <p style={{ fontSize: '0.85rem', color: '#334155', lineHeight: 1.55 }}>
            Conventional weather alerts (e.g., district-level "Orange Alert for Pune") cover thousands of square kilometers. Yet three locations 2 km apart receiving the exact same 150mm rainfall face radically different outcomes: a flat plateau remains safe, while a 36° steep cut slope fails in a landslide, and an upstream gorge produces a lethal flash surge. <strong>SAHYADRUSHTI answers: "Which exact locations may become dangerous, why, and what should people do?"</strong>
          </p>
        </div>

        <div className="card">
          <div className="card-header">
            <h3 className="card-title">
              <Globe size={18} style={{ color: '#0284c7' }} />
              2. Alignment with UN SDG 13.1 & 11.5
            </h3>
          </div>
          <p style={{ fontSize: '0.85rem', color: '#334155', lineHeight: 1.55 }}>
            Targeted specifically at <strong>SDG 13.1</strong> (Strengthening resilience and adaptive capacity to climate-related hazards and natural disasters) and <strong>SDG 11.5</strong> (Significantly reducing the number of deaths and people affected by disasters). Directly aids vulnerable rural settlements, transport lifelines, and domestic tourists unaware of mountain catchment mechanics.
          </p>
        </div>

        <div className="card">
          <div className="card-header">
            <h3 className="card-title">
              <CheckCircle2 size={18} style={{ color: '#16a34a' }} />
              3. What Works Today vs. Field Deployment
            </h3>
          </div>
          <p style={{ fontSize: '0.85rem', color: '#334155', lineHeight: 1.55 }}>
            <strong>Works Today:</strong> End-to-end FastAPI backend, trained geotechnical ML pipeline, Leaflet interactive geospatial map, trilingual interface (मराठी/English/Hindi), historical incident database, CAP-format exporter, scenario simulator, and deterministic demo comparison.<br/>
            <strong>Requires Field Deployment:</strong> Physical installation of 4 in-situ telemetered rain & FDR soil-moisture stations and formal API integration with DDMA Pune control room.
          </p>
        </div>

        <div className="card">
          <div className="card-header">
            <h3 className="card-title">
              <Mountain size={18} style={{ color: '#ea580c' }} />
              4. Scalability Beyond Lonavala
            </h3>
          </div>
          <p style={{ fontSize: '0.85rem', color: '#334155', lineHeight: 1.55 }}>
            The platform's underlying architecture separates pilot-specific geographic coordinates from the core geotechnical physics and inference engine. It can readily scale across the 1,600 km Western Ghats escarpment — including Tamhini Ghat, Mahabaleshwar, Malshej Ghat, Varandha Ghat, and Amboli Ghat — by supplying localized digital elevation models and historical rainfall thresholds.
          </p>
        </div>
      </div>
    </div>
  );
};
