<template>
  <PrimeCard
    class="shadow-none border-solid border-2 hover:border-cyan-500 duration-200"
    :pt="{
      header: {
        class: ['text-center', 'pt-2']
      },
    }"
  >
    <template #header>
      <NuxtImg
        :src="productData.thumbnail"
        sizes="150px md:200px lg:500px"
      />
    </template>
    <template #title>
      <div class="prose text-center">
        <h3 class="mb-0">{{ productData.manufacturer }}</h3>
      </div>
    </template>
    <template #content>
      <div class="prose text-center">
        <h4 class="mb-0">{{ productData.name }}</h4>
        <h4 class="text-red-600 font-semibold">${{ productData.price }}</h4>
      </div>
    </template>
    <template #footer>
      <div class="flex justify-between gap-2 flex-col">
        <NuxtLink
          :to="{ name: 'storeProductDetails', params: { id: productData.id } }"
          class="w-full no-underline"
        >
          <PrimeButton
            size="small"
            class="w-full block"
            severity="secondary"
          >
            <Icon name="ph:info" size="20px"/>
            {{ $t("store.viewDetails") }}
          </PrimeButton>
        </NuxtLink>
        <CatalogCartAddProduct
          size="small"
          :product-id="productData.id"
          :disabled="!productData.in_stock"
          class="w-full"
        >
          {{ $t("store.addToCart") }}
        </CatalogCartAddProduct>
      </div>
    </template>
    
  </PrimeCard>
</template>

<script setup lang="ts">
const props = defineProps<{
  productData: Product
}>();
</script>