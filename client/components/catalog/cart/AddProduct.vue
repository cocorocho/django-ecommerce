<template>
  <PrimeButton
    severity="primary"
    @click="cartStore.addProductToCart(productId, quantity)"
    class="block"
  >
    <slot />
  </PrimeButton>
</template>

<script setup lang="ts">
import { useCartStore } from '~/store/cart';
import { useToast } from 'primevue/usetoast';

const toast = useToast();
const props = defineProps<{
  productId: number,
  quantity?: number,
}>();

const cartStore = useCartStore();
</script>