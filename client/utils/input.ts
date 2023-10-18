export const validateChars = (event: KeyboardEvent, disallowedChars: Array<string> | undefined) => {
  if (Array.isArray(disallowedChars) && disallowedChars.length) {
    if (disallowedChars.includes(event.key)) event.preventDefault();
  }
}