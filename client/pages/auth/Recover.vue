<template>
  <LayoutFormContainer
    :header="$t('authentication.message.recoverYourAccount')"
  >
    <FormkitForm
      id="account-recover"
      @submit="submitForm"
    >
      <FormKit
        id="email"
        type="email"
        name="email"
        :label="$t('authentication.email')"
        input-class="w-full"
        required
      />
    </FormkitForm>
    <div
      v-if="resetMailSent"
      class="prose"
    >
      <p>
        {{ $t("authentication.message.emailResetSuccess") }}
      </p>
    </div>
  </LayoutFormContainer>
</template>

<script setup lang="ts">
import { useAuthStore } from '~/store/auth';

definePageMeta({
  path: "/account/recover/",
  name: "recover"
})

const { isAuthenticated } = useAuthStore();

if (isAuthenticated) {
  navigateTo("/");
}

interface IRecover {
  email: string,
}

const resetMailSent = ref<boolean>(false);

const submitForm = async (formData: IRecover, node: any) => {
  resetMailSent.value = false;

  try {
    const URL = "/account/reset_password/";
    await useFetchApi(URL, { body: formData, method: "POST" });
    node.reset();
    resetMailSent.value = true;
  } catch (error) {
    if (error.response._data) {
      node.setErrors(error.response._data.non_field_errors, error.response._data);
    }
  }
}
</script>