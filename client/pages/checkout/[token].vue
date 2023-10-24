<template>
  <LayoutContainer
    id="checkout-form"
  >
    <div class="grid lg:grid-cols-5">
      <div class="col-span-3">
        <FormkitForm
          v-model="checkoutFormData"
          :submit-label="$t('payment.placeOrder')"
          @submit="submitOrder"
        >
          <section id="contact">
            <p class="section-header">{{ $t("store.contact") }}</p>
            <div>
              <FormKit
                type="email"
                placeholder="Email"
                validation="required"
                name="email"
                id="email"
              />
            </div>
          </section>
          <section id="delivery">
            <p class="section-header">{{ $t("store.delivery") }}</p>
            <FormKit
              type="group"
              name="shipping_address"
            >
              <CatalogCheckoutFormAddres />
            </FormKit>
          </section>
          <section id="payment">
            <p class="section-header">{{ $t('payment.payment') }}</p>
            <FormKit
              type="group"
              name="payment"
            >
              <CatalogCheckoutFormPayment />
            </FormKit>
          </section>
        </FormkitForm>
      </div>
      <div>
        TODO items
      </div>
    </div>
    {{ checkoutFormData }}
  </LayoutContainer>
</template>

<script setup lang="ts">
import { useCartStore } from '~/store/cart';

definePageMeta({
  name: "cartCheckOut"
});

const route = useRoute();
const cartStore = useCartStore();

const checkoutFormData = ref();

const checkoutToken: string | string[] = route.params?.token;
const { data } = await cartStore.fetchCheckoutSessionData(checkoutToken);

const submitOrder = async (formData, node) => {
  const response = await cartStore.submitOrder(checkoutToken, formData);
}
</script>

<style scoped>
.section-header {
  @apply text-3xl font-semibold mb-2;
}

#checkout-form section:not(:first-child) {
  @apply mt-4;
}

#checkout-form:deep(.formkit-input) {
  @apply w-full;
}
#checkout-form:deep(.grid) {
  @apply gap-x-4;
}
</style>