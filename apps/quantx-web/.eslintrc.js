module.exports = {
  root: true,
  extends: [
    'next',
    'next/core-web-vitals',
    'eslint:recommended',
  ],
  parserOptions: {
    ecmaVersion: 2022,
    sourceType: 'module',
  },
  rules: {
    'flag-naming': [
      'error',
      {
        pattern: '^[a-z]+\\.[a-z]+\\.[a-z]+$',
        message: 'Flag keys must follow {domain}.{feature}.{variant} pattern',
      },
    ],
    'cache-keys': [
      'error',
      {
        message: 'Cache keys must follow namespaced format: ["domain", "resource", variant]',
      },
    ],
    'no-sensitive-data-logging': [
      'error',
      {
        message: 'Do not log PII or sensitive data in client code',
      },
    ],
    'react/jsx-no-duplicate-key': 'error',
    'react/jsx-key': 'error',
  },
  overrides: [
    {
      files: ['**/tests/**/*.ts', '**/tests/**/*.tsx'],
      rules: {
        '@typescript-eslint/no-explicit-any': 'off',
      },
    },
  ],
};