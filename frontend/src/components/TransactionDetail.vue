<script setup lang="ts">
import { ref, watch } from 'vue'
import api from '../utils/axios'
import TransactionStatusDropdown from './TransactionStatusDropdown.vue'
import type { 
  Contractor, 
  Status, 
  Transaction, 
  UpdateTransactionStatusRequest,
  ApiError 
} from '../types'

const props = defineProps<{ transactionId: number }>()
const transaction = ref<Transaction | null>(null)

const fetchTransaction = async (): Promise<void> => {
  const res = await api.get<Transaction>(`/transactions/${props.transactionId}`)
  transaction.value = res.data
}

watch(() => props.transactionId, fetchTransaction, { immediate: true })

const onStatusChange = async (newStatusId: number): Promise<void> => {
  try {
    const statusData: UpdateTransactionStatusRequest = { status_id: newStatusId }
    await api.put(`/transactions/${props.transactionId}/status`, statusData)
    fetchTransaction()
  } catch (err: unknown) {
    const apiError = err as ApiError
    console.error('Failed to update transaction status:', apiError)
  }
}

const formatDate = (dateString: string): string => {
  return new Date(dateString).toISOString().split('T')[0]
}

const formatAmount = (amount: number): string => {
  return `$${amount.toFixed(2)}`
}
</script>

<template>
  <div v-if="transaction" class="space-y-4">
    <table class="min-w-full text-sm text-gray-700">
      <tbody>
        <tr><td class="font-semibold pr-4 py-1">Amount</td><td>{{ formatAmount(transaction.amount) }}</td></tr>
        <tr><td class="font-semibold pr-4 py-1">Date</td><td>{{ formatDate(transaction.date) }}</td></tr>
        <tr>
          <td class="font-semibold pr-4 py-1">To contractor</td>
          <td class="flex items-center gap-3">
            <img :src="transaction.contractor.image_url" :alt="transaction.contractor.name" class="w-8 h-8 rounded-full object-cover" />
            <span>{{ transaction.contractor.name }}</span>
          </td>
        </tr>
        <tr><td class="font-semibold pr-4 py-1">State</td><td>{{ transaction.status.name }}</td></tr>
        <tr>
          <td class="font-semibold pr-4 py-1">Change transaction's state</td>
          <td class="w-48">
            <TransactionStatusDropdown
              :currentStatusId="transaction.status.id"
              @change="onStatusChange"
            />
          </td>
        </tr>
      </tbody>
    </table>
    <button @click="$emit('close')" class="mt-4 w-full rounded bg-gray-200 py-2 px-4 text-gray-700 font-semibold hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2">Close</button>
  </div>
</template> 