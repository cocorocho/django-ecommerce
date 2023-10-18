<template>
  <div class="join items-center">
    <button
      class="btn btn-sm join-item w-11"
      :class="{'btn-disabled': cartStore.busy || value === min}"
      @click="decrement"
    >
      <span
        v-if="cartStore.busy"
        class="loading loading-spinner loading-sm"
      ></span>
      <Icon
        v-else
        name="ic:sharp-minus"
        color="black"
      />
    </button>
    <input
      type="number"
      class="w-14 join-item input-sm text-center border-t border-b"
      @keypress.stop="validateChars($event, ['-'])"
      v-model="value"
      v-bind="$attrs"
    />
    <button
      class="btn btn-sm join-item w-11"
      :class="{'btn-disabled': cartStore.busy || value === max}"
      @click="increment"
    >
      <span
        v-if="cartStore.busy"
        class="loading loading-spinner loading-sm"
      ></span>
      <Icon
        v-else
        name="ic:sharp-plus" color="black"
      />
    </button>
  </div>
</template>

<script setup lang="ts">
import { useCartStore } from '~/store/cart';

const attrs = useAttrs();
const props = defineProps<{
  initialValue: string
  min?: string
  max?: string
}>();
const emit = defineEmits([
  "incremented", "decremented", "valueChanged"
]);
const cartStore = useCartStore();

const value = ref<string>(props.initialValue);

const decrement = () => {
  const newValue: number = parseInt(value.value) - 1;

  if (props.min) {
    const min: number = parseInt(props.min);
    if (newValue < min) return;
  }
  value.value = newValue.toString();
  emit("decremented", newValue);
};

const increment = () => {
  const newValue: number = parseInt(value.value) + 1;

  if (props.max) {
    const max: number = parseInt(props.max);
    if (newValue > max) return;
  }
  value.value = newValue.toString();
  emit("incremented", newValue);
};

const inputDebounceMs: number = 300; // Miliseconds
watch(
  useDebounce(value, inputDebounceMs),
  (newValue, oldValue) => emit("valueChanged", newValue, oldValue)
);
</script>

<style scoped>
/* Chrome, Safari, Edge, Opera */
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

/* Firefox */
input[type=number] {
  -moz-appearance: textfield;
}
</style>
