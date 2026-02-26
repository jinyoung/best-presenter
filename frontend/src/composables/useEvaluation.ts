import { ref, computed } from 'vue'
import type { EvaluateRequest, EvaluateResponse, EvaluationResult, MultiSpeakerResponse } from '../types/evaluation'
import { isMultiSpeaker } from '../types/evaluation'
import { postEvaluate } from '../api/client'

export function useEvaluation() {
  const result = ref<EvaluationResult | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)
  const selectedSpeaker = ref<string | null>(null)

  const isMultiSpeakerResult = computed(() =>
    result.value ? isMultiSpeaker(result.value) : false
  )

  const multiSpeakerResult = computed<MultiSpeakerResponse | null>(() =>
    result.value && isMultiSpeaker(result.value) ? result.value : null
  )

  const singleResult = computed<EvaluateResponse | null>(() => {
    if (!result.value) return null
    if (isMultiSpeaker(result.value)) {
      // Return selected speaker's evaluation
      const speaker = selectedSpeaker.value ?? result.value.speakers[0]
      return speaker ? result.value.evaluations[speaker] ?? null : null
    }
    return result.value
  })

  async function evaluate(request: EvaluateRequest) {
    loading.value = true
    error.value = null
    result.value = null
    selectedSpeaker.value = null

    try {
      result.value = await postEvaluate(request)
      // Auto-select first speaker for multi-speaker results
      if (result.value && isMultiSpeaker(result.value)) {
        selectedSpeaker.value = result.value.speakers[0] ?? null
      }
    } catch (e: any) {
      error.value = e.response?.data?.detail || e.message || '평가 중 오류가 발생했습니다.'
    } finally {
      loading.value = false
    }
  }

  function selectSpeaker(speaker: string) {
    selectedSpeaker.value = speaker
  }

  function reset() {
    result.value = null
    error.value = null
    selectedSpeaker.value = null
  }

  return {
    result,
    loading,
    error,
    evaluate,
    reset,
    selectedSpeaker,
    isMultiSpeakerResult,
    multiSpeakerResult,
    singleResult,
    selectSpeaker,
  }
}
