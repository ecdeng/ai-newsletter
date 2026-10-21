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
