<template>
  <div>
    <CatalogBanner
      :banner-url="category.banner"
      :title="category.name"
    />
    <div class="container mx-auto pt-4">
      <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-y-8">
        <div
          v-for="subCategory in category.sub_categories"
          :key="subCategory.slug"
        >
          <NuxtLink
            :to="{ name: 'productSubCategory', params: { subCategorySlug: subCategory.slug } }"
            class="text-center link-hover"
          >
            <NuxtImg
              :src="subCategory.thumbnail"
              height="400px"
              class="mx-auto"
            />
            <div class="prose">
              <h2>
                {{ subCategory.name }}
              </h2>
            </div>
          </NuxtLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useProductCategoryStore } from '~/store/products';

definePageMeta({
  name: "productCategory"
});

const route = useRoute();
const productCategoryStore = useProductCategoryStore();
const { data: category } = await productCategoryStore.retrieveCategory(route.params.categorySlug);
</script>