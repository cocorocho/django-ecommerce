<template>
  <LayoutContainer>
    <div class="w-96 mx-auto mt-8">
      <div class="text-center prose">
        <h2>
          {{ $t("authentication.signUp") }}
        </h2>
      </div>
      <BaseForm
        :errors="errors?._errors"
      >
        <BaseInput
          wrapper-class="mt-8"
          id="first_name"
          name="first_name"
          :label="$t('authentication.firstName')"
          v-model="formData.first_name"
          :errors="errors?.first_name?._errors"
        />

        <BaseInput
          wrapper-class="mt-8"
          id="last_name"
          name="last_name"
          :label="$t('authentication.lastName')"
          v-model="formData.last_name"
          :errors="errors?.last_name?._errors"
        />

        <BaseInput
          wrapper-class="mt-8"
          name="email"
          id="email"
          :label="$t('authentication.email')"
          v-model="formData.email"
          :errors="errors?.email?._errors"
        />

        <BaseInput
          wrapper-class="mt-8"
          class="w-full"
          type="password"
          name="password"
          id="password"
          :label="$t('authentication.password')"
          v-model="formData.password"
          :errors="errors?.password?._errors"
          :feedback="false"
        />

        <BaseInput
          wrapper-class="mt-8"
          class="w-full"
          type="password"
          name="confirm_password"
          id="confirm_password"
          :label="$t('authentication.confirmPassword')"
          v-model="formData.confirm_password"
          :errors="errors?.confirm_password?._errors"
          :feedback="false"
        />
        
        <template #actions>
          <div class="text-center mt-8">
            <PrimeButton
              type="submit"
              @click.prevent="submitForm"
            >
              {{ $t("authentication.signUp") }}
            </PrimeButton>

            <div>
              <NuxtLink
                class="link"
                :to="{ name: 'signin' }"
              >
                  <small>{{ $t("authentication.message.alreadyHaveAccount") }} {{ $t("authentication.signIn") }}</small>
              </NuxtLink>
            </div>
          </div>
        </template>
      </BaseForm>
    </div>

  </LayoutContainer>
  <!-- <div class="container mx-auto">
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
          name="re_password"
          type="password"
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
  </div> -->
</template>

<script setup lang="ts">
import { useAuthStore } from "~/store/auth";
import { z } from "zod";

definePageMeta({
  path: "/signup/",
  name: "signup"
})

const { t } = useI18n();

const { signUpUser, signInUser, isAuthenticated } = useAuthStore();

if (isAuthenticated) await navigateTo("/");

const formData = ref<SignupForm>({
  first_name: "",
  last_name: "",
  email: "",
  password: "",
  confirm_password: ""
});

const zodSchema = z.object({
  first_name: z.string().min(1),
  last_name: z.string().min(1),
  email: z.string().email().min(1),
  password: z.string().min(8),
  confirm_password: z.string().min(8),
}).superRefine(({ confirm_password, password}, ctx) => {
  if (confirm_password !== password) {
    ctx.addIssue({
      code: "custom",
      message: t("form.error.passwordNotMatch"),
    });
  }
});

const { validate, pushErrors, errors } = useZodForm(zodSchema, formData);

const submitForm = async () => {
  const formValid = validate();

  if (formValid.success) {
    try {
      await signUpUser(formData.value);

      // Signin after signup
      await signInUser(formData.value);
    } catch (error) {
      if (error?.response?._data) {
        pushErrors(error?.response?._data);
      }
    }
  };
}
</script>

<style scoped>
.container:deep(input) {
  width: 100%;
}
</style>