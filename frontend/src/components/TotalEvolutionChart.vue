<script setup>
import { computed } from 'vue';
import { Line } from 'vue-chartjs';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
import { formatCurrency } from '../utils/regions';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const props = defineProps({
  data: {
    type: Array,
    required: true,
    default: () => []
  },
  availableYears: {
    type: Array,
    required: true,
    default: () => []
  }
});

const chartData = computed(() => {
  // Agrupar por año
  const yearlyData = props.availableYears.map(year => {
    const yearStats = props.data.filter(d => d.anio === year);
    const total = yearStats.reduce((sum, stat) => sum + (stat.importe_total || 0), 0);
    return { year, total };
  });

  return {
    labels: yearlyData.map(d => d.year.toString()),
    datasets: [{
      label: 'Importe Total Concedido',
      data: yearlyData.map(d => d.total),
      borderColor: '#3b82f6',
      backgroundColor: 'rgba(59, 130, 246, 0.1)',
      tension: 0.4,
      fill: true,
      borderWidth: 3,
      pointRadius: 5,
      pointHoverRadius: 7,
      pointBackgroundColor: '#3b82f6',
      pointBorderColor: '#ffffff',
      pointBorderWidth: 2,
    }]
  };
});

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false
    },
    tooltip: {
      callbacks: {
        label: (context) => {
          return `Importe: ${formatCurrency(context.parsed.y)}`;
        }
      },
      backgroundColor: '#1e293b',
      titleColor: '#ffffff',
      bodyColor: '#ffffff',
      padding: 12,
      borderColor: '#475569',
      borderWidth: 1,
    }
  },
  scales: {
    x: {
      grid: {
        display: false
      },
      ticks: {
        font: {
          size: 11,
          family: 'Inter, system-ui, sans-serif'
        }
      }
    },
    y: {
      beginAtZero: true,
      grid: {
        color: '#e2e8f0'
      },
      ticks: {
        font: {
          size: 11,
          family: 'Inter, system-ui, sans-serif'
        },
        callback: function(value) {
          return formatCurrency(value);
        }
      }
    }
  }
};
</script>

<template>
  <div class="bg-white rounded-lg shadow-md p-4 h-full flex flex-col">
    <div class="flex items-center justify-between mb-3">
      <h2 class="text-lg font-bold text-slate-900">
        Evolución del Importe Total
      </h2>
    </div>

    <p class="text-xs text-slate-600 mb-3">
      Tendencia histórica de subvenciones concedidas
    </p>

    <div class="flex-1 min-h-0">
      <Line :data="chartData" :options="chartOptions" />
    </div>
  </div>
</template>

<style scoped>
</style>
