<template>
  <div>
    <template v-if="isAuthenticated">
      <PrimeButton
        type="button"
        class="p-0"
        @click="toggle"
        aria-haspopup="true"
        aria-controls="overlay_menu"
        text
        rounded
      >
        <Icon name="ph:user" />
      </PrimeButton>
      <PrimeMenu ref="menu" id="overlay_menu" :model="authenticatedMenuItems" :popup="true" />
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
const { isAuthenticated } = useAuth();
const { t } = useI18n();
const menu = ref();

const toggle = (event: MouseEvent) => {
    menu.value.toggle(event);
};

const authenticatedMenuItems = [
  {
    label: t("authentication.signOut"),
    command: async () => {
      await authStore.signOut();
    }
  }
];
</script>