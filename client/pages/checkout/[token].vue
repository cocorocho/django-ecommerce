<template>
  <LayoutContainer
    id="checkout-form"
  >
    <div class="grid lg:grid-cols-2">
      <div>
        <BaseForm
          :errors="errors?._errors"
        >
          <section
            v-if="!isAuthenticated"
            id="contact"
          >
            <p class="section-header">
              {{ $t("store.contact") }}
            </p>
            <div class="mt-6">
              <div class="text-end">
                <NuxtLink
                  class="link"
                  :to="{ name: 'signin', query: { redirect: route.fullPath }}"
                >
                    <small>{{ $t("authentication.message.alreadyHaveAccount") }} {{ $t("authentication.signIn") }}</small>
                </NuxtLink>
              </div>
              <BaseInput
                type="text"
                name="email"
                id="email"
                :label="$t('authentication.email')"
                v-model="formData.email"
                :errors="errors?.email?._errors"
              />
            </div>
          </section>
          <section id="delivery">
            <p class="section-header">{{ $t("store.delivery") }}</p>

            <template v-if="!isAuthenticated">
              <CatalogCheckoutFormAddress
                class="mt-6"
                @input="formData.shipping_address = $event"
                :errors="errors?.shipping_address"
              />
            </template>
            <template v-else>
              <UserAddressList
                @addressSelected="formData.shipping_address = $event"
                :errors="errors?.shipping_address"
              />
            </template>
          </section>
          <section id="payment">
            <p class="section-header">{{ $t('payment.payment') }}</p>
            <CatalogCheckoutFormPayment
              :errors="errors?.payment"
              @input="formData.payment = $event"
            />
          </section>
        </BaseForm>
      </div>
      <div>
        <section
          id="order-summary"
          v-if="checkoutData"
        >
          <PrimeAccordion
            class="lg:hidden"
            :activeIndex="0"
          >
            <PrimeAccordionTab
              :header="$t('store.orderSummary')"
            >
              <CatalogCartSummary
                :cart-data="checkoutData.cart"
                :total-price="checkoutData.total_price"
              />
            </PrimeAccordionTab>
          </PrimeAccordion>
          <div
            class="hidden lg:block"
          >
            <p class="section-header">
              {{ $t('store.orderSummary') }}
            </p>
            <CatalogCartSummary
              :cart-data="checkoutData.cart"
              :total-price="checkoutData.total_price"
            />
          </div>
        </section>
      </div>
      <div class="mt-8 text-center">
        <PrimeButton
          @click="submitOrder"
          severity="success inline w-60"
        >
          {{ $t('payment.placeOrder') }}
        </PrimeButton>
      </div>
    </div>
  </LayoutContainer>
</template>

<script setup lang="ts">
import { useCartStore } from '~/store/cart';
import { z } from "zod";

definePageMeta({
  name: "cartCheckOut",
});

const { t } = useI18n();

const route = useRoute();
const checkoutToken: string | string[] = route.params?.token;

const cartStore = useCartStore();

const { isAuthenticated } = useAuth();

// Validate/Get checkout session data
const { data: checkoutData } = await cartStore.fetchCheckoutSessionData(checkoutToken);

const formData = ref<FinalizeOrderForm>({
  email: "",
  shipping_address: {
    country: "",
    city: "",
    first_name: "",
    last_name: "",
    postal_code: "",
    address: ""
  },
  payment: {
    card_number: "",
    expiration_date: "",
    security_code: "",
    name_on_card: "",
    billing_address: undefined,
    use_shipping_address_as_billing_address: true
  }
});

// TODO
const zodSchema = z.object({
  email: z.string().email().optional().or(z.literal("")).superRefine((value, ctx) => {
    // Conditionally require email if user is not authenticated
    if (!isAuthenticated && !value) {
      return ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: t("form.isRequired", { name: t('email') }),
        path: ['email']
      })
    }
  }),
  shipping_address: z.object({
    country: z.string().min(1),
    city: z.string().min(1),
    first_name: z.string().min(1),
    last_name: z.string().min(1),
    postal_code: z.string().min(1),
    address: z.string().min(1),
  }).optional().or(
    z.string()
  ),
  payment: z.object({
    card_number: z.string().min(1),
    expiration_date: z.string().regex(/^(0[1-9]|1[0-2])\/?([0-9]{4}|[0-9]{2})$/),
    security_code: z.string().regex(/^\d{3}$/),
    name_on_card: z.string().min(1),
  })
});

const { validate, pushErrors, errors } = useZodForm(zodSchema, formData);

const submitOrder = async () => {
  const formValid = validate();

  if (formValid.success) {
    try {
      await cartStore.submitOrder(checkoutToken, formData.value);
    } catch (error) {
      if (error?.response._data) {
        pushErrors(error.response._data);
      }
    }
  }
};
</script>

<style scoped>
#checkout-form:deep(.section-header) {
  @apply text-3xl font-semibold mb-2;
}

#checkout-form section:not(:first-child) {
  @apply mt-4;
}

#checkout-form:deep(.input-wrapper) {
  @apply w-full;
}
#checkout-form:deep(input) {
  @apply w-full;
}
#checkout-form:deep(.grid) {
  @apply gap-x-4;
}
</style>