<template>
  <button
    type="button"
    @click="cartStore.addProductToCart(productId, quantity)"
  >
    <slot />
  </button>
</template>

<script setup lang="ts">
import { useCartStore } from '~/store/cart';

const props = defineProps<{
  productId: number,
  quantity?: number,
}>();

const cartStore = useCartStore();
</script>