# Author IDs for lab members

Source: OpenAlex API (authors and works endpoints), the public ORCID registry, and UvA profile pages. Checked on 2026-09-19.

An OpenAlex ID was accepted only with positive evidence: University of Amsterdam (UvA) among the profile's affiliations, a work already listed in `data/publications/`, or a unique name plus a matching earlier affiliation.

## Accepted

| Member | ORCID | OpenAlex IDs | Evidence |
|---|---|---|---|
| Angelo Tomaselli | 0000-0003-1796-7413 | A5014654199 | UvA and University of Bologna affiliations; topics in venture capital and corporate finance. |
| Jonathan Sitruk | none found | A5016125049 | UvA affiliation (2025), SKEMA earlier; topics in crowdfunding and venture capital. Profile has no ORCID and the UvA page lists none. |
| Kevin Curran | 0000-0001-6500-9864 | A5076260611 | UvA affiliation; topics in management and organization studies. |
| Lien De Cuyper | 0000-0002-5743-8105 | A5052412155, A5100280802, A5042879541 | Main profile: UvA, ETH Zurich, Imperial. A5100280802: one work, "On Startups and Joiners" (2024), co-authored with Yuval Engel. A5042879541: two works with ETH Zurich affiliation, which matches the main profile. |
| Martin Obschonka | 0000-0002-0853-7166 | A5021701198, A5140758739, A5143523524 | Main profile: UvA (2026), QUT, Jena; 199 works in entrepreneurship psychology. The two split profiles each hold one 2026 work with UvA affiliation. |
| Onajomo Akemu | 0000-0002-7375-0297 | A5082470127 | OpenAlex shows Erasmus University Rotterdam and Nazarbayev University, not UvA. The linked ORCID record lists UvA employment since 2022 and Nazarbayev before that. Works are on social enterprise (Fairphone case). Unique name. |
| Sumeet Malik | 0000-0003-0622-7807 | A5054991620 | UvA, IE University and Virginia Tech affiliations; topics in entrepreneurship and governance. |
| Taehyun Lee | 0000-0001-7684-1058 | A5101723934 | UvA and Yonsei affiliations; ORCID record lists UvA employment; works include the "sharing economy" category papers (UvA, 2024) and "Institutionalizing Place" (2019). See the warning below. |
| Vilma Chila | 0000-0002-8316-3918 | A5007261133 | UvA and Tilburg affiliations; entrepreneurship topics. |
| Yuval Engel | 0000-0001-5383-922X | A5069769106 | UvA, VU Amsterdam and Haifa affiliations; entrepreneurship topics. |

## Warning: Taehyun Lee's profile is contaminated

A5101723934 belongs to the lab member, but OpenAlex has merged a namesake into it. About 20 of its 29 works are World Bank reports (Mongolia, China, Afghanistan economic updates), plus a Korean policing paper and a 2026 Korean law paper. Any automatic import of works from this ID must be filtered by hand. The lab director should confirm that the ORCID is his.

## No verified ID (files left unchanged)

| Member | Result |
|---|---|
| Jorge Sandoval | 235 namesakes; none with UvA affiliation or management topics. |
| Natalie Jones | 152 namesakes; see rejected ID below. |
| Ridam Dhawan | No OpenAlex author profile. |
| Yang Mei | 2186 name matches; none with UvA affiliation in management. UvA page lists no ORCID. |

## Rejected look-alike IDs

| Name searched | ID | Reason |
|---|---|---|
| Angelo Tomaselli | A5035359881 | "Angelo Rodolfo Tomaselli", one 1989 Italian statistics paper. |
| Kevin Curran | A5002868461 | Ulster University computer scientist (networking, localization). |
| Kevin Curran | A5055001531, A5101152425, A5113036894 | Memorial Sloan Kettering oncologist. |
| Kevin Curran | A5075379579 | Media studies, University of Oklahoma. |
| Sumeet Malik | A5019004487 | Chemistry (photocatalysis, adsorption). |
| Sumeet Malik | A5060066593, A5065908941, A5140412974 | No affiliation and unrelated topics; no evidence. |
| Taehyun Lee | A5047678891, A5101723937, A5101723935, A5066633811, A5101723936 | Engineering, telecommunications and photonics researchers in Korea. |
| Taehyun Lee | A5001222511 | Finance, London School of Business and Finance; no link to UvA or Yonsei. |
| Natalie Jones | A5074006933 | "Natalie P Jones", UvA affiliation but a single 2020 journalism study (communication science). No link to entrepreneurship. |
| Natalie Jones | A5071642618, A5102958517, A5087461549 and others | Environmental science, forensic psychology, occupational therapy, medicine. |
| Yang Mei | A5102898539 | "Jingmei Yang", dentistry (ACTA Amsterdam). |
| Yang Mei | A5100438299 and other "Mei Yang" profiles | Chemistry, materials, physics, medicine. |
| Jorge Sandoval | A5023885241, A5102855769, A5101910233, A5101910232, A5101910235, A5044966518 | Petroleum engineering, cardiology, hydrology, agronomy, visual research methods. |
