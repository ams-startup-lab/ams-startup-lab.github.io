// @ts-check
import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://www.ams-startup-lab.org',
  // Addresses used by the old Wix site keep working.
  redirects: {
    '/projects-1': '/projects',
    '/news-media': '/news',
    '/events-1': '/events',
  },
});
