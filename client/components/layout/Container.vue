<template>
  <div class="container mx-auto p-4 md:px-0">
    <div>
      <slot name="label" />
      <div
        class="prose"
        v-if="label && !$slots.label"
      >
        <h2>{{ label }}</h2>
      </div>
    </div>
    <slot />
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  label?: string
}>();
</script>