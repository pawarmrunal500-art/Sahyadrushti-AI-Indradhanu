/**
 * Centralized authentic image registry for SAHYADRUSHTI AI
 * Strictly maps genuine Lonavala, Khandala, and Western Ghats photographic assets
 */

export const LOCATION_IMAGES: Record<string, string> = {
  bhushi_dam: '/images/locations/bhushi_dam.jpg',
  kune_falls: '/images/locations/kune_falls.jpg',
  tiger_point: '/images/locations/tiger_point.jpg',
  lions_point: '/images/locations/lions_point.jpg',
  rajmachi_route: '/images/locations/rajmachi.jpg',
  khandala_expressway: '/images/locations/amrutanjan_bridge.jpg',
  adoshi_tunnel: '/images/locations/adoshi_tunnel.jpg',
  monkey_hill: '/images/locations/monkey_hill.jpg',
  thakurwadi: '/images/locations/thakurwadi.jpg',
  patan_village: '/images/locations/patan_village.jpg',
  valvan_dam: '/images/locations/lonavala_valleys.jpg',
  lonavala_town: '/images/locations/lonavala_valleys.jpg',
  lonavala_valleys: '/images/locations/lonavala_valleys.jpg'
};

export const FEATURE_IMAGES = {
  overviewBanner: '/images/banner_lonavala_overview.jpg',
  landslide: '/images/features/feat_landslide.jpg',
  flashflood: '/images/features/feat_flashflood.jpg',
  weather: '/images/features/feat_weather.jpg',
  terrain: '/images/features/feat_terrain.jpg',
  incidents: '/images/features/feat_incidents.jpg',
  safety: '/images/features/feat_safety.jpg',
  rescue: '/images/features/feat_rescue.jpg',
  corridor: '/images/features/feat_corridor.jpg'
};

export function getLocationImage(id?: string): string {
  if (!id) return '/images/locations/lonavala_valleys.jpg';
  return LOCATION_IMAGES[id] || '/images/locations/lonavala_valleys.jpg';
}

