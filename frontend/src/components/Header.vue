<template>
  <header class="bg-white shadow-sm border-b border-slate-200 sticky top-0 z-30">
    <div class="px-4 sm:px-6 lg:px-8 py-4">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-xl font-bold text-slate-900">Consultas e Informes</h1>
          <p class="text-xs text-slate-500">Base de Datos Nacional de Subvenciones</p>
        </div>

        <div class="flex items-center gap-4">
          <div class="text-right">
            <p class="text-xs text-slate-500">Última actualización</p>
            <p class="text-sm font-semibold text-slate-900">{{ lastUpdate }}</p>
          </div>
          <button class="p-2 hover:bg-slate-100 rounded-lg transition-colors">
            <svg class="w-5 h-5 text-slate-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue';

const lastUpdate = computed(() => {
  const now = new Date();
  return now.toLocaleDateString('es-ES', { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
});
</script>

<style scoped>
</style>
