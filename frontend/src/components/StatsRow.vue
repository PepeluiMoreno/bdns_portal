<script setup>
import StatCard from './StatCard.vue';

const props = defineProps({
  stats: {
    type: Object,
    required: true,
    default: () => ({
      totalConcesiones: 0,
      totalImporte: 0,
      beneficiariosUnicos: 0,
      convocatoriasActivas: 0,
      topBeneficiario: { nombre: '', importe: 0 },
      concentracionTop10: 0,
      importeMedio: 0,
      ccaaLider: { nombre: '', importe: 0 }
    })
  }
});
</script>

<template>
  <div class="space-y-6">
    <!-- Fila 1: Métricas Principales -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <StatCard
        label="Total de Concesiones"
        :value="stats.totalConcesiones"
        format="number"
        :trend="12"
      >
        <template #icon>
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        </template>
      </StatCard>

      <StatCard
        label="Importe Total Concedido"
        :value="stats.totalImporte"
        format="currency"
        :trend="8"
      >
        <template #icon>
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </template>
      </StatCard>

      <StatCard
        label="Beneficiarios Únicos"
        :value="stats.beneficiariosUnicos"
        format="number"
        :trend="15"
      >
        <template #icon>
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.856-1.487M15 10a3 3 0 11-6 0 3 3 0 016 0zM15 20H9m6 0h.01" />
          </svg>
        </template>
      </StatCard>

      <StatCard
        label="Convocatorias Activas"
        :value="stats.convocatoriasActivas"
        format="number"
        :trend="5"
      >
        <template #icon>
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
        </template>
      </StatCard>
    </div>

    <!-- Fila 2: Análisis Avanzado -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <StatCard
        label="Top Beneficiario"
        :value="stats.topBeneficiario.importe"
        :subtitle="stats.topBeneficiario.nombre"
        format="currency"
      >
        <template #icon>
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
          </svg>
        </template>
      </StatCard>

      <StatCard
        label="Concentración Top 10"
        :value="stats.concentracionTop10"
        subtitle="% del total"
        format="number"
      >
        <template #icon>
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
          </svg>
        </template>
      </StatCard>

      <StatCard
        label="Importe Medio"
        :value="stats.importeMedio"
        format="currency"
      >
        <template #icon>
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
          </svg>
        </template>
      </StatCard>

      <StatCard
        label="CCAA Líder"
        :value="stats.ccaaLider.importe"
        :subtitle="stats.ccaaLider.nombre"
        format="currency"
      >
        <template #icon>
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
        </template>
      </StatCard>
    </div>
  </div>
</template>

<style scoped>
</style>
