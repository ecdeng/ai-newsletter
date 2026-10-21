# INF-1 — The Historical Case Engine
## Technical specification

**Companion to:** `../BLUEPRINT.md` (which specifies the exercises this engine serves and the assessment architecture it sits inside)
**Status:** point-in-time data layer **prototyped and tested against live SEC data**; 13/13 smoke tests passing as of 21 October 2026. Everything else in this document is specified but unbuilt.
**Code in this directory:** `pit/client.py`, `pit/comps.py`, `pit/case.py`, `test_pit.py`

---

## 1. What this is, and the one idea behind it

A replay harness. You freeze a date **T** for a real company, serve the student *only* what was knowable at T, make them produce a thesis and a position, advance the clock, and reveal what happened.

**The value is not realism. It is time compression plus free ground truth.** A three-year holding period becomes a 40-minute exercise in which the correct answer already exists and costs nothing to obtain. That is why this beats a market simulator for a fundamental-analysis curriculum: a simulator's distinguishing feature is live price feedback, and price feedback is the *least* valid assessment signal available in a low-validity domain (see `../BLUEPRINT.md` §2.1).

A second, less obvious benefit: because every student in a cohort gets the **identical stimulus**, their scores are comparable. That is the property that makes an OSCE work, and it is why a *fixed* library of 20–40 cases is better assessment than a dynamic any-company-any-date engine — which would also cost far more and require data licences you probably cannot get.

**Scope boundary.** This engine serves *fundamental* cases on a quarters clock. It is not a trading simulator, it does not model execution or market impact, and it should never score a student on P&L.

---

## 2. Architecture

```
                    ┌──────────────────────────────────────────┐
                    │  SOURCES                                 │
                    │  SEC XBRL (free, PIT by construction)    │
                    │  price/options vendor (paid)             │
                    │  transcripts (IR sites / vendor)         │
                    │  consensus (hand-curated — see §3.4)     │
                    └───────────────────┬──────────────────────┘
                                        │
                    ┌───────────────────▼──────────────────────┐
         LAYER 1    │  pit/client.py    as-of filtering        │  BUILT + TESTED
         data       │  pit/comps.py     PIT comp sets          │
                    │  on-disk cache → reproducible builds     │
                    └───────────────────┬──────────────────────┘
                                        │
                    ┌───────────────────▼──────────────────────┐
         LAYER 2    │  pit/case.py      CaseManifest           │  BUILT + TESTED
         authoring  │  validate_pit_safety()  ← the guardrail  │
                    │  facts_from_sec()       ← leak-proof     │
                    └───────────────────┬──────────────────────┘
                                        │
                    ┌───────────────────▼──────────────────────┐
         LAYER 3    │  clock: step → reveal payload            │  SPECIFIED
         runtime    │  submission store (append-only, locked)  │
                    │  student_view() strips key + resolutions │
                    └───────────────────┬──────────────────────┘
                                        │
                    ┌───────────────────▼──────────────────────┐
         LAYER 4    │  deterministic graders (cells, traps)    │  SPECIFIED
         grading    │  model auto-grader  → INF-2              │  (INF-2 separate)
                    │  LLM rubric grader  → INF-6 golden set   │
                    │  calibration scorer → INF-4              │
                    └──────────────────────────────────────────┘
```

**Design decisions worth defending:**

