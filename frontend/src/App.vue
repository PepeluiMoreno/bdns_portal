<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import Sidebar from './components/Sidebar.vue';
import Header from './components/Header.vue';
import YearSelector from './components/YearSelector.vue';
import StatsRow from './components/StatsRow.vue';
import SpainMap from './components/SpainMap.vue';
import BeneficiaryTypePieChart from './components/BeneficiaryTypePieChart.vue';
import TotalEvolutionChart from './components/TotalEvolutionChart.vue';
import StatCard from './components/StatCard.vue';
import RegionHeatmap from './components/RegionHeatmap.vue';
import RegionStatsTable from './components/RegionStatsTable.vue';
import ConvocatoriaSearch from './components/ConvocatoriaSearch.vue';
import InternationalBeneficiaries from './components/InternationalBeneficiaries.vue';
import Dashboard2 from './components/Dashboard2.vue';
import { fetchEstadisticasPorOrgano, fetchEstadisticasPorTipoEntidad, fetchConcentracion } from './services/graphql';
import { getAvailableYears, groupByRegionAndYear, calculateAdvancedStats, getHeatmapColor, spanishRegions } from './utils/regions';

const stats = ref({
  totalConcesiones: 0,
  totalImporte: 0,
  regiones: 0,
  beneficiarios: 0,
});

const loading = ref(true);
const activeTab = ref('dashboard');
const selectedYear = ref(new Date().getFullYear());
const availableYears = ref([]);
const estadisticasPorTipo = ref([]);
const estadisticasPorOrgano = ref([]);
const advancedStats = ref({
  totalConcesiones: 0,
  totalImporte: 0,
  beneficiariosUnicos: 0,
  convocatoriasActivas: 0,
  topBeneficiario: { nombre: 'N/A', importe: 0 },
  concentracionTop10: 0,
  importeMedio: 0,
  ccaaLider: { nombre: 'N/A', importe: 0 }
});

const handleNavigation = (sectionId) => {
  activeTab.value = sectionId;
};

const filteredStatsByYear = computed(() => {
  return estadisticasPorTipo.value.filter(stat => stat.anio === selectedYear.value);
});

const regionDataByYear = computed(() => {
  const grouped = groupByRegionAndYear(estadisticasPorOrgano.value);
  const result = {};

  // Calcular min/max para escala de colores
  let maxImporte = 0;
  Object.values(grouped).forEach(yearData => {
    const dataForYear = yearData[selectedYear.value];
    if (dataForYear && dataForYear.importe_total > maxImporte) {
      maxImporte = dataForYear.importe_total;
    }
  });

  // Asignar colores a cada región
  for (const [region, regionInfo] of Object.entries(spanishRegions)) {
    const yearData = grouped[region]?.[selectedYear.value];
    if (yearData) {
      result[region] = {
        ...yearData,
        color: getHeatmapColor(yearData.importe_total, 0, maxImporte),
      };
    } else {
      result[region] = {
        numero_concesiones: 0,
        importe_total: 0,
        color: '#e0f2fe'
      };
    }
  }

  return result;
});

watch(selectedYear, async (newYear) => {
  try {
    const concentracion = await fetchConcentracion(newYear, null, 10);
    advancedStats.value = calculateAdvancedStats(
      estadisticasPorOrgano.value,
      estadisticasPorTipo.value,
      concentracion,
      newYear
    );
  } catch (error) {
    console.error('Error updating stats for year:', newYear, error);
  }
});

onMounted(async () => {
  try {
    loading.value = true;

    // Fetch datos por tipo de entidad
    const estatsPorTipo = await fetchEstadisticasPorTipoEntidad();
    estadisticasPorTipo.value = estatsPorTipo;

    // Fetch datos por órgano
    const estatsOrgano = await fetchEstadisticasPorOrgano();
    estadisticasPorOrgano.value = estatsOrgano;

    // Extraer años disponibles
    availableYears.value = getAvailableYears(estatsOrgano);
    if (availableYears.value.length > 0) {
      selectedYear.value = availableYears.value[availableYears.value.length - 1];
    }

    // Fetch concentración
    const concentracion = await fetchConcentracion(selectedYear.value, null, 10);

    // Calcular stats avanzadas
    advancedStats.value = calculateAdvancedStats(
      estatsOrgano,
      estatsPorTipo,
      concentracion,
      selectedYear.value
    );

    // Stats existentes (para otros tabs)
    let totalConcesiones = 0;
    let totalImporte = 0;
    const regiones = new Set();

    estatsOrgano.forEach(item => {
      totalConcesiones += item.numero_concesiones || 0;
      totalImporte += item.importe_total || 0;
      if (item.organo_nombre) {
        regiones.add(item.organo_nombre);
      }
    });

    stats.value = {
      totalConcesiones,
      totalImporte,
      regiones: regiones.size,
      beneficiarios: Math.floor(totalConcesiones * 0.8),
    };
  } catch (error) {
    console.error('Error loading data:', error);
  } finally {
    loading.value = false;
  }
});

