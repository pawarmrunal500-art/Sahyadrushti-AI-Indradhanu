import React, { useEffect, useRef, useState, useCallback } from 'react';
import L from 'leaflet';
import { LocationItem, IncidentRecord, ShelterItem, CorridorItem, SensorNode, RiskLevel, HazardType } from '../types';
import {
  Layers, RotateCcw, Search, Eye, ShieldAlert, Mountain, Compass,
  X, MapPin, CheckCircle2, AlertCircle, Loader2
} from 'lucide-react';
import {
  searchLocalGazetteer, toLocationItem, RegionalPlace, findNearestStation
} from '../utils/gazetteer';
import { apiClient } from '../api';

interface InteractiveMapProps {
  locations: LocationItem[];
  incidents: IncidentRecord[];
  shelters: ShelterItem[];
  corridors: CorridorItem[];
  sensors: SensorNode[];
  selectedLocation: LocationItem | null;
  onSelectLocation: (loc: LocationItem) => void;
  lang: 'mr' | 'en' | 'hi';
}

export const InteractiveMap: React.FC<InteractiveMapProps> = ({
  locations,
  incidents,
  shelters,
  corridors,
  sensors,
  selectedLocation,
  onSelectLocation,
  lang
}) => {
  const mapContainerRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<L.Map | null>(null);
  const layerGroupsRef = useRef<{ [key: string]: L.LayerGroup }>({});

  const [basemapType, setBasemapType] = useState<'topo' | 'osm'>('topo');
  const [showLandslideLayer, setShowLandslideLayer] = useState(true);
  const [showFloodLayer, setShowFloodLayer] = useState(true);
  const [showTouristLayer, setShowTouristLayer] = useState(true);
  const [showCorridorsLayer, setShowCorridorsLayer] = useState(true);
  const [showIncidentsLayer, setShowIncidentsLayer] = useState(true);
  const [showSheltersLayer, setShowSheltersLayer] = useState(true);
  const [showSensorsLayer, setShowSensorsLayer] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [isSearching, setIsSearching] = useState(false);
  const [searchFeedback, setSearchFeedback] = useState<{ type: 'success' | 'error' | 'info'; message: string } | null>(null);
  const [suggestions, setSuggestions] = useState<any[]>([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const searchContainerRef = useRef<HTMLDivElement>(null);

  // Close suggestions when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (searchContainerRef.current && !searchContainerRef.current.contains(event.target as Node)) {
        setShowSuggestions(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Default Pilot Region Center: Lonavala - Khandala Bhor Ghat (18.755, 73.395)
  const LONAVALA_CENTER: [number, number] = [18.755, 73.395];
  const DEFAULT_ZOOM = 13;

  // Initialize Leaflet Map
  useEffect(() => {
    if (!mapContainerRef.current) return;

    if (!mapInstanceRef.current) {
      const map = L.map(mapContainerRef.current, {
        center: LONAVALA_CENTER,
        zoom: DEFAULT_ZOOM,
        minZoom: 10,
        maxZoom: 17,
        zoomControl: false
      });

      L.control.zoom({ position: 'bottomright' }).addTo(map);

      // Attribution control with official licensing
      L.control.attribution({
        position: 'bottomleft',
        prefix: '© OpenStreetMap contributors, OpenTopoMap, NASA/SRTM DEM'
      }).addTo(map);

      mapInstanceRef.current = map;

      // Create layer groups
      layerGroupsRef.current = {
        basemap: L.layerGroup().addTo(map),
        landslide: L.layerGroup().addTo(map),
        flood: L.layerGroup().addTo(map),
        tourist: L.layerGroup().addTo(map),
        corridors: L.layerGroup().addTo(map),
        incidents: L.layerGroup().addTo(map),
        shelters: L.layerGroup().addTo(map),
        sensors: L.layerGroup().addTo(map),
        search: L.layerGroup().addTo(map)
      };
    }

    return () => {
      // Cleanup on unmount
      if (mapInstanceRef.current) {
        mapInstanceRef.current.remove();
        mapInstanceRef.current = null;
      }
    };
  }, []);

  // Update Basemap Tiles (Topographic Hillshade vs Standard OSM)
  useEffect(() => {
    if (!mapInstanceRef.current || !layerGroupsRef.current.basemap) return;
    const baseGroup = layerGroupsRef.current.basemap;
    baseGroup.clearLayers();

    if (basemapType === 'topo') {
      // OpenTopoMap for true Sahyadri relief and elevation contour lines
      L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
        maxZoom: 16,
        attribution: 'Map data: &copy; OpenStreetMap contributors, SRTM | Map style: &copy; OpenTopoMap (CC-BY-SA)'
      }).addTo(baseGroup);
    } else {
      // Standard OSM Carto
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
        attribution: '&copy; OpenStreetMap contributors'
      }).addTo(baseGroup);
    }
  }, [basemapType]);

  // Render Markers and Features based on Layer Toggles
  useEffect(() => {
    if (!mapInstanceRef.current) return;

    // 1. Locations Layer (Split into Tourist vs Landslide vs Flood)
    const touristGroup = layerGroupsRef.current.tourist;
    const lsGroup = layerGroupsRef.current.landslide;
    const ffGroup = layerGroupsRef.current.flood;

    touristGroup?.clearLayers();
    lsGroup?.clearLayers();
    ffGroup?.clearLayers();

    locations.forEach((loc) => {
      const isSelected = selectedLocation?.id === loc.id;
      const markerSize = isSelected ? 38 : 30;
      const borderStyle = isSelected ? '3px solid #ffffff' : '2px solid #ffffff';

      // Custom HTML Pin Icon
      const iconHtml = `
        <div class="custom-hazard-pin ${loc.status}" style="width: ${markerSize}px; height: ${markerSize}px; border: ${borderStyle}; font-size: ${isSelected ? '0.85rem' : '0.72rem'}">
          ${loc.risk_score}
        </div>
      `;

      const customIcon = L.divIcon({
        className: 'custom-leaflet-marker',
        html: iconHtml,
        iconSize: [markerSize, markerSize],
        iconAnchor: [markerSize / 2, markerSize / 2]
      });

      const marker = L.marker(loc.coordinates, { icon: customIcon });

      marker.bindTooltip(`
        <div style="font-family: inherit; font-size: 0.82rem; line-height: 1.3">
          <strong>${lang === 'mr' ? loc.name_mr : (lang === 'hi' ? loc.name_hi : loc.name)}</strong><br/>
          <span style="color: ${getRiskColor(loc.status)}; font-weight: 700">${loc.status_label}</span><br/>
          <small>Risk Index: ${loc.risk_score}/100${(loc.score_capped || loc.risk_score >= 96) ? ` (Capped at ${loc.current_hazard === 'landslide' ? 98 : 96})` : ''} • Slope: ${loc.slope_deg}°</small>
        </div>
      `, { direction: 'top', offset: [0, -14] });

      marker.on('click', () => {
        onSelectLocation(loc);
      });

      // Target to appropriate layer group
      if (loc.category === 'tourist_spot' && showTouristLayer) {
        touristGroup?.addLayer(marker);
      } else if (loc.current_hazard === 'landslide' && showLandslideLayer) {
        lsGroup?.addLayer(marker);
      } else if (loc.current_hazard === 'flash_flood' && showFloodLayer) {
        ffGroup?.addLayer(marker);
      }
    });

    // 2. Corridors Layer
    const corridorGroup = layerGroupsRef.current.corridors;
    corridorGroup?.clearLayers();
    if (showCorridorsLayer) {
      corridors.forEach((c) => {
        const color = c.current_status === 'CLOSED' ? '#dc2626' : (c.current_status === 'CAUTION' ? '#ea580c' : '#059669');
        const latlngs: [number, number][] = [
          c.coordinates_start,
          c.center_coords,
          c.coordinates_end
        ];

        const line = L.polyline(latlngs, {
          color: color,
          weight: 6,
          opacity: 0.85,
          dashArray: c.current_status === 'CAUTION' ? '8, 6' : undefined
        });

        line.bindTooltip(`
          <div style="font-size: 0.8rem">
            <strong>${c.corridor_name}</strong><br/>
            <span>${c.segment_name}</span><br/>
            <strong>Status: ${c.current_status}</strong>
          </div>
        `);

        corridorGroup?.addLayer(line);
      });
    }

    // 3. Historical Incidents Layer
    const incidentGroup = layerGroupsRef.current.incidents;
    incidentGroup?.clearLayers();
    if (showIncidentsLayer) {
      incidents.forEach((inc) => {
        const iconHtml = `
          <div class="custom-hazard-pin incident" title="${inc.title}">
            ⚠️
          </div>
        `;
        const icon = L.divIcon({
          className: 'custom-leaflet-marker',
          html: iconHtml,
          iconSize: [28, 28],
          iconAnchor: [14, 14]
        });

        const marker = L.marker(inc.coordinates, { icon });
        marker.bindTooltip(`
          <div style="font-size: 0.8rem; max-width: 220px">
            <strong>${lang === 'mr' ? inc.title_mr : inc.title}</strong><br/>
            <small>${inc.date_time.slice(0, 10)} • ${inc.verification_status}</small><br/>
            <span style="color: #64748b">${inc.impact_summary}</span>
          </div>
        `);
        incidentGroup?.addLayer(marker);
      });
    }

    // 4. Shelters Layer
    const shelterGroup = layerGroupsRef.current.shelters;
    shelterGroup?.clearLayers();
    if (showSheltersLayer) {
      shelters.forEach((s) => {
        const iconHtml = `
          <div class="custom-hazard-pin shelter" title="${s.name}">
            🏠
          </div>
        `;
        const icon = L.divIcon({
          className: 'custom-leaflet-marker',
          html: iconHtml,
          iconSize: [28, 28],
          iconAnchor: [14, 14]
        });

        const marker = L.marker(s.coordinates, { icon });
        marker.bindTooltip(`
          <div style="font-size: 0.8rem">
            <strong>${lang === 'mr' ? s.name_mr : s.name}</strong><br/>
            <span>Capacity: ${s.capacity_persons} persons</span><br/>
            <small style="color: #0284c7">Status: ${s.status}</small>
          </div>
        `);
        shelterGroup?.addLayer(marker);
      });
    }

    // 5. Sensors Layer
    const sensorGroup = layerGroupsRef.current.sensors;
    sensorGroup?.clearLayers();
    if (showSensorsLayer) {
      sensors.forEach((sn) => {
        const iconHtml = `
          <div class="custom-hazard-pin sensor" title="${sn.station_name}">
            📡
          </div>
        `;
        const icon = L.divIcon({
          className: 'custom-leaflet-marker',
          html: iconHtml,
          iconSize: [26, 26],
          iconAnchor: [13, 13]
        });

        const marker = L.marker(sn.coordinates, { icon });
        marker.bindTooltip(`
          <div style="font-size: 0.8rem">
            <strong>${sn.station_name}</strong><br/>
            <span>${sn.latest_value} ${sn.unit}</span><br/>
            <small>Battery: ${sn.battery_pct}% • [SIMULATED SENSOR]</small>
          </div>
        `);
        sensorGroup?.addLayer(marker);
      });
    }

  }, [
    locations, incidents, shelters, corridors, sensors, selectedLocation,
    showTouristLayer, showLandslideLayer, showFloodLayer, showCorridorsLayer,
    showIncidentsLayer, showSheltersLayer, showSensorsLayer, lang
  ]);

  // Handle selected location pan
  useEffect(() => {
    if (!mapInstanceRef.current || !selectedLocation) return;
    mapInstanceRef.current.flyTo(selectedLocation.coordinates, 14, {
      duration: 1.2
    });
  }, [selectedLocation]);

  // Point and zoom to a searched location
  const selectAndZoomPlace = useCallback((place: any) => {
    if (!mapInstanceRef.current) return;

    // 1. Clear previous search pins
    const searchGroup = layerGroupsRef.current.search;
    searchGroup?.clearLayers();

    // 2. Build custom animated pin marker
    const iconHtml = `
      <div class="custom-search-marker-pin" title="${place.name}">
        <div class="search-pulse-ring"></div>
        <div class="search-pin-core">📍</div>
      </div>
    `;

    const customIcon = L.divIcon({
      className: 'custom-search-marker-wrapper',
      html: iconHtml,
      iconSize: [40, 40],
      iconAnchor: [20, 20]
    });

    const marker = L.marker(place.coordinates, { icon: customIcon });

    const nearestInfo = findNearestStation(place.coordinates, locations);
    const nearestText = nearestInfo
      ? `${nearestInfo.station.name} (~${nearestInfo.distanceKm.toFixed(1)} km, Risk: ${nearestInfo.station.risk_score}/100)`
      : null;

    const placeTitle = lang === 'mr' ? (place.name_mr || place.name) : (lang === 'hi' ? (place.name_hi || place.name) : place.name);

    marker.bindPopup(`
      <div style="font-family: inherit; font-size: 0.84rem; line-height: 1.45; min-width: 210px; padding: 2px;">
        <div style="background: #2563eb; color: #ffffff; font-size: 0.68rem; font-weight: 700; padding: 2px 7px; border-radius: 4px; display: inline-block; margin-bottom: 4px;">
          📍 ${lang === 'mr' ? 'शोधलेले क्षेत्र' : 'Searched Region'}
        </div>
        <div style="font-weight: 800; font-size: 1.05rem; color: #0f172a;">${placeTitle}</div>
        ${place.name_mr && lang !== 'mr' ? `<div style="font-size: 0.8rem; color: #166534; font-weight: 600;">${place.name_mr}</div>` : ''}
        <div style="font-size: 0.74rem; color: #64748b; margin-top: 3px;">
          ${place.region || 'Western Ghats / Maval Corridor'}
        </div>
        <div style="margin-top: 6px; padding-top: 6px; border-top: 1px solid #e2e8f0; font-size: 0.72rem; color: #334155;">
          <div><strong>📍 Coords:</strong> ${place.coordinates[0].toFixed(4)}°N, ${place.coordinates[1].toFixed(4)}°E</div>
          <div><strong>🏔️ Elev / Slope:</strong> ${place.elevation_m || 625}m MSL • ${place.slope_deg || 6.5}°</div>
          ${nearestText ? `<div style="margin-top: 3px;"><strong>📡 Nearest Sensor:</strong> ${nearestText}</div>` : ''}
        </div>
        <div style="margin-top: 6px; font-size: 0.72rem; color: #047857; background: #f0fdf4; border: 1px solid #bbf7d0; padding: 4px 6px; border-radius: 4px;">
          ${lang === 'mr' ? (place.guidance_mr || place.guidance) : (lang === 'hi' ? (place.guidance_hi || place.guidance) : place.guidance)}
        </div>
      </div>
    `, { autoClose: false, closeOnClick: false });

    searchGroup?.addLayer(marker);
    marker.openPopup();

    // 3. Smooth flyTo camera animation and zoom (level 14)
    mapInstanceRef.current.flyTo(place.coordinates, 14, {
      duration: 1.4
    });

    // 4. Update selected location in parent state so details panel updates
    const fullLocItem = toLocationItem(place, locations);
    onSelectLocation(fullLocItem);

    // 5. Update UI feedback
    setSearchQuery(placeTitle);
    setShowSuggestions(false);
    setSearchFeedback({
      type: 'success',
      message: lang === 'mr' 
        ? `📍 '${placeTitle}' क्षेत्र दर्शवले व झूम केले!`
        : `📍 Pointed and zoomed to '${placeTitle}' region!`
    });
  }, [locations, lang, onSelectLocation]);

  const handleClearSearch = () => {
    setSearchQuery('');
    setSuggestions([]);
    setShowSuggestions(false);
    setSearchFeedback(null);
    layerGroupsRef.current.search?.clearLayers();
    if (mapInstanceRef.current) {
      mapInstanceRef.current.flyTo(LONAVALA_CENTER, DEFAULT_ZOOM, { duration: 1 });
    }
  };

  const handleResetView = () => {
    handleClearSearch();
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = e.target.value;
    setSearchQuery(val);
    if (searchFeedback) setSearchFeedback(null);

    if (val.trim().length >= 1) {
      const matches = searchLocalGazetteer(val.trim(), locations).slice(0, 6);
      setSuggestions(matches);
      setShowSuggestions(matches.length > 0);
    } else {
      setSuggestions([]);
      setShowSuggestions(false);
    }
  };

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    const cleanQuery = searchQuery.trim();
    if (!cleanQuery) return;

    setShowSuggestions(false);

    // 1. Search in local gazetteer (Kamshet, Karla, Malavli, etc. + pilot locations)
    const localMatches = searchLocalGazetteer(cleanQuery, locations);
    if (localMatches.length > 0) {
      selectAndZoomPlace(localMatches[0]);
      return;
    }

    // 2. Fall back to backend / online geocoding
    setIsSearching(true);
    setSearchFeedback({
      type: 'info',
      message: lang === 'mr' ? 'ठिकाण शोधत आहे...' : 'Searching region...'
    });

    try {
      const geoResults = await apiClient.geocode(cleanQuery);
      if (geoResults && geoResults.length > 0) {
        selectAndZoomPlace(geoResults[0]);
      } else {
        setSearchFeedback({
          type: 'error',
          message: lang === 'mr'
            ? `'${cleanQuery}' सापडले नाही. कामशेत, कार्ला, पवना किंवा लोणावळा शोधा.`
            : `No region found for '${cleanQuery}'. Try searching Kamshet, Karla, Pawna, or Lonavala.`
        });
      }
    } catch (err) {
      setSearchFeedback({
        type: 'error',
        message: lang === 'mr' ? 'शोध अयशस्वी झाला.' : 'Search failed. Please try again.'
      });
    } finally {
      setIsSearching(false);
    }
  };

  return (
    <div className="map-wrapper" style={{ height: '100%', minHeight: '520px' }}>
      {/* Map DOM Target */}
      <div ref={mapContainerRef} className="map-element" />

      {/* Floating Controls & Search */}
      <div className="map-floating-panel" style={{ width: '310px', maxWidth: 'calc(100% - 24px)' }}>
        <div className="map-search-container" ref={searchContainerRef}>
          <form onSubmit={handleSearch} style={{ display: 'flex', gap: '4px', marginBottom: '4px' }}>
            <div style={{ position: 'relative', flex: 1 }}>
              <input
                type="text"
                placeholder={lang === 'mr' ? 'कामशेत, कार्ला, लोणावळा शोधा...' : 'Search Kamshet, Karla, Lonavala...'}
                value={searchQuery}
                onChange={handleInputChange}
                onFocus={() => {
                  if (searchQuery.trim().length >= 1 && suggestions.length > 0) {
                    setShowSuggestions(true);
                  }
                }}
                className="form-input"
                style={{ paddingLeft: '28px', paddingRight: searchQuery ? '24px' : '8px', fontSize: '0.8rem', padding: '5px 24px 5px 28px', width: '100%' }}
              />
              <Search size={14} style={{ position: 'absolute', left: '8px', top: '9px', color: '#64748b' }} />
              {searchQuery && (
                <button
                  type="button"
                  onClick={handleClearSearch}
                  style={{
                    position: 'absolute',
                    right: '6px',
                    top: '7px',
                    background: 'none',
                    border: 'none',
                    cursor: 'pointer',
                    color: '#94a3b8',
                    display: 'flex',
                    alignItems: 'center',
                    padding: 0
                  }}
                  title="Clear search"
                >
                  <X size={14} />
                </button>
              )}
            </div>
            <button
              type="submit"
              className="btn-primary"
              disabled={isSearching}
              style={{ padding: '5px 12px', fontSize: '0.78rem', whiteSpace: 'nowrap' }}
            >
              {isSearching ? <Loader2 size={13} className="spin" /> : (lang === 'mr' ? 'शोधा' : 'Search')}
            </button>
          </form>

          {/* Autocomplete Suggestions Dropdown */}
          {showSuggestions && suggestions.length > 0 && (
            <div className="search-suggestions-dropdown">
              {suggestions.map((item) => {
                const itemTitle = lang === 'mr' ? (item.name_mr || item.name) : item.name;
                return (
                  <div
                    key={item.id}
                    className="search-suggestion-item"
                    onClick={() => selectAndZoomPlace(item)}
                  >
                    <MapPin size={13} style={{ color: '#2563eb', flexShrink: 0 }} />
                    <div style={{ minWidth: 0, flex: 1 }}>
                      <div style={{ fontWeight: 600, fontSize: '0.8rem', color: '#1e293b', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                        {itemTitle}
                        {item.name_mr && lang !== 'mr' ? ` (${item.name_mr})` : ''}
                      </div>
                      <div style={{ fontSize: '0.68rem', color: '#64748b', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                        {item.region || item.category || 'Region'}
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          )}

          {/* Search Feedback Banner */}
          {searchFeedback && (
            <div className={`search-feedback-banner ${searchFeedback.type}`}>
              {searchFeedback.type === 'success' && <CheckCircle2 size={12} />}
              {searchFeedback.type === 'error' && <AlertCircle size={12} />}
              {searchFeedback.type === 'info' && <Loader2 size={12} className="spin" />}
              <span>{searchFeedback.message}</span>
            </div>
          )}
        </div>

        {/* Quick Map Actions */}
        <div style={{ display: 'flex', gap: '6px', alignItems: 'center', flexWrap: 'wrap', marginTop: '6px' }}>
          <button
            onClick={() => setBasemapType(basemapType === 'topo' ? 'osm' : 'topo')}
            className="btn-secondary"
            style={{ padding: '3px 8px', fontSize: '0.74rem' }}
            title="Toggle Topographic Relief vs Street Map"
          >
            <Mountain size={13} /> {basemapType === 'topo' ? 'Topo Relief' : 'Standard'}
          </button>

          <button
            onClick={handleResetView}
            className="btn-secondary"
            style={{ padding: '3px 8px', fontSize: '0.74rem' }}
            title="Reset to Lonavala Center"
          >
            <RotateCcw size={13} /> Reset
          </button>
        </div>
      </div>

      {/* Layer Toggles Floating Drawer */}
      <div style={{
        position: 'absolute',
        top: '12px',
        right: '12px',
        zIndex: 800,
        background: 'rgba(255, 255, 255, 0.96)',
        backdropFilter: 'blur(6px)',
        padding: '8px 12px',
        borderRadius: '8px',
        boxShadow: '0 4px 10px rgba(0,0,0,0.1)',
        fontSize: '0.75rem',
        maxWidth: '200px'
      }}>
        <div style={{ fontWeight: 700, marginBottom: '6px', display: 'flex', alignItems: 'center', gap: '4px' }}>
          <Layers size={13} /> {lang === 'mr' ? 'नकाशा स्तर' : 'Map Overlays'}
        </div>
        <label style={{ display: 'flex', alignItems: 'center', gap: '6px', cursor: 'pointer', marginBottom: '4px' }}>
          <input type="checkbox" checked={showTouristLayer} onChange={(e) => setShowTouristLayer(e.target.checked)} />
          <span>{lang === 'mr' ? 'पर्यटन स्थळे' : 'Tourist Spots'}</span>
        </label>
        <label style={{ display: 'flex', alignItems: 'center', gap: '6px', cursor: 'pointer', marginBottom: '4px' }}>
          <input type="checkbox" checked={showLandslideLayer} onChange={(e) => setShowLandslideLayer(e.target.checked)} />
          <span>{lang === 'mr' ? 'दरड प्रवण क्षेत्र' : 'Landslide Slopes'}</span>
        </label>
        <label style={{ display: 'flex', alignItems: 'center', gap: '6px', cursor: 'pointer', marginBottom: '4px' }}>
          <input type="checkbox" checked={showFloodLayer} onChange={(e) => setShowFloodLayer(e.target.checked)} />
          <span>{lang === 'mr' ? 'पूर / सांडवा प्रवाह' : 'Flash Flood / Surge'}</span>
        </label>
        <label style={{ display: 'flex', alignItems: 'center', gap: '6px', cursor: 'pointer', marginBottom: '4px' }}>
          <input type="checkbox" checked={showCorridorsLayer} onChange={(e) => setShowCorridorsLayer(e.target.checked)} />
          <span>{lang === 'mr' ? 'द्रुतगती व रेल्वे मार्ग' : 'Transit Corridors'}</span>
        </label>
        <label style={{ display: 'flex', alignItems: 'center', gap: '6px', cursor: 'pointer', marginBottom: '4px' }}>
          <input type="checkbox" checked={showIncidentsLayer} onChange={(e) => setShowIncidentsLayer(e.target.checked)} />
          <span>{lang === 'mr' ? 'ऐतिहासिक घटना' : 'Incident Layer'}</span>
        </label>
        <label style={{ display: 'flex', alignItems: 'center', gap: '6px', cursor: 'pointer', marginBottom: '4px' }}>
          <input type="checkbox" checked={showSheltersLayer} onChange={(e) => setShowSheltersLayer(e.target.checked)} />
          <span>{lang === 'mr' ? 'निवारा केंद्र' : 'Safe Shelters'}</span>
        </label>
        <label style={{ display: 'flex', alignItems: 'center', gap: '6px', cursor: 'pointer' }}>
          <input type="checkbox" checked={showSensorsLayer} onChange={(e) => setShowSensorsLayer(e.target.checked)} />
          <span>{lang === 'mr' ? 'IoT सेन्सर' : 'IoT Nodes [Sim]'}</span>
        </label>
      </div>

      {/* Real Georisk Legend */}
      <div className="map-legend-panel">
        <div style={{ fontWeight: 700, marginBottom: '4px' }}>
          {lang === 'mr' ? 'धोका पातळी दर्शक (०-१००)' : 'Risk Grade (0-100)'}
        </div>
        <div className="legend-item">
          <div className="legend-swatch" style={{ background: '#16a34a' }}></div>
          <span>0-25: {lang === 'mr' ? 'कमी' : 'Low'}</span>
        </div>
        <div className="legend-item">
          <div className="legend-swatch" style={{ background: '#d97706' }}></div>
          <span>25-55: {lang === 'mr' ? 'मध्यम' : 'Moderate'}</span>
        </div>
        <div className="legend-item">
          <div className="legend-swatch" style={{ background: '#ea580c' }}></div>
          <span>55-78: {lang === 'mr' ? 'जास्त' : 'High'}</span>
        </div>
        <div className="legend-item">
          <div className="legend-swatch" style={{ background: '#dc2626' }}></div>
          <span>78-100: {lang === 'mr' ? 'अतिधोका' : 'Very High'}</span>
        </div>
      </div>
    </div>
  );
};

function getRiskColor(status: RiskLevel): string {
  switch (status) {
    case 'low': return '#16a34a';
    case 'moderate': return '#d97706';
    case 'high': return '#ea580c';
    case 'very_high': return '#dc2626';
    default: return '#64748b';
  }
}
