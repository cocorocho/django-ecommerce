<template>
  <LayoutContainer>
    <div class="grid md:grid-cols-3 gap-x-2">
      <div class="md:col-span-2">
        <div>
          <Carousel
            ref="mainCarousel"
            class="py-3 border"
          >
            <Slide
              v-for="image in data.images"
              :key="image.image"
            >
              <NuxtImg
                :src="image.image"
                height="600px"
              />
            </Slide>
            <template #addons>
              <Navigation
                class="lg:!hidden"
              />
            </template>
          </Carousel>
        </div>
        <div
          v-if="data.images"
          class="hidden md:block mt-2"
        >
          <Carousel
            id="gallery"
            ref="gallery"
            :items-to-show="data.images?.length >= 8 ? 8 : 5"
          >
            <Slide
              v-for="(image, index) in data.images"
              :key="index"
              class="px-2"
              :class="{
                'border-primary': currentSlide === index,
              }"
            >
              <button
                type="button"
                @click="slideTo(index)"
              >
                <NuxtImg
                  :src="image.image"
                  height="80px"
                  width="80px"
                />
              </button>
            </Slide>
          </Carousel>
        </div>
      </div>
      <div class="flex flex-col justify-around">
        <div>
          <div class="font-semibold">
            <h1 class="text-4xl">
              {{ data.manufacturer }}
            </h1>
            <h2 class="text-2xl">
              {{ data.name }}
            </h2>
          </div>
          <h1 class="text-4xl font-bold pt-6">
            <span class="text-2xl">$</span>{{ data.price }}
          </h1>
          <p
            class="font-semibold"
            :class="[data.in_stock ? 'text-green-500' : 'text-red-500']"
          >
            {{ data.in_stock ? $t('store.inStock') : $t('store.outOfStock') }}
          </p>
        </div>
        <div class="pt-2 space-y-4">
          <CatalogCartAddProduct
            class="btn w-full btn-secondary btn-outline"
            :class="{'btn-disabled': !data.in_stock}"
            :product-id="data.id"
          >
            {{ $t("store.addToCart") }}
          </CatalogCartAddProduct>
          <button
            class="btn w-full btn-primary"
            :class="{'btn-disabled': !data.in_stock}"
          >
            {{ $t("store.buyNow") }}
          </button>
        </div>
        <div class="pt-2">
          <p class="text-lg">
            {{ data.description }}
          </p>
        </div>
      </div>
    </div>
  </LayoutContainer>
</template>

<script setup lang="ts">
import { useProductStore } from '~/store/products';

definePageMeta({
  name: "storeProductDetails"
});

const route = useRoute();
const productStore = useProductStore();
const currentSlide = ref<number>(0);
const mainCarousel = ref();
const gallery = ref();

const slideTo = (index: number) =>  {
  currentSlide.value = index;
  mainCarousel.value.slideTo(index);
  gallery.value.slideTo(index);
}

const productId: string | string[] = route.params?.id;
const { data } = await productStore.retrieveProductDetails(productId);
</script>


<style scoped>
#gallery:deep(.carousel__slide) {
  @apply border border-2;
}

#gallery:deep(.carousel__track) {
  @apply gap-x-2;
}
</style>