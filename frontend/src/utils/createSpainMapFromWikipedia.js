import fs from 'fs';

// Leer el JSON extraído del SVG de Wikipedia
const extracted = JSON.parse(fs.readFileSync('/tmp/spain_regions_extracted.json', 'utf8'));

// Mapeo de IDs numéricos a nombres de comunidades
// Generado automáticamente analizando centroides de paths y posiciones de textos
const regionMapping = {
  '_129272280': { name: 'Cataluña', id: 'cataluna' },
  '_129182272': { name: 'Comunidad Valenciana', id: 'comunidad-valenciana' },
  '_128752360': { name: 'Islas Baleares', id: 'islas-baleares' },
  '_129252504': { name: 'Castilla-La Mancha', id: 'castilla-la-mancha' },
  '_129253112': { name: 'Aragón', id: 'aragon' },
  '_129786416': { name: 'Comunidad Foral de Navarra', id: 'navarra' },
  '_129181960': { name: 'La Rioja', id: 'la-rioja' },
  '_127677112': { name: 'País Vasco', id: 'pais-vasco' },
  '_129423256': { name: 'Cantabria', id: 'cantabria' },
  '_130150024': { name: 'Castilla y León', id: 'castilla-y-leon' },
  '_129003504': { name: 'Extremadura', id: 'extremadura' },
  '_127780568': { name: 'Galicia', id: 'galicia' },
  '_128682832': { name: 'Asturias', id: 'asturias' },
  '_128683144': { name: 'Región de Murcia', id: 'region-de-murcia' },
  '_129811768': { name: 'Canarias', id: 'canarias' },
  '_128681296': { name: 'Andalucía', id: 'andalucia' },
  '_130150096': { name: 'Comunidad de Madrid', id: 'comunidad-de-madrid' },
  '_128750616': { name: 'Ceuta', id: 'ceuta' },
  '_129003024': { name: 'Melilla', id: 'melilla' }
};

// Convertir polygons points a path d
const pointsToPath = (points) => {
  const coords = points.trim().split(/\s+/);
  if (coords.length < 2) return '';

  let d = 'M' + coords[0] + ' ' + coords[1];
  for (let i = 2; i < coords.length; i += 2) {
    if (i + 1 < coords.length) {
      d += ' L' + coords[i] + ' ' + coords[i + 1];
    }
  }
  d += ' Z';
  return d;
};

// Procesar regiones
const locations = extracted.regions
  .map(region => {
    const mapping = regionMapping[region.id];
    if (!mapping) return null; // Excluir regiones no mapeadas

    // Convertir polygon a path si es necesario
    let pathData = region.path;
    if (region.type === 'polygon') {
      pathData = pointsToPath(region.path);
    }

    return {
      name: mapping.name,
      id: mapping.id,
      path: pathData
    };
  })
  .filter(Boolean);

// Crear el mapa final
const spainMap = {
  label: 'Mapa de España - Comunidades Autónomas',
  viewBox: extracted.viewBox,
  locations
};

// Guardar
const outputPath = '/home/jose/dev/bdns/apps/frontend/src/utils/spainMapWikipedia.js';
const fileContent = `// Mapa de España basado en SVG de Wikimedia Commons
// Licencia: CC-BY-SA 3.0
// Incluye todas las 19 comunidades autónomas

export default ${JSON.stringify(spainMap, null, 2)};
`;

fs.writeFileSync(outputPath, fileContent);

console.log(`✓ Mapa creado en ${outputPath}`);
console.log(`Total de regiones: ${locations.length}`);
console.log(`ViewBox: ${extracted.viewBox}`);
console.log('\nRegiones incluidas:');
locations.forEach(loc => console.log(`  - ${loc.name} (${loc.id})`));
