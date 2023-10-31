export const buildMediaUrl = (url: string) => {
  const config = useRuntimeConfig();
  const fullUrl: string = config.public.apiURL + "/media/" + url;
  return fullUrl;
}