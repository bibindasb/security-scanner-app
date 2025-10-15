// frontend/src/utils/validators.js
export const isValidUrl = (string) => {
  try {
    new URL(string);
    return true;
  } catch (_) {
    return false;
  }
};

export const validateScanTarget = (url) => {
  if (!url) return 'URL is required';
  if (!isValidUrl(url)) return 'Please enter a valid URL';
  if (!url.startsWith('http://') && !url.startsWith('https://')) {
    return 'URL must start with http:// or https://';
  }
  return null;
};