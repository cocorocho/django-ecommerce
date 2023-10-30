import { defineStore } from "pinia";

export const useProductCategoryStore = defineStore("category", {
  state: () => ({
    loading: false,
    categories: [],
  }),
  actions: {
    async fetchCategories() {
      const categoriesURL: string = "product/store/category/";

      try {
        const { data, pending } = await useApiFetch(categoriesURL);
        this.loading = pending.value;
        if (Array.isArray(data.value) && data.value.length) {
          this.categories = data.value;
        }
      } catch (error) {
        console.log(error);
      }
    },
    async retrieveCategory(slug: string | string[]) {
      const categoryURL: string = `product/store/category/${slug}/`;

      return useApiFetch<ProductCategory>(categoryURL);
    },
    async retrieveSubCategoryProducts(categorySlug: string | string[], subCategorySlug: string | string[], page: undefined | number) {
      const subCategoryURL: string = `product/store/category/${categorySlug}/${subCategorySlug}/`;

      return useApiFetch<PaginatedResponse>(subCategoryURL, { query: { page: page }});
    }
  }
});

export const useProductStore = defineStore("productStore", {
  state: () => ({}),
  actions: {
    async retrieveProductDetails(productId: string | string[]) {
      const productDetailsURL: string = `product/${productId}/`;

      return useApiFetch<Product>(productDetailsURL);
    },
  },
})