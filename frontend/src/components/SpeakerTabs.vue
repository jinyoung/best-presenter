<script setup lang="ts">
defineProps<{
  speakers: string[]
  selected: string
}>()

const emit = defineEmits<{
  select: [speaker: string]
}>()
</script>

<template>
  <div class="flex gap-1 flex-wrap">
    <button
      v-for="speaker in speakers"
      :key="speaker"
      @click="emit('select', speaker)"
      :class="[
        'px-4 py-2 rounded-lg text-sm font-medium transition-colors',
        selected === speaker
          ? 'bg-blue-600 text-white shadow-sm'
          : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
      ]"
    >
      {{ speaker }}
    </button>
  </div>
</template>
