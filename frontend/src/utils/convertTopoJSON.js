import * as topojson from 'topojson-client';
import { geoPath, geoIdentity } from 'd3-geo';
import fs from 'fs';

// Read the TopoJSON file
const topoData = JSON.parse(fs.readFileSync('/tmp/spain_autonomous_regions.json', 'utf8'));

// Extract the autonomous regions
const geojson = topojson.feature(topoData, topoData.objects.autonomous_regions);

// Calculate bounds to create viewBox
const bounds = {
  minX: Infinity,
  minY: Infinity,
  maxX: -Infinity,
  maxY: -Infinity
};

// Create a projection (identity for now, we'll scale later)
const projection = geoIdentity().reflectY(true);
const pathGenerator = geoPath(projection);

// Generate SVG paths for each region
const locations = geojson.features.map(feature => {
  const path = pathGenerator(feature);
  const name = feature.properties.name;
  const id = feature.id;

  // Create a simplified ID (kebab-case)
  let simplifiedId = name
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "") // Remove diacritics
    .replace(/[^a-z0-9\s-]/g, '') // Remove special chars
    .replace(/\s+/g, '-'); // Replace spaces with hyphens

  return {
    name,
    id: simplifiedId,
    path,
    numericId: id
  };
});

// Calculate viewBox from all paths
locations.forEach(loc => {
  if (loc.path && loc.path !== 'null') {
    const pathData = loc.path;
    // Extract coordinates from path (simplified approach)
    const coords = pathData.match(/[\d.]+/g);
    if (coords) {
      for (let i = 0; i < coords.length; i += 2) {
        const x = parseFloat(coords[i]);
        const y = parseFloat(coords[i + 1]);
        if (!isNaN(x) && !isNaN(y)) {
          bounds.minX = Math.min(bounds.minX, x);
          bounds.minY = Math.min(bounds.minY, y);
          bounds.maxX = Math.max(bounds.maxX, x);
          bounds.maxY = Math.max(bounds.maxY, y);
        }
      }
    }
  }
});

const width = bounds.maxX - bounds.minX;
const height = bounds.maxY - bounds.minY;
const viewBox = `${bounds.minX} ${bounds.minY} ${width} ${height}`;

// Create the final map object
const mapData = {
  label: 'Mapa de España (Comunidades Autónomas)',
  viewBox,
  locations: locations.filter(loc => loc.path && loc.path !== 'null')
};

// Write to file
const outputPath = '/home/jose/dev/bdns/apps/frontend/src/utils/spainCompleteMap.js';
const fileContent = `// Mapa completo de España con todas las comunidades autónomas
// Generado desde TopoJSON del Instituto Geográfico Nacional
// Incluye las 17 comunidades autónomas + Ceuta + Melilla

export default ${JSON.stringify(mapData, null, 2)};
`;

fs.writeFileSync(outputPath, fileContent);

console.log(`Map data written to ${outputPath}`);
console.log(`Total locations: ${mapData.locations.length}`);
console.log(`ViewBox: ${viewBox}`);
console.log('\\nLocations:');
mapData.locations.forEach(loc => {
  console.log(`  - ${loc.name} (${loc.id})`);
});
