<template>
  <LayoutContainer>
    <LayoutFormContainer
      :header="$t('authentication.signIn')"
    >
      <FormkitForm
        type="form"
        :submit-label="$t('authentication.signIn')"
        @submit="submitForm"
      >
        <FormKit
          id="email"
          type="email"
          name="email"
          :label="$t('authentication.email')"
          required
        />

        <FormKit
          id="password"
          type="password"
          name="password"
          :label="$t('authentication.password')"
          required
        />
      </FormkitForm>
      <div class="pt-6 text-sm">
        <div>
          {{ $t('authentication.message.forgotYourPassword') }}
          <NuxtLink :to="{name: 'recover'}">
            {{ $t("authentication.resetPassword") }}
          </NuxtLink>
        </div>
        <div>
          {{ $t('authentication.message.dontHaveAnAccount') }}
          <NuxtLink :to="{name: 'signup'}">
            {{ $t('authentication.signUp') }}
          </NuxtLink>
        </div>
      </div>
    </LayoutFormContainer>
  </LayoutContainer>
</template>

<script setup lang="ts">
import { useAuthStore } from "~/store/auth"

definePageMeta({
  path: "/signin/",
  name: "signin"
});

const { signInUser, isAuthenticated } = useAuthStore();

if (isAuthenticated) {
  await navigateTo("/")
}

const submitForm = async (formData: ISignIn, node: any) => {
  try {
    await signInUser(formData);
  } catch (error: any) {
    console.log(error)
    if (error?.response?._data) {
      node.setErrors(error.response._data?.non_field_errors, error.response._data);
    }
  }
}
</script>

<style scoped>
.container:deep(input) {
  width: 100%;
}
</style>