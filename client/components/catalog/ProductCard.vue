<template>
  <div class="card border p-4 border-2 h-[500px]">
    <figure class="min-h-[250px]">
      <div class="relative">
        <Carousel>
          <Slide v-for="image in productData.images" :key="image.image">
            <NuxtImg :src="image.image" height="250px" fit="contain" width="100%"/>
          </Slide>
          <template #addons>
            <Navigation />
          </template>
        </Carousel>
      </div>
    </figure>
    <div class="card-body p-4">
      <div class="prose text-center">
        <h2 class="mb-0">{{ productData.product.manufacturer }}</h2>
        <h3 class="mb-0">{{ productData.product.name }}</h3>
        <h3 class="text-red-600 font-semibold">${{ productData.price }}</h3>
      </div>
    </div>
    <div class="card-actions justify-between">
      <button class="btn btn-primary btn-sm font-semibold">
        <Icon name="ph:info" size="20px"/>
        {{ $t("store.seeSpecs") }}
      </button>
      <button class="btn btn-secondary btn-sm font-semibold">
        <!-- TODO Add to cart -->
        <Icon name="ph:shopping-cart" size="20px" />
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  productData: SubCategoryProduct
}>();
</script>