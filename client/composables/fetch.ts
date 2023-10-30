import type {
  NitroFetchRequest,
  NitroFetchOptions
} from "nitropack";
import { defu } from "defu";
import { UseFetchOptions } from "nuxt/app";

export function useApiFetch<T> (url: string | (() => string), options: UseFetchOptions<T> = {}) {
  const config = useRuntimeConfig();

  const defaults: UseFetchOptions<T> = {
    baseURL: config.public.apiURL,
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
    },
  };

  const params = defu(options, defaults);

  return useFetch(url, params);
}

export function useFetchApi<T> (url: string, opts: NitroFetchOptions<NitroFetchRequest> = {}) {
  // `$fetch` wrapper
  const config = useRuntimeConfig();
  const csrfToken = useCookie<string | undefined>("csrftoken");
  
  const apiURL = config.public.apiURL;
  const headers: {[key: string]: string} = {
    "Content-Type": "application/json",
  };
  
  if (csrfToken.value) headers["X-CSRFToken"] = csrfToken.value;

  let params = reactive({
    baseURL: apiURL,
    headers: headers,
    credentials: "include",
    ...opts
  });

  return $fetch<T>(url, params);
}