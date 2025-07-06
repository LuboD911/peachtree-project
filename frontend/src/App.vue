<script setup lang="ts">
import LogoutButton from './components/LogoutButton.vue';
import { useAuthStore } from './stores/auth';
 
const auth = useAuthStore();
</script>

<template>
  <div class="app-container">
    <header>
      <LogoutButton v-if="auth.access_token" />
    </header>
    <router-view />
  </div>
</template>

<style scoped>
.app-container {
  min-height: 100vh;
  background-image: url('./assets/background-img.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  background-attachment: fixed;
}

header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }
}
</style>
