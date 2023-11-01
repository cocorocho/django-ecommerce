import { defineStore } from "pinia";

export const useProductCategoryStore = defineStore("category", {
  state: () => ({
    loading: false,
    categories: [] as ProductCategory[],
  }),
  actions: {
    async fetchCategories() {
      const categoriesURL: string = "product/store/category/";

      return useApiFetch<ProductCategory[]>(categoriesURL, {
        onResponse: async ({ response }) => {

          if (response.ok) {
            this.categories = response?._data;
          }
        },
      });
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
    async fetchFeatured() {
      const URL = "store/product/featured/"

      return useApiFetch<FeaturedProduct[]>(URL)
    }
  },
})