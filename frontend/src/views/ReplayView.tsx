import React, { useState } from 'react';
import { ReplayFrame, DemoScenarioData, LocationItem } from '../types';
import {
  Play, Pause, RotateCcw, Sliders, Zap, AlertTriangle,
  TrendingUp, Mountain, Droplets, Compass, CheckCircle2
} from 'lucide-react';
import { apiClient } from '../api';

interface ReplayViewProps {
  replayTimeline: ReplayFrame[];
  demoScenario: DemoScenarioData | null;
  locations: LocationItem[];
  lang: 'mr' | 'en' | 'hi';
}

export const ReplayView: React.FC<ReplayViewProps> = ({
  replayTimeline,
  demoScenario,
  locations,
  lang
}) => {
  // Replay timeline state
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);

  // Scenario Simulator state
  const [simRain1h, setSimRain1h] = useState(38);
  const [simRain24h, setSimRain24h] = useState(165);
  const [simRain48h, setSimRain48h] = useState(240);
  const [simSoilMoisture, setSimSoilMoisture] = useState(86);
  const [simResults, setSimResults] = useState<any[] | null>(null);
  const [simulating, setSimulating] = useState(false);

  // Fallback replay frames if backend timeline is loading
  const frames: ReplayFrame[] = replayTimeline.length > 0 ? replayTimeline : [
    {
      step_index: 1,
      timestamp_label: "00:00 (T+00h) - Baseline Pre-Monsoon Calm",
      rainfall_1h_mm: 2.1,
      cumulative_24h_mm: 12.0,
      soil_saturation_pct: 42.0,
      storm_stage: "Green / Baseline",
      narrative: "Intermittent light rain across Lonavala plateau. Soil saturation at nominal 42%. All stream stages normal.",
      narrative_mr: "हळुवार पाऊस, मातीची आर्द्रता ४२%. परिस्थिती पूर्णपणे सुरक्षित.",
      points_state: {
        "bhushi_dam": { risk_level: "low", score: 14 },
        "khandala_expressway": { risk_level: "low", score: 18 },
        "rajmachi_route": { risk_level: "moderate", score: 28 },
        "patan_village": { risk_level: "low", score: 12 }
      },
      active_incidents: []
    },
    {
      step_index: 2,
      timestamp_label: "04:00 (T+04h) - Early Morning Ghat Inflow",
      rainfall_1h_mm: 14.5,
      cumulative_24h_mm: 48.0,
      soil_saturation_pct: 58.0,
      storm_stage: "Moderate Inflow",
      narrative: "Orographic enhancement causes steady downpours along the crest line. Runoff begins entering Bhushi Dam reservoir.",
      narrative_mr: "घाटमाथ्यावर पावसाचा जोर वाढला. धरणात पाण्याचा प्रवाह सुरू.",
      points_state: {
        "bhushi_dam": { risk_level: "moderate", score: 38 },
        "khandala_expressway": { risk_level: "moderate", score: 34 },
        "rajmachi_route": { risk_level: "moderate", score: 46 },
        "patan_village": { risk_level: "low", score: 24 }
      },
      active_incidents: []
    },
    {
      step_index: 3,
      timestamp_label: "08:00 (T+08h) - Sustained Downpour",
      rainfall_1h_mm: 28.0,
      cumulative_24h_mm: 96.0,
      soil_saturation_pct: 71.0,
      storm_stage: "Advisory Escalation",
      narrative: "Catchment soil saturation crosses 70%. Inclinometer at Amrutanjan slope detects minor micro-strain. Tourist footfall active.",
      narrative_mr: "पावसाची संततधार. पर्यटकांची गर्दी वाढलेली असताना मातीची संपृक्तता ७०% पार.",
      points_state: {
        "bhushi_dam": { risk_level: "moderate", score: 54 },
        "khandala_expressway": { risk_level: "high", score: 62 },
        "rajmachi_route": { risk_level: "high", score: 68 },
        "patan_village": { risk_level: "moderate", score: 42 }
      },
      active_incidents: []
    },
    {
      step_index: 4,
      timestamp_label: "12:00 (T+12h) - Intense Convective Squall",
      rainfall_1h_mm: 44.5,
      cumulative_24h_mm: 152.0,
      soil_saturation_pct: 84.0,
      storm_stage: "Critical Flash-Surge Window",
      narrative: "Sudden cloudburst-like squall hits Tiger Valley catchment (44.5 mm/h). Bhushi Dam waterfall surges abruptly over steps. AI model issues automated flash surge advisory.",
      narrative_mr: "टायगर व्हॅलीत ढगफुटीसदृश पाऊस. भुशी धरणाच्या पायऱ्यांवर पाण्याचा अचानक प्रचंड लोंढा. मॉडेलकडून तात्काळ इशारा.",
      points_state: {
        "bhushi_dam": { risk_level: "very_high", score: 86 },
        "khandala_expressway": { risk_level: "high", score: 78 },
        "rajmachi_route": { risk_level: "very_high", score: 89 },
        "patan_village": { risk_level: "high", score: 67 }
      },
      active_incidents: ["Bhushi waterfall surge: Police clear tourists from cascade steps."]
    },
    {
      step_index: 5,
      timestamp_label: "16:00 (T+16h) - Critical Slope Saturation",
      rainfall_1h_mm: 32.0,
      cumulative_24h_mm: 194.0,
      soil_saturation_pct: 91.0,
      storm_stage: "Peak Hazard: Escarpment Instability",
      narrative: "Antecedent 48h rainfall surpasses 240mm. Basalt overburden on 36° slope loses effective cohesion. Boulder roll detected on Bhor Ghat rail line km 118.",
      narrative_mr: "४८ तासांत २४० मिमी पाऊस. मंकी हिल ते ठाकूरवाडी दरम्यान रेल्वे ट्रॅकवर दगड पडले. महामार्गावर वेग मर्यादा लागू.",
      points_state: {
        "bhushi_dam": { risk_level: "high", score: 79 },
        "khandala_expressway": { risk_level: "very_high", score: 88 },
        "rajmachi_route": { risk_level: "very_high", score: 94 },
        "patan_village": { risk_level: "very_high", score: 82 }
      },
      active_incidents: ["Thakurwadi rail track rockfall reported; speed restriction enacted.", "Patan village committee evacuates upper terrace homes."]
    },
    {
      step_index: 6,
      timestamp_label: "20:00 (T+20h) - Storm Easing & Post-Event Vigilance",
      rainfall_1h_mm: 8.0,
      cumulative_24h_mm: 218.0,
      soil_saturation_pct: 87.0,
      storm_stage: "Receding Inflow / Lingering Geotechnical Risk",
      narrative: "Rain intensity subsides to 8 mm/h, but saturated slopes remain prone to delayed rotational slump for up to 18 hours. Emergency shelters accommodate 65 evacuated villagers.",
      narrative_mr: "पाऊस मंदावला तरी डोंगरउतार अजूनही धोकादायक स्थितीत. मदत केंद्रात ग्रामस्थांची सोय.",
      points_state: {
        "bhushi_dam": { risk_level: "moderate", score: 52 },
        "khandala_expressway": { risk_level: "high", score: 72 },
        "rajmachi_route": { risk_level: "high", score: 78 },
        "patan_village": { risk_level: "high", score: 70 }
      },
      active_incidents: ["Road clearance crews active at Bhor Ghat.", "Relief center at Bhangarwadi operational."]
    }
  ];

  const currentFrame = frames[currentStepIndex] || frames[0];

  // Auto-play timer
  React.useEffect(() => {
    let timer: any;
    if (isPlaying) {
      timer = setInterval(() => {
        setCurrentStepIndex((prev) => (prev + 1) % frames.length);
      }, 3500);
    }
    return () => clearInterval(timer);
  }, [isPlaying, frames.length]);

  const handleRunSimulation = async () => {
    setSimulating(true);
    const payload = {
      rain_1h_mm: simRain1h,
      rain_24h_mm: simRain24h,
      rain_48h_mm: simRain48h,
      forecast_24h_mm: simRain24h * 0.9,
      soil_moisture_pct: simSoilMoisture,
      baseline_location_ids: ["bhushi_dam", "khandala_expressway", "patan_village", "lonavala_town"]
    };

    const res = await apiClient.runSimulation(payload);
    setSimulating(false);
    if (res && res.results) {
      setSimResults(res.results);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      {/* Signature Replay Banner */}
      <div className="view-header-card" style={{ borderLeft: '4px solid var(--accent-yellow)' }}>
        <div style={{ maxWidth: '820px' }}>
          <span className="view-header-badge" style={{ background: 'var(--accent-yellow-light)', color: '#92400e', borderColor: 'var(--accent-yellow)' }}>
            <Zap size={12} />
            <span>⚡ HACKATHON SIGNATURE FEATURE</span>
          </span>
          <h2 className="view-header-title">
            {lang === 'mr'
              ? 'ऐतिहासिक वादळ रीप्ले व परिस्थिती सिम्युलेटर'
              : 'Historical Storm Event Replay & Geotechnical Scenario Simulator'}
          </h2>
          <p className="view-header-desc">
            {lang === 'mr'
              ? 'जुलै २०२६ च्या मुसळधार पावसात धोका कसा वाढला? वेळेनुसार पावसाचा जोर, मातीची संपृक्तता आणि धरणाच्या सांडव्यावरील पाण्याचा लोंढा रीप्ले करून पहा.'
              : 'Examine how a severe 24-hour monsoon cloudburst evolved across the Sahyadri Ghats. Observe real-time transitions from low baseline into critical escarpment rockfall and waterfall flash surges.'}
          </p>
        </div>
      </div>

      {/* 24-Hour Storm Replay Timeline Control Bar */}
      <div className="replay-timeline-bar">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.5rem' }}>
          <div>
            <span style={{
              background: '#38bdf8',
              color: '#0f172a',
              fontSize: '0.72rem',
              fontWeight: 800,
              padding: '2px 8px',
              borderRadius: '4px',
              textTransform: 'uppercase'
            }}>
              Step {currentStepIndex + 1} of {frames.length}
            </span>
            <h3 style={{ fontSize: '1.15rem', fontWeight: 700, color: '#ffffff', marginTop: '4px' }}>
              {currentFrame.timestamp_label}
            </h3>
          </div>

          {/* Controls */}
          <div style={{ display: 'flex', gap: '8px' }}>
            <button
              onClick={() => setIsPlaying(!isPlaying)}
              className="btn-primary"
              style={{ padding: '6px 14px', fontSize: '0.8rem', background: isPlaying ? '#ea580c' : '#16a34a' }}
            >
              {isPlaying ? <Pause size={14} /> : <Play size={14} />} {isPlaying ? 'Pause' : 'Play Timeline'}
            </button>

            <button
              onClick={() => { setIsPlaying(false); setCurrentStepIndex(0); }}
              className="btn-secondary"
              style={{ padding: '6px 12px', fontSize: '0.8rem', background: '#1e293b', color: '#ffffff', border: '1px solid #334155' }}
            >
              <RotateCcw size={14} /> Reset
            </button>
          </div>
        </div>

        {/* Timeline Slider */}
        <input
          type="range"
          min={0}
          max={frames.length - 1}
          value={currentStepIndex}
          onChange={(e) => {
            setIsPlaying(false);
            setCurrentStepIndex(parseInt(e.target.value));
          }}
          className="timeline-slider"
        />

        <div className="timeline-ticks">
          {frames.map((f, idx) => (
            <span
              key={idx}
              onClick={() => { setIsPlaying(false); setCurrentStepIndex(idx); }}
              style={{
                cursor: 'pointer',
                fontWeight: currentStepIndex === idx ? 800 : 400,
                color: currentStepIndex === idx ? '#38bdf8' : '#94a3b8'
              }}
            >
              T+{idx * 4}h
            </span>
          ))}
        </div>

        {/* Step Meteorological Conditions */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))',
          gap: '12px',
          marginTop: '1.25rem',
          paddingTop: '1rem',
          borderTop: '1px solid #1e293b'
        }}>
          <div>
            <div style={{ fontSize: '0.72rem', color: '#94a3b8' }}>1-Hour Rain Intensity</div>
            <div style={{ fontSize: '1.3rem', fontWeight: 800, color: '#38bdf8' }}>
              {currentFrame.rainfall_1h_mm} mm/h
            </div>
          </div>

          <div>
            <div style={{ fontSize: '0.72rem', color: '#94a3b8' }}>Cumulative 24h Rain</div>
            <div style={{ fontSize: '1.3rem', fontWeight: 800, color: '#ffffff' }}>
              {currentFrame.cumulative_24h_mm} mm
            </div>
          </div>

          <div>
            <div style={{ fontSize: '0.72rem', color: '#94a3b8' }}>Soil Mantle Saturation</div>
            <div style={{ fontSize: '1.3rem', fontWeight: 800, color: currentFrame.soil_saturation_pct > 80 ? '#f87171' : '#34d399' }}>
              {currentFrame.soil_saturation_pct} %
            </div>
          </div>

          <div>
            <div style={{ fontSize: '0.72rem', color: '#94a3b8' }}>Storm Stage</div>
            <div style={{ fontSize: '0.95rem', fontWeight: 700, color: '#f59e0b', marginTop: '4px' }}>
              {currentFrame.storm_stage}
            </div>
          </div>
        </div>

        {/* Narrative Box */}
        <div style={{
          marginTop: '1rem',
          background: '#1e293b',
          padding: '10px 14px',
          borderRadius: '8px',
          fontSize: '0.82rem',
          color: '#e2e8f0',
          lineHeight: 1.45,
          borderLeft: '4px solid #38bdf8'
        }}>
          <strong>{lang === 'mr' ? 'घडामोडींचा अहवाल:' : 'Event Chronology:'}</strong>{' '}
          {lang === 'mr' ? currentFrame.narrative_mr : currentFrame.narrative}
        </div>
      </div>

      {/* Deterministic Hackathon 3-Minute Presentation Comparison */}
      <div className="card" style={{ border: '2px solid #f59e0b', background: '#fffdf5' }}>
        <div className="card-header" style={{ borderBottomColor: '#fde68a' }}>
          <div>
            <span style={{
              background: '#fef3c7',
              color: '#b45309',
              padding: '2px 8px',
              borderRadius: '4px',
              fontSize: '0.72rem',
              fontWeight: 800,
              textTransform: 'uppercase'
            }}>
              Core Problem Proof: Same Rain, Divergent Hazard
            </span>
            <h3 className="card-title" style={{ marginTop: '4px', color: '#78350f' }}>
              {lang === 'mr'
                ? '३-स्थान तुलना: १६० मिमी पाऊस, तरीही धोका पूर्णपणे वेगळा का?'
                : 'Deterministic Proof: Uniform 160mm Rainfall vs 3 Divergent Local Outcomes'}
            </h3>
          </div>
        </div>

        <p style={{ fontSize: '0.85rem', color: '#78350f', lineHeight: 1.4, marginBottom: '1rem' }}>
          {lang === 'mr'
            ? 'जिल्हास्तरीय हवामान इशारा संपूर्ण लोणावळा तालुक्यासाठी एकच दिला जातो. परंतु प्रत्यक्ष धोका कसा बदलतो ते खालील ३ प्रत्यक्ष ठिकाणी पहा:'
            : 'Broad meteorological warnings issue a single "heavy rain" alert for the entire taluka. SAHYADRUSHTI proves how terrain slope, catchment drainage, and antecedent wetness create radically different physical risks under identical rainfall:'}
        </p>

        <div className="grid-3">
          {/* Location A */}
          <div style={{
            background: '#ffffff',
            border: '2px solid #86efac',
            borderRadius: '10px',
            padding: '14px',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-between'
          }}>
            <div>
              <span className="hazard-badge low">Low Risk (Score: 24/100)</span>
              <h4 style={{ fontSize: '1rem', fontWeight: 800, color: '#092415', marginTop: '6px' }}>
                Location A: Ryewood / Town Plateau
              </h4>
              <div style={{ fontSize: '0.75rem', color: '#64748b', marginTop: '2px' }}>
                Slope: <strong>6.5°</strong> • Drainage Dist: <strong>220m</strong>
              </div>
              <div style={{ fontSize: '0.78rem', color: '#15803d', marginTop: '8px', lineHeight: 1.4, background: '#f0fdf4', padding: '8px', borderRadius: '6px' }}>
                <strong>VERDICT: SAFE & STABLE.</strong> Gentle flat plateau (6.5°) rapidly dissipates surface water without shear stress failure.
              </div>
            </div>
          </div>

          {/* Location B */}
          <div style={{
            background: '#ffffff',
            border: '2px solid #fca5a5',
            borderRadius: '10px',
            padding: '14px',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-between',
            boxShadow: '0 0 10px rgba(220, 38, 38, 0.15)'
          }}>
            <div>
              <span className="hazard-badge very_high">Critical Landslide (Score: 82/100)</span>
              <h4 style={{ fontSize: '1rem', fontWeight: 800, color: '#991b1b', marginTop: '6px' }}>
                Location B: Amrutanjan Cut Slope
              </h4>
              <div style={{ fontSize: '0.75rem', color: '#64748b', marginTop: '2px' }}>
                Slope: <strong>36.5°</strong> • Soil Moisture: <strong>86%</strong>
              </div>
              <div style={{ fontSize: '0.78rem', color: '#991b1b', marginTop: '8px', lineHeight: 1.4, background: '#fef2f2', padding: '8px', borderRadius: '6px' }}>
                <strong>VERDICT: CRITICAL LANDSLIDE.</strong> Identical rain on 36.5° steep fractured cut slope saturates basalt overburden, destroying effective friction.
              </div>
            </div>
          </div>

          {/* Location C */}
          <div style={{
            background: '#ffffff',
            border: '2px solid #fdba74',
            borderRadius: '10px',
            padding: '14px',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-between'
          }}>
            <div>
              <span className="hazard-badge high">High Flash-Surge (Score: 78/100)</span>
              <h4 style={{ fontSize: '1rem', fontWeight: 800, color: '#c2410c', marginTop: '6px' }}>
                Location C: Bhushi Downstream Cascade
              </h4>
              <div style={{ fontSize: '0.75rem', color: '#64748b', marginTop: '2px' }}>
                Slope: <strong>24.5°</strong> • Catchment: <strong>4.8 km²</strong>
              </div>
              <div style={{ fontSize: '0.78rem', color: '#c2410c', marginTop: '8px', lineHeight: 1.4, background: '#fff7ed', padding: '8px', borderRadius: '6px' }}>
                <strong>VERDICT: LETHAL WATER SURGE.</strong> 4.8 km² steep upstream Tiger Valley funnels rainfall into sudden hydraulic surge over the steps.
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Interactive Scenario Simulator Panel */}
      <div className="card">
        <div className="card-header">
          <h3 className="card-title">
            <Sliders size={18} style={{ color: 'var(--sahyadri-700)' }} />
            {lang === 'mr' ? 'थेट एआय सिम्युलेटर: "जर पाऊस वाढला तर काय?"' : 'Interactive "What If the Storm Intensifies?" Simulator'}
          </h3>
          <span style={{ fontSize: '0.75rem', color: '#64748b' }}>
            Runs Live Python ML Inference Pipeline
          </span>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.25rem' }}>
          {/* Sliders Input */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', fontWeight: 600 }}>
                <span>1-Hour Rain Intensity (mm/h):</span>
                <span style={{ color: 'var(--sahyadri-700)', fontWeight: 800 }}>{simRain1h} mm/h</span>
              </div>
              <input
                type="range"
                min={0}
                max={90}
                value={simRain1h}
                onChange={(e) => setSimRain1h(parseInt(e.target.value))}
                style={{ width: '100%', accentColor: 'var(--sahyadri-700)' }}
              />
            </div>

            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', fontWeight: 600 }}>
                <span>24-Hour Rainfall (mm):</span>
                <span style={{ color: 'var(--sahyadri-700)', fontWeight: 800 }}>{simRain24h} mm</span>
              </div>
              <input
                type="range"
                min={10}
                max={350}
                value={simRain24h}
                onChange={(e) => setSimRain24h(parseInt(e.target.value))}
                style={{ width: '100%', accentColor: 'var(--sahyadri-700)' }}
              />
            </div>

            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', fontWeight: 600 }}>
                <span>48-Hour Antecedent Rain (mm):</span>
                <span style={{ color: 'var(--sahyadri-700)', fontWeight: 800 }}>{simRain48h} mm</span>
              </div>
              <input
                type="range"
                min={20}
                max={450}
                value={simRain48h}
                onChange={(e) => setSimRain48h(parseInt(e.target.value))}
                style={{ width: '100%', accentColor: 'var(--sahyadri-700)' }}
              />
            </div>

            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', fontWeight: 600 }}>
                <span>Soil Moisture Saturation (%):</span>
                <span style={{ color: '#ea580c', fontWeight: 800 }}>{simSoilMoisture} %</span>
              </div>
              <input
                type="range"
                min={20}
                max={100}
                value={simSoilMoisture}
                onChange={(e) => setSimSoilMoisture(parseInt(e.target.value))}
                style={{ width: '100%', accentColor: '#ea580c' }}
              />
            </div>

            <button
              onClick={handleRunSimulation}
              disabled={simulating}
              className="btn-primary"
              style={{ padding: '0.75rem', marginTop: '8px' }}
            >
              <Zap size={16} /> {simulating ? 'Calculating Inference...' : 'Run Geotechnical Stress Test'}
            </button>
          </div>

          {/* Simulation Output Cards */}
          <div>
            <div style={{ fontSize: '0.82rem', fontWeight: 700, color: '#092415', marginBottom: '8px' }}>
              Simulated Risk Outcomes Across Locations:
            </div>

            {!simResults ? (
              <div style={{
                background: '#f8fafc',
                border: '1px dashed #cbd5e1',
                borderRadius: '8px',
                padding: '2rem 1rem',
                textAlign: 'center',
                color: '#64748b',
                fontSize: '0.82rem'
              }}>
                Adjust sliders and click "Run Geotechnical Stress Test" to pass inputs through the trained machine learning pipeline.
              </div>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                {simResults.map((r, idx) => (
                  <div key={idx} style={{
                    background: '#ffffff',
                    border: '1px solid #e2e8f0',
                    borderRadius: '8px',
                    padding: '10px 12px',
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center'
                  }}>
                    <div>
                      <div style={{ fontWeight: 700, fontSize: '0.88rem', color: '#092415' }}>
                        {r.location_name}
                      </div>
                      <div style={{ fontSize: '0.72rem', color: '#64748b' }}>
                        Slope: {r.slope_deg}° • Baseline: {r.baseline_score}
                      </div>
                    </div>

                    <div style={{ textAlign: 'right' }}>
                      <span className={`hazard-badge ${r.simulated_level}`}>
                        Score: {r.simulated_score} / 100
                      </span>
                      <div style={{
                        fontSize: '0.72rem',
                        fontWeight: 700,
                        color: r.delta_score >= 0 ? '#dc2626' : '#16a34a',
                        marginTop: '2px'
                      }}>
                        {r.delta_score >= 0 ? `+${r.delta_score}` : r.delta_score} from Baseline
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
