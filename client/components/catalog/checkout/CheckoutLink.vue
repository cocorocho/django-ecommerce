<template>
  <PrimeButton
    type="button"
    @click="proceedCartCheckout"
    class="block w-80"
    :loading="requestBusy"
    icon="pi pi-search"
  >
    {{ $t("store.checkOut") }}
  </PrimeButton>
</template>

<script setup lang="ts">
import { useCartStore } from "~/store/cart";

const requestBusy = ref<boolean>(false);

const cartStore = useCartStore();

const proceedCartCheckout = async() => {
  requestBusy.value = true;
  try {
    await cartStore.checkoutCart();
  } catch (error) {
    console.log(error);
  } finally {
    requestBusy.value = false;
  }
}
</script>