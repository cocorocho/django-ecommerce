<template>
  <Transition>
    <div
      v-if="toastStore.getToasts.length"
      class="toast toast-center toast-bottom z-50"
    >
      <div
        v-for="toast in toastStore.getToasts"
        class="alert"
        :class="toast.status ? STATUS_MAP[toast.status] : ''"
      >
        <span>{{ $t(toast.message) }}</span>
      </div>
    </div>
  </Transition>
</template>

<script setup lang="ts">
import { useToastStore } from '~/store/toast';

const toastStore = useToastStore();
const STATUS_MAP : {[key: string]: string} = {
  "success": "alert-success",
  "error": "alert-error",
  "info": "alert-info"
};
</script>

<style scoped>
.v-enter-active,
.v-leave-active {
  transition: opacity 0.2s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}
</style>