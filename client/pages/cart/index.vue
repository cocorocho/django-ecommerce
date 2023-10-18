<template>
  <LayoutContainer
    :label="cartStore.hasItems ? $t('store.yourCart') : ''"
  >
    <template
      v-if="cartStore.hasItems && data"
    >
      <CatalogCartTable
        :cart-items="data.items"
      />
      <div class="divider"></div>
      <div class="flex justify-end">
        <div class="flex">
          <p class="font-semibold">{{ $t("store.estimatedTotal") }}</p>
          <p class="ml-2">
            <span>$</span>
            {{ data.total_price }}
          </p>
        </div>
      </div>
    </template>
    <template v-else>
      <div class="pt-24 text-center">
        <p class="text-5xl">{{ $t("store.cartIsEmpty") }}</p>
        <NuxtLink
          to="/"
          class="mt-10 btn btn-secondary"
        >
          {{ $t("store.continueShopping") }}
        </NuxtLink>
      </div>
    </template>
  </LayoutContainer>
</template>

<script setup lang="ts">
import { useCartStore } from '~/store/cart';

const cartStore = useCartStore();

const { data } = await cartStore.fetchCartDetails();
</script>