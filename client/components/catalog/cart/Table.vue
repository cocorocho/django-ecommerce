<template>
  <PrimeDataTable
    :value="cartItems"
  >
    <PrimeColumn field="product" :header="$t('store.product')">
      <template #body="{ data }">
        <div class="flex">
          <NuxtImg
            width="100px"
            height="100px"
            :src="data.product.thumbnail"
          />
          <div class="pl-2">
            <p class="font-semibold">{{ data.product.name }}</p>
            <p><span>$</span>{{ data.product.price }}</p>
            <div class="md:hidden mt-2">
              <ClientOnly>
                <CatalogCartItemQuantity
                  :cart-item="data"
                />
              </ClientOnly>
            </div>
          </div>
        </div>
      </template>
    </PrimeColumn>
    <PrimeColumn
      field="quantity" :header="$t('store.quantity')"
      :pt="{
        root: {
          class: 'hidden md:display-revert'
        }
      }"
    >
      <template #body="{ data }">
        <div class="hidden md:display-unset">
          <CatalogCartItemQuantity
            :cart-item="data"
          />
        </div>
      </template>
    </PrimeColumn>
    <PrimeColumn field="total_price" :header="$t('store.total')">
      <template #body="{ data }">
        $ {{ data.total_price }}
      </template>
    </PrimeColumn>
  </PrimeDataTable>
</template>

<script setup lang="ts">
const props = defineProps<{
  cartItems?: Array<CartItem>
}>();
</script>