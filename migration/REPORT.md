# Migration report: ams-startup-lab.org (Wix) to data files

Source: server-rendered HTML fetched with curl on 2026-09-19. All text and links were copied by script from the HTML.

## Counts

| Collection | Files |
|---|---|
| members | 14 (10 faculty, 4 phd) |
| publications | 19 (8 in 2025, 7 in 2024, 4 in 2023) |
| news | 7 |
| projects | 3 |
| events | 0 (page says "No events at the moment") |

The brief expected 16 publications. The live page lists 19.

## Members

- Site order: Engel, Obschonka, Curran, De Cuyper, Lee, Akemu, Malik, Sitruk, Chila, Tomaselli, Mei, Dhawan, Jones, Sandoval.
- Only Yuval Engel has a lab role printed ("Lab Director").
- No uva_url in the supplied mapping for: Onajomo Akemu, Ridam Dhawan, Natalie Jones, Jorge Sandoval. The projects page links Sandoval to https://www.uva.nl/en/profile/s/a/j.i.sandoval-sandoval/j.i.sandoval-sandoval.html (not added to his member file).
- No Google Scholar link on the page for: Yang Mei, Ridam Dhawan, Natalie Jones (icon shown, no href).
- Jorge Sandoval: the Google Scholar icon links to his LinkedIn URL (https://www.linkedin.com/in/jiso/). scholar_url omitted.
- Martin Obschonka: the LinkedIn href is a LinkedIn search-results URL, not a profile URL. Copied as is. Needs a real profile URL.
- Lien De Cuyper: the Scholar href is a Google Scholar author search URL, not a profile. Copied as is.
- The team page HTML repeats a hidden "Ridam Dhawan / PhD Candidate" block after every member (Wix hover template). Ignored.
- Photo URLs: migration/photo-urls.txt (slug, tab, wixstatic URL). Photos not downloaded.

## Publications

- Titles are the printed headings, including trailing periods where printed.
- No DOI visible in the href (ScienceDirect PII links): 2025-sitruk-emotional-brightness-and, 2025-chila-time-to-say.
- DOIs taken from non-doi.org hrefs (Springer, SAGE, OUP): ".pdf" suffix and the OUP article id "/8202956" were stripped.
- 2025-obschonka-artificial-intelligence-and: the href carries a personal `casa_token` query string. Copied exactly; should be replaced with the clean DOI link.
- 2024-chila-from-loss-to: printed as "Strategic Organization, 0(0)". Placeholder volume/issue omitted.
- Article numbers are stored in `pages` as printed ("105094", "106482", "Article 106382", "Article 102917", "Article 106272", "dtaf024"). Small Business Economics items have "1-24" style page ranges as printed.
- Printed "Advance online publication" (status left as published because the page does not say in press/forthcoming): 2024-curran-sharing-the-spotlight, 2023-obschonka-job-burnout-and, 2023-becker-network-to-passion, 2023-bergmann-what-drives-solo.
- Every publication has at least one team-page member among its authors.
- "Lee, E." in 2024-curran-sharing-the-spotlight is not Taehyun Lee. Not tagged.
- No publications on the page for: Lee, Akemu, Malik, Mei, Dhawan, Jones, Sandoval.
- The home page prints the 2024 JBV title as "firm-specific incentives"; the publications page prints "firm specific incentives". The publications page version was used.
- The 2024 JBV entry has a second "Read more" label with no link.

## News

- Dates printed as "March 2 - 2025" etc. Converted to ISO.
- Outlet derived from link domain: LinkedIn, The Next Web (thenextweb.com), The Conversation, Forbes. For eiexchange.com no outlet name is printed, so the domain is used as outlet.
- `summary` holds the printed teaser. For six items this is "Related to the publication ..."; the related-publication hrefs are not stored:
  - 2024-09-19: https://doi.org/10.1002/sej.1502
  - 2024-04-26 and 2024-02-19: https://journals.sagepub.com/doi/10.1177/10422587231178865
  - 2023-03-08, 2023-02-21, 2023-01-23: https://journals.aom.org/doi/abs/10.5465/amj.2021.1197
- The 2024-02-19 title is printed with a closing quote but no opening quote ("Benevolent sexism’ in startups..."). Copied as printed.
- `members` set only where the title names a member (one item). The other items concern Engel and De Cuyper papers but do not name them.

## Projects

- In the HTML, the title "Combating Masculine Defaults in the STEM sector" comes second, but its body text comes third (after the Sandoval project text). Order used: Psychology (10), Masculine Defaults (20), Socio-cognitive (30). Check against the visual layout.
- `url` is the "Read More" href of each project. `status` is active (page heading: "What we are currently busy with").
- `partners` filled only for the Masculine Defaults project (the printed collaboration list). The funder (Ministry of Social Affairs and Employment) is in the body only.
- The Sandoval text contains "the the" as printed. Kept.
- `summary` is the first sentence of the body.

## Site

- No social links in header or footer. Header has the UvA Amsterdam Business School logo only.
- Footer: "© 2024 - Amsterdam Startup Lab".
- The address is printed across two lines; joined with a space.
- The home page has a contact form (Submit / "Thanks for submitting!"). Field labels are not in the server HTML; not migrated.
- The nav item "Contact" links to the home page (anchor).

## Old URLs

- https://www.ams-startup-lab.org/
- https://www.ams-startup-lab.org/team
- https://www.ams-startup-lab.org/publications
- https://www.ams-startup-lab.org/projects-1
- https://www.ams-startup-lab.org/news-media
- https://www.ams-startup-lab.org/events-1
