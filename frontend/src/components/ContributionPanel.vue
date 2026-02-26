<script setup lang="ts">
import type { SpeakerContribution } from '../types/evaluation'

defineProps<{
  contributions: SpeakerContribution[]
}>()

const COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#EC4899']
</script>

<template>
  <div class="space-y-4">
    <h3 class="text-base font-semibold text-gray-800">대화 기여도</h3>

    <!-- Speaking ratio bar -->
    <div class="flex rounded-lg overflow-hidden h-6">
      <div
        v-for="(c, i) in contributions"
        :key="c.speaker"
        :style="{ width: (c.speaking_ratio * 100) + '%', backgroundColor: COLORS[i % COLORS.length] }"
        class="flex items-center justify-center text-xs text-white font-medium truncate px-1"
        :title="`${c.speaker}: ${(c.speaking_ratio * 100).toFixed(1)}%`"
      >
        <span v-if="c.speaking_ratio > 0.1">{{ (c.speaking_ratio * 100).toFixed(0) }}%</span>
      </div>
    </div>

    <!-- Legend + details -->
    <div class="space-y-3">
      <div
        v-for="(c, i) in contributions"
        :key="c.speaker"
        class="flex items-start gap-3"
      >
        <div
          class="w-3 h-3 rounded-full mt-1 flex-shrink-0"
          :style="{ backgroundColor: COLORS[i % COLORS.length] }"
        />
        <div class="min-w-0">
          <div class="flex items-center gap-2 text-sm">
            <span class="font-medium text-gray-800">{{ c.speaker }}</span>
            <span class="text-gray-400">
              {{ c.utterance_count }}회 발화 · {{ c.word_count }}단어
            </span>
          </div>
          <p v-if="c.role_summary" class="text-sm text-gray-600 mt-0.5">
            {{ c.role_summary }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>
