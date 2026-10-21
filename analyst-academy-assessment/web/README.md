# Assessment Blueprint — website

A static site generated from `../BLUEPRINT.md` and `../case-engine/SPEC.md`.
No framework, no runtime dependencies, no build step required at deploy time —
`public/` is committed, so Vercel just serves it.

## Deploying to Vercel

The generated output is already committed, so **no build step is needed.**

### Option A — Vercel dashboard (easiest)

1. <https://vercel.com/new> → import `ecdeng/ai-newsletter`.
2. Set **Root Directory** to `analyst-academy-assessment/web`.
3. Framework Preset: **Other**. Leave Build Command empty.
   Output Directory: `public`.
4. Deploy.

### Option B — CLI

```bash
cd analyst-academy-assessment/web
npx vercel --prod
```

When prompted, accept the defaults; `vercel.json` already sets `cleanUrls`,
caching for `/static/*`, and a couple of sane security headers.

## Publishing to here.now

`publish_herenow.py` calls the here.now public API directly (create → upload →
finalize); it needs no installer and no bundled scripts.

```bash
cd analyst-academy-assessment/web
python3 publish_herenow.py                 # anonymous site, EXPIRES IN 24 HOURS
HERENOW_API_KEY=... python3 publish_herenow.py          # permanent
HERENOW_API_KEY=... python3 publish_herenow.py --slug my-slug   # update in place
```

Two things worth knowing, both learned the hard way:

- **Without an API key the Site is anonymous and expires after 24 hours.** The
  create response says so in `publishStatus.persistence` / `expiresAt`. Set
  `HERENOW_API_KEY` for a permanent Site.
- **Uploads go straight to `*.r2.cloudflarestorage.com`, not to here.now.** In a
  sandbox or behind an egress allowlist, both hosts must be allowed, or the
  create call succeeds, every upload fails, and finalize reports missing files.

`index.html` must sit at the root of the published directory, which is why the
script publishes `public/` rather than the repo folder above it.

## Regenerating after editing the markdown

The site is generated, so edit the markdown — never the HTML.

```bash
cd analyst-academy-assessment/web
python3 -m pip install -r requirements.txt
python3 build.py      # writes ./public
python3 check.py      # validates links, anchors and leaked markdown
```

`build.py` asserts the expected shape of the source (15 modules, 58 exercises,
7 infrastructure items, 7 parts) and fails loudly if a markdown edit breaks it,
rather than silently dropping content.

`check.py` walks every generated page and verifies there is no leaked markdown
in visible prose, that all internal links and `#anchors` resolve, and that no
page is suspiciously short. Both should pass before you deploy.

## Information architecture

| Page | What it is for |
|---|---|
| `index.html` | Landing. The argument, the headline numbers, the five highest-value exercises, the simulator recommendation. |
| `approach.html` | The evidence base — read before the module detail. |
| `modules.html` + `modules/m01…m15` | Per-module content coverage and full exercise detail. Worked answers are collapsed by default so the page scans. |
| `exercises.html` | **All 58 exercises, filterable** by module, difficulty, build complexity and grading method. Filter state is reflected in the URL, so a filtered view is shareable. |
| `intensives.html` | The nine guest intensives, flagged as the lowest-confidence material. |
| `infrastructure.html` | INF-1…INF-7 plus what *not* to build. |
| `case-engine.html` | The case engine technical spec and five worked example cases. |
| `roadmap.html` | Phased build plan. |
| `provenance.html` | Research constraints, depth by module, corrections. |
| `verification.html` | What to check before it reaches a student. |
| `sources.html` | Sources by topic. |

## QA

`shoot.js` (Playwright) screenshots key pages at desktop and mobile widths, in
light and dark, asserts there are no console errors and no horizontal overflow,
and exercises the catalogue filter end to end. It is a local QA tool, not part
of the build:

```bash
cd public && python3 -m http.server 8077 &
cd .. && node shoot.js
```
