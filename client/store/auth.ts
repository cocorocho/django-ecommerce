import { defineStore } from 'pinia';


export const useAuthStore = defineStore('auth', {
  state: () => ({
    loading: false,
  }),
  actions: {
    async signUpUser(payload: ISignUp) {
      const URL = "/account/"

      try {
        this.loading = true;
        payload.re_password = payload.password_confirm;
        const response = await useFetchApi(URL, { method: "POST", body: payload });
        return response;
      } finally {
        this.loading = false;
      }
    },
    async signInUser(payload: ISignIn) {
      const URL = "/account/signin/"

      try {
        this.loading = true;
        await useFetchApi(URL, { method: "POST", body: payload });
        // session-id is set to cookie

        // Redirect to home
        await navigateTo("/");
      } finally {
        this.loading = false;
      }
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
