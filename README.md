# Amsterdam Startup Lab website

Source of https://www.ams-startup-lab.org. Repository: https://github.com/ams-startup-lab/ams-startup-lab.github.io. A static site (Astro) whose content lives in `data/`. A weekly Claude routine proposes new publications, news, and events as pull requests. A person approves by merging and rejects by closing.

- How it works: `docs/ARCHITECTURE.md`
- Day-to-day tasks: `docs/RUNBOOK.md`
- Taking over the system: `docs/HANDOVER.md`
- The weekly job: `ROUTINE_PROMPT.md`
- Record of the move from Wix: `migration/`

## Quick start
```
npm ci
npm run dev                      # site at http://localhost:4321
pip install -r pipeline/requirements.txt
python pipeline/fetch_openalex.py   # writes pipeline/out/
```
Requires Node 22 or newer and Python 3.10 or newer.
