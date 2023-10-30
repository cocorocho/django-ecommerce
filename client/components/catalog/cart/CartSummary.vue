<template>
  <div>
    <ul class="list-none p-0">
      <li
        v-for="item in cartData.items"
        :key="item.id"
        class="shadow-md p-4"
      >
        <div class="flex">
          <div
            v-badge="item.quantity"
            class="border"
          >
            <NuxtImg
              :src="item.product.thumbnail"
              sizes="80px md:100px"
              v-badge="4"
            />
          </div>
          <div class="p-4 flex justify-between grow">
            <div>
              <p class="font-semibold m-0">
                {{ item.product.manufacturer }}
              </p>
              <small>
                {{ item.product.name }}
              </small>
            </div>
            <div class="flex items-center">
              <span>$</span>
              {{ item.total_price }}
            </div>
          </div>
        </div>
      </li>
      <li>
        <div class="flex justify-end pt-4 px-4">
          <div>
            <p class="font-semibold m-0 text-end">
              {{ $t("store.total") }}
            </p>
            <p class="m-0">
              <span>$</span>{{ totalPrice }}
            </p>
          </div>
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  cartData: Cart,
  totalPrice: string
}>();
</script>

<style scoped>
.p-badge {
  z-index: 1;
}
</style>