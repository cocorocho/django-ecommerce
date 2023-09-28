<template>
  <div class="shadow-md">
    <div class="navbar bg-base-200 flex-col">
      <div class="container mx-auto">
        <div class="navbar-center">
          <NuxtLink to="/">
            <img src="https://placehold.co/200x40" alt="">
          </NuxtLink>
        </div>
        <div class="navbar-end">
          <div class="flex justify-end">
            <NuxtLink to="/cart/" class="link-neutral">
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