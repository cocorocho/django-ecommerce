<template>
  <NuxtLink
    to="/cart/"
    class="cart-link"
    v-badge="cartStore.hasItems ? cartStore.numItems : null"
  >
    <Icon name="ph:shopping-cart" />
  </NuxtLink>
</template>

<script setup lang="ts">
import { useCartStore } from "~/store/cart";

const cartStore = useCartStore();
</script>