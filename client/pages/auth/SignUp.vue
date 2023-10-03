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
          id="first_name"
          name="first_name"
          :label="$t('authentication.firstName')"
          required
        />
    
        <FormKit
          id="last_name"
          name="last_name"
          :label="$t('authentication.lastName')"
          required
        />
    
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
    
        <FormKit
          id="re_password"
          type="password"
          name="password_confirm"
          :label="$t('authentication.confirmPassword')"
          validation="required|confirm"
          validation-visibility="live"
        />
      </FormkitForm>
      <div class="pt-6 text-sm">
        <div>
          {{ $t('authentication.message.alreadyHaveAccount') }}
          <NuxtLink :to="{name: 'signin'}">
            {{ $t('authentication.signIn') }}
          </NuxtLink>
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