<script setup lang="ts">
import { ref } from 'vue'
import axios, { AxiosResponse } from 'axios'
import { useRouter } from 'vue-router'
import type { RegisterRequest, ApiError } from '../types'

const username = ref<string>('')
const password = ref<string>('')
const confirmPassword = ref<string>('')
const error = ref<string>('')
const router = useRouter()
const API_URL: string = import.meta.env.VITE_API_URL || ''

const register = async (): Promise<void> => {
  if (password.value !== confirmPassword.value) {
    error.value = 'Passwords do not match'
    return
  }
  try {
    const registerData: RegisterRequest = { 
      username: username.value, 
      password: password.value 
    }
    await axios.post(`${API_URL}/auth/register`, registerData)
    router.push('/login')
  } catch (e: unknown) {
    const apiError = e as ApiError
    error.value = apiError.response?.data?.message || 'Registration failed'
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center">
    <div class="w-full max-w-md p-8 bg-white/90 rounded-2xl shadow-2xl border border-pink-100 flex flex-col items-center">
      <div class="w-full mb-6">
        <h2 class="text-center text-3xl font-extrabold text-pink-600 drop-shadow">Create your account</h2>
      </div>
      <form class="w-full space-y-6" @submit.prevent="register">
        <div class="space-y-4">
          <div class="flex flex-col items-center">
            <label for="username" class="sr-only">Username</label>
            <input id="username" v-model="username" name="username" type="text" autocomplete="username" required class="w-3/4 rounded-lg border border-gray-300 px-4 py-2 text-gray-900 placeholder-gray-400 focus:border-pink-400 focus:ring-2 focus:ring-pink-200 focus:outline-none text-base transition" placeholder="Username" />
          </div>
          <div class="flex flex-col items-center">
            <label for="password" class="sr-only">Password</label>
            <input id="password" v-model="password" name="password" type="password" autocomplete="new-password" required class="w-3/4 rounded-lg border border-gray-300 px-4 py-2 text-gray-900 placeholder-gray-400 focus:border-pink-400 focus:ring-2 focus:ring-pink-200 focus:outline-none text-base transition" placeholder="Password" />
          </div>
          <div class="flex flex-col items-center">
            <label for="confirmPassword" class="sr-only">Confirm Password</label>
            <input id="confirmPassword" v-model="confirmPassword" name="confirmPassword" type="password" autocomplete="new-password" required class="w-3/4 rounded-lg border border-gray-300 px-4 py-2 text-gray-900 placeholder-gray-400 focus:border-pink-400 focus:ring-2 focus:ring-pink-200 focus:outline-none text-base transition" placeholder="Confirm Password" />
          </div>
        </div>
        <div v-if="error" class="text-red-600 text-sm text-center">{{ error }}</div>
        <div class="flex justify-center">
          <button type="submit" class="w-2/3 rounded-full bg-gradient-to-r from-pink-500 via-purple-500 to-indigo-500 py-2 px-6 text-lg font-bold text-white shadow-lg hover:scale-105 hover:from-pink-600 hover:to-indigo-600 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-pink-400 focus:ring-offset-2">
            Register
          </button>
        </div>
        <div class="text-center text-sm text-gray-500">
          Already have an account?
          <router-link to="/login" class="text-pink-600 hover:text-pink-500 font-semibold">Sign in</router-link>
        </div>
      </form>
    </div>
  </div>
</template> 