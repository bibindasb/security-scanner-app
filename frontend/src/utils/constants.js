// frontend/src/utils/constants.js
export const SCAN_STATUS = {
  PENDING: 'pending',
  RUNNING: 'running',
  COMPLETED: 'completed',
  FAILED: 'failed',
  CANCELLED: 'cancelled',
};

export const SEVERITY_LEVELS = {
  CRITICAL: 'critical',
  HIGH: 'high',
  MEDIUM: 'medium',
  LOW: 'low',
  INFO: 'info',
};

export const SCAN_TYPES = {
  QUICK: 'quick',
  FULL: 'full',
  HEADERS: 'headers',
  SSL: 'ssl',
  PORTS: 'ports',
  CUSTOM: 'custom',
};

export const AI_PROVIDERS = {
  OLLAMA: 'ollama',
  OPENAI: 'openai',
  OPENROUTE: 'openroute',
};

export const OWASP_CATEGORIES = {
  A1: 'A01:2021 - Broken Access Control',
  A2: 'A02:2021 - Cryptographic Failures',
  A3: 'A03:2021 - Injection',
  A4: 'A04:2021 - Insecure Design',
  A5: 'A05:2021 - Security Misconfiguration',
  A6: 'A06:2021 - Vulnerable and Outdated Components',
  A7: 'A07:2021 - Identification and Authentication Failures',
  A8: 'A08:2021 - Software and Data Integrity Failures',
  A9: 'A09:2021 - Security Logging and Monitoring Failures',
  A10: 'A10:2021 - Server-Side Request Forgery',
};

export default {
  SCAN_STATUS,
  SEVERITY_LEVELS,
  SCAN_TYPES,
  AI_PROVIDERS,
  OWASP_CATEGORIES,
};