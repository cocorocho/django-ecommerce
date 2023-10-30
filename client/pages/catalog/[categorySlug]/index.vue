<template>
  <div v-if="category">
    <CatalogBanner
      v-if="category.banner"
      :banner-url="category.banner"
      :title="category.name"
    />
    <LayoutContainer>
      <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-y-8">
        <div
          v-for="subCategory in category.sub_categories"
          :key="subCategory.slug"
          class="text-center"
        >
          <NuxtLink
            :to="{ name: 'productSubCategory', params: { subCategorySlug: subCategory.slug } }"
            class="no-underline hover:underline"
          >
            <NuxtImg
              :src="subCategory.thumbnail"
              sizes="150px md:250px"
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
    </LayoutContainer>
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