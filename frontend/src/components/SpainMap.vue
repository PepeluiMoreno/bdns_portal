<script setup>
import { ref, computed } from 'vue';
import spainMap from '../utils/spainMapWikipedia';
import { spanishRegions, formatCurrency } from '../utils/regions';

const props = defineProps({
  year: {
    type: Number,
    required: true
  },
  regionData: {
    type: Object,
    required: true,
    default: () => ({})
  }
});

const hoveredRegion = ref(null);
const selectedRegion = ref(null);
const tooltipPosition = ref({ x: 0, y: 0 });

// Los nombres en el mapa de Wikipedia ya coinciden con los del sistema
// Solo usamos el nombre directamente
const getRegionName = (location) => {
  return location.name;
};

const getRegionColor = (location) => {
  const regionName = getRegionName(location);
  return props.regionData[regionName]?.color || '#e0f2fe';
};

const handleMouseEnter = (location, event) => {
  const regionName = getRegionName(location);
  hoveredRegion.value = regionName;
  updateTooltipPosition(event);
};

const handleMouseMove = (event) => {
  if (hoveredRegion.value) {
    updateTooltipPosition(event);
  }
};

const handleMouseLeave = () => {
  hoveredRegion.value = null;
};

const handleClick = (location) => {
  const regionName = getRegionName(location);
  selectedRegion.value = selectedRegion.value === regionName ? null : regionName;
};

const updateTooltipPosition = (event) => {
  const svgElement = event.currentTarget.closest('svg');
  if (svgElement) {
    const rect = svgElement.getBoundingClientRect();
    tooltipPosition.value = {
      x: event.clientX - rect.left,
      y: event.clientY - rect.top
    };
  }
};

const sortedRegions = computed(() => {
  return Object.entries(props.regionData)
    .map(([nombre, data]) => ({
      nombre,
      importe_total: data.importe_total || 0,
      numero_concesiones: data.numero_concesiones || 0
    }))
    .sort((a, b) => b.importe_total - a.importe_total);
});
</script>

