<script setup lang="ts">
import { ref } from 'vue'
import axios, { AxiosResponse } from 'axios'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'
import type { LoginRequest, LoginResponse, ApiError } from '../types'

const username = ref<string>('')
const password = ref<string>('')
const error = ref<string>('')
const auth = useAuthStore()
const router = useRouter()
const API_URL: string = import.meta.env.VITE_API_URL || ''

const login = async (): Promise<void> => {
  try {
    const loginData: LoginRequest = {
      username: username.value,
      password: password.value
    }
    
    const res: AxiosResponse<LoginResponse> = await axios.post(`${API_URL}/auth/login`, loginData)
    auth.setToken(res.data.access_token)
    auth.setRefreshToken(res.data.refresh_token)
    router.push('/')
  } catch (e: unknown) {
    const apiError = e as ApiError
    error.value = 'Invalid credentials'
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center p-4">
    <div class="w-full max-w-md bg-white/80 border border-blue-200 shadow-2xl rounded-3xl p-10 backdrop-blur-lg">
      <h2 class="text-center text-3xl font-bold text-blue-700 mb-8 drop-shadow-md">Welcome Back</h2>
      
      <form @submit.prevent="login" class="space-y-6">
        <div class="space-y-4">
          <div>
            <label for="username" class="sr-only">Username</label>
            <input
              id="username"
              v-model="username"
              name="username"
              type="text"
              autocomplete="username"
              required
              class="w-full rounded-xl border border-blue-300 bg-white px-4 py-3 text-gray-900 placeholder-gray-400 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 focus:outline-none text-base transition"
              placeholder="Enter your username"
            />
          </div>

          <div>
            <label for="password" class="sr-only">Password</label>
            <input
              id="password"
              v-model="password"
              name="password"
              type="password"
              autocomplete="current-password"
              required
              class="w-full rounded-xl border border-blue-300 bg-white px-4 py-3 text-gray-900 placeholder-gray-400 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 focus:outline-none text-base transition"
              placeholder="Enter your password"
            />
          </div>
        </div>

        <div v-if="error" class="text-center text-red-500 text-sm">{{ error }}</div>

        <div class="flex justify-center">
          <button
            type="submit"
            class="w-full rounded-full bg-blue-400 hover:bg-blue-500 text-white font-semibold py-3 px-6 shadow-md transition duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-300 focus:ring-offset-2"
          >
            Sign In
          </button>
        </div>

        <div class="text-center text-sm text-gray-600">
          Don't have an account?
          <router-link to="/register" class="text-blue-600 hover:underline font-medium ml-1">
            Register
          </router-link>
        </div>
      </form>
    </div>
  </div>
</template>
