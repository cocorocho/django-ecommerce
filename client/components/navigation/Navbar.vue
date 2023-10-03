<template>
  <div
    ref="nav"
    class="shadow-md"
  >
    <div class="navbar bg-base-200 flex-col">
      <div class="container mx-auto">
        <div class="navbar-start">
          <NavigationDrawer
            class="md:hidden"
            activator-class="btn btn-ghost rounded-full"
          >
            <ul class="menu">
              <li>
                <ClientOnly>
                  <h2 class="menu-title">
                    {{ $t("store.category", 2) }}
                  </h2>
                </ClientOnly>
                <ul>
                  <li
                    v-for="category in categories"
                    :key="category.slug"
                  >
                    <NuxtLink
                      :to="{ name: 'productCategory', params: { categorySlug: category.slug } }"
                      class="link link-neutral link-hover link-underline font-semibold"
                    >
                      {{ category.name }}
                    </NuxtLink>
                  </li>
                </ul>
              </li>
            </ul>
          </NavigationDrawer>
        </div>
        <div class="navbar-center">
          <NuxtLink to="/">
            <img
              src="https://placehold.co/200x40"
            >
          </NuxtLink>
        </div>
        <div class="navbar-end">
          <div class="flex justify-end">
            <NuxtLink
              to="/cart/"
              class="link-neutral"
            >
              <Icon name="ph:shopping-cart" />
            </NuxtLink>
          </div>
        </div>
      </div>
    </div>
    <NavigationNavProductCategories
      class="hidden md:block"
    />
  </div>
</template>

<script setup lang="ts">
import { useProductCategoryStore } from '~/store/products';

const productCategoryStore = useProductCategoryStore();

// Fetch categories
await productCategoryStore.fetchCategories();

// Use categories from store
const categories = productCategoryStore.categories;

const nav = ref();
const navIsVisible = ref<boolean>(true);

const { stop } = useIntersectionObserver(
  nav,
  ([{ isIntersecting }], observerElement) => {
    navIsVisible.value = isIntersecting;
  }
);
</script>