<template>
  <div class="container mx-auto">
    <LayoutFormContainer
      :header="$t('authentication.resetPassword')"
    >
      <FormkitForm
        id="password-reset"
        @submit="submitForm"
      >
        <FormKit
          id="new_password"
          type="password"
          :label="$t('authentication.password')"
          name="new_password"
          input-class="w-full"
          required
        />
        
        <FormKit
          id="new_password_confirm"
          type="password"
          :label="$t('authentication.confirmPassword')"
          name="new_password_confirm"
          validation="required|confirm"
          validation-visibility="live"
          input-class="w-full"
          required
        />
      </FormkitForm>
    </LayoutFormContainer>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  path: "/account/recover/:uid/:token/",
  name: "resetPassword"
})

const route = useRoute();
const { uid, token } = route.params;

interface IResetPasswordConfirm {
  new_password: string,
  new_password_confirm: string
}

const submitForm = async (formData: IResetPasswordConfirm, node: any) => {
  try {
    const URL = "account/reset_password_confirm/"
    const payload = {
      uid: uid,
      token: token,
      new_password: formData.new_password,
      re_new_password: formData.new_password_confirm
    };
    await useFetchApi(URL, { method: "POST", body: payload });
    navigateTo({ name: "signin" });
  } catch (error) {
    if (error.response._data) {
      node.setErrors(
        error.response._data?.token,
        error.response._data
      )
    }
  }
}
</script>