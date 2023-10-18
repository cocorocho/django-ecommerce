<template>
  <div class="flex">
    <InputNumberWithControls
      min="1"
      :initialValue="cartItem.quantity.toString()"
      @valueChanged="onValueChanged"
    />
    <div class="ml-4">
      <button
        class="btn btn-ghost"
        @click="cartStore.removeCartItem(cartItem.id)"
      >
        <!-- TODO Remove product from cart -->
        <Icon name="solar:trash-bin-minimalistic-linear" />
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useCartStore } from '~/store/cart';

const props = defineProps<{
  cartItem: CartItem
}>();

const cartStore = useCartStore();
const onValueChanged = async (newValue: string) => {
  await cartStore.changeItemQuantity(props.cartItem.id, newValue);
};
</script>