# Architecture

The website is a static site. All content lives in data files in this repository. A weekly routine proposes new content as pull requests. A person approves by merging.

```
Sources                    Weekly routine (Claude)            GitHub                         Live site
OpenAlex, Crossref         pipeline/*.py fetch and compare    claude/auto-* PR -> gate -> merge
abs.uva.nl profiles        Claude judges relevance,           claude/cand-* PRs -> person merges or closes
UvA news, press search     writes data files                  digest issue                   Deploy workflow
GitHub issues (suggestions)                                                                  -> GitHub Pages
```

## Parts

| Part | Where | Job |
| --- | --- | --- |
| Site | `src/`, Astro | Turns data files into pages |
| Schemas | `src/content.config.ts` | Rejects malformed data at build time |
| Pages | `src/pages/` | Home (with the motion intro), Team, Publications, Activities, Network, News |
| Data | `data/` | One file per member, publication, news item, event, project, activity, and network organisation |
| Fetch scripts | `pipeline/` | Deterministic collection from sources. No judgement |
| Routine prompt | `ROUTINE_PROMPT.md` | The weekly job: judge, write files, open pull requests, write the digest |
| Workflows | `.github/workflows/` | Build, deploy, auto-merge gate, record rejections, heartbeat, link check |

## Rules that keep it safe

1. The routine never pushes to `main` and never merges. Only workflows and people merge.
2. New publications, news, events, and member changes always need a person. Not every member paper belongs to the lab.
3. Only two things merge without review: metadata completion on already approved publications, and additions to `data/rejected.yaml` (papers the routine set aside as irrelevant, reported once in the digest). `pipeline/check_auto_diff.py` enforces this field by field.
4. News items must pass `pipeline/verify_url.py`: the page exists and names the lab or a member. Titles and dates come from the page.
5. A failed fetch never changes data.
6. A closed candidate is recorded in `data/rejected.yaml` and is not proposed again.
7. The repository is public and holds only public information: names, titles, publications, links, and photos that were already on the website. The one secret, the OpenAlex API key, lives in the cloud environment and never in the repository.
8. Anyone may open a suggestion issue. The routine acts only on issues from organization members and lists the rest in the digest.

## State

There is no database. State is: the data files, `data/rejected.yaml`, and the open pull requests.
