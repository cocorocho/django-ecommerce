<template>
  <div class="card border p-4 border-2 h-[500px]">
    <figure>
      <div class="relative">
        <NuxtImg :src="productData.thumbnail" height="250px" fit="contain" width="100%"/>
      </div>
    </figure>
    <div class="card-body p-4">
      <div class="prose text-center">
        <h2 class="mb-0">{{ productData.manufacturer }}</h2>
        <h3 class="mb-0">{{ productData.name }}</h3>
        <h3 class="text-red-600 font-semibold">${{ productData.price }}</h3>
      </div>
    </div>
    <div class="card-actions justify-between">
      <NuxtLink
        :to="{ name: 'storeProductDetails', params: { id: productData.id } }"
        class="btn btn-primary btn-sm font-semibold"
      >
        <Icon name="ph:info" size="20px"/>
        {{ $t("store.viewDetails") }}
      </NuxtLink>
      <CatalogCartAddProduct
        class="btn btn-sm btn-secondary btn-outline"
        :class="{'btn-disabled': !productData.in_stock}"
        :product-id="productData.id"
      >
        {{ $t("store.addToCart") }}
      </CatalogCartAddProduct>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  productData: Product
}>();
</script>