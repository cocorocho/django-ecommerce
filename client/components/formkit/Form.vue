<template>
  <FormKit
    type="form"
  >
    <slot />
  </FormKit>
</template>

<style scoped>
.formkit-form:deep(.formkit-outer) {
  padding-bottom: 8px;
}
</style>