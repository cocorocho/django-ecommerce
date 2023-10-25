<template>
  <div :class="wrapperClass">
    <template v-if="floatLabel && $attrs.label">
      <span class="p-float-label">
        <component :is="inputTypes[type]"
          :class="{ 'p-invalid': errors }"
          aria-describedby="text-error"
          v-bind="$attrs"
        />
        <label
          :for="$attrs.id"
          v-if="$attrs.label"
        >
          {{ $attrs.label }}
        </label>
      </span>
    </template>
    <template v-else>
      <label
        :for="$attrs.id"
        v-if="$attrs.label"
      >
        {{ $attrs.label }}
      </label>
      <component :is="inputTypes[type]"
        :class="{ 'p-invalid': errors }"
        aria-describedby="text-error"
        v-bind="$attrs"
      />
    </template>
    <template v-if="errors">
      <small class="p-error block" v-for="error in errors">{{ error || '&nbsp;' }}</small>
    </template>
  </div>
</template>

<script setup lang="ts">
type InputType = "text" | "password";

const inputTypes = {
  "text": "PrimeInputText",
  "password": "PrimePassword"
};

const props = withDefaults(
  defineProps<{
    floatLabel?: boolean,
    type?: InputType,
    errors?: string[],
    wrapperClass?: string
  }>(),
  {
    floatLabel: true,
    type: "text"
  }
);

const value = ref();
</script>

<style scoped>
.p-error::first-letter {
  @apply uppercase;
}
</style>