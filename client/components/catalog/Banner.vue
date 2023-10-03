<template>
  <div class="bg-black relative">
    <div class="container ml-auto">
      <NuxtImg
        :src="bannerUrl"
      />
    </div>
    <div class="absolute top-0 w-full h-full">
      <div class="container mx-auto flex flex-col h-full justify-center px-4 md:px-0">
        <div class="prose">
          <h1 class="text-neutral-content">
            {{ title }}
          </h1>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  bannerUrl: string,
  title: string
}>();
</script>