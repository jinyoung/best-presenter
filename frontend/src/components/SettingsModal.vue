<script setup lang="ts">
import { ref, watch } from 'vue'
import { getSettings, saveSettings } from '../api/client'

const props = defineProps<{ visible: boolean }>()
const emit = defineEmits<{
  (e: 'close'): void
  (e: 'saved'): void
}>()

const apiKey = ref('')
const model = ref('gpt-4o')
const maskedKey = ref('')
const saving = ref(false)
const errorMsg = ref('')
const showKey = ref(false)

const models = ['gpt-4o', 'gpt-4o-mini', 'gpt-4-turbo']

watch(() => props.visible, async (v) => {
  if (!v) return
  errorMsg.value = ''
  apiKey.value = ''
  showKey.value = false
  try {
    const s = await getSettings()
    maskedKey.value = s.api_key_masked
    model.value = s.model
  } catch {
    maskedKey.value = ''
  }
})

async function handleSave() {
  saving.value = true
  errorMsg.value = ''
  try {
    const body: { api_key?: string; model?: string } = { model: model.value }
    if (apiKey.value) body.api_key = apiKey.value
    await saveSettings(body)
    emit('saved')
    emit('close')
  } catch {
    errorMsg.value = '설정 저장에 실패했습니다.'
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <Teleport to="body">
    <div v-if="visible" class="fixed inset-0 z-50 flex items-center justify-center bg-black/40" @click.self="emit('close')">
      <div class="bg-white rounded-2xl shadow-xl w-full max-w-md mx-4 p-6 space-y-5">
        <div class="flex items-center justify-between">
          <h2 class="text-lg font-semibold text-gray-900">설정</h2>
          <button @click="emit('close')" class="text-gray-400 hover:text-gray-600 text-xl leading-none">&times;</button>
        </div>

        <!-- API Key -->
        <div class="space-y-1.5">
          <label class="block text-sm font-medium text-gray-700">OpenAI API Key</label>
          <div v-if="maskedKey && !apiKey" class="text-xs text-gray-500">현재: {{ maskedKey }}</div>
          <div class="relative">
            <input
              v-model="apiKey"
              :type="showKey ? 'text' : 'password'"
              placeholder="sk-..."
              class="w-full border border-gray-300 rounded-lg px-3 py-2 pr-10 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
            <button
              type="button"
              @click="showKey = !showKey"
              class="absolute right-2 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 text-xs"
            >
              {{ showKey ? '숨김' : '보기' }}
            </button>
          </div>
        </div>

        <!-- Model -->
        <div class="space-y-1.5">
          <label class="block text-sm font-medium text-gray-700">모델</label>
          <select
            v-model="model"
            class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          >
            <option v-for="m in models" :key="m" :value="m">{{ m }}</option>
          </select>
        </div>

        <div v-if="errorMsg" class="text-sm text-red-600">{{ errorMsg }}</div>

        <button
          @click="handleSave"
          :disabled="saving"
          class="w-full bg-blue-600 text-white rounded-lg py-2.5 text-sm font-medium hover:bg-blue-700 disabled:opacity-50 transition"
        >
          {{ saving ? '저장 중...' : '저장' }}
        </button>
      </div>
    </div>
  </Teleport>
</template>
