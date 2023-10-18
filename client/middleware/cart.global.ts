import { useCartStore } from "~/store/cart"

export default defineNuxtRouteMiddleware((to, from) => {
  const cartStore = useCartStore();

  // Initialize cart fetch/create
  cartStore.initializeCart();
})