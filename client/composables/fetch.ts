export const useApiFetch = (url: string, opts = {}) => {
  // `useFetch` wrapper
  const config = useRuntimeConfig();
  const apiURL = config.public.apiURL;
  const headers: {[k: string]: any} = {
    "Content-Type": "application/json"
  };

  return useFetch(url, { baseURL: apiURL, headers: headers });
}

export const useFetchApi = (url: string, opts: object) : Promise<unknown> => {
  // `$fetch` wrapper
  const config = useRuntimeConfig();
  const apiURL = config.public.apiURL;
  const headers = {
    "Content-Type": "application/json"
  };

  return $fetch(url, {
    baseURL: apiURL,
    headers: headers,
    credentials: "include",
    ...opts
  }
  );
}