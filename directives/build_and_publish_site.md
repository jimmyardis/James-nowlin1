# Directive: build and publish the James Nowlin real estate site

## Goal
A fast, static, search- and AI-answer-optimized site for James Nowlin (Realty ONE Group Reside,
SC license #129577), hosted on GitHub Pages from `docs/`.

## Inputs
- `src/content.py` — every word on the site, plus agent facts and area data. Edit here only.
- `src/photos/` — area photos (Wikimedia Commons) + `credits.json` + `headshot.png`.
- `src/assets/` — `style.css`, `site.js`, self-hosted web fonts.

## Tools (execution/)
| Script | Does |
|---|---|
| `build_site.py` | Renders all pages, images, schema, `sitemap.xml`, `robots.txt`, `llms.txt` into `docs/` |
| `screenshot.py [paths]` | Serves `docs/` locally, screenshots desktop (1366) + mobile (390), flags overflow and console errors |
| `commons_search.py "<query>"` | Lists free-licensed Commons photos (title, size, license, artist) |
| `commons_download.py picks.json outdir` | Downloads chosen photos at 1280px and records credits; resumable |
| `check_links.py` | Verifies every resources-page URL (status, redirects, non-HTML targets). Run before each publish |

## Steps
1. Edit `src/content.py`.
2. `python3 execution/build_site.py`
3. `python3 execution/screenshot.py` and look at `.tmp/shots/`. Fix anything that overflows or collides.
4. Commit and push `main`. Pages serves `/docs` automatically in about a minute.

## Custom domain (when James buys one)
`SITE_URL=https://example.com BASE_PATH= python3 execution/build_site.py` writes `docs/CNAME` and
absolute canonicals; then set the domain in the repo's Pages settings and add DNS
(A records to GitHub Pages IPs or a CNAME to `jimmyardis.github.io`).

## Rules that must hold
- **SC advertising (S.C. Code 40-57-135(E))**: brokerage name with a link to its homepage on every page
  (footer). Never show another brokerage's listing (photo, address, remarks) without written permission.
- **Fair Housing**: describe places and homes, never who should live there. No "family-friendly",
  "safe", "exclusive". Naming the school district is factual and OK; ranking schools is not.
- **No invented proof**: no fake reviews, sales counts or market stats. Add real ones only.
- **Photo licenses**: every CC BY / BY-SA photo shows its credit line and is listed on /photo-credits/.
  The build skips any photo with no credit entry.
- Listings and lead capture stay in James's Realty ONE Group tools (search, home value, ONE app),
  which keeps IDX rules satisfied and leads in his CRM.

## Resources page (/resources/)
Data lives in `src/resources.py`: the ordered new-resident checklist plus grouped official links, each
tagged by county for the on-page filter. Run `check_links.py` before publishing; update a URL to its
final redirect target when one is reported. Only link providers whose official domain is confirmed;
when unsure, link the county's own utility-provider list instead.

## Learned (edge cases)
- Guessed domains are often wrong (JMWSC is lcjmwsc.com, Lexington Two is lex2.org). Confirm every
  domain from a search result or the county's own nav; never publish a guessed URL.
- richlandcountysc.gov (and a few others) return 403 to scripts; confirm those by search, then list
  them in `resources.VERIFIED_MANUALLY`. One city "utilities" URL 200'd but redirected to a JPG, so
  the checker now fails non-HTML targets.
- SC sequence for new residents: county vehicle tax -> DMV registration (45 days) -> SC license
  (90 days) -> 4% legal residence application, which requires the SC license and registration.
- Wikimedia Commons rate-limits hard (HTTP 429, Retry-After up to 600s). Request only standard thumb
  widths (1280); non-standard widths (1600) triggered the long waits. Batch metadata in one API call.
- The downloader must fetch bytes before creating the file; otherwise an interrupted run leaves a
  0-byte file that a resume skips. It also backfills missing credits for files already on disk.
- Google's raw GitHub font files are blocked here (403); Google Fonts CSS + fonts.gstatic.com works.
  An old user agent gets TTF (for Pillow); a modern one gets WOFF2 (for the web).
- Map labels are sized in SVG units, so they shrink with the map. On phones and in the sidebar the CSS
  bumps them to 34–36px; label offsets for each pin live in `content.py` (`label_dx`, `label_dy`, `label_anchor`).
