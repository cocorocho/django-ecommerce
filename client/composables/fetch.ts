import { useAuthStore } from "~/store/auth";

export const useApiFetch = (url: string, opts: any) => {
  // `useFetch` wrapper
  const config = useRuntimeConfig();
  const apiURL = config.public.apiURL;
  const headers: {[k: string]: any} = {
    "Content-Type": "application/json"
  };

  const { isAuthenticated } = useAuthStore();
  if (isAuthenticated) {
    const token = useCookie("token");
    headers.authorization = `Token ${token}`;
  }

  return useFetch(url, { baseURL: apiURL, headers: headers, ...opts });
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