<template>
  <LayoutContainer
    :label="data.header"
    v-if="data"
  >
    <div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4">
      <div
        v-for="product in data?.products"
        :key="product.id"
        class="p-2"
      >
        <CatalogProductCard
          :product-data="product"
          class="hover:border-secondary animation-color duration-200"
        />
      </div>
    </div>
  </LayoutContainer>
</template>

<script setup lang="ts">
definePageMeta({
  name: "catalogFeatured",
});

const route = useRoute();
const { slug } = route.params;

const { data } = await useApiFetch(
  `store/product/featured/${slug}/`,
);
</script>