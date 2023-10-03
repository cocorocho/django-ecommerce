<template>
  <div class="w-full bg-white py-1">
    <div class="container mx-auto">
      <div
        v-for="category in categories"
        :key="category.slug"
        class="dropdown dropdown-hover static"
      >
        <NuxtLink
          :to="{ name: 'productCategory', params: { categorySlug: category.slug } }"
          class="btn btn-ghost btn-sm"
        >
          {{ category.name }}
        </NuxtLink>
        <ul
          tabindex="0"
          class="dropdown-content z-[1] p-2 w-full absolute left-0 !transition-none bg-white shadow-md"
        >
          <div class="container mx-auto">
            <div class="divider my-0" />
            <div class="grid grid-cols-3 lg:grid-cols-4 gap-y-8 p-4">
              <li
                v-for="subCategory in category.sub_categories"
                :key="subCategory.slug"
              >
                <NuxtLink
                  :to="{ name: 'productSubCategory', params: { categorySlug: category.slug, subCategorySlug: subCategory.slug } }"
                  class="text-center"
                >
                  <NuxtImg
                    :src="subCategory.thumbnail"
                    height="100px"
                    class="mx-auto"
                  />
                  <div>
                    {{ subCategory.name }}
                  </div>
                </NuxtLink>
              </li>
            </div>
          </div>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useProductCategoryStore } from '~/store/products';

const productCategoryStore = useProductCategoryStore();
const categories = productCategoryStore.categories;
</script>

<style scoped>
.grid:deep(a) {
  @apply link-neutral link-hover font-semibold;
}
</style>