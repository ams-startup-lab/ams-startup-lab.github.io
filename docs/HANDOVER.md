# Handover

Everything needed to run this website is in this repository, except three accounts. To take over, get access to each.

| What | Where | How to transfer |
| --- | --- | --- |
| Code, data, workflows | GitHub organization (see README for the name) | Current owner adds you as organization **Owner** |
| Domain `ams-startup-lab.org` | Registrar account (Wix at the time of writing) | Transfer the domain to your registrar account, or receive the login |
| Weekly routine | The current maintainer's Claude account, claude.ai/code, Routines | Routines cannot be transferred. Create a new one in your account (below), then the old owner deletes theirs |

Keep at least two organization owners at all times.

## Recreate the routine
1. claude.ai/code, Routines, New routine.
2. Repository: this repository. Schedule: weekly.
3. Prompt: everything below the line in `ROUTINE_PROMPT.md`.
4. Environment network access: custom allowlist with `api.openalex.org`, `api.crossref.org`, `pub.orcid.org`, `abs.uva.nl`, `www.uva.nl`, `registry.npmjs.org`, `pypi.org`, `files.pythonhosted.org`, and general web access for press search if the plan allows it.
5. Run once by hand. Check that a `digest` issue appears.

## Without Claude routines
The same prompt and scripts can run from a scheduled GitHub Actions workflow using `anthropics/claude-code-action` and an API key stored as a repository secret. Nothing else changes.

## Repository settings to check after any transfer
- Settings, Pages: source "GitHub Actions", custom domain `www.ams-startup-lab.org`, HTTPS enforced.
- Settings, Actions, General: workflow permissions "Read and write", and "Allow GitHub Actions to create and approve pull requests" on.
- Labels exist: `auto`, `digest`, `suggestion`, `routine-alert`, `links`.
- Branch protection on `main`, if used, must still let the `github-actions` bot push `data/rejected.yaml` and merge `auto` pull requests.

## DNS records (GitHub Pages)
- Apex `A`: 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153
- `www` `CNAME`: `<organization>.github.io`
- File `public/CNAME` holds `www.ams-startup-lab.org`.

## Costs
GitHub Pages and Actions: free for public repositories. Domain: yearly fee at the registrar. Claude subscription of the maintainer for the routine.
