<script setup>
import { computed } from 'vue';
import { Pie } from 'vue-chartjs';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { getBeneficiaryTypeLabel, formatCurrency } from '../utils/regions';

ChartJS.register(ArcElement, Tooltip, Legend);

const props = defineProps({
  year: {
    type: Number,
    required: true
  },
  data: {
    type: Array,
    required: true,
    default: () => []
  }
});

const chartData = computed(() => {
  // Filtrar por año
  const yearData = props.data.filter(d => d.anio === props.year);

  if (yearData.length === 0) {
    return {
      labels: ['Sin datos'],
      datasets: [{
        data: [1],
        backgroundColor: ['#e0f2fe'],
      }]
    };
  }

  // Agrupar por tipo de entidad
  const grouped = yearData.reduce((acc, stat) => {
    const tipo = stat.tipo_entidad;
    if (!acc[tipo]) {
      acc[tipo] = 0;
    }
    acc[tipo] += stat.importe_total;
    return acc;
  }, {});

  // Ordenar por importe descendente y tomar top 10
  const sorted = Object.entries(grouped)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10);

  return {
    labels: sorted.map(([tipo]) => getBeneficiaryTypeLabel(tipo)),
    datasets: [{
      data: sorted.map(([, importe]) => importe),
      backgroundColor: [
        '#3b82f6', // Azul
        '#ef4444', // Rojo
        '#10b981', // Verde
        '#f59e0b', // Ámbar
        '#8b5cf6', // Púrpura
        '#ec4899', // Rosa
        '#06b6d4', // Cian
        '#14b8a6', // Teal
        '#f97316', // Naranja
        '#84cc16'  // Lima
      ],
      borderWidth: 2,
      borderColor: '#ffffff',
    }]
  };
});

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: true,
      position: 'right',
      labels: {
        padding: 8,
        font: {
          size: 10,
          family: 'Inter, system-ui, sans-serif'
        },
        usePointStyle: true,
        pointStyle: 'circle',
        boxWidth: 10,
        boxHeight: 10,
        generateLabels: (chart) => {
          const data = chart.data;
          if (data.labels.length && data.datasets.length) {
            return data.labels.map((label, i) => {
              const dataset = data.datasets[0];
              const backgroundColor = Array.isArray(dataset.backgroundColor)
                ? dataset.backgroundColor[i]
                : dataset.backgroundColor;

              return {
                text: label,
                fillStyle: backgroundColor,
                strokeStyle: backgroundColor,
                hidden: false,
                index: i
              };
            });
          }
          return [];
        }
      }
    },
    tooltip: {
      callbacks: {
        label: (context) => {
          const label = context.label || '';
          const value = formatCurrency(context.parsed);
          const total = context.dataset.data.reduce((sum, val) => sum + val, 0);
          const percentage = ((context.parsed / total) * 100).toFixed(1);
          return `${label}: ${value} (${percentage}%)`;
        }
      },
      backgroundColor: '#1e293b',
      titleColor: '#ffffff',
      bodyColor: '#ffffff',
      padding: 12,
      borderColor: '#475569',
      borderWidth: 1,
    }
  }
};
</script>

<template>
  <div class="bg-white rounded-lg shadow-md p-4 h-full flex flex-col">
    <div class="flex items-center justify-between mb-3">
      <h2 class="text-lg font-bold text-slate-900">
        Distribución por Tipo de Beneficiario
      </h2>
      <span class="px-2 py-1 bg-primary-100 text-primary-700 rounded-full text-xs font-medium">
        {{ year }}
      </span>
    </div>

    <p class="text-xs text-slate-600 mb-3">
      Importes concedidos por forma jurídica (Top 10)
    </p>

    <div class="flex-1 min-h-0">
      <Pie :data="chartData" :options="chartOptions" />
    </div>
  </div>
</template>

<style scoped>
</style>
