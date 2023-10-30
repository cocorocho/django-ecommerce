<template>
  <label :for="_id">
    <PrimeCard
      :pt="{
        root: {
          class: [
            'cursor-pointer',
            {
              'border-[var(--primary-color)]': checkbox?.checked,
              'border-solid': checkbox?.checked,
              'border-2': checkbox?.checked
            }
          ]
        },
        header: { class: 'capitalize' }
      }"
    >
      <template #title class="capitalize">
        <div class="flex justify-between">
          <div v-if="address">
            {{ address.name }}
          </div>
          <div v-else>
            {{ $t("useDifferentAddress") }}
          </div>
          <PrimeRadioButton
            :inputId="_id"
            :value="_id"
            v-bind="$attrs"
            ref="checkbox"
          />
        </div>
      </template>
      <template #content>
        <template v-if="address">
          <div>
            {{address.address}} - {{ address.postal_code }}
          </div>
          <div>
            {{ address.city }} {{ address.country }}
          </div>
        </template>
        <template v-else>
          <slot />
        </template>
      </template>
    </PrimeCard>
  </label>
</template>

<script setup lang="ts">
const props = defineProps<{
  address?: Address,
  id?: string
}>();

const checkbox = ref();
const _id = ref(
  props.address?.id.toString() || props.id
);
</script>