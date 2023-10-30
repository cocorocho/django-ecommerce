<template>
  <div class="grid gap-y-2">
    <UserAddressCard
      v-for="address in data"
      :key="address.id"
      :address="address"
      v-model="selectedAddress"
    />
    <PrimeDivider type="solid">
      <p class="capitalize font-bold">
        {{ $t('or') }}
      </p>
    </PrimeDivider>
    <UserAddressCard
      id="addr"
      :value="customAddress?.formData"
      v-model="selectedAddress"
    >
      <CatalogCheckoutFormAddress
        ref="customAddress"
        :errors="$attrs?.errors"
      />
    </UserAddressCard>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '~/store/auth';

const authStore = useAuthStore();
const customAddress = ref();
const { data } = await authStore.fetchUserAddresses();
const selectedAddress = ref();

const emit = defineEmits(['addressSelected',]);

watch(selectedAddress, (value) => {
  emit('addressSelected', value);
});
</script>