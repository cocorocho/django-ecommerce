<template>
  <PrimeMenubar
    :model="menuItems"
    class="border-0 rounded-none hidden lg:block !py-2 bg-black"
    :pt="{
      menu: {
        class: ['container-centered']
      },
      menuitem: {
        class: ['px-2']
      },
    }"
  >
    <template #item="{ item }">
      <NuxtLink
        :to="item.route"
      >
        <PrimeButton
          :label="item.label"
          severity="info"
          size="small"
          text
        />
      </NuxtLink>
    </template>
  </PrimeMenubar>
</template>

<script setup lang="ts">
import { useProductCategoryStore } from '~/store/products';

const productCategoryStore = useProductCategoryStore();
const categories = productCategoryStore.categories;

const menuItems = categories.map((category: ProductCategory) => ({
  label: category.name,
  route: { name: 'productCategory', params: { categorySlug: category.slug } },
}))
</script>