</script>

<template>
  <div class="flex min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
    <!-- Sidebar -->
    <Sidebar @navigate="handleNavigation" />

    <!-- Main Content Area -->
    <div class="flex-1 flex flex-col">
      <!-- Header -->
      <Header />

      <!-- Contenido Principal -->
      <main class="flex-1 px-4 sm:px-6 lg:px-8 py-8">
        <!-- Contenedor con ancho máximo -->
        <div class="max-w-7xl mx-auto">
        <!-- Dashboard Tab -->
        <div v-if="activeTab === 'dashboard'" class="space-y-8 fade-in">
          <!-- Year Selector -->
          <YearSelector v-model="selectedYear" :available-years="availableYears" />

          <!-- Stats Cards - 2 filas de 4 tarjetas -->
          <StatsRow :stats="advancedStats" />

          <!-- Grid de 2 columnas: Mapa + (Pie Chart + Evolución) -->
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <!-- Mapa de España -->
            <SpainMap :year="selectedYear" :region-data="regionDataByYear" />

            <!-- Columna derecha: Pie Chart y Gráfica de Evolución apilados -->
            <div class="space-y-6">
              <!-- Pie Chart de Tipos de Beneficiarios -->
              <div class="h-[320px]">
                <BeneficiaryTypePieChart :year="selectedYear" :data="filteredStatsByYear" />
              </div>

              <!-- Gráfica de Evolución del Importe Total -->
              <div class="h-[320px]">
                <TotalEvolutionChart :data="estadisticasPorOrgano" :available-years="availableYears" />
              </div>
            </div>
          </div>

          <!-- Tabla de Estadísticas (mantener existente) -->
          <RegionStatsTable />
        </div>

        <!-- Search Tab -->
        <div v-if="activeTab === 'search'" class="fade-in">
          <ConvocatoriaSearch />
        </div>

        <!-- Convocatorias Tab -->
        <div v-if="activeTab === 'convocatorias'" class="fade-in">
          <Dashboard2 />
        </div>

        <!-- International Tab -->
        <div v-if="activeTab === 'international'" class="fade-in">
          <InternationalBeneficiaries />
        </div>
        </div>
      </main>

      <!-- Footer -->
      <footer class="bg-white border-t border-slate-200">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div>
              <h3 class="font-semibold text-slate-900 mb-2">BDNS Consultas e Informes</h3>
              <p class="text-sm text-slate-600">
                Visualización interactiva de la Base de Datos Nacional de Subvenciones de España.
              </p>
            </div>
            <div>
              <h4 class="font-semibold text-slate-900 mb-3">Enlaces Útiles</h4>
              <ul class="space-y-2 text-sm text-slate-600">
                <li><a href="#" class="hover:text-primary-600 transition-colors">Documentación</a></li>
                <li><a href="#" class="hover:text-primary-600 transition-colors">API GraphQL</a></li>
                <li><a href="#" class="hover:text-primary-600 transition-colors">Contacto</a></li>
              </ul>
            </div>
            <div>
              <h4 class="font-semibold text-slate-900 mb-3">Información</h4>
              <p class="text-sm text-slate-600">
                Datos actualizados diariamente desde la BDNS oficial.
              </p>
            </div>
          </div>
          <div class="border-t border-slate-200 mt-8 pt-8 text-center text-sm text-slate-600">
            <p>&copy; 2024 BDNS Consultas e Informes. Todos los derechos reservados.</p>
          </div>
        </div>
      </footer>
    </div>
  </div>
</template>

<style scoped>
.fade-in {
  animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
</style>
