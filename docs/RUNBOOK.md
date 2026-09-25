# Runbook

## Weekly: approve or reject
1. Open the newest issue labelled `digest`. It links this week's pull requests.
2. For each pull request: **Merge** to publish, **Close** to reject. Both work in the GitHub mobile app.
3. The site updates a few minutes after a merge.

## Edit something by hand
Edit the file under `data/` on github.com (pencil icon) and commit. If the file breaks a schema the build fails, and the live site stays as it was. The error names the file and field.

## Add a publication, news item, or event by hand
Copy an existing file in the matching `data/` folder, rename it, edit the values, commit.

## Add a member
Create `data/members/<first-last>.yaml` from an existing file. Add `orcid` and `openalex_ids` so their papers are found. Set `joined` so older papers are not proposed.

## A member moves to another institution but stays with the lab
Set `group: affiliate` in their file, add `affiliation` (the institution) and `affiliation_url` (their profile there), and remove `uva_url`. They appear under "Affiliated researchers" and their papers are still proposed. Example: `data/members/lien-de-cuyper.yaml`.

## A member leaves the lab
Set `left: YYYY-MM-DD` in their file. They move to alumni and their new papers are no longer proposed.

## Add an organisation to the Network page

The Network page (called Partners until September 2026; the data still lives in `data/partners/`) is a logo wall of organisations the lab has worked with, past or present. Ongoing collaborations belong under Activities, as research projects. Partners are never added by the routine. A member tells the director, who adds the partner by hand or opens a suggestion issue.

1. Ask the member to confirm with the partner that the lab may name it on the website. For a logo, ask separately.
2. Add `data/partners/<slug>.yaml` with `name`, `url`, `members` (member slugs), `group: uva` for UvA centres and labs (shown under "Our friends at the UvA"), and `confirmed` (the date of the member's confirmation).
3. For a logo, put a PNG with a transparent background in `public/partners/` and add `logo: /partners/<file>` and `logo_permission: <date>`. The build fails if a logo has no permission date.

The Network menu item appears once the first organisation exists.

## Add an activity

The Activities page lists what the lab does besides papers: research projects (`data/projects/`), upcoming events (`data/events/`), and teaching, academic service and talks (`data/activities/`). Activities are never added by the routine. A member sends the item to the director, who adds it by hand.

1. Add `data/activities/<slug>.yaml` with `title`, `kind` (`teaching`, `service` or `talk`), `year`, `summary` (one or two sentences), `members` (member slugs), and optionally `url` and `until` (a later year, or `present`).
2. Only public information. If the item names a company or client, the member first checks that they agree, as for partners.

A group with no items is hidden on the live site.

## Undo a change
Open the merged pull request and press **Revert**, then merge the revert.

## Propose a rejected item after all
Delete its line from `data/rejected.yaml`.

## The routine stopped
An issue "Weekly update routine has not run for 10 days" appears. Open claude.ai/code, then Routines. Check that the routine is enabled and that GitHub access is still authorised. Run it once by hand. If the routine is gone, recreate it from `ROUTINE_PROMPT.md` (see HANDOVER).

## Build locally
`npm ci`, then `npm run dev`. Pipeline: `pip install -r pipeline/requirements.txt`, then `python pipeline/fetch_openalex.py`.

## Member photos
Photos live in `public/team/<slug>.jpg` (320 by 320 pixels) and are linked with `photo: /team/<slug>.jpg` in the member file. Members supplied their own photos for the website. For a new member, ask them for a photo. A member without a photo gets an initials tile. The routine never adds photos.

## The site is down
1. Check https://github.com/ams-startup-lab/ams-startup-lab.github.io/actions — a red Deploy run means a bad commit. Revert it.
2. Check the domain has not expired at Wix (Settings, Premium Subscriptions, the Domain line).
3. Check DNS still points to GitHub: the apex has the four `185.199.*.153` A records, and `www` is a CNAME to `ams-startup-lab.github.io`.
4. Check Settings, Pages in the repository still shows the custom domain `www.ams-startup-lab.org` with HTTPS enforced.
