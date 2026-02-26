<script setup lang="ts">
import { ref } from 'vue'
import type { Rewrites } from '../types/evaluation'

const props = defineProps<{ rewrites: Rewrites }>()

const tabs = [
  { key: '30sec_executive' as const, label: '임원용 30초' },
  { key: '2min_engineer' as const, label: '개발자용 2분' },
  { key: 'doc_summary' as const, label: '문서용 요약' },
]

const activeTab = ref<keyof Rewrites>('30sec_executive')
</script>

<template>
  <div class="space-y-3">
    <h3 class="text-lg font-semibold text-gray-800">리라이트</h3>
    <div class="flex gap-1 border-b">
      <button
        v-for="tab in tabs"
        :key="tab.key"
        @click="activeTab = tab.key"
        :class="[
          'px-3 py-2 text-sm font-medium border-b-2 transition-colors',
          activeTab === tab.key
            ? 'border-blue-500 text-blue-600'
            : 'border-transparent text-gray-500 hover:text-gray-700'
        ]"
      >
        {{ tab.label }}
      </button>
    </div>
    <div class="bg-gray-50 rounded-lg p-4 text-sm text-gray-700 whitespace-pre-wrap leading-relaxed">
      {{ rewrites[activeTab] }}
    </div>
  </div>
</template>
