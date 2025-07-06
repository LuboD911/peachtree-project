<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '../utils/axios'
import type { 
  Contractor, 
  Status, 
  Transaction, 
  ApiError,
  KeyboardEvent 
} from '../types'

const emit = defineEmits<{
  (e: 'select', id: number): void
}>()

const transactions = ref<Transaction[]>([])
const sort_by = ref<string>('date')
const sort_order = ref<string>('desc')
const search = ref<string>('')
let searchTimeout: number | null = null

const fetchTransactions = async (): Promise<void> => {
  const res = await api.get<Transaction[]>('/transactions', {
    params: { sort_by: sort_by.value, sort_order: sort_order.value, search: search.value }
  })
  transactions.value = res.data
}

onMounted(fetchTransactions)

const formatDate = (dateString: string): string => {
  return new Date(dateString).toISOString().split('T')[0]
}

const formatAmount = (amount: number): string => {
  return `-$${amount.toFixed(2)}`
}

const formatPaymentType = (type: string | undefined): string => {
  if (!type) return ''
  
  // Convert snake_case to Title Case
  return type
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}

const handleSort = (field: string): void => {
  if (sort_by.value === field) {
    // Toggle order if same field
    sort_order.value = sort_order.value === 'asc' ? 'desc' : 'asc'
  } else {
    // Set new field with default desc order
    sort_by.value = field
    sort_order.value = 'desc'
  }
  fetchTransactions()
}

const getSortIcon = (field: string): string => {
  if (sort_by.value !== field) {
    return ''
  }
  return sort_order.value === 'asc' ? '↑' : '↓'
}

const handleSearchInput = (event: Event): void => {
  // Prevent any unintended behavior when using keyboard shortcuts
  event.stopPropagation()
  
  // Clear any existing timeout
  if (searchTimeout) {
    clearTimeout(searchTimeout)
  }
  
  // Only search if there's actual content or if the search was cleared
  if (search.value.trim() !== '' || search.value === '') {
    searchTimeout = setTimeout(() => {
      fetchTransactions()
    }, 500)
  }
}

const handleSearchKeydown = (event: KeyboardEvent): void => {
  // Prevent Cmd+A/Ctrl+A from causing any unintended behavior
  if (event.metaKey && event.key === 'a') {
    // Allow the default select all behavior but prevent any side effects
    event.stopPropagation()
  }
}

const handleTransactionClick = (event: Event, txId: number): void => {
  // Prevent any unintended clicks
  event.stopPropagation()
  emit('select', txId)
}

// Expose the fetchTransactions method to parent components
defineExpose({
  fetchTransactions
})
</script>

<template>
  <div>
    <div class="flex flex-col sm:flex-row gap-4 mb-4 items-center">
      <input v-model="search" @input="handleSearchInput" @keydown="handleSearchKeydown" placeholder="Search by contractor..." class="flex-1 rounded border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 px-3 py-2" />
      
      <div class="flex items-center gap-2">
        <span class="text-sm font-medium text-gray-700">Sort by:</span>
        <button 
          @click="handleSort('date')" 
          :class="[
            'flex items-center gap-1 px-3 py-2 rounded border text-sm font-medium transition-colors',
            sort_by === 'date' 
              ? 'bg-indigo-100 border-indigo-300 text-indigo-700' 
              : 'bg-white border-gray-300 text-gray-700 hover:bg-gray-50'
          ]"
        >
          Date {{ getSortIcon('date') }}
        </button>
        <button 
          @click="handleSort('contractor')" 
          :class="[
            'flex items-center gap-1 px-3 py-2 rounded border text-sm font-medium transition-colors',
            sort_by === 'contractor' 
              ? 'bg-indigo-100 border-indigo-300 text-indigo-700' 
              : 'bg-white border-gray-300 text-gray-700 hover:bg-gray-50'
          ]"
        >
          Beneficiary {{ getSortIcon('contractor') }}
        </button>
        <button 
          @click="handleSort('amount')" 
          :class="[
            'flex items-center gap-1 px-3 py-2 rounded border text-sm font-medium transition-colors',
            sort_by === 'amount' 
              ? 'bg-indigo-100 border-indigo-300 text-indigo-700' 
              : 'bg-white border-gray-300 text-gray-700 hover:bg-gray-50'
          ]"
        >
          Amount {{ getSortIcon('amount') }}
        </button>
      </div>
    </div>
    
    <ul class="divide-y divide-gray-200 bg-gray-50 rounded shadow">
      <li v-for="tx in transactions" :key="tx.id" @click="handleTransactionClick($event, tx.id)" class="flex items-center gap-4 px-4 py-3 cursor-pointer hover:bg-indigo-50 transition">
        <span :style="{ borderLeft: '5px solid ' + tx.status.color }" class="h-6"></span>
        <span class="flex-1 text-gray-700">{{ formatDate(tx.date) }}</span>
        <div class="flex-1 flex items-center gap-3">
          <img :src="tx.contractor.image_url" :alt="tx.contractor.name" class="w-8 h-8 rounded-full object-cover" />
          <div class="flex flex-col">
            <span class="text-gray-700 font-medium">{{ tx.contractor.name }}</span>
            <span v-if="tx.type" class="text-xs text-gray-500">{{ formatPaymentType(tx.type) }}</span>
          </div>
        </div>
        <span class="flex-1 text-gray-700">{{ formatAmount(tx.amount) }}</span>
      </li>
    </ul>
  </div>
</template> 