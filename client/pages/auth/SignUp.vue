<template>
  <div class="container mx-auto">
    <LayoutFormContainer
      :header="$t('authentication.signUp')"
    >
      <FormkitForm
        type="form"
        :submit-label="$t('authentication.signUp')"
        @submit="submitForm"
      >
        <FormKit
          name="first_name"
          id="first_name"
          :label="$t('authentication.firstName')"
          required
        />
    
        <FormKit
          name="last_name"
          id="last_name"
          :label="$t('authentication.lastName')"
          required
        />
    
        <FormKit
          type="email"
          name="email"
          id="email"
          :label="$t('authentication.email')"
          required
        />
    
        <FormKit
          type="password"
          name="password"
          id="password"
          :label="$t('authentication.password')"
          required
        />
    
        <FormKit
          type="password"
          name="password_confirm"
          id="re_password"
          :label="$t('authentication.confirmPassword')"
          validation="required|confirm"
          validation-visibility="live"
        />
      </FormkitForm>
      <div class="pt-6 text-sm">
        <div>
          {{ $t('authentication.message.alreadyHaveAccount') }}
          <NuxtLink :to="{name: 'signin'}">{{ $t('authentication.signIn') }}</NuxtLink>
        </div>
      </div>
    </LayoutFormContainer>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from "~/store/auth";

definePageMeta({
  path: "/signup/",
  name: "signup"
})

const { signUpUser, signInUser, isAuthenticated } = useAuthStore();

if (isAuthenticated) await navigateTo("/");

const submitForm = async (formData: ISignUp, node: any) => {
  try {
    await signUpUser(formData);
    await signInUser({ email: formData.email, password: formData.password });
  } catch (error: any) {
    if (error?.response?._data) {
      node.setErrors(error.response._data?.non_field_errors, error.response._data)
    }
  }
}
</script>

<style scoped>
.container:deep(input) {
  width: 100%;
}
</style>