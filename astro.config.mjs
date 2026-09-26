// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://www.ams-startup-lab.org',
  trailingSlash: 'always',
  integrations: [sitemap()],
});
