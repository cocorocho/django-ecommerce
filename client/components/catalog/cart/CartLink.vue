<template>
  <NuxtLink
      to="/cart/"
      class="link-neutral"
    >
    <ClientOnly>
      <div class="indicator">
        <span
          v-if="cartStore.hasItems"
          class="indicator-item badge badge-secondary badge-sm w-4 h-4"
        >
          {{ cartStore.numItems }}
        </span>
        <Icon name="ph:shopping-cart" />
      </div>
    </ClientOnly>
  </NuxtLink>
</template>

<script setup lang="ts">
import { useCartStore } from "~/store/cart";

const cartStore = useCartStore();
</script>