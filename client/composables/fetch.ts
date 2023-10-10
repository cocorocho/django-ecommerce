export const useApiFetch = (url: string, opts = {}) => {
  // `useFetch` wrapper
  const config = useRuntimeConfig();
  const apiURL = config.public.apiURL;
  const headers: {[k: string]: any} = {
    "Content-Type": "application/json"
  };
  let params = reactive({
    baseURL: apiURL,
    headers: headers,
    ...opts
  });
  
  return useFetch(url, params);
}

export const useFetchApi = (url: string, opts: object) : Promise<unknown> => {
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

  return $fetch(url, params);
}