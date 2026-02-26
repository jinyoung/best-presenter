<script setup lang="ts">
import { ref, onMounted } from 'vue'
import HomeView from './views/HomeView.vue'
import SettingsModal from './components/SettingsModal.vue'
import { getSettings } from './api/client'

const showSettings = ref(false)
const apiKeySet = ref(true) // assume true until checked

onMounted(async () => {
  try {
    const s = await getSettings()
    apiKeySet.value = s.api_key_set
    if (!s.api_key_set) showSettings.value = true
  } catch {
    // backend not ready yet or network error — don't block
  }
})

function onSettingsSaved() {
  apiKeySet.value = true
}
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <header class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold text-gray-900">Best Presenter</h1>
          <p class="text-sm text-gray-500">EQI 6축 프레젠테이션 평가 시스템</p>
        </div>
        <button
          @click="showSettings = true"
          class="p-2 rounded-lg text-gray-500 hover:text-gray-700 hover:bg-gray-100 transition"
          title="설정"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>
    </header>
    <main>
      <HomeView />
    </main>

    <SettingsModal :visible="showSettings" @close="showSettings = false" @saved="onSettingsSaved" />
  </div>
</template>
