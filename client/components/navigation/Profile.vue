<template>
  <div>
    <template v-if="authStore.isAuthenticated">
      <Icon name="ph:user" />
      <!-- TODO -->
    </template>
    <template v-else>
      <NuxtLink
        :to="{name: 'signin'}"
      >
        <Icon name="ph:user" />
      </NuxtLink>
    </template>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '~/store/auth';

const authStore = useAuthStore();
</script>