- **Manifests are JSON on disk, not rows in a database.** Cases are reviewable, diffable, and survive a platform rewrite. A case is editorial content with an answer key; it should be in version control.
- **The cache is part of the contract, not an optimisation.** A case built today must rebuild identically in two years. Cache every API response and commit the cache alongside the manifest, or a later SEC restatement silently changes your case.
- **`student_view()` is a method on the manifest, not a separate file.** One object, one source of truth, and the stripping logic is testable. Maintaining parallel "student" and "instructor" copies of a case is how answer keys leak.
- **Append-only submission store with hard locks.** Several exercises (M03-E4's two-phase design, M13-E1's pre-commitment, M14-E2's re-underwrite) are *only* valid if the earlier submission cannot be revised. The lock is the instrument.

---

## 3. Data sourcing

### 3.1 What is free, verified reachable, and sufficient

**SEC XBRL via `data.sec.gov` is the backbone and it is genuinely excellent for this purpose.** Verified working from a sandboxed container on 21 Oct 2026.

| Endpoint | What it gives | Verified |
|---|---|---|
| `/api/xbrl/companyconcept/CIK{cik}/us-gaap/{tag}.json` | every reported value of one concept, **each stamped with `filed` + `accn`** | ✅ 200 |
| `/api/xbrl/companyfacts/CIK{cik}.json` | all facts for one company (tens of MB for large filers) | ✅ |
| `/submissions/CIK{cik}.json` | full filing history with dates and accession numbers | ✅ 200 |
| `/api/xbrl/frames/us-gaap/{tag}/USD/CY2019Q4I.json` | one fact per entity for one period — **6,180 entities** on the Assets frame tested | ✅ 200 |

**Why this single-handedly solves the hardest problem:** every fact carries the filing date of the document it came from. So "what did the filings say on date T" is *always* reconstructible. No commercial point-in-time licence is needed for financials.

### 3.2 Two access gotchas, both found the hard way

**(a) The SEC requires an email-style User-Agent. A URL is not enough.** Tested directly:

| User-Agent | Result |
|---|---|
| `analyst-academy-case-engine (github.com/ecdeng/ai-newsletter)` | **HTTP 403** |
| `AnalystAcademy CaseEngine research@domain.test` | **HTTP 200** |

`pit/client.py` fails fast with a clear error rather than letting you debug a 403. Rate limit is 10 req/s; the client self-throttles to 8.

**(b) `www.sec.gov` and `data.sec.gov` are different hosts with different reachability.** In this container `data.sec.gov` returned 200 while `www.sec.gov` returned 403 at the egress proxy. The XBRL APIs live on `data.sec.gov`; **document retrieval (the actual 10-K HTML/PDF) lives on `www.sec.gov/Archives/`.** If your build environment can reach one but not the other, you can get all the *numbers* and none of the *documents* — which is survivable for the financial exhibits but not for the filing-reading exercises (M07-E1). Check both hosts before scoping.

### 3.3 What costs money

| Need | Options | Reality |
|---|---|---|
| **Prices with delistings** | Polygon.io (**$0 / $29 / $79 / $199** per month — publicly listed; note it rebranded to "Massive" in late 2025), Tiingo, EODHD | Cheapest real gap-filler. **Do not use free Yahoo-style feeds for a case library** — they carry survivorship bias, so your worst outcomes silently disappear. |
| **Historical index membership** | Norgate Data; CRSP via academic channels | **Norgate pricing could not be found** — treat as quote-based. Needed only if you build index-flow cases. |
| **Option chains (historical)** | vendor-specific, generally expensive | Needed for M10-E4 and M13-E1's implied-move work. **Consider hand-curating the straddle price for a fixed case library instead** — it is one number per case. |
| **Transcripts** | IR sites (free, patchy), AlphaSense/Tegus, Quartr | For a *fixed* library you need a few dozen. **Manual collection is entirely tractable** and legally cleanest. |
| **Point-in-time fundamentals** | Sharadar SF1, Compustat PIT | **Not needed — EDGAR covers it.** Note Sharadar no longer publishes pricing and its professional tier likely applies to a paid training product; the **licensing question matters more than the price.** |
| **Historical consensus** | I/B/E/S, Visible Alpha, FactSet | The one genuine gap. See §3.4. |

### 3.4 Historical consensus: the unsolved gap and the recommended workaround

There is no cheap, licensable source of historical sell-side consensus. Four options, in order of preference:

1. **Use management guidance as the bar instead of consensus.** Guidance is in the 8-K, the press release and the transcript — free, point-in-time, unambiguous. It is a *different* bar than consensus, but it supports most of what Modules 10 and 13 teach, and the guidance-versus-consensus gap can then be taught conceptually. **Start here.**
2. **Hand-curate a consensus table for the fixed library.** For 20–40 cases this is a few hundred data points, and historical consensus figures are quoted verbatim all over contemporaneous coverage and inside the transcripts themselves ("versus the Street's $1.42"). Labour-intensive, legally clean, sufficient. **This is the recommended path for a production library.**
3. **License I/B/E/S summary data** for a bounded ticker/date universe. Cleanest, expensive. Use the **unadjusted** files and apply your own split adjustments — the adjusted files suffer rounding corruption on high-split stocks.
4. **Reconstruct a proxy** from estimates mentioned in public coverage. Noisy; disclose it as a proxy in the manifest's `curated_consensus.source` field.

Whichever you choose, **record the provenance in the manifest.** A case whose bar is guidance and a case whose bar is consensus are testing subtly different skills, and the grader needs to know which.

---

## 4. Point-in-time discipline: four leaks and how each is closed

This is the section to get right. **Authoring a case by hand *will* leak future information, and the leak is silent.** Hence mechanical enforcement.

### Leak 1 — Restated financials *(closed, free, and demonstrable)*

Today's database shows restated history; the analyst at T saw as-first-reported numbers, often with a different segment structure.

**Real, tested example.** Envista Holdings (CIK 1757073), FY2019 revenue:

| Filed | Form | FY2019 revenue |
|---|---|---|
| 2020-02-21 | 10-K | **$2.7516bn** |
| 2021-02-19 | 10-K | $2.7516bn |
| 2022-02-24 | 10-K | **$2.2848bn** |

An analyst on 30 June 2021 saw **$2.7516bn**. A current database shows **$2.2848bn** — a **−$467m, −17.0%** difference (almost certainly a discontinued-operations reclassification). FY2020 shows the same pattern: $2.2820bn → $1.9291bn, **−15.5%**.

**A case built from current data would hand the student a revenue base the market never saw, and every growth rate, margin and multiple computed from it would be wrong.**

*Closed by:* `client.as_of()` / `client.latest_as_of()` filter on the `filed` field; `case.facts_from_sec()` builds manifests straight from the as-filed record so the filing date travels with the value; `comps.leak_report()` lets an author check, before shipping, whether a given case even *has* a restatement problem.

### Leak 2 — Index-membership survivorship

Today's index constituent list is not the list at T. Comp sets and any screening universe built on current membership are silently biased toward survivors.

*Closed by:* for a fixed library, **hard-code the comp set in the manifest** and source it from a contemporaneous document (the company's own proxy peer group, or the peer list in a contemporaneous sell-side note). Do not derive it from a current index. If you build index-flow cases, you need a historical-constituents dataset.

### Leak 3 — Delisting survivorship in prices

Cheap price APIs routinely omit dead tickers, so the worst outcomes vanish from your case set and your library quietly over-represents companies that made it.

*Closed by:* use a price vendor whose reference data includes delisted tickers, and **deliberately include failures in the library.** A case library with no zeros teaches that bear cases do not happen.

### Leak 4 — The author's own knowledge

The subtlest leak. An author who knows how the story ended writes a case whose exhibits quietly foreshadow it — including the wrong three key drivers in the expert key, or a trap that is only "obvious" in hindsight.

*Closed by:* process, not code. **Have the expert key written by a second person who is shown only the T-dated materials** and asked to produce the driver ranking cold. Where the two keys disagree, that disagreement is itself information about how answerable the case is — and if they disagree badly, the case is not gradeable.

### The validator

`case.validate_pit_safety()` checks four things and is **tested to catch all three mechanical leak classes**:

1. No served fact has `filed > T`.
2. **Every served fact actually exists in the SEC record with that value under that accession number.** This is the check that catches a value pasted from a current database — tested against the Envista restatement, and the error message names the failure mode explicitly.
3. No served filing is dated after T.
4. No calibration question resolves on or before T (which would make it already knowable).

```
TEST 10 — the validator catches the leak it exists to catch
  MISMATCH: Revenues 2019-12-31 manifest says 2,284,800,000 but accn
  0001628280-20-001914 reports 2,751,600,000. This is the signature of a value
  copied from a CURRENT database rather than from the as-filed document.
  LEAK: fact GrossProfit 2019-01-01..2019-12-31 was filed 2022-02-24, after
  the freeze date 2020-06-30.
  DEGENERATE: calibration question Q9 resolves 2020-01-01, on or before the
  freeze date 2020-06-30 — it is already knowable.
```

**Run the validator in CI on every manifest.** A leaked case is worse than no case, because it teaches students that the information was gettable.

### One thing the prototype corrected about the original plan

`../BLUEPRINT.md` described the `frames` endpoint as "excellent for building point-in-time cross-sectional comp sets." **Testing showed that overclaims it.** Frame rows carry `{cik, entityName, loc, end, val, accn}` and **no `filed` field**, so you cannot tell from the payload whether a value was filed before your cutoff, and the SEC has already chosen which filing to surface.

**Corrected guidance, now implemented in `pit/comps.py`: use `frames` for discovery and screening; use `companyconcept` for values.** A comp set is 8–15 names, so the per-name cost is trivial; resolving 6,000+ frame rows to filing dates would not be.

---

## 5. The case manifest

```python
CaseManifest(
    case_id, title, entity_name, cik,
    freeze_date,          # T — the single most important field
    reveal_steps,         # [{step, label, payload_ref, unlock_rule}, ...]
    served_facts,         # [ServedFact(tag, period, value, filed, accn, form)]
    served_filings,       # filing history as of T
    curated_consensus,    # {source, provenance, values} — see §3.4
    deliverables,         # [Deliverable(did, name, due_at_step, time_limit, artifact)]
    traps,                # [Trap(tid, description, detect, points)] — scored independently
    check_cells,          # {name: {expected, rel_tol}} for the model auto-grader
    calibration,          # [CalibrationQuestion(...)] with resolutions withheld
    notes,
)
```

Three fields carry most of the design weight:

- **`served_facts` with provenance.** Each fact carries `filed` and `accn`. This is what makes the validator possible and what makes a case auditable two years later when a student disputes a grade.
- **`traps` scored independently.** A student who catches three of four traps should score 75% of the trap points, not fail the case. Independent scoring also makes the case *diagnostic* — you learn which trap class a cohort systematically misses, which tells you which video to fix.
- **`calibration` with resolutions withheld at serve time.** `student_view()` strips them. Because the case is historical, resolution is instant, which is what makes the forecast ledger (INF-4) cheap.

---

## 6. Case authoring workflow

Roughly **6–10 hours per case** once the engine exists, dropping toward 4 as the authors build pattern libraries.

1. **Pick the situation, not the company.** The library should span situation *types* — a guidance raise smaller than the beat, a cyclical peak misread as secular, a crowded long in a de-grossing, an accounting red flag, a capital-allocation error, a spin-off with a broken comp set. Sector diversity matters far less than situation diversity, because the skills are situation-specific.
2. **Choose T so the interesting decision is live.** Usually 1–10 days before a print, or immediately after a disclosure that changes the debate. A T where nothing is pending produces a case with no decision in it.
3. **Build facts mechanically:** `case.facts_from_sec(cik, tags, T)`. Never hand-type financials.
4. **Run `comps.leak_report(cik, tag, T)`.** If the case has a large restatement between T and today, you have two choices — and both are fine: serve as-filed and never mention it, or make the restatement *the teaching point* (see Case C in §9).
5. **Collect documents and the transcript** for T and earlier.
6. **Curate the bar** — guidance, or hand-curated consensus, with provenance recorded.
7. **Write the expert key cold, via a second author** who sees only T-dated materials (Leak 4).
8. **Plant traps**, each with a mechanical detection rule.
9. **Write calibration questions** that resolve after T, with sources.
10. **Run the validator**, then dry-run with two pilot students before the case enters the graded pool.

**Build the first 8–12 cases as files plus a form. Do not build the web app until the cases have been run with real students twice.** The content is the asset; the delivery layer is replaceable and will be rewritten anyway.

---

## 7. Grading integration

The engine produces submissions; three graders consume them.

| Grader | Consumes | Owns |
|---|---|---|
| **Deterministic** | numeric fields, trap detections, calibration probabilities | `check_cells`, `traps`, Brier scoring |
| **Model auto-grader (INF-2)** | uploaded workbooks | check cells, **perturbation tests**, hygiene, formula consistency |
| **LLM rubric grader (INF-6)** | memos, notes, transcripts | rubric dimensions at 0–5, reference-guided, against anchors |

Three rules carried from `../BLUEPRINT.md` §2.7 and worth restating because they are easy to violate here:

1. **Never send a numeric answer to an LLM when a deterministic check exists.** Evidence on LLM grading of quantitative work is poor — in one evaluation a frontier model passed 7 of 48 proofs that all contained critical errors. Numbers go to the deterministic grader; the LLM grades only reasoning, and only with the worked key in context.
2. **One strong judge calibrated against a golden set**, not a panel. The 2024 panel-of-models recommendation was contested by 2026 work showing nine judges across seven families behave like ~2 independent votes and that the best single judge matches or beats the panel.
3. **Score outcome only as calibration.** The engine *knows* what happened, which makes it tempting to grade on it. Don't. Reveal the outcome, score the student's stated probabilities with a proper scoring rule, and leave the P&L out of the grade entirely.

---

## 8. Build plan

**MVP (≈4–6 weeks, one engineer plus an analyst author)**
- `pit/` layer — **done and tested**
- 8–12 cases as JSON manifests plus a static document bundle
- Clock as a manual instructor action (release step 2 by email or on a schedule)
- Deterministic grading of numeric fields and calibration
- Submissions in an append-only store with a hard lock

**v1 (+8–10 weeks)**
- Web runtime with timers, staged release and answer locking
- INF-2 integration for workbook grading
- INF-6 anchor set and LLM rubric grading for memos
- 20–25 cases
- Validator in CI

**v2**
- 30–40 cases spanning the situation taxonomy
- Cohort analytics: which traps are systematically missed, per-case difficulty calibration
- Dependency-graph comparison in the model grader

**Deliberately out of scope, permanently:** live market data, order execution, market-impact modelling, P&L leaderboards.

---

## 9. Example test cases

Five cases, each specified to the point where an author could build it. Case A is the flagship. **Data-availability reality is stated per case**, because three of the five are buildable from free sources alone and two are not.

---

### Case A — "The Raise That Was Smaller Than the Beat"
**Serves:** M13-E1 (earnings event clock), M06-E3 (guidance bridge), M10-E1 (expectations gap)
**Situation type:** guidance raise concealing 2H deceleration
**Data:** free (EDGAR + transcript + hand-curated guidance). Add a straddle price by hand for the implied-move component.

**Setup.** T is the morning of the Q2 print. The student gets: eight quarters of as-filed segment financials, the last two transcripts, management's FY guidance as given at Q1, the current price and multiple, and a hand-curated consensus FY revenue and EPS. Deliverable 1 is a preview memo with a **pre-commitment table** — what they will do in each of four outcomes. Then the print is released.

**The print.** Q2 revenue beats by **$30m**. FY guidance is raised by **$20m**. Management's call language is confident.

**The planted arithmetic (verified).** The raise is **$10m smaller than the beat**, so implied 2H revenue *falls* from $2,030m to $2,020m. 1H growth was **+12.71%**; implied 2H growth is **−1.46%** — **14.17 points of deceleration inside a guidance raise.** Decomposed: **2.70 points is a harder comp, 11.47 points is genuine implied slowdown** (2.70 + 11.47 = 14.17 ✓). Implied Q4 is **−2.86% y/y** against an FY+1 consensus requiring **+6.16%** — a **9-point reacceleration nobody has underwritten**, derivable with no view at all.

**Traps (independently scored).** The raise-smaller-than-beat arithmetic (20 pts); the comp-base effect (10); guidance given only on the call, not in the release (10); a tax-rate-driven component of the EPS beat (10); the exit-rate gap vs. next year's consensus (15); an after-hours overshoot that retraces by the open (10).

**Grading.** Deterministic: the bridge, the implied 2H figures, the two-year stacks under both conventions, the exit rate. LLM: preview-memo quality, first-read discipline, and — the highest-value dimension — **pre-commitment consistency**, i.e. did the action match what they committed to, and if not, is the deviation justified by new information rather than by the price.

**Why it is the flagship.** It integrates modelling, expectations, earnings mechanics and decision discipline; every trap is objectively detectable; and the central insight is pure arithmetic, so the answer key is not a matter of taste.

---

### Case B — "Eight Years of Twelve Percent"
**Serves:** M10-E2 (reverse DCF as a frontier), M11-E1, M04-E3
**Situation type:** high-multiple compounder where the debate is duration, not growth
**Data:** free (EDGAR) + price. Fully buildable from `pit/`.

**Setup.** T is an ordinary day, no catalyst pending — deliberately, because this case is about what is *already priced*. The student gets as-filed financials, the current price, and a WACC. **Two-phase with a lock:** Phase 1 (20 min) they state the core debate and three key drivers from financials alone; this locks. Phase 2 (40 min) they receive consensus, the multiple vs. history, and a reverse-DCF template, and re-write.

**The frontier (verified).** Sales $10.0bn, tax 21%, WACC 8%, 8-year horizon, EV $25.0bn (2.50x sales). Steady-state value is 1.185/0.08 = **$14.812bn = 59% of price**, so **41% of the price is future value creation**. Holding margin at 15.0% and incremental investment at 30%, **implied sales CAGR is 9.935%** (PV explicit $7.926bn + PV CV $17.074bn = $25.000bn ✓). The frontier: at 4.0% CAGR the price needs a **20.37% margin**; at a 12.0% margin it needs a **14.59% CAGR**; at a 45% investment rate it needs **10.89%**. Companion solve: with IC₀ $10.0bn, ROIC 18%, WACC 8% and IC growing 8%, **the market-implied CAP at EV $22.0bn is 12.96 years** (10.0 + 12.96 × 0.926 = 22.000 ✓).

**Grading.** Deterministic: every solve, with the PV required to reconcile to the given price. **The measured quantity is the delta between the two phases** — which specific expectations datapoint changed the debate, and whether the student retrofits Phase 1 as having been right. The grader receives both submissions and is instructed to detect retrofitting.

**Why it works.** It is robust to prior knowledge of the company, because the scored thing is a reasoning shift, not an answer.

---

### Case C — "The Numbers You Were Never Shown"
**Serves:** M07-E1 (filing craft), M06 (restatements), M08-E2 (comp-set normalisation)
**Situation type:** a restatement/reclassification that changes the entire growth narrative
**Data:** free, and **this case already exists in the tested data** — Envista, CIK 1757073.

**Setup.** This is the one case where the point-in-time leak *is* the lesson. Run it in two halves.

**Half 1.** T = 30 June 2021. Students get Envista's as-filed financials and are asked for the three-year revenue trajectory, the growth algorithm, and a view. The as-filed record at T shows FY2017 **$2.8109bn**, FY2018 **$2.8445bn**, FY2019 **$2.7516bn** — a business with essentially flat-to-declining revenue around $2.8bn.

**Half 2.** Students are then shown the *current* record for the same periods: FY2019 **$2.2848bn**, FY2020 **$1.9291bn**. **FY2019 is 17.0% lower and FY2020 15.5% lower than what an analyst saw at the time.** They must: identify what happened (a discontinued-operations reclassification — the filings say so), recompute every growth rate and margin on the restated basis, and answer the real question: *which basis should a comp sheet use, and what does that do to a multiple built on the other one?*

**Grading.** Deterministic: both sets of growth rates and margins, and the multiple computed on each basis. LLM: a 200-word note on what this implies for any screen, backtest or comp sheet built from a current database. Full credit requires the student to state that **both figures are correct answers to different questions**, and to say which question a comp sheet is asking.

**Why include it.** It inoculates students against the single most common error in quantitative equity work, using a real company and real numbers rather than a parable — and it is free to build, because the SEC serves both versions with their filing dates attached. It also does something no other case does: it teaches students to distrust their own data.

---

### Case D — "Both Legs Losing"
**Serves:** M12-E4 (de-grossing recognition), M04-E2 (flow vs. information)
**Situation type:** positioning-driven drawdown with theses intact
**Data:** **needs market data** — prices, a crowding proxy, short interest, borrow. Not buildable from EDGAR alone. The cheapest honest version uses prices plus a hand-built basket of names documented as crowded at the time.

**Setup.** The student holds a stated book of three longs and two shorts. Over four releases spaced 10 minutes apart (simulating four hours), they receive market, sector, factor, basket and single-name data. At each stage they state what is happening, their confidence, and what they would do. **Earlier answers lock.**

**The staged evidence.** Stage 1: the market-neutral book is −1.8%, the index +0.1% — correctly *unclear*. Stage 2: **both legs are losing** — longs down and shorts up, index flat. This is the diagnostic moment, because information cannot move both legs against you; only forced unwinding does. Stage 3: a crowded-long basket −4.2%, crowded-short +3.1%, momentum sharply negative — confirmed. Stage 4: borrow fees spike on both shorts — **a consequence, not new information**, and a student who upgrades confidence on it has double-counted.

**Grading.** The key **changes as evidence accumulates**: calling de-grossing at stage 1 scores *lower* than saying "unclear" and calling it at stage 2. Premature confidence is penalised, which is the opposite of what students expect. The scored quantity is the **confidence trajectory**, not the final answer. Action key: with theses intact, do nothing or add within limits, and explicitly do **not** cover shorts into the squeeze — which is exactly what the P&L pressure pushes toward.

---

### Case E — "Your Own Thesis, Twelve Weeks Later"
**Serves:** M14-E2 (forced re-underwrite), M03-E3 (falsification clause)
**Situation type:** longitudinal thesis-creep test
**Data:** free (EDGAR) + prices. The student picks the company; the engine supplies the subsequent tape.

**Setup.** Not a case so much as a **harness around the student's own capstone.** Three sittings.

- **Sitting 1.** The student locks a thesis, a trading plan, and three kill criteria. Each criterion must parse into `{metric, threshold, direction, resolution_date}` — **a criterion that cannot be mechanically evaluated scores zero**, which is a hard, objective and genuinely discriminating check. "If the competitive environment deteriorates" is not a kill criterion.
- **Sitting 2 (weeks later).** The engine serves the real subsequent tape — the next print, the price action, two news items — from masked historical data. The student must state whether any criterion triggered and then exit, hold unchanged, or hold with an **explicitly amended** thesis naming the new information that justifies the amendment.
- **Sitting 3.** Full post-mortem against the sitting-1 document.

**Grading.** The trigger check is **binary and mechanical**, because sitting 1's criteria were stored as structured records and the tape either crosses them or does not. **This is the cleanest measurement in the whole program.** The qualitative half asks whether an amendment is justified by new information rather than by the price — the grader gets both documents plus the intervening tape and must quote the specific new information cited.

**The failure mode it exists to catch.** Criterion: "exit if services attach is below 32% at the Q4 print." Attach reports at **29.5%** and the stock is **up 11%** on a revenue beat elsewhere. The trigger has objectively fired. The student writes: *"Attach came in at 29.5%, but revenue beat and the stock is working, so the thesis is intact and the attach ramp is just delayed a quarter."* That is textbook thesis creep, in the student's own handwriting, against their own pre-commitment, with the price doing the arguing. **Showing them those two documents side by side is the most valuable single output of the program**, and it is impossible without a longitudinal instrument.

---

### Coverage check

| Case | Free data? | Modules served |
|---|---|---|
| A — raise smaller than beat | ✅ (+1 hand-curated straddle) | M13, M06, M10 |
| B — eight years of 12% | ✅ | M10, M11, M04 |
| C — numbers you were never shown | ✅ **already in tested data** | M07, M06, M08 |
| D — both legs losing | ❌ needs market/positioning data | M12, M04 |
| E — your own thesis, 12 weeks later | ✅ (+prices) | M14, M03 |

**Three of five are buildable today from free, verified-reachable sources.** Start there.

---

## 10. Risks and open questions

| Risk | Mitigation |
|---|---|
| **An authored case leaks the future and nobody notices** | The validator, run in CI on every manifest. Plus the second-author cold key for Leak 4, which code cannot catch. |
| **The SEC changes or rate-limits the API** | Cache everything and commit the cache. A case must be reproducible from its cache with no network. |
| **`www.sec.gov` unreachable in the build environment** | You can get all the numbers and none of the documents. Check both hosts before scoping; collect documents manually for a fixed library if needed. |
| **Hand-curated consensus is wrong** | Record provenance per figure; prefer management guidance as the bar where possible; have a second author verify the bar for any case where the gap is the graded quantity. |
| **Cases become googleable** | Mask tickers and dates, which also removes the temptation to pattern-match. Accept that a determined student can identify the company — and note that identifying it does not give them the T-dated view, which is the actual skill. |
| **Answer keys contain errors** | Given documented spreadsheet error base rates, assume yours do too. Independent review of every key, and treat the first two student cohorts per case as pilots. |
| **Outcome-grading creep** | The engine knows what happened, so the temptation is structural. Make it a code-level constraint: the grader interface should not expose the realised return to anything except the calibration scorer. |

**Open questions for Fundamental Edge:**
1. Can you reach `www.sec.gov/Archives/` from your build environment? It determines whether filing-reading exercises are in or out of the MVP.
2. Guidance or consensus as the default bar? It changes what the preview-memo exercises test, and it is cheaper to decide now than to re-author.
3. Who writes the cold expert keys? This is the one part of the workflow that cannot be automated and that determines whether the cases are gradeable at all.
