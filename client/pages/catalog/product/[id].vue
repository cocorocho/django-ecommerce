<template>
  <LayoutContainer>
    <div
      v-if="data"
      class="grid md:grid-cols-3 gap-x-2"
    >
      <div class="md:col-span-2">
        <PrimeCarousel
          :value="data.images"
          container-class="max-w-[90vw]"
          :circular="true"
          :pt="{
            item: { class: 'text-center' }
          }"
        >
          <template #item="slotProps">
            <NuxtImg
              :src="slotProps.data.image"
              class="w-full max-w-[600px]"
            />
          </template>
        </PrimeCarousel>
      </div>
      <div class="flex flex-col justify-around">
        <div>
          <div class="font-semibold">
            <h1 class="text-4xl">
              {{ data.manufacturer }}
            </h1>
            <h2 class="text-2xl">
              {{ data.name }}
            </h2>
          </div>
          <h1 class="text-4xl font-bold pt-6">
            <span class="text-2xl">$</span>{{ data.price }}
          </h1>
          <p
            class="font-semibold"
            :class="[data.in_stock ? 'text-green-500' : 'text-red-500']"
          >
            {{ data.in_stock ? $t('store.inStock') : $t('store.outOfStock') }}
          </p>
        </div>
        <div class="pt-2 space-y-4">
          <CatalogCartAddProduct
            :disabled="!data.in_stock"
            :product-id="data.id"
            class="w-full"
          >
            {{ $t("store.addToCart") }}
          </CatalogCartAddProduct>
          <PrimeButton
            severity="success"
            class="w-full block"
            :disabled="!data.in_stock"
          >
            {{ $t("store.buyNow") }}
          </PrimeButton>
        </div>
        <div class="pt-2">
          <p class="text-lg">
            {{ data.description }}
          </p>
        </div>
      </div>
    </div>
  </LayoutContainer>
</template>

<script setup lang="ts">
import { useProductStore } from '~/store/products';

definePageMeta({
  name: "storeProductDetails"
});

const route = useRoute();
const productStore = useProductStore();

const productId: string | string[] = route.params?.id;
const { data } = await productStore.retrieveProductDetails(productId);

useSeoMeta({
  description: data.value?.description_short,
  ogDescription: data.value?.description_short
});
</script>


<style scoped>
#gallery:deep(.carousel__slide) {
  @apply border border-2;
}

#gallery:deep(.carousel__track) {
  @apply gap-x-2;
}
</style>