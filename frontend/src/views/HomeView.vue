<script setup lang="ts">
import { ref } from 'vue'
import { useEvaluation } from '../composables/useEvaluation'
import TranscriptInput from '../components/TranscriptInput.vue'
import OptionSelectors from '../components/OptionSelectors.vue'
import RadarChart from '../components/RadarChart.vue'
import ScoreCard from '../components/ScoreCard.vue'
import CheckpointBreakdown from '../components/CheckpointBreakdown.vue'
import ImprovementList from '../components/ImprovementList.vue'
import RewritePanel from '../components/RewritePanel.vue'
import LoadingOverlay from '../components/LoadingOverlay.vue'
import SpeakerTabs from '../components/SpeakerTabs.vue'
import ContributionPanel from '../components/ContributionPanel.vue'

const audience = ref('')
const purpose = ref('')

const {
  result,
  loading,
  error,
  evaluate,
  selectedSpeaker,
  isMultiSpeakerResult,
  multiSpeakerResult,
  singleResult,
  selectSpeaker,
} = useEvaluation()

async function handleSubmit(transcript: string, removeFillers: boolean) {
  await evaluate({
    transcript,
    audience: audience.value || undefined,
    purpose: purpose.value || undefined,
    remove_fillers: removeFillers,
  })
}
</script>

<template>
  <LoadingOverlay :visible="loading" />

  <div class="max-w-7xl mx-auto px-4 py-6">
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Left: Input -->
      <div class="space-y-4">
        <div class="bg-white rounded-xl shadow-sm border p-5 space-y-4">
          <h2 class="text-lg font-semibold text-gray-800">평가 입력</h2>
          <OptionSelectors v-model:audience="audience" v-model:purpose="purpose" />
          <TranscriptInput @submit="handleSubmit" />
        </div>

        <div v-if="error" class="bg-red-50 border border-red-200 rounded-xl p-4 text-sm text-red-700">
          {{ error }}
        </div>

        <!-- Contribution Panel (for multi-speaker, shown under input) -->
        <div v-if="multiSpeakerResult" class="bg-white rounded-xl shadow-sm border p-5">
          <ContributionPanel :contributions="multiSpeakerResult.contributions" />
        </div>
      </div>

      <!-- Right: Results -->
      <div class="space-y-4">
        <template v-if="result">
          <!-- Speaker Tabs (multi-speaker only) -->
          <div v-if="isMultiSpeakerResult && multiSpeakerResult && selectedSpeaker" class="bg-white rounded-xl shadow-sm border p-4">
            <h3 class="text-sm font-medium text-gray-500 mb-2">화자별 평가</h3>
            <SpeakerTabs
              :speakers="multiSpeakerResult.speakers"
              :selected="selectedSpeaker"
              @select="selectSpeaker"
            />
          </div>

          <!-- Score + Radar (uses singleResult for both modes) -->
          <template v-if="singleResult">
            <div class="bg-white rounded-xl shadow-sm border p-5">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4 items-start">
                <ScoreCard :scores="singleResult.scores" />
                <RadarChart :scores="singleResult.scores" />
              </div>
            </div>

            <div class="bg-white rounded-xl shadow-sm border p-5">
              <CheckpointBreakdown :checkpoints="singleResult.checkpoint_breakdown" />
            </div>

            <div class="bg-white rounded-xl shadow-sm border p-5">
              <ImprovementList :improvements="singleResult.improvement_points" />
            </div>

            <div class="bg-white rounded-xl shadow-sm border p-5">
              <RewritePanel :rewrites="singleResult.rewrites" />
            </div>
          </template>
        </template>

        <div v-else-if="!loading" class="bg-white rounded-xl shadow-sm border p-12 text-center text-gray-400">
          <p class="text-lg">트랜스크립트를 입력하고 평가를 시작하세요</p>
          <p class="text-sm mt-1">결과가 여기에 표시됩니다</p>
        </div>
      </div>
    </div>
  </div>
</template>
