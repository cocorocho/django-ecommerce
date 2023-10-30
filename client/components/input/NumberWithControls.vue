<template>
  <BaseInput
    v-model="value"
    type="number"
    showButtons
    buttonLayout="horizontal"
    :pt="{
      input: {
        class: ['w-20'],
        size: 'small'
      }
    }"
  />
</template>

<script setup lang="ts">
const props = defineProps<{
  initialValue: number
}>();

const value = ref<number>(props.initialValue);

const emit = defineEmits([
  "valueChanged"
]);

const inputDebounceMs: number = 300; // Miliseconds
watch(
  useDebounce(value, inputDebounceMs),
  (newValue, oldValue) => emit("valueChanged", newValue, oldValue)
);
</script>