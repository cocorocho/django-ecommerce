import { defineStore } from "pinia";


export const useProductCategoryStore = defineStore("category", {
  state: () => ({
    loading: false,
    categories: [],
  }),
  actions: {
    async fetchCategories() {
      const categoriesURL: string = "store/category/";

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
    async retrieveCategory(slug: string) {
      const categoryURL: string = `store/category/${slug}/`;

      return useApiFetch(categoryURL);
    },
    async retrieveSubCategoryProducts(categorySlug: string, subCategorySlug: string, page: undefined | number) {
      const subCategoryURL: string = `store/category/${categorySlug}/${subCategorySlug}/`;

      return useApiFetch(subCategoryURL);
    }
  },
});