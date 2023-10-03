<template>
  <div class="container mx-auto">
    <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 p-8">
      <div
        v-for="product in data.results"
        v-if="!pending && data?.results.length"
        class="p-2"
      >
        <CatalogProductCard
          :product-data="product"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useProductCategoryStore } from '~/store/products';

definePageMeta({
  name: "productSubCategory"
});

const route = useRoute();

const productCategoryStore = useProductCategoryStore();
const { data, pending } = await productCategoryStore.retrieveSubCategoryProducts(
  route.params.categorySlug,
  route.params.subCategorySlug,
  1
);
</script>