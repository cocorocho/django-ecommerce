<template>
  <button
    type="button"
    class="btn btn-primary btn-outline w-80"
    @click="proceedCartCheckout"
  >
    <span class="loading loading-spinner" v-if="requestBusy"></span>
    {{ $t("store.checkOut") }}
  </button>
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