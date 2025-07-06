<script setup lang="ts">
import TransactionForm from '../components/TransactionForm.vue'
import TransactionList from '../components/TransactionList.vue'
import TransactionDetail from '../components/TransactionDetail.vue'
import { ref } from 'vue'

const selectedTransactionId = ref<number | null>(null)
const transactionListRef = ref<InstanceType<typeof TransactionList> | null>(null)

const onSelectTransaction = (id: number): void => {
  selectedTransactionId.value = id
}

const onTransactionCreated = (): void => {
  // Refresh the transactions list
  if (transactionListRef.value) {
    transactionListRef.value.fetchTransactions()
  }
}

const onCloseTransactionDetail = (): void => {
  selectedTransactionId.value = null
}
</script>

<template>
  <div class="min-h-screen py-8 px-4">
    <div class="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-4 gap-8">
      <div class="lg:col-span-1 bg-white rounded shadow p-6 h-fit">
        <h2 class="text-xl font-semibold text-gray-800 mb-4 border-b border-gray-200 pb-2">Make a Transfer</h2>
        <TransactionForm @transactionCreated="onTransactionCreated" />
      </div>
      <div class="lg:col-span-3 bg-white rounded shadow p-6">
        <!-- Show transaction list when no transaction is selected -->
        <div v-if="!selectedTransactionId">
          <h2 class="text-xl font-semibold text-gray-800 mb-4 border-b border-gray-200 pb-2">Transactions</h2>
          <TransactionList 
            ref="transactionListRef" 
            @select="onSelectTransaction" 
          />
        </div>
        <!-- Show transaction detail when a transaction is selected -->
        <div v-else>
          <h2 class="text-xl font-semibold text-gray-800 mb-4 border-b border-gray-200 pb-2">Details for Transaction #{{ selectedTransactionId }}</h2>
          <TransactionDetail 
            :transactionId="selectedTransactionId" 
            @close="onCloseTransactionDetail" 
          />
        </div>
      </div>
    </div>
  </div>
</template> 