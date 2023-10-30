export const useAuth = () => {
  const isAuthenticated = useCookie("authenticated");

  return {
    isAuthenticated
  }
}