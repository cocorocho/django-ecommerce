<template>
  <div>
    <div class="grid lg:grid-cols-2 gap-y-8">
      <BaseInput
        type="dropdown"
        :options="countries"
        optionLabel="name"
        optionValue="slug"
        :placeholder="$t('country')"
        v-model="formData.country"
        @update:modelValue="fetchCities"
        :errors="errors?.country?._errors"
        class="w-full"
      />
  
      <BaseInput
        type="dropdown"
        :options="cities"
        optionLabel="name"
        optionValue="slug"
        :placeholder="$t('stateOrCity')"
        v-model="formData.city"
        class="w-full"
        :errors="errors?.city?._errors"
      />
    </div>

    <div class="grid grid-cols-2 mt-8 gap-y-8">
      <BaseInput
        :label="$t('firstName')"
        v-model="formData.first_name"
        :errors="errors?.first_name?._errors"
      />

      <BaseInput
        :label="$t('lastName')"
        v-model="formData.last_name"
        :errors="errors?.last_name?._errors"
      />
    </div>

    <div class="grid mt-8 gap-y-8">
      <BaseInput
        :label="$t('postalCode')"
        v-model="formData.postal_code"
        :errors="errors?.postal_code"
      />

      <BaseInput
        :label="$t('address')"
        v-model="formData.address"
        :errors="errors?.address?._errors"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
interface Region {
  name: string
  slug: string
}

interface Country {
  name: string
  slug: string
  regions?: Array<Region>
}

const formData = ref<AddressForm>({
  country: "",
  city: "",
  first_name: "",
  last_name: "",
  postal_code: "",
  address: "",
});

const props = defineProps<{
  errors?: object
}>();

const emit = defineEmits(["input"]);

watch(
  formData,
  () => {
    emit("input", formData);
  },
  { deep: true }
);

const cities = ref<Region[] | []>([]);

const { data: countries } = await useApiFetch<Country[]>("geo/countries/");

defineExpose({ countries, formData });

const fetchCities = async (citySlug: string) => {
  if (citySlug) {
    const { data } = await useApiFetch<Country>(`geo/countries/${citySlug}`);
    cities.value = data.value?.regions || [];
  }
};
</script>