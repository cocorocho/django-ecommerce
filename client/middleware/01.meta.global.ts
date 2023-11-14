import { useStoreMeta } from "~/store/store";

export default defineNuxtRouteMiddleware(async (to, from) => {
  const storeMeta = useStoreMeta();
  await storeMeta.fetchStoreData();

  // Get CSRF Token
  await useApiFetch("set-csrf/");
});