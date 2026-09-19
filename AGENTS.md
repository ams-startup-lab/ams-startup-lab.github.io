## Development

When starting the dev server, use background mode:

```
astro dev --background
```

Manage the background server with `astro dev stop`, `astro dev status`, and `astro dev logs`.

## Documentation

Full documentation: https://docs.astro.build

Consult these guides before working on related tasks:

- [Adding pages, dynamic routes, or middleware](https://docs.astro.build/en/guides/routing/)
- [Working with Astro components](https://docs.astro.build/en/basics/astro-components/)
- [Using React, Vue, Svelte, or other framework components](https://docs.astro.build/en/guides/framework-components/)
- [Adding or managing content](https://docs.astro.build/en/guides/content-collections/)
- [Adding styles or using Tailwind](https://docs.astro.build/en/guides/styling/)
- [Supporting multiple languages](https://docs.astro.build/en/guides/internationalization/)

## Project rules

- Content lives in `data/`, one file per item, checked by `src/content.config.ts`. Run `npm run build` after any data change.
- The weekly routine follows `ROUTINE_PROMPT.md`: never push to `main`, never merge, never invent content.
- Read `docs/ARCHITECTURE.md` before changing workflows or `pipeline/check_auto_diff.py`. They are the safety layer.
- The repository is public. No email addresses, secrets, or private notes.
