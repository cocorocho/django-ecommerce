<template>
  <PrimeMenubar
    :model="menuItems"
    class="border-0 rounded-none hidden md:block !py-2 bg-black category-bar"
    :mobileActive="true"
    :pt="{
      menu: {
        class: [
          'container-centered',
          'md:flex',
        ],
      },
      menuitem: {
        class: ['px-2']
      }
    }"
    :button-props="{
      class: 'md:hidden'
    }"
    v-if="Array.isArray(categories) && categories.length"
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
const { data: categories } = await useAsyncData("categories", async () => productCategoryStore.categories);

const menuItems = categories.value?.map((category: ProductCategory) => ({
  label: category.name,
  route: { name: 'productCategory', params: { categorySlug: category.slug } },
}))
</script>

<style scoped>
.category-bar:deep(.p-menubar-root-list) {
  position: unset;
  background: inherit;
  display: flex;
}

.category-bar:deep(.p-menuitem) {
  width: initial;
}
</style>