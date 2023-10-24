<template>
  <div>
    <FormKit
      name="card_number"
      id="card_number"
      :placeholder="$t('payment.cardNumber')"
    />

    <div class="grid grid cols-2 gap-x-2">
      <FormKit
        name="expiration_date"
        id="expiration_date"
        :placeholder="$t('expirationDate')"
      />
      <FormKit
        name="security_code"
        id="security_code"
        :placeholder="$t('securityCode')"
      />
    </div>

    <FormKit
      name="name_on_card"
      id="name_on_card"
      :placeholder="$t('payment.nameOnCard')"
    />

    <FormKit
      type="checkbox"
      name="use_shipping_address_as_billing_address"
      id="use_shipping_address_as_billing_address"
      :label="$t('payment.useShippingAsBilling')"
      v-model="useShippingAddressAsBillingAdress"
    />

    <!-- <div
      v-show="!useShippingAddressAsBillingAdress"
    >
      <h4>{{ $t('billingAdress') }}</h4>
      <FormKit
        type="group"
        name="billing_addres"
      >
        <CatalogCheckoutFormAddres />
      </FormKit>
    </div> -->
  </div>
</template>

<script setup lang="ts">
const useShippingAddressAsBillingAdress = ref<boolean>(true);
</script>