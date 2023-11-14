<template>
  <LayoutContainer :fluid="true">
    <section id="featured">
      <CatalogFeatured />
    </section>
    <section id="hero">
    </section>
  </LayoutContainer>
</template>

<script setup lang="ts">
import { useStoreMeta } from '~/store/store';

const storeMeta = useStoreMeta();
const { data: storeMetaData } = await useAsyncData("storeMetaData", async () => storeMeta.store);

useSeoMeta({
  title: storeMetaData.value?.name,
  ogTitle: storeMetaData.value?.name,
  description: storeMetaData.value?.seo?.description,
  ogDescription: storeMetaData.value?.seo?.description
});
</script>

<style scoped>
#hero {
  height: 50dvh;
  @apply mt-8 flex justify-center items-center relative;
}

#hero::before {
  content: "";
  background-image: url('/hero.jpg');
  background-size: cover;
  z-index: -1;
  height: 100%;
  width: 100%;
  position: absolute;
  filter: brightness(.5);
}
</style>