// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  modules: [
    "@nuxtjs/eslint-module",
    "@nuxt/image",
    "@nuxtjs/i18n",
    "@pinia/nuxt",
    "@pinia-plugin-persistedstate/nuxt",
    "@vueuse/nuxt",
    "nuxt-icon",
    "nuxt-lodash",
    "nuxt-primevue"
  ],
  css: [
    "~/assets/css/main.css",
    "primevue/resources/themes/viva-light/theme.css",
  ],
  postcss: {
    plugins: {
      tailwindcss: {},
      autoprefixer: {},
    },
  },
  runtimeConfig: {
    public: {
      apiURL: process.env.DJANGO_URL ?? "http://localhost:8000"
    }
  },
  image: {
    domains: [
      process.env.DJANGO_URL ?? "http://localhost:8000",
      process.env.NODE_ENV === "development" ? "https://placehold.co" : "",
    ],
  },
  lodash: {
    prefix: "lodash"
  },
  piniaPersistedstate: {
    cookieOptions: {
      sameSite: true
    },
    storage: "localStorage"
  },
  primevue: {
    components: {
      prefix: "Prime",
    }
  },
  alias: {
    quill: process.dev ? "quill/dist/quill.js" : "quill",
  }
})
