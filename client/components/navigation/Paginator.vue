<template>
  <div class="join py-4">
    <NuxtLink
      v-for="page in numPages"
      :to="{ query: { page: page }}"
      class="join-item btn btn-sm"
      :class="{
        'btn-active': Number(currentPage) === page,
      }"
      @click="onPageChanged(page)"
    >
      {{ page }}
    </NuxtLink>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  currentPage: string | number,
  numPages: number,
  url: string,
  onPageChange?: Function
}>();

const maxShownButtons: number = 5;

const onPageChanged = (page: number) => {
  if (props.onPageChange && page !== Number(props.currentPage)) {
    props.onPageChange();
  }
}

// TODO pagination for lots of pages
</script>