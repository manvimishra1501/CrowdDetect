// Initialize Leaflet map
const map = L.map('heatmapContainer').setView([28.6139, 77.2090], 13); // Example: Delhi

// Add OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

// Placeholder: simulate crowd density zones
const dummyZones = [
  { lat: 28.615, lng: 77.205, intensity: 0.7 },
  { lat: 28.610, lng: 77.210, intensity: 0.9 },
  { lat: 28.618, lng: 77.215, intensity: 0.5 }
];

// Add circle markers for zones
dummyZones.forEach(zone => {
  L.circle([zone.lat, zone.lng], {
    color: 'red',
    fillColor: 'red',
    fillOpacity: zone.intensity,
    radius: 120
  }).addTo(map)
    .bindPopup(`Density: ${(zone.intensity * 100).toFixed(0)}%`);
});

// TODO: Replace dummyZones with backend heatmap data from processed video
