<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits<{
  submit: [transcript: string, removeFillers: boolean]
}>()

const transcript = ref('')
const removeFillers = ref(true)

function handleSubmit() {
  if (transcript.value.trim().length < 10) return
  emit('submit', transcript.value, removeFillers.value)
}
</script>

<template>
  <div class="space-y-3">
    <label class="block text-sm font-medium text-gray-700">트랜스크립트</label>
    <textarea
      v-model="transcript"
      rows="12"
      class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:ring-1 focus:ring-blue-500 resize-y"
      placeholder="발표/회의 트랜스크립트를 붙여넣으세요... (최소 10자)"
    />
    <label class="flex items-center gap-2 text-sm text-gray-600">
      <input type="checkbox" v-model="removeFillers" class="rounded" />
      군더더기 제거 (음, 어, 그...)
    </label>
    <button
      @click="handleSubmit"
      :disabled="transcript.trim().length < 10"
      class="w-full rounded-lg bg-blue-600 px-4 py-2.5 text-sm font-medium text-white hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
    >
      평가 시작
    </button>
  </div>
</template>
