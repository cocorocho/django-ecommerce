import * as z from "zod";

export const useZodForm = (zodSchema: z.ZodType, formData: Ref<object>) => {
  type formSchemaType = z.infer<typeof zodSchema>;
  const errors = ref<z.ZodFormattedError<formSchemaType> | null>({_errors: []});

  const resetErrors = () => errors.value = {_errors: []};

  const validate = () => {
    // Initially reset errors
    resetErrors();

    const validation = zodSchema.safeParse(formData.value);

    if (!validation.success) {
      errors.value = validation.error.format();
    };

    return validation;
  }

  const pushErrors = (object: {[key: string]: string} | string[]) => {
    // Set field level errors by field `name`
    if (isPlainObject(object)) {
      Object.keys(object).forEach(key => {
        lodashSet(errors.value, `${key}._errors`, lodashGet(object, key));
      })
      return;
    }

    // Set for level errors
    lodashSet(errors.value, "_errors", object);
  }

  return {
    errors,
    validate,
    pushErrors,
  }
}