export const buildMediaUrl = (url: string) => {
  const config = useRuntimeConfig();
  let mediaURL: string = config.public.mediaURL;

  if (!mediaURL.endsWith("/")) {
    mediaURL += "/";
  }

  const fullUrl: string = config.public.mediaURL + url;
  return fullUrl;
}