import { defineStore } from "pinia";
import { useToastStore } from "./toast";


export const useCartStore = defineStore('cart', {
  state: () => {
    return {
      busy: <boolean>false,
      _cart: <Cart | null>null,
    }
  },
  actions: {
    async _fetchCart(sessionId: string) {
      const URL = `store/cart/${sessionId}/`;
      const { data } = await useApiFetch(URL);
      this._cart = data.value;
    },
    async initializeCart() {
      /**
       * Initialize cart session
       * If no cart exists, create new session
       */
      const cartSessionId = useCookie("cart_session");

      if (cartSessionId.value) {
        await this._fetchCart(cartSessionId.value);
        return;
      }
    },
    async addProductToCart(productId: number, quantity: number = 1) {
      /**
       * Add product to cart
       */
      const cartSessionId = this._cart?.session_id;
      const URL = `store/cart/${cartSessionId}/item/`
      const toastStore = useToastStore();


      try {
        const data: CartItem = await useFetchApi(
          URL,
          {
            method: "POST",
            body: { product: productId, quantity: quantity },
            onResponseError: () => {
              toastStore.addToast("store.error.cantAddProductToCart", "error");
            }
          }
        )

        const newCartItemQuantity: number = data.quantity;
      
        if (newCartItemQuantity === 1) {
          // Means new item was added to cart
          this.cart?.items?.push(data);
        } else {
          const cartItem = this._cart?.items?.find(i => i.product === data.product);
          if (cartItem) cartItem.quantity = newCartItemQuantity;
        }

        toastStore.addToast(
          "store.itemAddedToCart",
          "info"
        );
      } catch (error) {
        console.log("err")
      }
    },
    async fetchCartDetails() {
      /**
       * Fetch cart data with details such as price, thumbnail, etc
       */
      const sessionId = this.cart?.session_id;
      const URL = `store/cart/${sessionId}/`;
      return useApiFetch<Cart>(URL);
    },
    async removeCartItem(cartItemId: number) {
      const cartSessionId = this._cart?.session_id;

      if (!cartSessionId) return;

      const URL: string = `store/cart/${cartSessionId}/item/${cartItemId}/`;
      const response = await useFetchApi(
        URL,
        {
          method: "DELETE",
          onResponse: async () => await this._fetchCart(cartSessionId),
        }
      );
    },
    async changeItemQuantity(cartItemId: number, newQuantity: string) {
      if (parseInt(newQuantity) < 1) return;
      if (!cartItemId) return;

      this.busy = true;
      const cartSessionId = this._cart?.session_id;
      const URL: string = `store/cart/${cartSessionId}/item/${cartItemId}/`
      const payload = { "quantity": newQuantity };
      
      try {
        const response = await useFetchApi(
          URL,
          {
            method: "PATCH",
            body: payload
          }
        );
        await this.fetchCartDetails();
      } catch (error) {
        const toastStore = useToastStore();
        toastStore.addToast("error.somethingWentWrong", "error")
      } finally {
        this.busy = false;
      }
    },
    async checkoutCart() {
      interface CartCheckOut {
        token: string
        cart: number
      }
      
      const router = useRouter();
      const cartSessionId = this._cart?.session_id;
      const URL: string = `checkout/`;

      const payload = {
        "cart_session_id": cartSessionId,
      };

      return useFetchApi<CartCheckOut>(
        URL,
        {
          method: "POST",
          body: payload,
          onResponse: async (context) => {
            if (context.response.ok) {
              await router.push({
                name: "cartCheckOut",
                params: { token: context.response._data.token }
              })
            }
          }
        }
      );
    },
    async fetchCheckoutSessionData(checkoutToken: string | string[]) {
      const router = useRouter();
      const URL: string = `checkout/${checkoutToken}`;

      // TODO onResponse is bugged?

      return useApiFetch(
        `http://localhost:8000/${URL}/`,
        {
          onResponse: async ({ response }) => {
            if (response.ok) {
              const responseCheckoutToken = response._data.token;
              if (responseCheckoutToken !== checkoutToken) {
                await router.push({
                  name: "cartCheckOut",
                  params: { token: response._data.token }
                });
              }
            }
          },
        },
      );
    },
    async submitOrder(checkoutToken: string, formData) {
      const URL: string = `checkout/${checkoutToken}/`;

      // TODO success page

      return useFetchApi(
        URL,
        {
          method: "POST",
          body: formData
        }
      )
    }
  },
  getters: {
    cart: (state) => state._cart,
    hasItems: (state) => state._cart?.items?.length > 0,
    numItems: (state) => state._cart?.items?.length,
  },
  persist: {
    storage: persistedState.cookies,
  }
})
