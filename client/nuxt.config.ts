// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  modules: [
    "@nuxtjs/eslint-module",
    "@nuxt/image",
    "@nuxtjs/i18n",
    "@formkit/nuxt",
    "@pinia/nuxt",
    "@pinia-plugin-persistedstate/nuxt",
    "@vueuse/nuxt",
    "nuxt-icon",
    "vue3-carousel-nuxt",
    "nuxt-lodash"
  ],
  css: ["~/assets/css/main.css"],
  postcss: {
    plugins: {
      tailwindcss: {},
      autoprefixer: {},
    },
  },
  runtimeConfig: {
    public: {
      apiURL: process.env.API_URL || "http://localhost:8000"
    }
  },
  image: {
    domains: [
      process.env.API_URL || "http://localhost:8000",
    ]
  },
  lodash: {
    prefix: "lodash"
  }
})
