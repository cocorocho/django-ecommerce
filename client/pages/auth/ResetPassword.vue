<template>
  <div class="container mx-auto">
    <LayoutFormContainer
      :header="$t('authentication.resetPassword')"
    >
      <BaseForm
        :errors="errors?._errors"
      >
        <BaseInput
          wrapper-class="mt-8"
          class="w-full"
          type="password"
          name="new_password"
          id="new_password"
          :label="$t('authentication.password')"
          v-model="formData.new_password"
          :errors="errors?.new_password?._errors"
          :feedback="false"
        />

        <BaseInput
          wrapper-class="mt-8"
          class="w-full"
          type="password"
          name="re_new_password"
          id="re_new_password"
          :label="$t('authentication.confirmPassword')"
          v-model="formData.re_new_password"
          :errors="errors?.re_new_password?._errors"
          :feedback="false"
        />
      </BaseForm>
    </LayoutFormContainer>
  </div>
</template>

<script setup lang="ts">
import { z } from "zod";

definePageMeta({
  path: "/account/recover/:uid/:token/",
  name: "resetPassword"
})

const route = useRoute();
const { t } = useI18n();
const { uid, token } = route.params;

interface PasswordResetForm {
  new_password: string,
  re_new_password: string
}

const formData = ref<PasswordResetForm>({
  new_password: "",
  re_new_password: ""
});

const zodSchema = z.object({
  new_password: z.string().min(8),
  re_new_password: z.string().min(8),
}).superRefine(({ new_password, re_new_password }, ctx) => {
  if (new_password !== re_new_password) {
    ctx.addIssue({
      code: "custom",
      message: t("form.error.passwordNotMatch")
    })
  }
})

const { validate, pushErrors, errors } = useZodForm(zodSchema, formData);

const submitForm = async () => {
  const formValid = validate();

  if (formValid.success) {
    try {
      const URL = "account/reset_password_confirm/"
      const payload = {
        uid: uid,
        token: token,
        new_password: formData.value.new_password,
        re_new_password: formData.value.re_new_password
      };
      await useFetchApi(URL, { method: "POST", body: payload });
      await navigateTo({ name: "signin" });
    } catch (error) {
      if (error.response._data) {
        pushErrors(error?.response?._data);
      }
    }
  }
}
</script>