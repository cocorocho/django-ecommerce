<template>
  <LayoutContainer>
    <div class="w-96 mx-auto mt-8">
      <div class="text-center prose">
        <h2>
          {{ $t("authentication.message.recoverYourAccount") }}
        </h2>
      </div>
      <BaseForm
        :errors="errors?._errors"
      >
        <BaseInput
          class="w-full"
          wrapper-class="mt-8"
          name="email"
          id="email"
          :label="$t('authentication.email')"
          v-model="formData.email"
          :errors="errors?.email?._errors"
        />
        
        <template #actions>
          <div class="text-center my-8">
            <div
              v-if="resetMailSent"
              class="prose my-4"
            >
              <p>
                {{ $t("authentication.message.emailResetSuccess") }}
              </p>
            </div>
            <PrimeButton
              type="submit"
              @click.prevent="submitForm"
            >
              {{ $t("authentication.resetPassword") }}
            </PrimeButton>

            <div class="flex flex-col gap-2 mt-4">
              <NuxtLink
                class="link"
                :to="{ name: 'signup' }"
              >
                  <small>{{ $t("authentication.message.newUser") }} {{ $t("authentication.signUp") }}</small>
              </NuxtLink>
              <NuxtLink
                class="link"
                :to="{ name: 'signin' }"
              >
                  <small>{{ $t("authentication.signIn") }}</small>
              </NuxtLink>
            </div>
          </div>
        </template>
      </BaseForm>
    </div>

  </LayoutContainer>
</template>

<script setup lang="ts">
import { z } from "zod";
import { useAuthStore } from '~/store/auth';

definePageMeta({
  path: "/account/recover/",
  name: "recover"
})

const { isAuthenticated, recoverAccount } = useAuthStore();

if (isAuthenticated) {
  await navigateTo("/");
};

const formData = ref<RecoverAccountForm>({
  email: "",
})

const zodSchema = z.object({
  email: z.string().min(1).email(),
});

const { validate , pushErrors, errors } = useZodForm(zodSchema, formData);

const resetMailSent = ref<boolean>(false);

const submitForm = async () => {
  const formValid = validate();

  if (formValid.success) {
    resetMailSent.value = false;

    try {
      await recoverAccount(formData.value);
      resetMailSent.value = true;
    } catch (error) {
      if (error.response._data) {
        pushErrors(error.response._data);
      }
    }
  };
}
</script>