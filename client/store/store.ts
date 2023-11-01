import { defineStore } from "pinia";

export const useStoreMeta = defineStore("store", {
  state: () => ({
    store: {} as StoreMetaData
  }),
  actions: {
    async fetchStoreData() {
      const URL: string = "store/meta/";

      return useApiFetch<StoreMetaData>(
        URL,
        {
          onResponse: ({ response }) => {
            if (response.ok && response._data) {
              this.store = response._data;
            }
          },
        });
    }
  }
})