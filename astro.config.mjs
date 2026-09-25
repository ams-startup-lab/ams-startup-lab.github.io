// @ts-check
import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://www.ams-startup-lab.org',
  // Addresses used by the old Wix site, and the former Projects and Events pages
  // (now part of Activities), keep working.
  redirects: {
    '/projects-1': '/activities',
    '/news-media': '/news',
    '/events-1': '/activities',
    '/projects': '/activities',
    '/events': '/activities',
  },
});
