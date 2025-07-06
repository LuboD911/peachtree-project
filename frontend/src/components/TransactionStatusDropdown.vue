<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import api from '../utils/axios'
import type { Status, ApiError, SelectEvent } from '../types'

const props = defineProps<{ currentStatusId: number }>()
const statuses = ref<Status[]>([])
const selected = ref<number>(props.currentStatusId)

const fetchStatuses = async (): Promise<void> => {
  const response = await api.get<Status[]>('/transactions/statuses')
  statuses.value = response.data
}

onMounted(fetchStatuses)

// Watch for changes in the currentStatusId prop and update selected
watch(() => props.currentStatusId, (newValue: number) => {
  selected.value = newValue
})

const emit = defineEmits<{
  (e: 'change', value: number): void
}>()

const onChange = (e: Event): void => {
  const value = Number((e.target as HTMLSelectElement).value)
  emit('change', value)
}
</script>

<template>
  <select :value="selected" @change="onChange" class="block w-full rounded border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 px-3 py-2">
    <option v-for="s in statuses" :key="s.id" :value="s.id">
      {{ s.name }}
    </option>
  </select>
</template> 