import { z } from "zod";

export default defineNuxtPlugin(() => {
  /**
   * Zod translated/custom error messages
   */
  const { t } = useNuxtApp().$i18n;

  const customErrorMap: z.ZodErrorMap = (issue, ctx) => {
    let nodeName = "";

    if (Array.isArray(issue.path) && issue.path.length) {
      // Get last index of `path` in case schema is nested
      nodeName = issue.path[issue.path.length - 1].toString().replaceAll("_", " ");
    }

    switch (issue.code) {
      case (z.ZodIssueCode.too_small): {
        // `min(1)` validation is interpreted as `required`
        if (issue.minimum === 1) {
          return { message: t("form.isRequired", { name: nodeName }) };
        }

        return { message: ctx.defaultError.replaceAll("String", nodeName) };
      }
    }

    return { message: ctx.defaultError };
  };
  
  z.setErrorMap(customErrorMap);
});
