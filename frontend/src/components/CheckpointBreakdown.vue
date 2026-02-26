<script setup lang="ts">
import { computed } from 'vue'
import type { CheckpointItem } from '../types/evaluation'
import { AXIS_LABELS } from '../types/evaluation'

const props = defineProps<{ checkpoints: CheckpointItem[] }>()

const grouped = computed(() => {
  const map = new Map<string, CheckpointItem[]>()
  for (const cp of props.checkpoints) {
    if (!map.has(cp.axis)) map.set(cp.axis, [])
    map.get(cp.axis)!.push(cp)
  }
  return map
})

function scoreColor(earned: number, max: number) {
  const ratio = earned / max
  if (ratio >= 0.8) return 'bg-green-500'
  if (ratio >= 0.6) return 'bg-blue-500'
  if (ratio >= 0.4) return 'bg-yellow-500'
  return 'bg-red-500'
}
</script>

<template>
  <div class="space-y-4">
    <h3 class="text-lg font-semibold text-gray-800">체크포인트 상세</h3>
    <div v-for="[axis, items] in grouped" :key="axis" class="border rounded-lg p-3">
      <h4 class="font-medium text-gray-700 mb-2">{{ AXIS_LABELS[axis] || axis }}</h4>
      <div v-for="cp in items" :key="cp.checkpoint" class="ml-2 mb-2">
        <div class="flex items-center justify-between text-sm">
          <span class="text-gray-600">{{ cp.checkpoint }}</span>
          <span class="flex items-center gap-1.5">
            <span :class="['inline-block w-2 h-2 rounded-full', scoreColor(cp.earned, cp.max_score)]" />
            <span class="font-mono">{{ cp.earned }}/{{ cp.max_score }}</span>
          </span>
        </div>
        <div v-if="cp.evidence_quotes.length" class="mt-1 ml-2 space-y-0.5">
          <div
            v-for="(q, i) in cp.evidence_quotes"
            :key="i"
            :class="['text-xs px-2 py-0.5 rounded', q.sentiment === 'positive' ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700']"
          >
            [{{ q.loc }}] {{ q.text }}
          </div>
        </div>
        <div v-if="cp.fix" class="text-xs text-orange-600 mt-1 ml-2">
          {{ cp.fix }}
        </div>
      </div>
    </div>
  </div>
</template>
