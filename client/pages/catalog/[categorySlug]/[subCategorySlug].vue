<template>
  <LayoutContainer>
    <div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4">
      <template v-if="!pending && data?.results">
        <div
          v-for="product in data?.results"
          :key="product.id"
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
      <PrimePaginator
        v-if="data"
        :total-records="data.count"
        :rows="data.num_items"
        @page="goToPage"
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
const productCategoryStore = useProductCategoryStore();

const currentPage = ref<number>(1);

const { data, pending, refresh } = await productCategoryStore.retrieveSubCategoryProducts(
  route.params.categorySlug,
  route.params.subCategorySlug,
  currentPage
);

const goToPage = ({ page }) => {
  const _page: number = page + 1;
  if (currentPage.value !== _page) {
    currentPage.value = _page;
    refresh();
  }
}
</script>