<script setup lang="ts">
const audience = defineModel<string>('audience', { default: '' })
const purpose = defineModel<string>('purpose', { default: '' })

const audienceOptions = [
  { value: '', label: '자동 감지' },
  { value: 'executive', label: '임원' },
  { value: 'pm', label: 'PM' },
  { value: 'engineer', label: '개발자' },
  { value: 'customer', label: '고객' },
  { value: 'auditor', label: '감사' },
]

const purposeOptions = [
  { value: '', label: '자동 감지' },
  { value: 'project_status', label: '진행상황 보고' },
  { value: 'architecture', label: '아키텍처 설명' },
  { value: 'decision_request', label: '의사결정 요청' },
  { value: 'persuasion', label: '설득' },
  { value: 'education', label: '교육' },
]
</script>

<template>
  <div class="grid grid-cols-2 gap-3">
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">청중</label>
      <select v-model="audience" class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm">
        <option v-for="o in audienceOptions" :key="o.value" :value="o.value">{{ o.label }}</option>
      </select>
    </div>
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">목적</label>
      <select v-model="purpose" class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm">
        <option v-for="o in purposeOptions" :key="o.value" :value="o.value">{{ o.label }}</option>
      </select>
    </div>
  </div>
</template>
