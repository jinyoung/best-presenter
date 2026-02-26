<script setup lang="ts">
import type { ImprovementPoint } from '../types/evaluation'

defineProps<{ improvements: ImprovementPoint[] }>()
</script>

<template>
  <div class="space-y-3">
    <h3 class="text-lg font-semibold text-gray-800">개선 포인트</h3>
    <div
      v-for="item in improvements"
      :key="item.priority"
      class="border rounded-lg p-4 space-y-2"
    >
      <div class="flex items-center gap-2">
        <span class="inline-flex items-center justify-center w-6 h-6 rounded-full bg-blue-100 text-blue-700 text-xs font-bold">
          {{ item.priority }}
        </span>
        <span class="font-medium text-gray-800">{{ item.title }}</span>
      </div>
      <p class="text-sm text-gray-600"><strong>이유:</strong> {{ item.why }}</p>
      <p class="text-sm text-gray-600"><strong>방법:</strong> {{ item.how }}</p>
      <div class="bg-gray-50 rounded p-2 text-sm text-gray-700">
        <strong>예시:</strong> {{ item.example_rewrite }}
      </div>
    </div>
  </div>
</template>
