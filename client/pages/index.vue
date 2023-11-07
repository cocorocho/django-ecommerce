<template>
  <LayoutContainer :fluid="true">
    <section id="featured">
      <CatalogFeatured />
    </section>
    <section id="hero">
        <div
          style="filter: none;"
        >
          <NuxtLink
            to="catalog/guitbass/"
          >
            <PrimeButton>
              {{ $t('store.shopNow') }}
            </PrimeButton>
          </NuxtLink>
        </div>
    </section>
  </LayoutContainer>
</template>

<style scoped>
#hero {
  height: 50dvh;
  @apply mt-8 flex justify-center items-center relative;
}

#hero::before {
  content: "";
  background-image: url('~/public/hero.jpg');
  background-size: cover;
  z-index: -1;
  height: 100%;
  width: 100%;
  position: absolute;
  filter: brightness(.5);
}
</style>