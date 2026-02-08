<script setup>
import { ref } from 'vue';

const emit = defineEmits(['navigate']);

const activeSection = ref('dashboard');

const menuSections = [
  {
    title: 'Consultas',
    icon: 'search',
    items: [
      { id: 'dashboard', label: 'Dashboard', icon: 'chart' },
      { id: 'search', label: 'Búsqueda de Concesiones', icon: 'search' },
      { id: 'convocatorias', label: 'Convocatorias', icon: 'list' },
      { id: 'international', label: 'Beneficiarios Internacionales', icon: 'globe' },
    ]
  },
  {
    title: 'Estadísticas',
    icon: 'chart-bar',
    items: [
      { id: 'stats-entidad', label: 'Por Tipo de Entidad', icon: 'building' },
      { id: 'stats-organo', label: 'Por Órgano', icon: 'office' },
      { id: 'stats-concentracion', label: 'Concentración', icon: 'trending' },
    ]
  },
  {
    title: 'Notificaciones',
    icon: 'bell',
    items: [
      { id: 'suscripciones', label: 'Mis Suscripciones', icon: 'bookmark' },
      { id: 'crear-suscripcion', label: 'Crear Suscripción', icon: 'plus' },
      { id: 'historial', label: 'Historial', icon: 'clock' },
    ]
  },
  {
    title: 'Monitorización ETL',
    icon: 'server',
    items: [
      { id: 'etl-estado', label: 'Estado del ETL', icon: 'activity' },
      { id: 'etl-logs', label: 'Logs de Ejecución', icon: 'file-text' },
      { id: 'etl-estadisticas', label: 'Estadísticas de Carga', icon: 'bar-chart' },
      { id: 'etl-sync', label: 'Sincronización', icon: 'refresh' },
    ]
  }
];

const navigate = (itemId) => {
  activeSection.value = itemId;
  emit('navigate', itemId);
};

const getIcon = (iconName) => {
  const icons = {
    'search': 'M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z',
    'chart': 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z',
    'list': 'M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2',
    'globe': 'M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z',
    'chart-bar': 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z',
    'building': 'M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4',
    'office': 'M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4',
    'trending': 'M13 7h8m0 0v8m0-8l-8 8-4-4-6 6',
    'bell': 'M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9',
    'bookmark': 'M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z',
    'plus': 'M12 4v16m8-8H4',
    'clock': 'M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z',
    'server': 'M5 12h14M5 12a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v4a2 2 0 01-2 2M5 12a2 2 0 00-2 2v4a2 2 0 002 2h14a2 2 0 002-2v-4a2 2 0 00-2-2m-2-4h.01M17 16h.01',
    'activity': 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z',
    'file-text': 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z',
    'bar-chart': 'M16 8v8m-4-5v5m-4-2v2m-2 4h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z',
    'refresh': 'M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15',
  };
  return icons[iconName] || icons['search'];
};
</script>

<template>
  <aside class="w-64 bg-gray-900 text-white min-h-screen flex flex-col shadow-xl">
    <!-- Logo / Header -->
    <div class="p-6 border-b border-gray-800">
      <h1 class="text-xl font-bold text-white">BDNS</h1>
      <p class="text-xs text-gray-400 mt-1">Consultas e Informes</p>
    </div>

    <!-- Menu -->
    <nav class="flex-1 overflow-y-auto py-4">
      <div v-for="section in menuSections" :key="section.title" class="mb-6">
        <!-- Section Title -->
        <div class="px-6 mb-2">
          <h3 class="text-xs font-semibold text-gray-400 uppercase tracking-wider">
            {{ section.title }}
          </h3>
        </div>

        <!-- Menu Items -->
        <ul class="space-y-1 px-3">
          <li v-for="item in section.items" :key="item.id">
            <button
              @click="navigate(item.id)"
              :class="[
                'w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-all duration-200',
                activeSection === item.id
                  ? 'bg-primary-600 text-white shadow-lg'
                  : 'text-gray-300 hover:bg-gray-800 hover:text-white'
              ]"
            >
              <svg class="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" :d="getIcon(item.icon)" />
              </svg>
              <span class="truncate">{{ item.label }}</span>
            </button>
          </li>
        </ul>
      </div>
    </nav>

    <!-- Footer -->
    <div class="p-4 border-t border-gray-800">
      <div class="flex items-center gap-3 px-3 py-2">
        <div class="w-8 h-8 rounded-full bg-primary-600 flex items-center justify-center">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
        </div>
        <div class="flex-1 min-w-0">
          <p class="text-sm font-medium text-white truncate">Usuario</p>
          <p class="text-xs text-gray-400 truncate">admin@bdns.es</p>
        </div>
      </div>
    </div>
  </aside>
</template>

<style scoped>
/* Estilos personalizados para el scrollbar */
nav::-webkit-scrollbar {
  width: 6px;
}

nav::-webkit-scrollbar-track {
  background: #1f2937;
}

nav::-webkit-scrollbar-thumb {
  background: #4b5563;
  border-radius: 3px;
}

nav::-webkit-scrollbar-thumb:hover {
  background: #6b7280;
}
</style>
