<template>
  <form>
    <slot />

    <template v-if="errors">
      <div class="mt-4">
        <small class="p-error block" v-for="error in errors">{{ error || '&nbsp;' }}</small>
      </div>
    </template>

    <div class="mt-4">
      <slot name="actions" />
    </div>
  </form>
</template>

<script setup lang="ts">
const props = defineProps<{
  errors?: string[]
}>();
</script>

<style scoped>
.p-error::first-letter {
  @apply uppercase;
}
</style>