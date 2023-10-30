<template>
  <div class="flex">
    <InputNumberWithControls
      :min="1"
      :initialValue="cartItem.quantity"
      @valueChanged="onValueChanged"
    />
    <div class="ml-4">
      <PrimeButton
        @click="cartStore.removeCartItem(cartItem.id)"
        size="small"
        severity="danger"
        class="p-[4px]"
      >
        <Icon name="solar:trash-bin-minimalistic-linear" height="30px"/>
      </PrimeButton>
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