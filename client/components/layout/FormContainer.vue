<template>
  <div class="max-w-sm m-auto rounded-xl border p-10">
    <div v-if="header">
      <div class="prose text-center">
        <h2>
          {{ header }}
        </h2>
      </div>
      <div class="divider"></div>
    </div>
    <slot />
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  header?: string,
}>();
</script>