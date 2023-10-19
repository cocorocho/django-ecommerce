import type {
  NitroFetchRequest,
  NitroFetchOptions
} from "nitropack";
import { UseFetchOptions } from "nuxt/app";

export function useApiFetch<T> (url: string, opts: UseFetchOptions<T> = {}) {
  // `useFetch` wrapper
  const config = useRuntimeConfig();
  const apiURL = config.public.apiURL;
  const headers: {[k: string]: any} = {
    "Content-Type": "application/json"
  };
  let params: UseFetchOptions<T> = reactive({
    baseURL: apiURL,
    headers: headers,
    credentials: "include",
    ...opts
  });
  
  return useFetch(url, params);
}

export function useFetchApi<T> (url: string, opts: NitroFetchOptions<NitroFetchRequest> = {}) {
  // `$fetch` wrapper
  const csrfToken = useCookie<string | undefined>("csrftoken");
  const config = useRuntimeConfig();
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