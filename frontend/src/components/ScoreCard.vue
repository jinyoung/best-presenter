<script setup lang="ts">
import { computed } from 'vue'
import type { ScoreSummary } from '../types/evaluation'

const props = defineProps<{ scores: ScoreSummary }>()

const grade = computed(() => {
  const t = props.scores.total
  if (t >= 90) return { label: '탁월', color: 'text-green-600', bg: 'bg-green-50' }
  if (t >= 75) return { label: '우수', color: 'text-blue-600', bg: 'bg-blue-50' }
  if (t >= 60) return { label: '양호', color: 'text-yellow-600', bg: 'bg-yellow-50' }
  if (t >= 40) return { label: '미흡', color: 'text-orange-600', bg: 'bg-orange-50' }
  return { label: '부족', color: 'text-red-600', bg: 'bg-red-50' }
})
</script>

<template>
  <div :class="['rounded-xl p-6 text-center', grade.bg]">
    <div class="text-sm text-gray-500 mb-1">EQI 총점</div>
    <div :class="['text-5xl font-bold', grade.color]">{{ scores.total }}</div>
    <div :class="['text-lg font-medium mt-1', grade.color]">{{ grade.label }}</div>
  </div>
</template>
