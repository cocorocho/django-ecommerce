import { defineStore } from "pinia";

export const useToastStore = defineStore("toast", {
  state: () => ({
    _toasts: <Array<Toast>>[],
  }),
  actions: {
    addToast(message: string, status: "success" | "info" | "error" | "warning" | undefined) {
      const toast: Toast = {
        message: message,
        status: status
      };
      this._toasts.push(toast);

      // Remove toast after timeout
      setTimeout(
        () => this.removeToast(toast),
        3000
      );
    },
    removeToast(toast: Toast) {
      const index = this.$state._toasts.indexOf(toast);

      if (index !== undefined) this.$state._toasts.splice(index, 1);
    }
  },
  getters: {
    getToasts: (state) => state._toasts,
  }
})