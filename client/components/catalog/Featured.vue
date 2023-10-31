<template>
  <PrimeCarousel
    v-if="products && products.length"
    container-class="md:px-8 relative"
    :value="products"
    :pt="{
      item: { class: 'flex justify-center' },
      nextButton: {
        class: 'absolute sm:relative z-[1] -right-2',
      },
      previousButton: {
        class: 'absolute sm:relative z-[1] -left-2',
      }
    }"
    :numVisible="3"
    :responsiveOptions="carouselSettings"
    :showIndicators="false"
    :autoplayInterval="10000"
    :circular="true"
  >
    <template #item="{ data }">
      <NuxtLink :to="{ name: 'catalogFeatured', params: { slug: data.slug }}" class="w-full">
        <div class="featured-card">
          <h2 class="featured-item-header">
            {{ data.header }}
          </h2>
          <NuxtImg :src="buildMediaUrl(data.image)" />
        </div>
      </NuxtLink>
    </template>
  </PrimeCarousel>
</template>

<script setup lang="ts">
import { useProductStore } from '~/store/products';

const productStore = useProductStore();

const { data: products } = await productStore.fetchFeatured();

const carouselSettings = ref([
  {
    breakpoint: "1024px",
    numVisible: 2,
    numScroll: 1
  },
  {
    breakpoint: "768px",
    numVisible: 1,
    numScroll: 1,
  },
  {
    breakpoint: "500px",
    numVisible: 1,
    numScroll: 1
  }
]);
</script>

<style scoped>
.featured-card {
  position: relative;
}

.featured-card {
  @apply
    px-2
    lg:px-4
    h-[200px]
    md:h-[300px];
}

.featured-card img {
  border-radius: 20px;
  width: 100%;
  height: 100%;
  object-fit: cover;
  filter: brightness(.6);
}

.featured-item-header {
  z-index: 1;
  @apply bottom-6 right-6 lg:bottom-6 lg:right-16 absolute text-white;
}

.featured-item-header * {
  @apply p-0 m-0;
}
</style>