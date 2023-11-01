<template>
  <PrimeMenubar
    :model="menuItems"
    class="border-0"
    :pt="{
      menu: {
        class: 'md:hidden'
      },
      menuitem: {
        class: 'no-underline'
      },
      button: {
        class: 'md:hidden justify-start'
      },
      end: {
        class: 'basis-2/3'
      },
      start: {
        class: 'hidden md:block'
      }
    }"
  >
    <template #end>
      <div class="flex">
        <div class="flex basis-1/2 justify-center items-center">
          <NuxtLink
            to="/"
            class="transition-transform duration-200 hover:scale-105"
            v-if="storeMetaData && storeMetaData.logo"
          >
            <NuxtImg :src="buildMediaUrl(storeMetaData.logo)"
              sizes="80px md:120px"
            />
          </NuxtLink>
        </div>
        <div class="flex basis-1/2 justify-end gap-x-2 md:gap-x-4 items-center">
          <NavigationProfile />
          <CatalogCartLink />
        </div>
      </div>
    </template>
    <template #item="{ item }">
      <template
        v-if="item.route"
      >
        <PrimeButton
          size="small"
          class="w-full"
          text
        >
          <NuxtLink
            :to="item.route"
            class="no-underline"
          >
            <Icon v-if="item.icon" :name="item.icon" />
            {{ item.label }}
          </NuxtLink>
        </PrimeButton>
      </template>
    </template>
  </PrimeMenubar>
  <NavigationNavProductCategories />
</template>

<script setup lang="ts">
import { useStoreMeta } from "~/store/store";
import { useProductCategoryStore } from '~/store/products';
import { useCartStore } from "~/store/cart";

const { t } = useI18n();
const cartStore = useCartStore();
const storeMeta = useStoreMeta();
const productCategoryStore = useProductCategoryStore();

// Fetch categories
const { data: productCategories } = await productCategoryStore.fetchCategories();
const { data: storeMetaData } = await useAsyncData("storeMetaData", async () => storeMeta.store);

const menuItems = ref([
  {
    label: t("home"),
    route: "/"
  },
  ...productCategories.value?.map((category: ProductCategory) => ({
    label: category.name,
    route: { name: "productCategory", params: { categorySlug: category.slug }},
  })) ?? [],
]);
</script>

<style scoped>
.p-menubar {
  @apply py-6 px-4 md:px-12;
}
</style>