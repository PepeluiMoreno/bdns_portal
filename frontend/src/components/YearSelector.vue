<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';

const props = defineProps({
  availableYears: {
    type: Array,
    required: true,
    default: () => []
  },
  modelValue: {
    type: Number,
    required: true
  }
});

const emit = defineEmits(['update:modelValue']);

const selectYear = (year) => {
  emit('update:modelValue', year);
};

const handleKeyPress = (event) => {
  if (props.availableYears.length === 0) return;

  const currentIndex = props.availableYears.indexOf(props.modelValue);

  if (event.key === 'ArrowLeft' && currentIndex > 0) {
    emit('update:modelValue', props.availableYears[currentIndex - 1]);
  } else if (event.key === 'ArrowRight' && currentIndex < props.availableYears.length - 1) {
    emit('update:modelValue', props.availableYears[currentIndex + 1]);
  }
};

onMounted(() => {
  window.addEventListener('keydown', handleKeyPress);
});

onBeforeUnmount(() => {
  window.removeEventListener('keydown', handleKeyPress);
});
</script>

<template>
  <div class="bg-white rounded-lg shadow-md p-6">
    <div class="flex items-center justify-between mb-4">
      <h2 class="text-lg font-bold text-slate-900">Ejercicio Fiscal</h2>
      <div class="flex items-center gap-2 text-sm text-slate-600">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <span>Usa ← → para navegar</span>
      </div>
    </div>

    <!-- Timeline -->
    <div class="relative">
      <!-- Línea de fondo -->
      <div class="absolute top-1/2 left-0 right-0 h-1 bg-slate-200 -translate-y-1/2 rounded-full"></div>

      <!-- Línea de progreso -->
      <div
        class="absolute top-1/2 left-0 h-1 bg-primary-500 -translate-y-1/2 rounded-full transition-all duration-300"
        :style="{
          width: availableYears.length > 0
            ? `${((availableYears.indexOf(modelValue) + 1) / availableYears.length) * 100}%`
            : '0%'
        }"
      ></div>

      <!-- Puntos de años -->
      <div class="relative flex justify-between items-center">
        <button
          v-for="year in availableYears"
          :key="year"
          @click="selectYear(year)"
          :class="[
            'relative flex flex-col items-center transition-all duration-300 focus:outline-none group',
            modelValue === year ? 'z-10' : 'z-0'
          ]"
          :aria-label="`Seleccionar año ${year}`"
          :aria-pressed="modelValue === year"
        >
          <!-- Punto -->
          <div
            :class="[
              'rounded-full transition-all duration-300 border-4 bg-white',
              modelValue === year
                ? 'w-6 h-6 border-primary-600 shadow-lg scale-125'
                : 'w-4 h-4 border-slate-300 hover:border-primary-400 hover:scale-110'
            ]"
          ></div>

          <!-- Etiqueta del año -->
          <span
            :class="[
              'mt-3 text-sm font-medium transition-all duration-300',
              modelValue === year
                ? 'text-primary-700 font-bold text-base'
                : 'text-slate-600 group-hover:text-slate-900'
            ]"
          >
            {{ year }}
          </span>
        </button>
      </div>
    </div>

    <!-- Año seleccionado destacado -->
    <div class="mt-6 text-center">
      <p class="text-sm text-slate-600">Año seleccionado</p>
      <p class="text-3xl font-bold text-primary-700">{{ modelValue }}</p>
    </div>
  </div>
</template>

<style scoped>
button:focus {
  outline: 2px solid #0ea5e9;
  outline-offset: 4px;
  border-radius: 9999px;
}
</style>
