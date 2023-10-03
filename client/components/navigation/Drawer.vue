<template>
  <div class="drawer">
    <input
      :id="drawerId"
      type="checkbox"
      class="drawer-toggle"
    >
    <div class="drawer-content">
      <label
        :for="drawerId"
        class="drawer-button"
        :class="activatorClass"
      >
        <slot name="activator" />
        <Icon
          v-if="!$slots.activator"
          name="solar:hamburger-menu-linear"
        />
      </label>
    </div> 
    <div class="drawer-side">
      <label
        :for="drawerId"
        class="drawer-overlay"
      />
      <ul
        class="menu p-4 w-80 min-h-full bg-base-200 text-base-content"
        :class="sidebarClass"
      >
        <slot />
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
import { token } from "@formkit/utils";

const props = defineProps<{
  activatorClass?: string,
  sidebarClass?: string,
}>();

const drawerId: string = token();
</script>
