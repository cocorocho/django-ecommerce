import ToastEventBus from 'primevue/toasteventbus';

export const useToastService = () => {
  const showToast = (options: {[key: string]: string}) => {
    const { t } = useNuxtApp().$i18n;

    const defaults = {
      severity: "success",
      life: 3000
    };
    options["summary"] = t(options["summary"]);
    const _options = {...defaults, ...options}
    ToastEventBus.emit('add', _options);
  }

  return { showToast };
};