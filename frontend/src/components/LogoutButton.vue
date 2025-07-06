<template>
  <button @click="logout">Logout</button>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import api from '../utils/axios';
import axios from 'axios';
import type { ApiError } from '../types';

const router = useRouter();
const auth = useAuthStore();

async function logout(): Promise<void> {
  try {
    // Use direct axios call to bypass the interceptor that adds access token
    const API_URL: string = import.meta.env.VITE_API_URL || '';
    await axios.post(`${API_URL}/auth/logout`, {}, {
      headers: {
        Authorization: `Bearer ${auth.refresh_token}`
      }
    });
    auth.logout();
    router.push('/login');
  } catch (err: unknown) {
    const apiError = err as ApiError;
    console.error('Logout failed:', apiError);

    // Even if logout fails, clear local state and redirect
    auth.logout();
    router.push('/login');
  }
}
</script>

<style scoped>
button {
  background-color: #f44336;
  color: white;
  border: none;
  padding: 10px 20px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 4px 2px;
  cursor: pointer;
  border-radius: 4px;
}
</style> 