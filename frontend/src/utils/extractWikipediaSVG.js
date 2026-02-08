import fs from 'fs';
import { parseString } from 'xml2js';

// Leer el SVG de Wikipedia
const svgContent = fs.readFileSync('/tmp/spain_autonomous.svg', 'utf8');

// Parsear el XML
parseString(svgContent, (err, result) => {
  if (err) {
    console.error('Error parsing SVG:', err);
    return;
  }

  // Extraer información del SVG
  const svg = result.svg;
  const viewBox = svg.$.viewBox;
  const width = svg.$.width;
  const height = svg.$.height;

  console.log('ViewBox:', viewBox);
  console.log('Width:', width);
  console.log('Height:', height);

  // Buscar todos los paths y polygons en el grupo principal
  let regions = [];

  // Función recursiva para buscar paths y polygons
  const findPaths = (obj, depth = 0) => {
    if (!obj) return;

    if (Array.isArray(obj)) {
      obj.forEach(item => findPaths(item, depth));
      return;
    }

    if (typeof obj !== 'object') return;

    // Si es un path o polygon
    if (obj.$ && (obj.$.d || obj.$.points)) {
      const id = obj.$.id || `region-${regions.length}`;
      const pathData = obj.$.d || obj.$.points;
      const fill = obj.$.fill || obj.$['i:fill'] || '';
      const style = obj.$.style || '';

      regions.push({
        id,
        path: pathData,
        fill,
        style,
        type: obj.$.d ? 'path' : 'polygon'
      });
    }

    // Recursión para hijos
    Object.keys(obj).forEach(key => {
      if (key !== '$' && key !== '#name') {
        findPaths(obj[key], depth + 1);
      }
    });
  };

  findPaths(svg);

  console.log(`\nFound ${regions.length} regions`);

  regions.forEach((region, i) => {
    console.log(`\n${i + 1}. ID: ${region.id}`);
    console.log(`   Type: ${region.type}`);
    console.log(`   Fill: ${region.fill}`);
    console.log(`   Path length: ${region.path.length}`);
  });

  // Guardar en JSON
  const output = {
    viewBox,
    width,
    height,
    regions
  };

  fs.writeFileSync('/tmp/spain_regions_extracted.json', JSON.stringify(output, null, 2));
  console.log('\n✓ Saved to /tmp/spain_regions_extracted.json');
});
