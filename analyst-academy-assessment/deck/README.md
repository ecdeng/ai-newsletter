# Deck — The Historical Case Engine

21 slides describing INF-1 and walking through three worked cases a student
can complete end to end. Built with `pptxgenjs`.

```bash
npm install pptxgenjs
NODE_PATH="$PWD/node_modules" node build.js      # writes historical-case-engine.pptx
```

`NODE_PATH` is required: the theme helper resolves `jszip` through pptxgenjs,
and without it `applyTheme` throws and the deck keeps Office's stock palette.

## Getting it into Google Slides

Drive converts a `.pptx` to native Google Slides on upload:

1. Drag `historical-case-engine.pptx` into Google Drive.
2. Right-click it → **Open with → Google Slides**.
3. **File → Save as Google Slides** to keep the converted copy.

(Or in an existing deck: **File → Import slides**.)

This repo does not upload it for you, because the Drive connector takes file
bytes inline and a `.pptx` of this size has to be base64-encoded into the call.
If the **Google Slides** connector is enabled in the chat, the deck can instead
be built natively in Drive with no import step and no conversion artefacts.

## Structure

| Slides | Content |
|---|---|
| 1–5 | The grading problem, why not a market simulator, the core idea, the clock |
| 6–10 | Architecture, the point-in-time leak (real Envista figures), the four leaks, the validator, data sourcing |
| 11 | Divider |
| 12–15 | **Case A** — pack, task, the arithmetic, grading, good vs. bad answer |
| 16–17 | **Case B** — two-phase task, the reverse-DCF frontier, good vs. bad |
| 18–19 | **Case C** — the restatement case, good vs. bad |
| 20–21 | What the engine refuses to do; build plan and open questions |

Every figure traces to the verified arithmetic in `../verification/` or to the
live SEC data in `../case-engine/`.

## QA performed

- `validate.py` — all validations passed
- `markitdown` — 21 slides, no placeholder text
- LibreOffice render inspected at 110 dpi; one alignment defect found and fixed
  (short quotes were vertically centring, so the two response columns did not
  line up)
