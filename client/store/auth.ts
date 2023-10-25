import { defineStore } from 'pinia';


export const useAuthStore = defineStore('auth', {
  state: () => ({
    loading: false,
  }),
  actions: {
    async signUpUser(payload: SignupForm) {
      const URL = "/account/"

      // Server expects `re_password` for password matching
      // Not `confirm_password`
      payload.re_password = payload.confirm_password;

      const _payload: any = Object.assign({}, payload);
      delete _payload.confirm_password;

      return useFetchApi(
        URL,
        {
          method: "POST",
          body: _payload,
          onRequest: () => {
            this.loading = true;
          },
          onResponse: () => {
            this.loading = false;
          }
        }
      )
    },
    async signInUser(payload: SigninForm) {
      const URL = "/account/signin/"

      return useFetchApi(
        URL,
        {
          method: "POST",
          body: payload,
          onResponse: async ({ response }) => {
            if (response.ok) await navigateTo("/");
            this.loading = false;
          },
        }
      );
    },
    async recoverAccount(payload: RecoverAccountForm) {
      /**
       * Send password reset request
       */
      const URL = "/account/reset_password/";

      return useFetchApi(
        URL,
        {
          method: "POST",
          body: payload,
        }
      )
    }
  },
  getters: {
    isAuthenticated: () => {
      // Key for cookie is `AUTH_COOKIE_KEY` on server
      const authenticated = useCookie("authenticated");

      if (authenticated.value) {
        return true;
      }
      return false;
    }
  }
});
