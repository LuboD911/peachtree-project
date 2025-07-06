<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import api from '../utils/axios'
import type { 
  Contractor, 
  SystemAccount, 
  CreateTransactionRequest, 
  ApiError,
  InputEvent 
} from '../types'

const contractor_id = ref<string>('')
const type = ref<string>('')
const amount = ref<string>('')
const account_id = ref<string>('')
const contractors = ref<Contractor[]>([])
const accounts = ref<SystemAccount[]>([])
const error = ref<string>('')

const emit = defineEmits<{
  (e: 'transactionCreated'): void
}>()

const fetchOptions = async (): Promise<void> => {
  try {
    const contractorsResponse = await api.get<Contractor[]>('/transactions/contractors')
    contractors.value = contractorsResponse.data
    
    const accountsResponse = await api.get<SystemAccount[]>('/transactions/accounts')
    
    if (accountsResponse.data) {
      accounts.value = accountsResponse.data
    } else {
      accounts.value = []
    }
  } catch (err: unknown) {
    const apiError = err as ApiError
    console.error('Error fetching options:', apiError)
    
    // Set empty arrays to prevent undefined errors
    if (!contractors.value) contractors.value = []
    if (!accounts.value) accounts.value = []
  }
}

const refreshAccounts = async (): Promise<void> => {
  try {
    const accountsResponse = await api.get<SystemAccount[]>('/transactions/accounts')
    if (accountsResponse.data) {
      accounts.value = accountsResponse.data
    }
  } catch (err: unknown) {
    const apiError = err as ApiError
    console.error('Error refreshing accounts:', apiError)
  }
}

onMounted(fetchOptions)

const selectedAccountBalance = computed((): number => {
  if (!account_id.value) return 0
  const account = accounts.value.find(a => a.id === parseInt(account_id.value))
  return account ? account.balance : 0
})

const isInsufficientBalance = computed((): boolean => {
  const numericAmount = parseFloat(amount.value) || 0
  return numericAmount > selectedAccountBalance.value
})

const balanceWarning = computed((): string => {
  if (!account_id.value || !amount.value) return ''
  const numericAmount = parseFloat(amount.value) || 0
  if (numericAmount > selectedAccountBalance.value) {
    return `Insufficient funds. Available: $${selectedAccountBalance.value.toFixed(2)}`
  }
  return ''
})

const formatAmount = (value: string): string => {
  // Remove all non-numeric characters except decimal point
  let numericValue = value.replace(/[^0-9.]/g, '')
  
  const parts = numericValue.split('.')
  if (parts.length > 2) {
    numericValue = parts[0] + '.' + parts.slice(1).join('')
  }
  
  // Limit to 2 decimal places
  if (parts.length === 2 && parts[1].length > 2) {
    numericValue = parts[0] + '.' + parts[1].substring(0, 2)
  }
  
  return numericValue
}

const submit = async (): Promise<void> => {
  try {
    error.value = ''
    
    const numericAmount = parseFloat(amount.value)
    if (isNaN(numericAmount) || numericAmount <= 0) {
      error.value = 'Please enter a valid amount'
      return
    }
    
    if (isInsufficientBalance.value) {
      error.value = `Insufficient funds. Available: $${selectedAccountBalance.value.toFixed(2)}`
      return
    }
    
    const transactionData: CreateTransactionRequest = {
      contractor_id: contractor_id.value,
      type: type.value,
      amount: numericAmount,
      account_id: account_id.value
    }
    
    await api.post('/transactions', transactionData)
    
    // Refresh account balances after successful transaction
    await refreshAccounts()
    
    // Clear the form
    contractor_id.value = type.value = ''
    amount.value = ''
    account_id.value = ''
    
    // Emit event to refresh transactions list
    emit('transactionCreated')
  } catch (err: unknown) {
    const apiError = err as ApiError
    console.error('Failed to create transaction:', apiError)
    error.value = apiError.response?.data?.message || 'Failed to create transaction'
  }
}
</script>

<template>
  <form @submit.prevent="submit" class="space-y-4">
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">From Account</label>
      <select v-model="account_id" required class="block w-full rounded border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
        <option value="" disabled>Select Account</option>
        <option v-for="account in accounts" :key="account.id" :value="account.id">
          {{ account.name }} - ${{ account.balance.toFixed(2) }}
        </option>
      </select>
    </div>
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">Contractor</label>
      <select v-model="contractor_id" required class="block w-full rounded border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
        <option value="" disabled>Select Contractor</option>
        <option v-for="c in contractors" :key="c.id" :value="c.id">{{ c.name }}</option>
      </select>
    </div>
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">Type</label>
      <select v-model="type" required class="block w-full rounded border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
        <option value="" disabled>Select Type</option>
        <option value="card_payment">Card Payment</option>
        <option value="online_transfer">Online Transfer</option>
        <option value="transaction">Transaction</option>
      </select>
    </div>
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">Amount</label>
      <div class="relative">
        <span class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500">$</span>
        <input 
          v-model="amount" 
          @input="amount = formatAmount(($event.target as HTMLInputElement).value)"
          type="text" 
          placeholder="0.00" 
          required 
          :class="[
            'block w-full rounded border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 pl-8',
            isInsufficientBalance ? 'border-red-500 focus:border-red-500 focus:ring-red-500' : ''
          ]"
        />
      </div>
      <div v-if="balanceWarning" class="text-red-600 text-sm mt-1">{{ balanceWarning }}</div>
    </div>
    <div v-if="error" class="text-red-600 text-sm">{{ error }}</div>
    <button 
      type="submit" 
      :disabled="isInsufficientBalance"
      :class="[
        'w-full rounded py-2 px-4 font-semibold focus:outline-none focus:ring-2 focus:ring-offset-2',
        isInsufficientBalance 
          ? 'bg-gray-400 text-gray-600 cursor-not-allowed' 
          : 'bg-indigo-600 text-white hover:bg-indigo-700 focus:ring-indigo-500'
      ]"
    >
      Submit
    </button>
  </form>
</template> 