<template>
  <div>
    <BaseInput
      type="mask"
      id="card_number"
      name="card_number"
      mask="9999 9999 9999 9999"
      :placeholder="$t('payment.cardNumber')"
      v-model="formData.card_number"
      :errors="errors?.card_number?._errors"
    />

    <div class="grid grid-cols-2 gap-x-2 mt-8">
      <BaseInput
        type="mask"
        id="expiration_date"
        name="expiration_date"
        mask="**/**"
        :placeholder="$t('expirationDate')"
        v-model="formData.expiration_date"
        :errors="errors?.expiration_date?._errors"
      />

      <BaseInput
        type="mask"
        id="security_code"
        name="security_code"
        :placeholder="$t('securityCode')"
        mask="***"
        v-model="formData.security_code"
        :errors="errors?.security_code?._errors"
      />
    </div>

    <div class="mt-8">
      <BaseInput
        name="name_on_card"
        id="name_on_card"
        :label="$t('payment.nameOnCard')"
        v-model="formData.name_on_card"
        :errors="errors?.name_on_card?._errors"
      />
    </div>

    <div class="mt-8">
      
      <div class="flex gap-x-1">
        <PrimeCheckbox
          name="use_shipping_address_as_billing_address"
          id="use_shipping_address_as_billing_address"
          v-model="formData.use_shipping_address_as_billing_address"
          :binary="true"
        />
        <label for="use_shipping_address_as_billing_address">{{ $t('payment.useShippingAsBilling') }}</label>
      </div>

      <Transition>
        <section
          id="billing_address"
          v-if="!formData.use_shipping_address_as_billing_address"
          class="overflow-hidden"
        >
          <p class="section-header">{{ $t("billingAddress") }}</p>
          <CatalogCheckoutFormAddress
            @input="formData.billing_address = $event"
            :errors="errors?.billing_address"
          />
        </section>
      </Transition>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  errors?: object
}>();

const formData = ref<PaymentForm>({
  card_number: "",
  expiration_date: "",
  security_code: "",
  name_on_card: "",
  use_shipping_address_as_billing_address: true,
  billing_address: undefined
});

const emit = defineEmits(["input"]);

watch(
  formData,
  () => {
    emit("input", formData);
  },
  { deep: true }
);
</script>

<style scoped>
.v-enter-active,
.v-leave-active {
  transition: max-height 0.5s ease-in-out;
  max-height: 500px;
}

.v-enter-from,
.v-leave-to {
  max-height: 0;
}
</style>