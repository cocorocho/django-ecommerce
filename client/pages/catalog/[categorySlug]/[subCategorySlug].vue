<template>
  <LayoutContainer>
    <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 p-8">
      <template v-if="pending">
        <SkeletonCard
          v-for="_ in 24"
        />
      </template>
      <div
        v-if="!pending && data?.results"
        v-for="product in data?.results"
        class="p-2"
      >
        <CatalogProductCard
          :product-data="product"
          class="hover:border-secondary animation-color duration-200"
        />
      </div>
    </div>
    <div class="text-center">
      <NavigationPaginator
        :url="route.path"
        :current-page="route.query?.page || 1"
        :numPages="data.num_pages"
        :on-page-change="refresh"
      />
    </div>
  </LayoutContainer>
</template>

<script setup lang="ts">
import { useProductCategoryStore } from '~/store/products';

definePageMeta({
  name: "productSubCategory"
});

const route = useRoute();
const currentPage = computed(() => route.query?.page || 1);
const productCategoryStore = useProductCategoryStore();

const { data, pending, refresh } = await productCategoryStore.retrieveSubCategoryProducts(
  route.params.categorySlug,
  route.params.subCategorySlug,
  currentPage
);
</script>