<template>
  <div class="bg-white rounded-lg shadow-md p-6">
    <div class="flex items-center justify-between mb-4">
      <h2 class="text-xl font-bold text-slate-900">
        Mapa de Subvenciones por CCAA
      </h2>
      <span class="px-3 py-1 bg-primary-100 text-primary-700 rounded-full text-sm font-medium">
        {{ year }}
      </span>
    </div>

    <p class="text-sm text-slate-600 mb-6">
      Distribución geográfica del importe concedido
    </p>

    <!-- Layout vertical: Mapa arriba, Tabla abajo -->
    <div class="space-y-6">
      <!-- SVG Map -->
      <div class="relative">
      <svg
        :viewBox="spainMap.viewBox"
        class="w-full h-auto"
        preserveAspectRatio="xMidYMid meet"
        @mousemove="handleMouseMove"
        @mouseleave="handleMouseLeave"
      >
        <!-- Fondo -->
        <rect x="0" y="0" width="700" height="642.727" fill="#f8fafc" />

        <!-- Todas las comunidades autónomas (ya incluye Canarias, Ceuta y Melilla en sus posiciones del SVG) -->
        <g id="spain-regions">
          <path
            v-for="location in spainMap.locations"
            :key="location.id"
            :id="location.id"
            :d="location.path"
            :fill="getRegionColor(location)"
            :class="[
              'transition-all duration-200 cursor-pointer',
              hoveredRegion === getRegionName(location) ? 'opacity-80' : 'opacity-100',
              selectedRegion === getRegionName(location) ? 'stroke-primary-700' : 'stroke-slate-300'
            ]"
            stroke-width="1"
            @mouseenter="handleMouseEnter(location, $event)"
            @click="handleClick(location)"
            :aria-label="`${getRegionName(location)}: ${formatCurrency(regionData[getRegionName(location)]?.importe_total || 0)}`"
            role="button"
            tabindex="0"
          >
            <title>{{ getRegionName(location) }}</title>
          </path>
        </g>

      </svg>

      <!-- Tooltip -->
      <div
        v-if="hoveredRegion"
        class="absolute bg-slate-900 text-white px-4 py-3 rounded-lg shadow-xl text-sm pointer-events-none z-50"
        :style="{
          left: `${tooltipPosition.x + 20}px`,
          top: `${tooltipPosition.y - 40}px`,
          transform: 'translate(-50%, -100%)'
        }"
      >
        <div class="font-semibold mb-1">{{ hoveredRegion }}</div>
        <div class="text-xs space-y-1">
          <div>Importe: {{ formatCurrency(regionData[hoveredRegion]?.importe_total || 0) }}</div>
          <div>Concesiones: {{ (regionData[hoveredRegion]?.numero_concesiones || 0).toLocaleString('es-ES') }}</div>
        </div>
      </div>
      </div>

      <!-- Tabla de regiones en dos columnas -->
      <div class="grid grid-cols-2 gap-4">
        <div class="bg-slate-50 rounded-lg p-3">
          <div class="space-y-0.5">
            <div
              v-for="region in sortedRegions.slice(0, Math.ceil(sortedRegions.length / 2))"
              :key="region.nombre"
              class="flex justify-between items-center py-1.5 px-2 hover:bg-white rounded transition-colors cursor-pointer text-xs"
              :class="{ 'bg-white shadow-sm': selectedRegion === region.nombre }"
              @click="selectedRegion = selectedRegion === region.nombre ? null : region.nombre"
            >
              <span class="font-medium text-slate-700 flex-1 truncate pr-2">{{ region.nombre }}</span>
              <span class="font-bold text-primary-700 whitespace-nowrap">{{ formatCurrency(region.importe_total) }}</span>
            </div>
          </div>
        </div>

        <div class="bg-slate-50 rounded-lg p-3">
          <div class="space-y-0.5">
            <div
              v-for="region in sortedRegions.slice(Math.ceil(sortedRegions.length / 2))"
              :key="region.nombre"
              class="flex justify-between items-center py-1.5 px-2 hover:bg-white rounded transition-colors cursor-pointer text-xs"
              :class="{ 'bg-white shadow-sm': selectedRegion === region.nombre }"
              @click="selectedRegion = selectedRegion === region.nombre ? null : region.nombre"
            >
              <span class="font-medium text-slate-700 flex-1 truncate pr-2">{{ region.nombre }}</span>
              <span class="font-bold text-primary-700 whitespace-nowrap">{{ formatCurrency(region.importe_total) }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Detalles de región seleccionada -->
    <div v-if="selectedRegion" class="mt-6 pt-6 border-t border-slate-200 fade-in">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-lg font-bold text-slate-900">{{ selectedRegion }}</h3>
        <button
          @click="selectedRegion = null"
          class="text-slate-500 hover:text-slate-700 transition-colors"
          aria-label="Cerrar detalles"
        >
          <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div class="bg-primary-50 p-4 rounded-lg">
          <p class="text-sm text-slate-600 mb-1">Total Concesiones</p>
          <p class="text-2xl font-bold text-primary-700">
            {{ (regionData[selectedRegion]?.numero_concesiones || 0).toLocaleString('es-ES') }}
          </p>
        </div>
        <div class="bg-primary-50 p-4 rounded-lg">
          <p class="text-sm text-slate-600 mb-1">Importe Total</p>
          <p class="text-2xl font-bold text-primary-700">
            {{ formatCurrency(regionData[selectedRegion]?.importe_total || 0) }}
          </p>
        </div>
        <div class="bg-primary-50 p-4 rounded-lg">
          <p class="text-sm text-slate-600 mb-1">Importe Medio</p>
          <p class="text-2xl font-bold text-primary-700">
            {{ formatCurrency((regionData[selectedRegion]?.importe_total || 0) / (regionData[selectedRegion]?.numero_concesiones || 1)) }}
          </p>
        </div>
      </div>
    </div>

    <!-- Leyenda -->
    <div class="mt-6 pt-6 border-t border-slate-200">
      <p class="text-sm font-medium text-slate-700 mb-3">Escala de Intensidad</p>
      <div class="flex flex-wrap items-center gap-4">
        <div class="flex items-center gap-2">
          <div class="w-6 h-6 bg-blue-100 rounded"></div>
          <span class="text-xs text-slate-600">Bajo</span>
        </div>
        <div class="flex items-center gap-2">
          <div class="w-6 h-6 bg-blue-300 rounded"></div>
          <span class="text-xs text-slate-600">Medio</span>
        </div>
        <div class="flex items-center gap-2">
          <div class="w-6 h-6 bg-blue-600 rounded"></div>
          <span class="text-xs text-slate-600">Alto</span>
        </div>
        <div class="flex items-center gap-2">
          <div class="w-6 h-6 bg-blue-900 rounded"></div>
          <span class="text-xs text-slate-600">Muy Alto</span>
        </div>
      </div>
      <p class="text-xs text-slate-500 mt-3">
        Mapa vectorial de España bajo licencia CC-BY-4.0 (@svg-maps/spain)
      </p>
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
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

path:focus {
  outline: 2px solid #0ea5e9;
  outline-offset: 2px;
}
</style>
