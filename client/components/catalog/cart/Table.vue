<template>
  <div class="overflow-x-auto">
    <table class="table table-pin-rows">
      <thead>
        <tr>
          <th class="w-4/6">{{ $t("store.product") }}</th>
          <th class="hidden md:display-unset">{{ $t("store.quantity") }}</th>
          <th>{{ $t("store.total") }}</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="cartItem in cartItems"
        >
          <td>
            <div class="flex">
              <NuxtImg
                width="100px"
                height="100px"
                :src="cartItem.product.thumbnail"
              />
              <div>
                <p class="font-semibold">{{ cartItem.product.name }}</p>
                <p><span>$</span>{{ cartItem.product.price }}</p>
                <div class="md:hidden mt-2">
                  <ClientOnly>
                    <CatalogCartItemQuantity
                      :cart-item="cartItem"
                    />
                  </ClientOnly>
                </div>
              </div>
            </div>
          </td>
          <td>
            <div class="hidden md:display-unset">
              <CatalogCartItemQuantity
                :cart-item="cartItem"
              />
            </div>
          </td>
          <td>
            <span>$</span>{{ cartItem.total_price }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  cartItems?: Array<CartItem>
}>();
</script>