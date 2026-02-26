<script setup lang="ts">
import { computed } from 'vue'
import { Radar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
  Tooltip,
} from 'chart.js'
import type { ScoreSummary } from '../types/evaluation'
import { AXES, AXIS_LABELS } from '../types/evaluation'

ChartJS.register(RadialLinearScale, PointElement, LineElement, Filler, Tooltip)

const props = defineProps<{ scores: ScoreSummary }>()

const chartData = computed(() => ({
  labels: AXES.map(a => AXIS_LABELS[a]),
  datasets: [
    {
      label: 'EQI 점수',
      data: AXES.map(a => props.scores[a as keyof ScoreSummary] as number),
      backgroundColor: 'rgba(59, 130, 246, 0.2)',
      borderColor: 'rgba(59, 130, 246, 1)',
      borderWidth: 2,
      pointBackgroundColor: 'rgba(59, 130, 246, 1)',
    },
  ],
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: true,
  scales: {
    r: {
      beginAtZero: true,
      max: 100,
      ticks: { stepSize: 20 },
    },
  },
  plugins: {
    tooltip: { enabled: true },
  },
}
</script>

<template>
  <div class="w-full max-w-md mx-auto">
    <Radar :data="chartData" :options="chartOptions" />
  </div>
</template>
