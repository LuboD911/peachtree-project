import axios, { AxiosInstance, InternalAxiosRequestConfig, AxiosResponse } from 'axios'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'
import type { ApiError } from '../types'

const API_URL: string = import.meta.env.VITE_API_URL || ''

// Create axios instance
const api: AxiosInstance = axios.create({
  baseURL: API_URL,
  timeout: 10000
})

// Request interceptor to add auth token
api.interceptors.request.use(
  (config: InternalAxiosRequestConfig): InternalAxiosRequestConfig => {
    const authStore = useAuthStore()
    if (authStore.access_token) {
      config.headers.Authorization = `Bearer ${authStore.access_token}`
    }
    return config
  },
  (error: unknown): Promise<never> => {
    return Promise.reject(error)
  }
)

// Response interceptor to handle token refresh
api.interceptors.response.use(
  (response: AxiosResponse): AxiosResponse => {
    return response
  },
  async (error: any): Promise<AxiosResponse> => {
    const originalRequest = error.config as InternalAxiosRequestConfig & { _retry?: boolean }
    const authStore = useAuthStore()
    const router = useRouter()

    // If error is 401 and we haven't already tried to refresh
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        // Try to refresh the token
        const newToken: string = await authStore.refreshAccessToken()
        
        // Update the original request with new token
        originalRequest.headers.Authorization = `Bearer ${newToken}`
        
        // Retry the original request
        return api(originalRequest)
      } catch (refreshError: unknown) {
        // Refresh failed, redirect to login
        router.push('/login')
        return Promise.reject(refreshError)
      }
    }

    return Promise.reject(error)
  }
)

export default api 