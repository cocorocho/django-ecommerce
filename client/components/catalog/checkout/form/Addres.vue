<template>
  <div>
    <FormKit
      type="select"
      id="country"
      name="country"
      :options="countries"
      :placeholder="$t('country')"
      validation="required"
      @input="fetchCities"
    />

    <FormKit
      type="select"
      id="city"
      name="state"
      :options="cities"
      :placeholder="$t('stateOrCity')"
      validation="required"
    />

    <div class="grid grid-cols-2">
      <FormKit
        id="first_name"
        name="first_name"
        :placeholder="$t('firstName')"
        validation="required"
      />
      <FormKit
        id="last_name"
        name="last_name"
        :placeholder="$t('lastName')"
        validation="required"
      />
    </div>
    <FormKit
      id="postal_code"
      name="postal_code"
      :placeholder="$t('postalCode')"
      validation="required"
    />
    <FormKit
      id="address"
      name="address"
      :placeholder="$t('address')"
      validation="required"
    />
    <div class="grid grid-cols-2">
      <FormKit
        id="first_name"
        name="first_name"
        :placeholder="$t('firstName')"
        validation="required"
      />
      <FormKit
        id="last_name"
        name="last_name"
        :placeholder="$t('lastName')"
        validation="required"
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

const cities = ref<Region[] | []>([]);

const { data: countries } = await useApiFetch<Country[]>(
  "geo/countries/", {
    transform: (data): Country[] => data?.map((i: Country) => ({label: i.name, value: i.slug}))
  }
);

const fetchCities = async (citySlug: string) => {
  if (citySlug) {
    const { data } = await useApiFetch<Country>(
      `geo/countries/${citySlug}`,
      { transform: (response) => (response?.regions.map((region: Region) => ({ label: region.name, value: region.slug }))) }
    );
    cities.value = data.value;
  }
};
</script>