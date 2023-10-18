<template>
  <LayoutContainer>
    <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 p-8">
      <template v-if="pending">
        <SkeletonCard
          v-for="_ in 24"
        />
      </template>
      <template v-if="!pending && data?.results">
        <div
          v-for="product in data?.results"
          class="p-2"
        >
          <CatalogProductCard
            :product-data="product"
            class="hover:border-secondary animation-color duration-200"
          />
        </div>
      </template>
    </div>
    <div class="text-center">
      <NavigationPaginator
        :url="route.path"
        :current-page="currentPage"
        :num-pages="data.num_pages"
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
const currentPage = computed<number>(
  () => {
    const defaultPage: number = 1;
    const queryPage: number | typeof NaN = lodashToNumber(route.query.page);
    const page: number =
      (typeof queryPage === "number" && !isNaN(queryPage))
        ? queryPage
        : defaultPage;
    return page
  });
const productCategoryStore = useProductCategoryStore();

const { data, pending, refresh } = await productCategoryStore.retrieveSubCategoryProducts(
  route.params.categorySlug,
  route.params.subCategorySlug,
  currentPage
);
</script>