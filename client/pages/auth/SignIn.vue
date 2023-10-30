<template>
  <LayoutContainer>
    <div class="w-96 mx-auto mt-8">
      <div class="text-center prose">
        <h2>
          {{ $t("authentication.signIn") }}
        </h2>
      </div>
      <BaseForm
        :errors="errors?._errors"
      >
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
        
        <template #actions>
          <div class="mt-8">
            <NuxtLink
              class="link"
              :to="{ name: 'recover' }"
            >
                <small>{{ $t("authentication.message.forgotYourPassword") }}</small>
            </NuxtLink>
          </div>
          <div class="text-center mt-8">
            <PrimeButton
              type="submit"
              @click.prevent="submitForm"
            >
              {{ $t("authentication.signIn") }}
            </PrimeButton>

            <div>
              <NuxtLink
                class="link"
                :to="{ name: 'signup' }"
              >
                  <small>{{ $t("authentication.message.newUser") }} {{ $t("authentication.signUp") }}</small>
              </NuxtLink>
            </div>
          </div>
        </template>
      </BaseForm>
    </div>
  </LayoutContainer>
</template>

<script setup lang="ts">
import { useAuthStore } from "~/store/auth";
import { z } from "zod";

definePageMeta({
  path: "/signin/",
  name: "signin",
});

const { signInUser, isAuthenticated } = useAuthStore();
const route = useRoute()

if (isAuthenticated) {
  await navigateTo("/")
};

const formData = ref<SigninForm>({
  email: "",
  password: ""
});

const zodSchema = z.object({
  email: z.string().min(1).email(),
  password: z.string().min(1)
});

const { validate, pushErrors, errors } = useZodForm(zodSchema, formData);

const submitForm = async () => {
  const formValid = validate();

  if (formValid.success) {
    try {
      await signInUser(formData.value);
    } catch (error) {
      if (error?.response._data) {
        pushErrors(error.response._data);
      }
    }
  }
}
</script>

<style scoped>
.container:deep(input) {
  width: 100%;
}
</style>