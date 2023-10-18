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
  let params: UseFetchOptions<T> = {
    baseURL: apiURL,
    headers: headers,
    ...opts
  };
  
  return useFetch(url, params);
}

export function useFetchApi<T> (url: string, opts: NitroFetchOptions<NitroFetchRequest> = {}) {
  // `$fetch` wrapper
  const config = useRuntimeConfig();
  const apiURL = config.public.apiURL;
  const headers = {
    "Content-Type": "application/json"
  };
  let params = reactive({
    baseURL: apiURL,
    headers: headers,
    ...opts
  });

  return $fetch<T>(url, params);
}