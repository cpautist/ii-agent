import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: __dirname,
  use: {
    baseURL: process.env.FRONTEND_BASE_URL || 'http://localhost:3000',
    headless: true,
  },
});
