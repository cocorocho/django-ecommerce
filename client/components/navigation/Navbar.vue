<template>
  <PrimeMenubar
    :model="menuItems"
    class="border-0"
    :pt="{
      menu: {
        class: ['container-centered', 'justify-end']
      }
    }"
  >
    <template #end>
      <div class="flex gap-x-4">
        <NavigationProfile />
        <CatalogCartLink />
      </div>
    </template>
    <template #item="{ item }">
      <template
        v-if="item.route"
      >
        <NuxtLink
          :to="item.route"
          v-badge="cartStore.hasItems ? cartStore.numItems : null"
        >
          <Icon v-if="item.icon" :name="item.icon" />
        </NuxtLink>
      </template>
    </template>
  </PrimeMenubar>
  <NavigationNavProductCategories
    class="hidden md:block"
  />
</template>

<script setup lang="ts">
import { useProductCategoryStore } from '~/store/products';
import { useCartStore } from "~/store/cart";

const cartStore = useCartStore();

const menuItems = ref([
  // {
  //   label: "cart",
  //   route: "/cart/",
  //   icon: "ph:shopping-cart"
  // },
  // {
  //   label: "user",
  // }
]);

const productCategoryStore = useProductCategoryStore();

// Fetch categories
await productCategoryStore.fetchCategories();

// Use categories from store
const categories = productCategoryStore.categories;
</script>

<style scoped>
.p-menubar {
  @apply py-6 px-12;
}
</style>