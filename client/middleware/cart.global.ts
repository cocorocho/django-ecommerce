import { useCartStore } from "~/store/cart"

export default defineNuxtRouteMiddleware(async (to, from) => {
  const cartStore = useCartStore();

  // Initialize cart fetch/create
  await cartStore.initializeCart();
})