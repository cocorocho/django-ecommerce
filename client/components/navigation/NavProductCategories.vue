<template>
  <div class="w-full bg-white">
    <div class="container mx-auto">
      <div class="dropdown dropdown-hover static" v-for="category in categories">
        <label tabindex="0" class="btn btn-ghost m-1 font-semibold">{{ category.name }}</label>
        <ul tabindex="0" class="dropdown-content z-[1] p-2 w-full absolute left-0 !transition-none h-56 bg-white" v-if="!pending">
          <div class="container mx-auto">
            <div class="divider my-0"></div>
            <div class="grid grid-cols-3 lg:grid-cols-4 gap-y-8 p-4">
              <li v-for="subCategory in category.sub_categories" :key="subCategory.slug">
                <NuxtLink
                  :to="{ name: 'productCategory', params: { name: subCategory.slug } }"
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
const categoriesURL = "store/category/";

const { data: categories, pending } = await useApiFetch(categoriesURL);
</script>

<style scoped>
.grid:deep(a) {
  @apply link-neutral link-hover font-semibold;
}
</style>