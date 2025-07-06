import { defineStore } from 'pinia'
import axios, { AxiosResponse } from 'axios'
import type { LoginResponse, ApiError } from '../types'

interface AuthState {
  access_token: string;
  refresh_token: string;
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    access_token: localStorage.getItem('access_token') || '',
    refresh_token: localStorage.getItem('refresh_token') || ''
  }),
  actions: {
    setToken(token: string): void {
      this.access_token = token
      localStorage.setItem('access_token', token)
    },
    setRefreshToken(token: string): void {
      this.refresh_token = token
      localStorage.setItem('refresh_token', token)
    },
    async refreshAccessToken(): Promise<string> {
      try {
        const response: AxiosResponse<LoginResponse> = await axios.post(
          `${import.meta.env.VITE_API_URL || ''}/auth/refresh`, 
          {}, 
          {
            headers: {
              Authorization: `Bearer ${this.refresh_token}`
            }
          }
        )
        this.setToken(response.data.access_token)
        return response.data.access_token
      } catch (error) {
        // Refresh token is expired, logout user
        this.logout()
        throw error as ApiError
      }
    },
    logout(): void {
      this.access_token = ''
      this.refresh_token = ''
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
    }
  }
})