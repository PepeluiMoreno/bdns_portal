// Mock data para desarrollo y diseño de UI

// Flag para activar/desactivar mock data
export const USE_MOCK_DATA = true; // Cambiar a false para usar datos reales

// Años disponibles para el selector (2015-2025)
export const mockYears = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025];

// Helper para generar datos con tendencia de crecimiento
const generateYearData = (baseData, year, baseYear = 2020) => {
  const yearDiff = year - baseYear;
  const growthFactor = 1 + (yearDiff * 0.08); // 8% de crecimiento anual
  return baseData.map(item => ({
    ...item,
    anio: year,
    numero_concesiones: Math.floor(item.numero_concesiones * growthFactor),
    importe_total: Math.floor(item.importe_total * growthFactor)
  }));
};

// Datos base (año 2020)
const base2020Organo = [
  { organo_nombre: 'Andalucía', numero_concesiones: 12000, importe_total: 350000000 },
  { organo_nombre: 'Cataluña', numero_concesiones: 15000, importe_total: 420000000 },
  { organo_nombre: 'Comunidad de Madrid', numero_concesiones: 17000, importe_total: 550000000 },
  { organo_nombre: 'Comunidad Valenciana', numero_concesiones: 10000, importe_total: 300000000 },
  { organo_nombre: 'Galicia', numero_concesiones: 8000, importe_total: 230000000 },
  { organo_nombre: 'Castilla y León', numero_concesiones: 6800, importe_total: 200000000 },
  { organo_nombre: 'País Vasco', numero_concesiones: 6500, importe_total: 250000000 },
  { organo_nombre: 'Canarias', numero_concesiones: 5400, importe_total: 160000000 },
  { organo_nombre: 'Castilla-La Mancha', numero_concesiones: 4700, importe_total: 140000000 },
  { organo_nombre: 'Región de Murcia', numero_concesiones: 3600, importe_total: 108000000 },
  { organo_nombre: 'Aragón', numero_concesiones: 3800, importe_total: 120000000 },
  { organo_nombre: 'Extremadura', numero_concesiones: 2900, importe_total: 88000000 },
  { organo_nombre: 'Islas Baleares', numero_concesiones: 3100, importe_total: 102000000 },
  { organo_nombre: 'Asturias', numero_concesiones: 2700, importe_total: 82000000 },
  { organo_nombre: 'Comunidad Foral de Navarra', numero_concesiones: 2400, importe_total: 76000000 },
  { organo_nombre: 'Cantabria', numero_concesiones: 1950, importe_total: 60000000 },
  { organo_nombre: 'La Rioja', numero_concesiones: 1400, importe_total: 43000000 },
  { organo_nombre: 'Ceuta', numero_concesiones: 380, importe_total: 12000000 },
  { organo_nombre: 'Melilla', numero_concesiones: 320, importe_total: 10000000 },
];

const base2020Tipo = [
  { tipo_entidad: 'B', numero_concesiones: 38000, importe_total: 1000000000 },
  { tipo_entidad: 'A', numero_concesiones: 19500, importe_total: 820000000 },
  { tipo_entidad: 'G', numero_concesiones: 15000, importe_total: 370000000 },
  { tipo_entidad: 'Q', numero_concesiones: 10000, importe_total: 520000000 },
  { tipo_entidad: 'P', numero_concesiones: 7200, importe_total: 310000000 },
  { tipo_entidad: 'F', numero_concesiones: 5500, importe_total: 180000000 },
  { tipo_entidad: 'N', numero_concesiones: 3500, importe_total: 152000000 },
  { tipo_entidad: 'PF', numero_concesiones: 2700, importe_total: 78000000 },
  { tipo_entidad: 'J', numero_concesiones: 2300, importe_total: 64000000 },
  { tipo_entidad: 'R', numero_concesiones: 1600, importe_total: 43000000 },
];

// Generar datos para todos los años (2015-2025)
export const mockEstadisticasPorOrgano = [
  ...generateYearData(base2020Organo, 2015),
  ...generateYearData(base2020Organo, 2016),
  ...generateYearData(base2020Organo, 2017),
  ...generateYearData(base2020Organo, 2018),
  ...generateYearData(base2020Organo, 2019),
  ...generateYearData(base2020Organo, 2020),
  ...generateYearData(base2020Organo, 2021),
  ...generateYearData(base2020Organo, 2022),
  ...generateYearData(base2020Organo, 2023),
  ...generateYearData(base2020Organo, 2024),
  ...generateYearData(base2020Organo, 2025),
];

export const mockEstadisticasPorTipoEntidad = [
  ...generateYearData(base2020Tipo, 2015),
  ...generateYearData(base2020Tipo, 2016),
  ...generateYearData(base2020Tipo, 2017),
  ...generateYearData(base2020Tipo, 2018),
  ...generateYearData(base2020Tipo, 2019),
  ...generateYearData(base2020Tipo, 2020),
  ...generateYearData(base2020Tipo, 2021),
  ...generateYearData(base2020Tipo, 2022),
  ...generateYearData(base2020Tipo, 2023),
  ...generateYearData(base2020Tipo, 2024),
  ...generateYearData(base2020Tipo, 2025),
];

// Datos de concentración (Top 10 beneficiarios)
export const mockConcentracion = [
  { beneficiario_nombre: 'TELEFÓNICA SA', importe_total: 125000000, numero_concesiones: 45 },
  { beneficiario_nombre: 'IBERDROLA SA', importe_total: 98000000, numero_concesiones: 38 },
  { beneficiario_nombre: 'REPSOL SA', importe_total: 87000000, numero_concesiones: 32 },
  { beneficiario_nombre: 'ENDESA SA', importe_total: 76000000, numero_concesiones: 29 },
  { beneficiario_nombre: 'BANCO SANTANDER SA', importe_total: 65000000, numero_concesiones: 25 },
  { beneficiario_nombre: 'BBVA SA', importe_total: 58000000, numero_concesiones: 22 },
  { beneficiario_nombre: 'NATURGY ENERGY GROUP SA', importe_total: 52000000, numero_concesiones: 19 },
  { beneficiario_nombre: 'INDITEX SA', importe_total: 45000000, numero_concesiones: 16 },
  { beneficiario_nombre: 'ACS ACTIVIDADES CONSTRUCCIÓN SA', importe_total: 42000000, numero_concesiones: 15 },
  { beneficiario_nombre: 'FERROVIAL SA', importe_total: 38000000, numero_concesiones: 14 },
];

// Función helper para obtener datos mockeados según el año
export function getMockDataForYear(year) {
  return {
    estadisticasPorOrgano: mockEstadisticasPorOrgano.filter(d => d.anio === year),
    estadisticasPorTipoEntidad: mockEstadisticasPorTipoEntidad.filter(d => d.anio === year),
    concentracion: mockConcentracion
  };
}
