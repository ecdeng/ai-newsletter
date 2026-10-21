# Assessment & Exercise Blueprint
## Fundamental Edge — Analyst Academy

**Prepared:** 21 October 2026
**Source syllabus:** *Fundamental Edge — Analyst Academy Brochure* (15 core modules + 9 topical intensives; $4,750; 30+ hours recorded core curriculum plus 20+ hours guest content; head trainer Brett Caughran, analyst trainer Andrew Carr)

---

## How to read this document

**Part 1** is the executive summary: the approach, the five most valuable exercises, and the infrastructure recommendation.
**Part 2** is the assessment architecture — the evidence base that determines *why* the exercises are shaped as they are. Read it before Part 3 or the rubrics will look arbitrary.
**Part 3** is the syllabus breakdown: all 15 modules plus the 9 intensives, each with expected content coverage and its exercises in full detail.
**Part 4** specifies the shared infrastructure, including the market-simulator question you asked about.
**Part 5** is the build roadmap.
**Part 6** is sources, grouped by topic.
**Part 7** is the verification queue — everything in here that should be checked before it reaches a paying student.

**Exercise IDs** run `M07-E2` (module 7, exercise 2); infrastructure is `INF-1`…`INF-7`; intensives are `TI1`…`TI9`.

**Difficulty** maps to the course's own stated audience segments: *beginner* = undergrad/MBA/career-switcher, pre-seat; *intermediate* = intern, 0–1 year analyst, sell-side junior; *advanced* = 1–3 year analyst, or the "struggling in the seat" segment the brochure names explicitly.

**Build complexity** is used consistently: **low** = question bank or static content, authoring effort only, no code; **medium** = templated files plus a deterministic auto-grader, or an LLM-graded rubric with anchors; **high** = custom platform, simulator, point-in-time data pipeline, or voice role-play.

---

## Confidence and provenance — read this before quoting any number

This blueprint was built from twelve parallel research passes plus five targeted verification passes. **Two tooling constraints shaped what was achievable, and you should know exactly what they were.**

1. **No source in this project was opened as a document.** `WebFetch` failed DNS resolution on every host for the entire project, and direct `curl` was refused by the environment's egress proxy (`CONNECT tunnel failed, 403`) for every host tested — `sec.gov`, `cfainstitute.org`, `fundamentedge.com`, `valueinvestorsclub.com` and others. Per the proxy's own guidance, blocked hosts are to be reported rather than routed around, so no workaround was attempted. **All external evidence came through search-result extraction.** Where I reproduce a rubric weight or a statistic, it is a fragment quoted out of the underlying document by a search layer, not my own read of the page.
2. **Web-search budget is pooled per turn (200 calls shared across all parallel agents).** Early research passes consumed it, so several later passes ran with **zero searches** and wrote from model knowledge, honestly labelled. I re-dispatched verification passes once the budget reset, which closed many of the gaps — but it means research depth is **uneven by module**, and the document says where.

**Research depth by module:**

| Depth | Modules |
|---|---|
| **Good** (real searches, 90–180 sources each) | M01, M02, M03, M04, M05, M06, M07, M08, M10, M14 |
| **Content strong, sourcing verified in a second pass** | M11, assessment architecture (Part 2) |
| **Content strong, external sourcing thin or in progress** | M09, M12, M13, M15, the nine intensives |

**What is nonetheless reliable:** **every piece of arithmetic in this document was independently computed and verified**, mostly in Python, across multiple passes. Where a worked example appears, the numbers tie, the identities close, and several examples were *rejected and rebuilt* when verification showed they produced degenerate or impossible results (a scenario tree that implied a 0% bull probability; a maintenance-capex calculation that returned a negative number). The mathematics is the most trustworthy content here; the citations are the least.

**Corrections made during this work that are worth carrying forward**, because the wrong versions are in wide circulation:

- **Justified P/E uses ROE with the cost of equity.** The widely-quoted form "(1 − g/ROIC)/(r − g)" is correct only for an all-equity firm, or read as **EV/NOPAT with r = WACC**. Mixing ROIC with a cost of equity is a specific, gradeable error.
- **"Leverage raises P/E" is not a general rule** and is mis-keyed in many question banks. The break-even is where the after-tax cost of debt equals the unlevered equity earnings yield; below it, leverage *lowers* P/E.
- **Buyback accretion is already inside EPS growth.** Adding a full shareholder yield on top of a return decomposition double-counts it by roughly 200–300bp a year. Only dividends belong in the separate yield term.
- **Kelly's gambling form is wrong for assets.** f* = (p·b − q)/b assumes you lose the entire stake; a losing long loses a *fraction*. The correct form is **f* = (p·a − q·b)/(a·b)**, which for plausible inputs returns >100% of capital in a single name — and *that* absurdity is the real argument for fractional Kelly.
- **The SEC's institutional short reporting is Form SHO** (not "Form SHORT") under Rule 13f-2, with compliance **deferred to 2 January 2028** and first filings due 14 February 2028; the Fifth Circuit **remanded without vacatur** in August 2025.
- **Rule 10b-18** (buyback safe harbour) and **Rule 10b5-1** (trading plans) are different rules; "10b5-18" is a conflation.
- **The pre-mortem's famous "+30%" figure** is routinely attributed to Klein (2007); the underlying evidence is **Mitchell, Russo & Pennington (1989)**.
- **"Work samples are the highest-validity selection method (.54)"** is no longer the best-supported reading; a 2022 re-analysis re-ranked structured interviews above it. The lesson is **structure, not modality**.
- **The LLM "panel of judges" recommendation is contested** by 2026 work; start with one strong judge calibrated against a golden set.
- **Quinnipiac G.A.M.E. is a portfolio competition** ranked on Sharpe ratio, not a stock-pitch competition; **NIBC is a corporate-transaction pitchbook competition.** Both are commonly mis-described as pitch competitions, including in my own initial research brief.
- **Bessembinder's circulating percentages do not reconcile** against his 25,967-stock sample (1,092/25,967 = 4.21%, not the quoted 4.31%). Use the paper's own internally consistent framings.

**One provenance matter you should decide on.** The ordered list of the nine thesis-development steps (M03) was glyph-confirmed **only** on a leaked Fundamental Edge deck marked "strictly confidential," hosted on a third-party study-notes site. The step *names* have independent corroboration from FE's own public materials; the leaked source is cited nowhere in Part 6. If you are Fundamental Edge, you have the authoritative version. If you are not, you should decide whether that material belongs in your project at all — I have flagged it rather than laundering it. The same applies to a pirated "NVDA Guided Quick Dive" and several re-uploaded module decks found during research and deliberately excluded.
# Part 1 — Executive Summary

## The approach in one page

Fundamental Edge's Analyst Academy teaches a **buy-side** process: fifteen recorded modules and nine guest intensives aimed at making a junior analyst useful when a PM says *"go look at XYZ and tell me what you think."* An assessment layer for it faces one hard constraint that shapes everything else.

**Investing is a low-validity domain.** Deliberate practice needs well-defined tasks, immediate feedback, repetition and error correction; stock picking natively supplies none of them. Accumulated practice explains under 1% of performance variance in the professions. And at an information ratio of 0.50, establishing skill at 95% confidence takes **15.37 years** — longer than the program, longer than most analyst tenures. **So the program cannot validly assess whether a student will make money.** Any assessment that tries is grading noise and teaching students to confuse outcomes with decisions.

What it *can* assess, rigorously:

1. **Reproducible analytical artifacts** — a model, a comp sheet, a reverse-DCF, an expectations bridge, a guidance decomposition. Objectively checkable with tolerances. Auto-gradeable.
2. **Judgment artifacts under constraint** — a memo, an earnings preview, a pitch, a trading plan, a kill note. Gradeable against analytic rubrics with human or LLM scoring plus anchors.
3. **Behaviour under adversarial pressure** — a PM grilling, a management meeting, a poke-holes session. Gradeable via OSCE-style stations where the stimulus is standardised.
4. **Forecast calibration**, measured longitudinally — the one outcome measure that is both valid and tractable, because masked historical data resolves instantly and a strictly proper scoring rule cannot be gamed.

That yields an eleven-layer architecture (§2.6) in which roughly **95% of assessment volume is auto-graded at about 5% of the cost**, and the expensive human judgment is concentrated on one capstone artefact and its live defence. The design borrows from medical education rather than from finance training, because medicine has already solved the reliability problem the superday has.

## The five highest-value exercises

| # | Exercise | Why it earns the top slot |
|---|---|---|
| 1 | **M13-E1 — The Earnings Event Clock** | The only exercise that integrates the whole course under a clock, with pre-commitment. A 20-step event timeline, five timed deliverables, fourteen independently-scored planted traps, and — critically — **scored on process fidelity and pre-commitment consistency, never on the outcome.** It is also the exercise the historical case engine exists to serve. |
| 2 | **M10-E1 — The Expectations Gap Trap** | Twin stimuli with **identical fundamentals** and opposite correct answers. It destroys the single most common junior error in the course — comparing your EPS to published consensus and calling the difference an edge. In the worked case a junior overstates their edge by **9x** and a "+7.6% beat" turns out to be a negative-EV long. Cannot be pattern-matched. |
| 3 | **M14-E2 — The Forced Re-Underwrite** | The only instrument that can actually measure thesis-creep resistance, because it is **not single-shot.** Three sittings weeks apart: lock a thesis and kill criteria, then face real subsequent tape and declare whether a criterion fired. The trigger check is **binary and mechanical** — the cleanest measurement in the program — and nothing publicly available tests this at all. |
| 4 | **M07-E1 — The 90-Minute 10-K Brief** | The most *valid* single exercise available, because **driver selection is the real skill and it has a defensible expert key** — unlike a price target. The research-plan column is nearly impossible to fake. |
| 5 | **M09-E4 — The Management Meeting Station** | Converts "quality of questioning," otherwise the hardest thing in the syllabus to measure, into a **binary logged outcome** via the only-if-asked disclosure device, with a planted MNPI bait as a critical-failure check. |

Honourable mentions that punch above their build cost: **M06-E1** (the 2-year stack ambiguity — three incompatible conventions, and the most-used one breaks hardest in the case it was adopted for), **M11-E1** (derive the multiple from the Gordon model, including the ROIC = WACC ⇒ EV/IC = 1 corollary), **M08-E1** (the industry P&L share-shift constraint, which makes guidance falsifiable), and **M01-E3** (alpha-load triage, where over-work is penalised harder than a missed winner).

## Recommended shared infrastructure

**You asked whether a full market simulator is worth building. It is not — and the reason is instructive rather than budgetary.** Fundamental analysis runs on a quarters-to-years clock; a real-time trading simulator optimises for execution and price feedback, and **price feedback is the least valid assessment signal available.** You would spend the most to measure the least.

Build a **historical case engine** instead (INF-1): freeze a date, serve only what was knowable then, demand a thesis and a sizing recommendation, advance the clock, release the print, force a post-mortem against the student's own original document. **Its value is not realism — it is time compression plus free ground truth.** A three-year holding period becomes a 40-minute exercise in which the right answer already exists. SEC EDGAR's XBRL APIs supply point-in-time as-filed data for free and solve the hardest look-ahead leak at zero cost; historical consensus is the one genuine gap, and the recommended fix is deliberately low-tech (hand-curate a few hundred data points for a fixed 20–40 case library, or use management guidance as the bar).

**And a fixed case library is better assessment than a dynamic simulator**, because identical stimuli across students is exactly what makes scores comparable. The apparent limitation is the design virtue.

Seven pieces of infrastructure, in build order: **INF-6** golden set and rubric store (long-lead, uncopyable) → **INF-2** model auto-grader (highest ROI; perturbation testing is the non-negotiable feature) → **INF-4** calibration ledger (cheapest, and the program's one defensible efficacy claim) → **INF-1** case engine MVP → **INF-5** synthetic company generator → **INF-7** idea ledger → **INF-3** role-play engine (highest cost, least defensible moat — the content is the asset, not the capability).

## Three things worth knowing before you start

**The single most important technical decision is mandatory structured submission fields** — target, horizon, conviction, catalyst with a date, falsification condition, size, liquidity, factor footprint. Free-form memos are not scoreable at scale; structured fields make auto-grading *and* calibration scoring essentially free, because every submission becomes a timestamped forecast at no extra student effort. Retrofitting them later means re-authoring everything.

**The syllabus has one real curriculum gap.** Sleeve risk management — gross and net exposure, beta and factor neutrality, correlation limits, stop-outs, drawdown governors, contribution-to-risk — appears almost nowhere across the fifteen modules, despite the program training pod analysts. There is also **no options primer anywhere**, yet the implied-move and hedging content requires one. Either the brochure understates the recorded content, or the assessment layer should cover both because the seat demands them.

**Several of the course's own frameworks are unpublished, and the blueprint says so rather than guessing.** ETIK is now confirmed as *"Everything There Is to Know"*; MIC's C is confirmed as *convergence*. But the **four reasons markets are not efficient**, the **seven hacks for variance vs. street**, the **substance of the nine thesis steps**, and **"spring-loaded"/"peak-on-peak"** are not public. Every exercise touching them is written to be robust to the gap — for example, M01 asks students to "name four structural sources of mispricing and the constraint on the natural arbitrageur for each," which is a better test anyway and survives whatever Caughran's four turn out to be. **An hour of his time removes a dozen caveats from this document.**
# Part 2 — The Assessment Architecture

Everything in this blueprint follows from one constraint, so it is worth stating before the exercises.

## 2.1 The binding constraint: investing is a low-validity domain

Deliberate practice requires four conditions: a well-defined task at an appropriate difficulty, immediate informative feedback, opportunity for repetition, and opportunity to correct errors. **Stock picking satisfies none of them natively.** That is precisely the gap an assessment layer exists to manufacture.

The evidence sharpens the point. A meta-analysis of deliberate practice found accumulated practice explains roughly **26% of performance variance in games, 21% in music, 18% in sports, 4% in education, and under 1% in the professions** (pooled 12%, CI 9–15%; the figures are exact and the professions number is the one that matters, though the finding is contested by Ericsson & Harwell). And Kahneman & Klein's conditions for trustworthy intuition require (a) an environment with sufficiently valid cues and (b) adequate opportunity to learn them through feedback. Equity markets are the canonical violation of both. Their notion of **"fractionated expertise"** matters just as much: within one domain an expert can be highly skilled on some tasks and no better than a novice on others, **and cannot tell which is which.**

Two consequences govern this entire document:

1. **Assess task by task; never issue a single composite "analyst score."** Fractionated expertise means a composite hides exactly the gaps that matter.
2. **Weight process over outcome.** In a low-validity environment, outcome scoring is mostly noise and actively teaches the wrong lesson by rewarding lucky bad process.

The arithmetic is unforgiving: at an information ratio of 0.50 it takes **15.37 years** to establish skill at 95% confidence. **The program literally cannot assess whether a student will make money.** It can assess process fidelity and forecast calibration. Tell students this in week one — it reframes every low score as diagnostic rather than evaluative.

## 2.2 Calibration is the one honest outcome measure

Given the above, the only outcome-based measure that is both valid and tractable over a 15-module course is the **calibration of probabilistic forecasts**: it generates many resolvable data points quickly, is scored by a strictly proper rule so it cannot be gamed, is demonstrably trainable, and is exactly what the syllabus already demands in Modules 10, 11, 13 and 15.

```
Brier score (binary):   BS = (1/N) Σ (f_t − o_t)²            range 0–1; 0 perfect, 0.25 = always 50%
Murphy decomposition:   BS = Reliability − Resolution + Uncertainty
Skill score:            BSS = 1 − BS/BS_ref
```

**Report all three components, not just the score.** The reliability/resolution split is pedagogically decisive: an analyst who says "60% confident" about everything has **excellent calibration and zero resolution** — and zero resolution means zero alpha. That distinction *is* the syllabus's "develop a differentiated view."

Two cautions. The multi-category Brier form has **range 0–2**, not 0–1, which is a standard source of confusion when comparing published scores — always state your convention. And the trainability evidence most people cite as "Mellers 2014" is more precisely **Chang, Chen, Mellers & Tetlock (2016)**: roughly **10–12% Brier improvement from under an hour of probabilistic-reasoning training**, sustained into a second year, with a 2024 reanalysis disputing it. Mellers (2014) establishes the training/teaming/tracking structure and uses the 0–2 convention.

Across 15 modules at 5–10 resolvable questions each, that is **75–150 scored forecasts per student** — enough for genuine individual measurement, which no competitor offers, and the basis for the one marketing claim the program can actually defend: not *"we'll make you money"* but *"we measurably improved your forecast calibration."*

## 2.3 Many short standardised stations beat one big exam

The superday is already an OSCE — a circuit of short, standardised stations with pre-built scoring instruments. Medical education has spent fifty years solving its reliability problem, and the findings transfer directly.

The dominant source of measurement error in performance assessment is **case specificity, not rater disagreement**: performance on one case predicts performance on another poorly. **Therefore more stations with one rater each beats fewer stations with multiple raters.** That is the most actionable single finding in this architecture.

On station count, be careful with the numbers in circulation. The defensible claim is that **minimal reliability requires on the order of 3–4 hours of testing time** (Van der Vleuten & Schuwirth, *Medical Education* 2005 — **not** the 1996 paper, which is where this is usually mis-cited). **Derive your station count arithmetically from that** — 3.5 hours ÷ station length — and say so. Do not print "a 10-station OSCE lands at 0.5–0.7"; those specific cell values are unverified.

On instruments, the evidence is precise and slightly counter-intuitive. Across 53 surgical residents and eight 15-minute stations, inter-station reliability was **α = 0.79 for a checklist, 0.85 for global ratings alone, and 0.89 for checklist-then-global**. So expert global ratings beat checklists, and adding a checklist on top of global ratings adds almost nothing. But **α = 0.79 is respectable — checklists are not unreliable**, they are just less good for judgment. (A separate finding that checklists actively *penalise* experts, because experts skip steps checklists reward, comes from Hodges et al. 2003 and is frequently conflated with the above. Keep them distinct.)

**The design rule: checklists for procedural stations, global rating scales for judgment stations, and never average the two into one number.**

## 2.4 Structure is the differentiator, not modality

The familiar claim that work-sample tests are the highest-validity selection method (the "0.54" figure) is **no longer the best-supported reading.** A major 2022 re-analysis argued prior meta-analyses systematically over-corrected for range restriction, and re-ranked the methods: **structured interviews ~.42, job knowledge tests ~.40, empirically keyed biodata ~.38, work samples ~.33, cognitive ability ~.31, integrity ~.31, assessment centres ~.29, conscientiousness ~.19, unstructured interviews ~.19.** (A circulating variant that omits the already-selected-sample adjustment puts job knowledge at .31 — state which variant you quote. There is also a 2023 rebuttal exchange worth citing alongside.)

The lesson is **structure, not modality**. So the Academy's differentiator is not "we use work samples" — everyone sells modelling tests. It is: **fixed stimuli, pre-built scoring instruments, behaviourally anchored scales, calibrated raters, and published reliability coefficients.**

One honest caveat: those coefficients predict *job performance*, not *learning*. Do not borrow them to claim the course's assessment predicts analyst success — that would require your own validation study.

## 2.5 What the assessment layer actually sells

Cognitive apprenticeship names six methods: modelling, coaching, scaffolding, articulation, reflection, exploration. Mapping them onto the Academy identifies exactly what a pre-recorded video course is missing:

| Method | In the syllabus? | What the assessment layer must add |
|---|---|---|
| **Modelling** | **Yes** — 30+ hours of Caughran and Carr working through TSLA, NVST, the frameworks. The product's core strength. | Think-aloud annotation of the expert's own screen recordings |
| **Coaching** | **Weakly** — three Q&A office hours plus kickoff and wrap-up. **The biggest gap.** | Rubric-based feedback on submitted work: LLM for volume, human for the capstone |
| **Scaffolding** | **Partly** — FEV, MIC, Focus Five, the nine-step process, ETIK | Faded exercise series; framework templates that progressively blank out |
| **Articulation** | **Barely** — the second big gap | Mandatory verbalisation: recorded pitches, written "why I believe this" memos, the live defence. **Articulation is also what makes work gradable, so it solves two problems at once** |
| **Reflection** | Named in M14 but not instrumented | Side-by-side comparison against expert exemplars; forced post-mortem against the original thesis; calibration feedback |
| **Exploration** | Implicitly the end state | The open capstone: the student's own name, no scaffolding |

**A video library is pure "modelling." The assessment layer is how you buy the other five — and coaching plus articulation are where a $4,750 price point is actually justified.**

Two further design consequences:

- **Fade, don't stream.** The cohort spans a Citadel-bound intern and a career-switching engineer. The expertise-reversal effect means instructional support that helps novices actively *harms* experts. So fade scaffolding within each exercise series (complete model → revenue build blanked → operating section blanked → raw build) and **route by diagnostic, not by self-report.**
- **Interleave, because selection is the skill.** Blocked practice (all the DCF problems inside the DCF module) teaches execution but not *choice of tool* — and the real buy-side task is "which tool does this situation call for." Every module's question set should end with a **mixed, unlabelled** set drawing on all prior modules, and the capstone should present situations with no indication of which framework applies.
- **Manage the NPS conflict honestly.** Desirable difficulties depress performance *during* learning while improving retention and transfer. A $4,750 self-paced product with hard, low-scoring practice sets will generate complaints unless you teach the learner the learning science up front and show them their **own improvement trajectory** rather than an absolute score.
- **Keep running after the course ends.** The optimal review gap is roughly 10–20% of the desired retention interval. For a program whose value is realised on the desk 6–12 months later, that implies review gaps of **3–8 weeks**, which means the assessment layer must outlive the 15 modules.

## 2.6 The eleven-layer architecture

| Layer | Volume | Instrument | Grader | Modules |
|---|---|---|---|---|
| **A. Retrieval drills** | 20–40 items/module, spaced and interleaved | MCQ, numeric entry | Auto | All |
| **B. Vignette item sets** | 10–15 vignettes × 4 items per cluster | MCQ on a 1–2pp case with exhibits | Auto | 01, 04, 05, 07, 08, 10, 11, 12, 13, 15 |
| **C. Faded modelling exercises** | 4–6 per modelling module | Workbook upload | Auto: check cells + perturbation + hygiene | 06, 07, 11, 13 |
| **D. Print-update drills** | 1 per earnings-related module | Fixed template + real release, 30–45 min | Auto — **the highest-fidelity autograde in the program** | 06, 10, 13 |
| **E. Constructed response** | 3–5 per module | Short written answers, minutes = points | LLM, reference-guided | 03, 04, 09, 10, 11, 12, 14, 15 |
| **F. Calibration ledger** | 5–10 resolvable questions/module → 75–150 total | Probability entry, auto-resolved | Auto: Brier + Murphy components | All |
| **G. Role-play stations** | Unlimited ungraded practice + 2 graded | AI management meeting; AI PM grilling | Checklist (deterministic) + LLM global ratings | 02, 05, 09, 14 |
| **H. Five-minute pitch** | 5–6 across the program | 3–5 min recording | ASR → LLM on anchored dimensions | 03, 05, 07, 11, 12, 14 |
| **I. Idea ledger / paper book** | Continuous | Structured submission with mandatory fields | Auto attribution + credibility-weighted peer review | 05, 12, 15 |
| **J. Capstone pitch + defence** | 1 | Page-limited memo + model + live defence | **Human, double-scored**, ICD-203-derived rubric + separate defence rubric | All |
| **K. Entrustment report** | 1 | Per-activity levels 1–5, not a percentage | Human, from the evidence in A–J | All |

**Layers A–F and I are roughly 95% of the volume at 5% of the cost. G, H and J are the differentiation. K is the credential.**

On K: borrow medical education's **entrustable professional activities** scale — 1 may observe only; 2 may act with direct supervision; 3 may act with indirect supervision; 4 may act unsupervised; 5 may supervise others. Reporting "can maintain a comp sheet and universe tracker unsupervised (4); can run a management meeting with indirect supervision (3); can size a position: observe only (1)" is **instantly legible to a hiring PM** and commercially far stronger than a percentage. It also fits the syllabus's own stated endpoint — "analyst progression: junior to full-stack partner."

**Governance:** no single assessment can be both authentic and reliable, so collect **many low-stakes data points of varied type and aggregate them** for any high-stakes decision. Dozens of cheap auto-graded items plus a handful of expensive human judgments, aggregated into a portfolio decision.

## 2.7 Two rules about graders that the evidence has recently changed

**Rule 1: do not send a numeric answer to an LLM when a deterministic check exists.** The evidence on LLM grading of quantitative work is poor — in one evaluation **GPT-5 passed 7 of 48 proofs that all contained critical errors.** Every number in this blueprint is checked arithmetically first; the LLM grades only reasoning, and only with the worked key in context. Reference-guided grading is the critical mitigation and it is not optional for finance.

**Rule 2: the "panel of models" recommendation is now contested — start with one strong judge.** The 2024 finding that a panel of small models beats a single large judge has been challenged by 2026 work showing that nine judges across seven families behave like roughly **two independent votes**, that panel accuracy falls 8–22 points short of what independent voting would predict, and that **the best single judge matches or beats the full panel in all conditions tested.** Panels do still help on *process-error* marking (κ 0.82 → 0.87). So: **one strong judge, calibrated against a human-labelled golden set; add a panel only if you measure independence and demonstrate it beats your best single judge on your own labels.**

Three more practical findings worth building in:
- **Use a 0–5 scale per dimension.** Human–LLM alignment is highest there.
- **Expect weaker agreement than the hype.** Many 2024–25 automated-essay-scoring studies report QWK **below the 0.70 benchmark**; one higher-education study found QWK of −0.04 to 0.02, none significant; another reports near-zero kappa with poor run-to-run repeatability. Better results exist (~0.68; ~0.60 holistic and worse on analytic traits; one physics preprint reports 0.80). The real lesson is in that preprint's own title: **validity is strongly task-dependent across assessment formats.** So **measure and report your own QWK per station type**, and do not claim human parity.
- **Build the golden set first.** It is the most durable asset in the grading stack and it is what lets you swap models later. The six-step human rater-calibration pipeline — anchor papers, training, qualification, seeded validity papers, double-scoring, recalibration — maps onto an LLM judge **unchanged**, and drift monitoring becomes essential because the underlying model will be silently updated. Pin model versions and record the version on every score.

**And one product-risk item that is not a footnote:** the moment an LLM-produced score is used by funds in hiring, the Academy is arguably supplying an automated employment decision tool, which engages NYC Local Law 144 and the EU AI Act's high-risk classification for education and vocational assessment. Mitigations: position outputs as **learning diagnostics, not employment recommendations**; keep a human in the loop for any certification decision; retain subgroup-level score analyses; document the rubric and model version behind every score. Also: **never score video or facial features** — score transcript substance plus a narrow, clearly-labelled set of prosodic features (pace, filler rate, pauses). Anything else is an avoidable fairness liability for marginal signal.
# Part 3 — Syllabus Breakdown

The course's own structure and naming are preserved throughout: fifteen numbered core modules, then the nine topical intensives. Each module gives **expected content coverage** (what a student should actually master, from the research, with provenance flagged where the course's own frameworks are unpublished) followed by its **exercises** in the required detail.

Where a syllabus bullet is vague, my reading of its scope is stated and I continue rather than stopping. Where two modules overlap — and several do substantially — the overlap is flagged and the content is assigned to one module so that exercises do not double-count.
## Module 01 — Fundamental Foundations

### Expected content coverage

**Scope.** The course's legitimacy-and-objective-function module: why fundamental research is paid for, where mispricing comes from, and what the analyst is actually optimising. Light on arithmetic, heavy on the mental model that every later module inherits.

**The canonical spine a student should master:**

| Topic | What mastery looks like |
|---|---|
| Fundamental analysis in market economies | Prices are an information-aggregation device, not a scoreboard; informative prices ration real capital. Able to answer an LP in 60 seconds: "what does your work do for anyone but your fund?" |
| Myth of efficient markets | Fama (1970) three forms defined **by information set**: weak (past prices), semi-strong (all public info), strong (incl. private). Critical framing: the entire buy-side enterprise is a bet against **semi-strong** efficiency using legally obtainable information. It is *not* a bet against strong-form efficiency — that bet is illegal. |
| Grossman–Stiglitz (1980) | If prices were fully efficient nobody would pay for information, so nobody would gather it, so prices couldn't be informative. Equilibrium requires noise. Alpha exists *in equilibrium* and its size is pinned by the marginal cost of research, not by anyone's cleverness. |
| Limits to arbitrage | Shleifer & Vishny (1997): arbitrage is done by specialists running **other people's money**, so it fails precisely when mispricing is largest. Performance-based arbitrage (PBA) is a positive feedback loop. **This is the most operationally important paper for a pod analyst** — the pod drawdown machinery *is* PBA, mechanised. |
| Four reasons markets are not efficient | See provenance note below. Teach as a **diagnostic**, not a list: the reason determines holding period and sizing. Flow-driven mispricing mean-reverts in days–weeks; information/behavioural in quarters; limits-to-arbitrage mispricing may never close. |
| Alpha load | Caughran's triage term: how much idiosyncratic, fundamentally-driven return is actually available. Assembled from his own statements: a function of (expectations-gap size) × (existence of a forcing mechanism) × (idiosyncratic share of variance). All three must be non-zero. |
| Voting vs weighing machine | Weighing = the earnings stream; voting = the multiple. The identity: (1+r_total) = (1+g_EPS)^T × (M_exit/M_entry). Horizon choice *is* a choice about which term you are forecasting. |
| Recipe: skills, process, judgment | Skills are learnable fast; process learnable slower; judgment is the bottleneck and only partly teachable. Juniors over-invest in skills because skills are legible and gradeable. |
| 10% mindset | A triage doctrine, not an optimism doctrine. Prior on any randomly-encountered name is "fairly priced"; the scarce resource is deep-dive hours, so the highest-leverage skill is fast, well-calibrated killing. |
| Pareto distribution | Bessembinder (2018): 25,967 US stocks, 1926–2016; **42.6%** beat one-month T-bills over their lifetime (≈ three of every seven); the best-performing **4%** account for the entire net wealth gain. Consequence for the analyst: P&L is made by 1–3 positions a year, so batting average is nearly uninformative and sizing the right tail is the job. |

**Prerequisites.** Residual claim / perpetuity; cost of capital; expected value, variance, Sharpe; what a benchmark and a factor are. No calculus.

**Junior vs. strong.** A junior writes "the market is mispricing this." A strong analyst writes: "the market is mispricing this *because* [named structural reason], it's worth X% to fair value, the forcing mechanism that closes it is Y on date Z, and the reason it hasn't been arbitraged is [specific constraint on the natural arbitrageur]." The second and fourth clauses are the ones juniors never write.

**Research provenance — read before building an answer key.**
- **Caughran's actual "four reasons" were not recoverable.** The module heading is confirmed on Fundamental Edge's own site and syllabus PDFs, but the enumerated list appears to exist only inside the paid video. Six of his public positions constrain it (flow-dominated price setting; "as the players at the poker table have shifted, the constraints of those new players have created new alpha pools"; fundamentals dominate beyond ~3 months; information abundance doesn't kill alpha). **Design the exercise so the key is "name four distinct structural sources of mispricing and, for each, the constraint on the natural arbitrageur"** — robust to whatever his four turn out to be, and a better test anyway.
- **The 80/10/10 prior** (~80% of stocks fairly priced, 10% tails each side) is a search-layer paraphrase of a podcast remark, not a verified verbatim quote. Verify before printing a number.
- **"10% mindset" is genuinely ambiguous** — it may mean the tails prior, or "be in the top 10% of effort." The heading alone doesn't disambiguate. Resolve with FE.
- **The voting/weighing quote is misattributed everywhere.** Graham & Dodd (1934) supplied the *voting machine* half; the short-run/long-run compression traces to Buffett in a 1973 interview. There is no primary source for Graham saying the famous sentence. This makes an excellent trap item.
- **Bessembinder secondary percentages don't reconcile.** 1,092/25,967 = 4.21%, but sources quote 4.3%; 90/25,967 = 0.347%, but sources quote 0.33% — different denominators. Use the paper's own internally consistent framings ("best-performing 4%", "42.6%", "four of every seven"); do **not** ask students to reconcile 1,092 with 25,967.

---

### M01-E1 — "Why Does This Job Exist?" (research-cost ceiling)

**Topics:** Fundamental analysis in market economies; Grossman–Stiglitz; goal of harvesting alpha.

**Learning objective.** Convert the abstract claim "research is costly, therefore alpha exists" into the fund's own arithmetic, so the student understands that their employer's cost base is the floor on the gross alpha they must find.

**Student task.** Given a one-page fund fact sheet (AUM, research/investment-team cost lines, fee terms), compute (a) research cost as % of AUM, (b) the gross alpha required for the LP to net zero, (c) the gross alpha required for the LP to net a stated 8% target. Then answer in ≤150 words, addressed to a sceptical pension trustee: what does this activity do for anyone other than the fund? **25 minutes.**

**Tools and environment.** Existing: any spreadsheet. No custom build.

**Grading rubric.**
- *Quantitative (60 pts, fully auto-gradeable):* three numeric answers, tolerance ±0.05pp. Part (b) must correctly gross up for both the management and incentive fee layers — the common error is netting only the incentive fee.
- *Qualitative (40 pts, LLM-graded against anchors):* 20 pts — names the price-informativeness → cost-of-capital → real-investment channel rather than asserting "liquidity"; 15 pts — states that the alpha is compensation for a cost borne, not evidence others are stupid; 5 pts — within word limit. Anchor answers at 40/25/10 supplied to the grader.

**Difficulty.** Beginner. **Build complexity.** Low (question bank + one spreadsheet).

**Example and worked answer.**
> Fund AUM $1,000m. Annual research + investment-team cost $25m (comp, data, expert networks, travel). Terms: 1.5% management fee, 20% incentive over a zero hurdle.
>
> (a) 25/1,000 = **2.50% of AUM**.
> (b) For the LP to net zero: gross alpha must cover the 1.5% management fee, and the incentive fee takes 20% of what remains. Let *g* = gross alpha. LP net = (g − 1.5%) × 0.80 = 0 → **g = 1.50%**. Note the research cost is borne inside the management fee here, and 1.5% < 2.5%, so this fund's fee load does not cover its own research budget — the gap is the GP's to fund or the LP's to bear via pass-through. That observation is worth 10 of the 20 structural points.
> (c) For LP net 8%: (g − 1.5%) × 0.80 = 8.0% → g − 1.5% = 10.0% → **g = 11.50% gross alpha**.
>
> Teaching payload: an 11.5% gross alpha requirement on a market-neutral book running 4x gross is a ~2.9% return on gross exposure — which is the bottom of the band pods actually target. The student should finish this exercise knowing that the fee stack, not the market, sets the bar.

---

### M01-E2 — Efficiency Forms and the Attribution Trap

**Topics:** Fama's three forms; myth of efficient markets; voting vs weighing machine.

**Learning objective.** Stop students strawmanning EMH, and inoculate them against uncritical sourcing.

**Student task.** 18 items. Part A (12 items): for each claim, state which form of efficiency it would contradict if true, or "none." Part B (4 items): identify the joint-hypothesis problem in four alpha claims. Part C (2 items): attribute two famous quotes and state your confidence. **30 minutes, closed book.**

**Tools and environment.** Existing: any quiz platform. No custom build.

**Grading rubric.** Entirely auto-gradeable except Part C's confidence justification.
- *Quantitative (90 pts):* Parts A and B machine-scored. Part B items require naming the missing factor model — an answer that claims alpha without specifying what it is risk-adjusted against scores zero.
- *Qualitative (10 pts, LLM or human):* Part C's reasoning. Full credit requires hedged attribution with a stated reason, not a confident wrong answer.

**Difficulty.** Beginner. **Build complexity.** Low.

**Example and worked answer.**
> *Part C, item 1:* "In the short run the market is a voting machine, in the long run a weighing machine." Attribute this quote.
>
> **Model answer (full credit):** Commonly attributed to Benjamin Graham, but this is not a verbatim Graham quote and no primary source has been found for it. Graham & Dodd's *Security Analysis* (1934) supplies the *voting machine* half — arguing the market should be seen as a voting machine registering choices "partly of reason and partly of emotion," explicitly *not* a precise weighing machine. The short-run/long-run compression traces to Warren Buffett in a 1973 interview. Keynes is a frequent further misattribution; his adjacent material is the beauty-contest passage in the *General Theory* (1936), which is a different argument — anticipating others' anticipations, not value-price convergence.
>
> **Zero credit:** "Benjamin Graham, *The Intelligent Investor*." This is the answer that demonstrates the habit the item is testing for.

---

### M01-E3 — Alpha Load Triage Drill *(flagship for this module)*

**Topics:** Alpha load; forms of mispricing; 10% mindset; idea generation.

**Learning objective.** Build fast, well-calibrated *killing*. The scarce resource is deep-dive hours; the skill is saying "no alpha load, next" within minutes, repeatedly, without ego.

**Student task.** Student receives 8 two-page name summaries (business description, 3-year financial summary, current multiple vs. own history and peers, consensus estimates and revision trend, short interest, ownership change, recent news headlines). They must: rank all 8 by alpha load; select the 2 worth a deep dive; for each of the 6 kills, state the single disqualifying reason in one sentence; for each of the 2 keeps, state the expectations gap, the forcing mechanism with a date, and the constraint on the natural arbitrageur. **45 minutes.** Hard stop — the time limit is the point.

**Tools and environment.** Custom data packs (templated, reusable). Generated from real historical situations with dates masked, so ground truth exists.

**Grading rubric.**
- *Quantitative (50 pts, semi-auto):* 25 pts — Spearman rank correlation between student ranking and the instructor key, scaled; 15 pts — did the 2 selected names include the 1–2 names that subsequently produced a >20% absolute move within 4 quarters (ground truth from the masked historical record); 10 pts — kill reasons drawn from a valid taxonomy (auto-matched against a controlled vocabulary of ~15 accepted disqualifiers).
- *Qualitative (50 pts, LLM-graded with human spot-check on 20%):* for each keep, 10 pts expectations gap stated as a *number vs. a named consensus figure* (not "the market is too pessimistic"); 10 pts forcing mechanism with a date; 5 pts arbitrageur constraint identified.
- **Scoring asymmetry that makes this work:** a student who deep-dives a name with no alpha load loses more points than one who kills a name that later moved. Over-work is penalised harder than a missed winner. This mirrors the real seat and is the opposite of how students expect to be graded.

**Difficulty.** Intermediate. **Build complexity.** Medium (templated data packs + rank-correlation auto-grader + LLM rubric).

**Example task prompt.**
> *Name D:* Specialty industrial distributor. Revenue $2.1bn growing 4–6% organically for six years; EBIT margin stable 11.5–12.2%; ROIC 14%; trades 18.5x NTM EPS vs. 5-year range 14–21x and peer median 19x. Consensus FY+1 EPS $4.12, revised +0.4% over three months. Short interest 2.1% of float. No insider activity. Last four prints: in line, in line, 1% beat, in line.
>
> **Model kill (full credit):** "No alpha load — numbers, multiple and positioning are all mid-range, and there is no identified forcing mechanism; the expectations gap is approximately zero." The point is that nothing is *wrong* with Name D. It is a perfectly good business that is perfectly fairly priced, which is the modal case under the 10% prior and must be killed in under three minutes.
>
> **Zero credit:** any answer that kills Name D for being "expensive at 18.5x" — it is mid-range versus both its own history and peers, so this reveals the student is screening on valuation level alone, the largest bucket in the universe.

---

### M01-E4 — Alpha or Beta? Attribution Autopsy

**Topics:** Alpha load (factor decomposition); goal of harvesting alpha.

**Learning objective.** Teach the student to distinguish "I was right" from "I was long beta" — the single failure pod risk teams catch instantly.

**Student task.** Given a 12-position book with realised returns, position betas, sector and style exposures, and the realised factor returns for the period, decompose total return into factor contribution and residual alpha. Then answer: which three positions actually generated alpha, and what share of the headline return was alpha? **40 minutes.**

**Tools and environment.** Existing: Excel/Sheets with a provided template. Optionally Python.

**Grading rubric.**
- *Quantitative (80 pts, fully auto-gradeable):* decomposition cell-checked against key, tolerance ±0.1pp; the per-position alpha column must tie to the book total (tie-check worth 15 pts on its own).
- *Qualitative (20 pts, LLM-graded):* the written conclusion must state the alpha share and note any pseudo-breadth — positions that look diversified but are one factor bet.

**Difficulty.** Intermediate. **Build complexity.** Low–medium (template + cell-tolerance grader).

**Example and worked answer.**
> A long position returned +20.0% over the year. Market return +12.0%; position beta to market 1.30; sector and style (momentum/growth) contribution calculated at +3.00%.
>
> Market contribution = 1.30 × 12.0% = **+15.60%**. Total factor = 15.60% + 3.00% = **+18.60%**. Alpha = 20.00% − 18.60% = **+1.40%**. Alpha share = 1.40/20.00 = **7.0%**.
>
> Written conclusion for full credit: 93% of the "win" was beta the PM could have bought with futures for a couple of basis points. The analyst was paid for 140bps.

---

### M01-E5 — Pareto P&L Lab

**Topics:** Pareto distribution and top-performer challenges; goal of harvesting alpha.

**Learning objective.** Internalise that batting average is nearly uninformative and that truncating the right tail is the most destructive habit available.

**Student task.** Given a year of 12 closed positions with basis-point contributions, compute batting average, average winner, average loser, slugging ratio and expectancy per position; verify expectancy ties to the total. Then run two stress tests: remove the single best position, and apply a "sell half after +25%" rule to every winner. Write 150 words on what the stress tests imply for position sizing. **35 minutes.**

**Tools and environment.** Existing: spreadsheet. No custom build.

**Grading rubric.**
- *Quantitative (70 pts, fully auto-gradeable):* all statistics plus the tie-check; both stress tests recomputed. Tolerance ±0.5bp.
- *Qualitative (30 pts, LLM-graded):* must conclude that batting average moved trivially while the year flipped sign, and connect this to dispersion in position size. An answer that recommends "improve the hit rate" scores ≤10.

**Difficulty.** Beginner–intermediate. **Build complexity.** Low.

**Example and worked answer.**
> Contributions (bps of allocated capital): +350, +180, +90, +60, +40, +25, +10, −15, −30, −55, −120, −200. Total = **+335bps**.
>
> Batting average = 7/12 = **58.3%**. Average winner = 755/7 = **+107.86bps**. Average loser = −420/5 = **−84.00bps**. Slugging = 107.86/84.00 = **1.284x**. Expectancy = (0.5833 × 107.86) + (0.4167 × −84.00) = 62.92 − 35.00 = **+27.92bps**. Tie-check: 27.92 × 12 = **335.0bps** ✓.
>
> **Stress test 1 — remove only the best position (+350):** total = 335 − 350 = **−15bps**. A full year of work goes negative. Batting average barely moves: 6/11 = **54.5%**; expectancy = **−1.36bps**.
>
> Teaching payload: batting average moved 3.8 points while the year moved from +335bps to −15bps. Sizing the right tail *is* the job.

---

### M01-E6 — Mispricing Diagnostic: Form, Forcing Mechanism, Half-Life

**Topics:** Four reasons markets are not efficient; forms of mispricing; limits to arbitrage.

**Learning objective.** Convert the "why are markets inefficient" list from recitation into a diagnostic that sets holding period and sizing.

**Student task.** Eight short historical vignettes (dates and tickers masked). For each: classify the form of mispricing from a supplied six-form taxonomy; name the forcing mechanism; name the constraint preventing the natural arbitrageur from acting; and assign an expected half-life from {hours–weeks, 1–4 quarters, 1–3 years, may never close}. **40 minutes.**

**Tools and environment.** Existing quiz platform; custom vignette bank.

**Grading rubric.**
- *Quantitative (60 pts, auto-gradeable):* four tagged fields per vignette against a key. Partial credit where two classifications are defensible — the key stores accepted alternates with reasons.
- *Qualitative (40 pts, LLM-graded):* the arbitrageur-constraint field is the one that separates students. Full credit names a *specific* constraint (borrow cost, mandate restriction, index rule, drawdown limit, redemption terms, capacity), not "people are irrational."

**Difficulty.** Intermediate–advanced. **Build complexity.** Low–medium (vignette authoring is the work).

**Example and worked answer.**
> *Vignette 5:* A mid-cap trades down 23% over nine sessions on no company news. Over the same window, a large multi-manager platform is widely reported to be reducing risk; the name screens in the top decile of "crowded hedge fund long" baskets; short interest is 3% of float; consensus estimates are unchanged; the next earnings date is seven weeks away.
>
> **Model answer:** Form = *technical/flow* (de-grossing, not fundamentals — estimates unchanged and no news). Forcing mechanism = exhaustion of the forced selling, plus the earnings print in seven weeks as a fundamental re-anchor. Arbitrageur constraint = the natural buyers are the same crowded funds now under their own risk limits, so the capital that would normally arbitrage this is being withdrawn exactly when the mispricing is largest — textbook performance-based arbitrage. Expected half-life = hours–weeks.
>
> **Common wrong answer:** classifying it as *estimate/level* mispricing. Estimates are explicitly unchanged; nothing about the numbers is wrong. Marking this as a fundamental mispricing is the error that leads a junior to write a 30-page deep dive on what is a two-week flow event.
## Module 02 — Life on the Buy-Side

### Expected content coverage

**Scope.** The institutional-context module: who's who, who pays for what, what each seat is optimising, and where the legal line sits. Deceptively important — most of the junior failures in later modules trace to not knowing what the PM is optimising.

| Topic | What mastery looks like |
|---|---|
| Buy-side structure and roles | Seat taxonomy (CIO, PM, senior/sector analyst, junior, risk, trading, compliance, IR). FE's own role arc: **"idea processor → resident industry expert"**, ending at M15's "junior to full-stack partner." |
| LPs and their goals | LP type determines **redemption terms → permitted holding period → which kind of mispricing the fund is allowed to trade.** A fund financed by quarterly-liquidity fund-of-funds money literally cannot hold a three-year limits-to-arbitrage thesis. This is Shleifer–Vishny with a cap table. |
| Single-manager vs multi-manager | Caughran's own numbers: pods run **"$2–$4 of borrowing for every $1 of equity"** and aim to turn **3–5% returns on gross into 10–20% on equity**. Drawdown limits exist formally or informally because the GP cannot let one PM leave a hole in levered equity — **"PMs will hit drawdown limits and get fired."** |
| Long-only business model | Fee compression (active US equity ~0.58% asset-weighted vs 1.00% equal-weighted in FY2025 Morningstar data; passive now >50% of long-term fund assets). The capacity trap: scale is both the cure for fee compression and the cause of alpha decay. A long-only analyst's "short" is an **underweight**, bounded below by a 0% weight. |
| Active share / tracking error | Active Share = ½ Σ|w_fund − w_index| over the union of holdings. Cremers–Petajisto's point: you need **two** dimensions — Active Share for stock selection, tracking error for factor deviation. |
| Analyst role and investment process | The stage-gate pipeline with explicit kill criteria at each gate; the PM check-in is the cheapest kill and the one juniors skip because they want to present finished work. |
| Information edge | The legal boundary. The buy-side bet is against **semi-strong** efficiency. Mosaic theory, Reg FD, expert-network chaperoning, pre-clearance, restricted lists. |
| Anatomy of a top analyst | FE's own trait list (from its info-session deck): analytics, communication, creativity, tenacity, **self-containment**, common sense, passion & work ethic, and an X-factor described as "a nose for money and intuition." |
| Repeatable process | A written process you could hand to someone else, plus a documented track record of calibrated judgment. |

**Prerequisites.** LP/GP structure; management vs incentive fee; lock-up, gate, high-water mark; long/short mechanics; beta; gross vs net exposure; notional vs capital. The single most common slip: percentages of *gross* vs percentages of *capital*.

**Junior vs. strong.** A junior pitches a thesis. A strong analyst pitches a thesis *plus* a sizing recommendation in bps of sleeve, the position's factor footprint, borrow cost, the ADV constraint, path risk around the next two prints, and a stop level — an idea the PM can actually implement without breaching anything.

**Research provenance.** Pod risk limits (the ~5% halve-risk / ~7.5% terminate ladder, 4–8x gross, single-name and industry caps, PM payout 10–20% of pod net P&L) are **crowd-sourced and firm-unconfirmed** — funds do not publish them, and sources conflict on the net-exposure band (−20/+20 vs −10/+10). **Design rule: always state the limit set in the exercise prompt and have students compute consequences. Never ask "what is Millennium's stop-out?" — the honest answer is "not publicly disclosed."** Firm AUM and pod counts likewise conflict across sources; use them only as narrative scale.

---

### M02-E1 — Same Idea, Three Seats *(flagship for this module)*

**Topics:** Buy-side structure; LPs; single- vs multi-manager; long-only model; investment objectives.

**Learning objective.** Internalise that an idea's value is seat-dependent — the central insight of the module and the thing that makes later pitch exercises gradeable.

**Student task.** Student receives one fully specified investment idea (thesis, 30% upside over 24 months, a −15% interim drawdown risk around a regulatory decision in month 7, $600m market cap, 11-day ADV to build the position, 2.9x borrow on the short leg of the pair) plus three seat descriptions: a multi-manager pod (stated: $200m sleeve, 4x gross, −5% halve / −7.5% terminate, 1-month LP liquidity), a Tiger-style single manager (stated: 1.3x gross, 55% net long, annual liquidity with a soft lock), and a benchmark-relative long-only ($20bn AUM, 3% tracking-error budget, stock is 0.04% of the index). For each seat: can this idea be owned? At what size? What changes about *how you would pitch it*? What would you have to add to the work? **60 minutes, written, 800 words max.**

**Tools and environment.** Existing: any text editor. No custom build. Data pack is templated.

**Grading rubric.**
- *Quantitative (40 pts, auto-gradeable):* six required computations — position size as % of sleeve under the pod's single-name cap; days-to-build at 10% of ADV; the drawdown arithmetic showing a −15% interim move on a correctly sized pod position against remaining risk budget; maximum expressible position in the long-only given the index weight; the borrow drag over 24 months; the gross-exposure impact. Tolerance ±2%.
- *Qualitative (60 pts, LLM-graded with human spot-check):* 20 pts — correctly concludes the pod **cannot** own this at meaningful size because of path risk, not thesis quality, and says so explicitly; 15 pts — identifies that the long-only's constraint is capacity and index weight, not conviction; 15 pts — the "how you'd pitch it differently" section differs materially across the three seats rather than restating the thesis; 10 pts — names the LP liquidity link in at least one seat.
- **Critical-failure marker (caps score at 50):** any answer concluding the idea is simply "good" or "bad" without seat-conditioning. That is the error the exercise exists to detect.

**Difficulty.** Intermediate. **Build complexity.** Low (templated prompt + LLM rubric).

**Example and worked answer (partial).**
> *Pod seat.* Correct single-name cap at 2% of an $800m gross book = $16m. A −15% interim drawdown on $16m = −$2.4m = **−1.2% of the $200m sleeve**. That alone is a quarter of the way to the halve-risk trigger from one position, before anything else in the book moves. With the regulatory decision in month 7 and a 24-month horizon, the pod is being asked to hold path risk it is structurally unable to hold. Correct answer: **ownable only as a small, hedged, pre-catalyst position, or not at all** — and the pitch must lead with the path, not the upside.
> *Long-only seat.* Index weight 0.04%, so the maximum active overweight a 3%-tracking-error fund would realistically take is a few multiples of that — call it 0.15%, i.e. $30m on $20bn. At 11 days to build, that is feasible. Here the binding constraint is **materiality**: a 30% move on a 0.15% position adds 4.5bps to the fund. Correct answer: ownable, trivially immaterial, and therefore probably not worth the analyst's hours — a different kind of "no."

---

### M02-E2 — Pod Economics and the Cost-Drag Trap

**Topics:** Single- vs multi-manager structures; investment objectives; fee structures.

**Learning objective.** Make the student fluent in returns-on-gross vs returns-on-capital, and show them that pod costs are fixed in gross terms, so halving the gross return more than halves the payout.

**Student task.** Build a pod P&L and payout model from stated terms, then run a three-point sensitivity on return-on-gross and explain the non-linearity in 100 words. **40 minutes.**

**Tools and environment.** Existing: Excel/Sheets with a named-output template (cells pre-labelled for auto-grading).

**Grading rubric.**
- *Quantitative (85 pts, fully auto-gradeable via named ranges + perturbation test):* gross P&L, costs, pod net P&L, return on allocated capital, payout pool, firm retention, and all three sensitivity cases. **Perturbation check worth 20 of the 85:** the grader changes the return-on-gross input and verifies outputs move correctly, which distinguishes a live model from hardcoded numbers.
- *Qualitative (15 pts, LLM-graded):* the written explanation must identify that costs are fixed as a percentage of *gross*, not of P&L. An answer that says "costs went up" scores zero.

**Difficulty.** Beginner–intermediate. **Build complexity.** Medium (template + auto-grader with perturbation).

**Example and worked answer.**
> Terms: $200m allocated capital, 4.0x gross, dollar-neutral ($400m long / $400m short), 4.00% return on gross, financing + borrow + commissions 0.75% of gross, PM payout 15% of pod net P&L.
>
> Gross exposure = 200 × 4.0 = **$800m**. Gross P&L = 0.0400 × 800 = **$32.0m**. Costs = 0.0075 × 800 = **$6.0m**. Pod net P&L = **$26.0m**. Return on allocated capital = 26.0/200 = **13.00%** — which sits inside Caughran's stated "3–5% on gross → 10–20% on equity." Payout pool = 0.15 × 26.0 = **$3.9m**. Firm retains 26.0 − 3.9 = **$22.1m**.
>
> **Sensitivity (the teaching payload).** At 2.00% on gross: gross P&L = 0.02 × 800 = $16.0m; costs still $6.0m; net = **$10.0m**; ROE = 10/200 = **5.0%**; payout = 0.15 × 10 = **$1.5m**. So **halving the return on gross (4.00% → 2.00%) cuts the payout by 61.5%** (1.5/3.9 − 1). At 4.00% return, costs consume 18.75% of gross P&L; at 2.00%, they consume 37.5%.

---

### M02-E3 — Dollar-Neutral Is Not Beta-Neutral

**Topics:** Single- vs multi-manager; alpha vs factor; risk limits.

**Learning objective.** The single best diagnostic in the module: a book can report zero net dollar exposure while carrying large net market risk.

**Student task.** Given long and short book notionals with weighted-average betas, compute net dollar beta, beta-adjusted net exposure as a multiple of capital, and the P&L from a stated market decline. Then propose two routes to beta-neutralise and state which breaches the gross limit. **30 minutes.**

**Tools and environment.** Existing: spreadsheet or even pen and paper.

**Grading rubric.**
- *Quantitative (80 pts, fully auto-gradeable):* five numeric answers, tolerance ±1%.
- *Qualitative (20 pts, LLM or human):* must identify that growing the short book raises gross and may breach the gross limit, which is *why* an index overlay is the usual answer.

**Difficulty.** Intermediate. **Build complexity.** Low.

**Example and worked answer.**
> Long book $400m at weighted-average beta 1.15; short book $400m at beta 0.85; allocated capital $200m. Net dollar exposure = 400 − 400 = **$0** ("dollar neutral").
>
> Dollar beta long = 400 × 1.15 = **$460m**. Dollar beta short = 400 × 0.85 = **$340m**. Net dollar beta = **$120m**. Beta-adjusted net exposure = 120/200 = **0.60**, i.e. the pod is **60% of capital net long the market** while reporting zero net dollar exposure.
>
> If the market falls 10%: P&L from market direction alone = −0.10 × 120 = **−$12.0m** = **−6.00% of allocated capital** — past the 5% halve-risk trigger and within 150bps of a 7.5% termination level, **with every single stock call correct.**
>
> Route (a): grow the short book at the same average beta. Required short notional = 460/0.85 = **$541.18m**, an incremental $141.18m, which raises gross from $800m to **$941.18m** and may breach the gross limit. Route (b): short $120m notional of a beta-1.0 index instrument. Gross rises only $120m and the pod keeps its single-name risk budget for alpha. **(b) is the usual answer, and the reason is the gross constraint, not the hedge quality.**

---

### M02-E4 — The MNPI Line: Compliance Station

**Topics:** Leveraging information edge; buy-side mindset; the legal boundary.

**Learning objective.** Produce reliable, fast judgment at the legal line — and the reflex to stop talking and call compliance.

**Student task.** Ten short scenarios delivered one at a time (an expert call where the consultant starts describing their current employer's unannounced quarter; an IR contact who volunteers a number not in the release; a supplier's comment at a conference; a 13D rumour from a broker; a data vendor whose panel appears to include a single dominant retailer's own POS data). For each: proceed / proceed with constraints / stop and escalate, plus one sentence of reasoning and the specific action. **35 minutes.** Then one 10-minute role-play: an AI "expert" who, if not interrupted, will volunteer material non-public information at turn 4.

**Tools and environment.** Scenario bank (low build) + voice/text role-play agent (high build, shared with M09's management-meeting station).

**Grading rubric.**
- *Quantitative (50 pts, auto-gradeable):* the three-way classification per scenario against a key reviewed by counsel. **Scenarios are deliberately weighted so that two are genuinely ambiguous and score full marks for "stop and escalate" with sound reasoning.**
- *Qualitative (50 pts; checklist from the transcript + LLM global rating):* the role-play is scored on a **binary, deterministic checklist** — did the student interrupt before the MNPI was fully disclosed; did they say the words that terminate the call; did they report it. Interrupting at turn 4 or earlier = full marks; allowing full disclosure = critical failure regardless of what they say afterwards.
- **This station needs legal review of the answer key before deployment, and the key should cite Reg FD and the relevant CFA Standard on material non-public information rather than paraphrasing.**

**Difficulty.** Intermediate. **Build complexity.** Low for the scenario bank; high for the role-play (but the engine is shared with M09 and M14).

**Example task prompt.**
> *Scenario 6.* You are 18 minutes into a paid expert call. The expert, a former regional VP who left the company 5 months ago, says: "I still talk to my old team every week. I can tell you the October comps are running —" **What do you do, in the next five seconds?**
>
> **Model answer (full credit):** Interrupt immediately, before the number. State that you cannot receive non-public information about current-period performance, that the expert should not share anything their former employer would consider confidential, and that you need to limit the discussion to their own historical experience and general industry dynamics. Terminate if they persist. Report the exchange to compliance the same day and note it in the call log. **The reflex — interrupting mid-sentence — is the graded behaviour.** A student who lets the sentence finish and then says "I shouldn't have heard that" has already failed the station: the information is now in their head and the fund has a problem.

---

### M02-E5 — Reading the Mandate Off the Cap Table

**Topics:** LPs and their investment goals; investment objectives; repeatable process.

**Learning objective.** Teach the inference chain from LP base → redemption terms → holding period → tradeable mispricing types.

**Student task.** Given three fund fact sheets (LP composition, redemption terms, gate/lock-up provisions, stated strategy, historical max drawdown), and the six-form mispricing taxonomy from M01-E6, state for each fund which mispricing forms it can and cannot harvest, and why. Then: one of the three funds has a mismatch between its stated strategy and its liquidity terms — identify it and say what will break. **45 minutes.**

**Tools and environment.** Existing. Templated fact sheets.

**Grading rubric.**
- *Quantitative (30 pts, auto-gradeable):* the mapping grid (3 funds × 6 mispricing forms, permitted/not) scored against a key with accepted alternates.
- *Qualitative (70 pts, LLM-graded):* 30 pts — correctly identifies the mismatched fund and names the specific mechanism (e.g. a three-year deep-value strategy financed by fund-of-funds money with quarterly liquidity and no gate, which will force selling into exactly the drawdown the strategy requires it to hold through); 25 pts — reasoning chains LP → terms → horizon → mispricing type rather than asserting; 15 pts — written clarity.

**Difficulty.** Advanced. **Build complexity.** Low.

**Example and worked answer (the mismatch item).**
> *Fund B:* "Concentrated deep value, 12 positions, 3–5 year holding period, targets 2x on entry." LP base: 70% fund-of-funds, 20% family office, 10% GP capital. Terms: quarterly redemption, 45 days' notice, no gate, no lock-up. Historical max drawdown 34%.
>
> **Model answer:** The strategy requires holding through multi-year drawdowns in illiquid, out-of-favour names; the liability structure permits 70% of the capital to leave within 45 days of any quarter-end, with no gate to stop it. A 34% drawdown in a fund-of-funds-dominated book will trigger redemptions precisely at the bottom, forcing liquidation of the most illiquid positions at the worst prices — which deepens the drawdown and triggers more redemptions. This is performance-based arbitrage with no circuit breaker. The fix is structural, not analytical: longer lock-ups, a gate, or a different LP base. **Full credit requires naming the feedback loop, not just saying "the terms are too short."**
## Module 03 — Thesis Development

### Expected content coverage

**Scope.** The module that turns a promising name into a defensible, falsifiable, communicable view. The course's single most structured module, and the one that most needs assessment because its output is an *artifact* you can grade.

**The nine-step thesis development process.** Recovered with high confidence as to step names and ordering, from two independent artifacts:

1. Expertise Development → 2. Promising Idea → 3. Model Construction → 4. Structured Due Diligence → 5. Expectations & Valuation Work → 6. Core Debate & Tailored Diligence → 7. Differential Insight → 8. Thesis Construction → 9. Presentation, Feedback & Monitoring

**Provenance warning — read before building an answer key.** The exact ordered string above was glyph-confirmed, but **only on a leaked Fundamental Edge deck** ("Thesis Development vFINALsplitPart 2," marked *strictly confidential*, hosted on a third-party study-notes site and even carrying a bogus "UC Berkeley" attribution). **That source is not citable.** The step *names* have a second, independent corroboration from FE's own public info-session deck, so they are high-confidence; the **substance of each step is unpublished anywhere.**

A separate, legitimate find explains a confusion you will otherwise hit: Caughran published an **"8 STEP PROCESS TO THESIS CREATION"** thread in 2022 that in fact enumerates a ninth step ("Trading plan"). That public 2022 idea→pitch→trade pipeline is best read as the **ancestor** of the Module-03 process, not the same list — Module 03 front-loads "Expertise Development" and folds the trading plan into monitoring. **Treat Module 03's nine steps as authoritative and the 2022 thread as the citable public version.**

If you are Fundamental Edge, overwrite the per-step content below from your own deck. If you are not, decide whether leaked course material belongs in your source list at all — I have flagged its provenance rather than laundering it.

**The non-obvious design feature, and the thing to build assessment around:** *Core Debate* sits at step 6, **after** expectations and valuation work (step 5). That ordering is a substantive pedagogical claim — you cannot know what the real debate is until you know what is priced in. And steps 6→7 are where the alpha is: everything before step 6 is table stakes that any competent analyst produces.

| Topic | What mastery looks like |
|---|---|
| Thesis-driven investing | Caughran, verbatim: *"A thesis is not a book report on a stock. Let me repeat, A THESIS IS NOT A BOOK REPORT ON A STOCK."* A thesis is "a package of research and analysis, distilled to its key elements, highlighting where the research is differential, communicated to the decision maker succinctly." |
| FEV framework | **F**undamentals / **E**xpectations / **V**aluation. Caughran's own origin post calls it "a simple stock selection framework." Used in two distinct roles: a **diligence scaffold** here in M03, and an **idea screen** in M05/M15. The E-leg is rendered as "what do we believe is true, and where is the expectations gap?" |
| Model as the analytical tool | The model's job is to locate variance, not to produce a number. Caughran, verbatim: *"The basic act of modeling is a necessary but non-differentiating factor… The model is just table stakes, a 'thinking tool.'"* |
| Key drivers and differentiated insight | Max three key drivers. If you have seven, you have none. "Variant perceptions only come about by deep industry knowledge and careful, disciplined research." |
| Variant perception | Steinhardt's term. Worth a definitional correction students usually get wrong: the common gloss "a non-consensus view that turns out right" is **looser than and different from** Steinhardt's — variant perception is a property of the *ex-ante analysis*, not of the outcome. |
| Thesis construction and delivery | Succinct, focused, humble. Lead with the conclusion. |
| Idea maintenance | Monitoring the pre-named key drivers and the catalyst calendar — **not** watching the price. In practice this is where most of a pod analyst's hours go and where most P&L is saved. |
| Coverage models and "thesis development latency" | **Genuinely ambiguous and unsourced** — see below. |

**"Coverage models impact thesis development latency" — flagged as the weakest bullet in the module.** No FE definition exists anywhere; searching the exact phrase returns only the syllabus itself. The bullet is also genuinely ambiguous between two readings: (a) *your seat's* coverage model — a deep sector specialist has high latency to a first idea but low marginal cost thereafter, while a go-anywhere generalist has the reverse; or (b) *sell-side* coverage density — a name with 25 analysts covering it has a tighter expectations distribution and so less latent mispricing than an orphaned small-cap. Both are defensible and both are useful. **Resolve with FE before writing an item keyed to either.**

**Prerequisites.** M01 (alpha load, forms of mispricing); M02 (seat and mandate); the ability to read a 10-K and build a simple driver model; basic probability and expected value.

**Junior vs. strong.** Junior: "I think it goes up." Strong: "Base case $128 at 55%, bull $155 at 20%, bear $84 at 25%; EV +12%; reward/risk 2.0:1; breakeven probability 33%; I am wrong if Q2 bookings grow below 6% or the new entrant's pricing holds below $X; I cut at $88 or on either signal; I revisit sizing after the September guide."

---

### M03-E1 — Stage-Gate Autopsy: Where Should This Have Died?

**Topics:** Nine-step process; coverage models and latency; efficient vetting.

**Learning objective.** Teach the *economics* of the process — that each gate exists to kill cheaply, and that the cost of a missed kill compounds. This is the inverse of how students instinctively think about a research process.

**Student task.** Student receives a complete, realistic 22-page research file on a name that ultimately did not work: the original screen output, the triage note, the first model, the diligence log with dated entries, four expert-call summaries, the valuation work, and the final (losing) thesis memo. Task: identify the **earliest** point in the file at which the idea should have been killed, cite the specific evidence that was already available at that point, and state which of the nine steps failed. Then: write the one-paragraph kill note that should have been written. **75 minutes.**

**Tools and environment.** Custom case file (templated; reusable across cohorts). Existing text tools otherwise.

**Grading rubric.**
- *Quantitative (40 pts, semi-auto):* the identified kill point is scored against a key as an *ordinal distance* — the key names the correct gate, and the student loses 8 pts per gate of distance in either direction. Citing the specific dated evidence is machine-checkable against a list of accepted evidence IDs (20 of the 40).
- *Qualitative (60 pts, LLM-graded, human spot-check 20%):* 25 pts — the failure is attributed to a *process* failure (e.g. diligence was confirmation-seeking; the core debate was never written) rather than to bad luck or a bad outcome; 20 pts — the kill note is specific and falsifiable, in the voice of a note to a PM; 15 pts — the student does **not** use information that only became available later in the file. **Hindsight leakage is the main failure mode and must be penalised explicitly** — the grader is given the file's date index and instructed to flag any reasoning that depends on a later-dated document.
- **Critical-failure marker:** an answer whose core claim is "the thesis was wrong because the stock went down" caps at 30. That is resulting, not analysis.

**Difficulty.** Advanced. **Build complexity.** Medium (the case file is the build; the grader is light).

**Example task prompt.**
> *From the diligence log, day 9:* "Call with former regional sales director. Confirmed our view that the new product is gaining traction — he said 'the reps are excited about it.' Also mentioned pricing pressure in the legacy line but said he wasn't close to that business."
>
> **Model answer for this entry:** This is the earliest evidence of the failure. The analyst recorded the confirming datapoint ("reps are excited") as a finding and discarded the disconfirming one (legacy pricing pressure) on the grounds that the source wasn't close to it — which is a reason to go find someone who *is*, not a reason to drop the thread. The legacy line was 61% of revenue (per the model built on day 6). The core debate was therefore mis-specified from day 9 onward: the analyst was debating new-product adoption when the stock turned on legacy price/mix. **The process failure is step 4 (Structured Due Diligence) feeding a wrong step 6 (Core Debate).** Full credit requires naming the 61% revenue weighting, because that is what makes the misallocation of diligence hours objectively wrong rather than a matter of taste.

---

### M03-E2 — Core Debate Identification *(flagship for this module)*

**Topics:** Core debate; key drivers; differentiated insight; FEV.

**Learning objective.** The highest-value single skill in the module: stating, in one sentence, the question the stock actually turns on. Gradeable because expert keys converge on it far more than students expect.

**Student task.** Six data packs, each ~15 pages (business description, segment financials, consensus estimates and revision history, the last two transcripts' Q&A sections, a price/multiple history, and ownership data). For each: write the core debate as a single question, name the three key drivers in priority order, and state for each driver what the market currently assumes and what evidence would resolve it. **90 minutes for all six — deliberately tight, about 15 minutes per name.**

**Tools and environment.** Custom data packs. Existing text tools.

**Grading rubric.**
- *Quantitative (45 pts, semi-auto):* key-driver identification scored against an expert key using a controlled vocabulary — each pack's key lists the 3 correct drivers plus 4 plausible-but-secondary and 4 wrong ones, with partial credit. Priority ordering scored by rank correlation. This is auto-gradeable once the vocabulary is built.
- *Qualitative (55 pts, LLM panel, reference-guided with the expert key supplied to the grader):* 25 pts — the core debate is phrased as a *question with a resolvable answer* rather than a topic ("Can they hold gross margin above 42% as the mix shifts to the OEM channel?" not "margin sustainability"); 20 pts — "what the market assumes" is stated as a **number tied to a named consensus line item**, not a sentiment; 10 pts — the resolving evidence is something the analyst could actually obtain.
- **Inter-rater note:** in piloting, require two human raters on 25% of packs and report quadratic weighted kappa. The core-debate dimension is the one most likely to drift; anchor it with three pre-scored exemplars per pack at the top, middle and bottom score points.

**Difficulty.** Intermediate–advanced. **Build complexity.** Medium (6 packs + controlled vocabulary + anchor exemplars).

**Example and model answer.**
> *Pack C:* A $4bn-cap specialty chemicals business. Two segments: Performance Additives (62% of revenue, 24% EBITDA margin, growing 3%) and Advanced Materials (38%, 31% margin, growing 14%). Consensus FY+1 EBITDA $412m, revised +2.1% over six months. Trades 11.2x EV/EBITDA vs. a 5-year range of 8–13x. Last two calls: management guided to "mid-teens" Advanced Materials growth and was asked three times about Additives pricing, answering twice with volume commentary instead of price.
>
> **Model core debate:** "Is Advanced Materials' 14% growth and 31% margin durable enough to re-rate the whole company, or does Additives pricing deflation cap group EBITDA such that the sum-of-the-parts argument never gets paid?"
>
> **Model key drivers, in order:** (1) Additives realised price/mix — because at 62% of revenue it dominates group EBITDA and management has now dodged the question three times, which is itself the strongest available evidence; (2) Advanced Materials incremental margin, because the re-rating case requires the mix shift to lift group margin, and that depends on incrementals, not on segment margin levels; (3) the multiple's dependence on segment disclosure — whether the company will break out enough for the market to value the parts separately.
>
> **Common wrong answer:** making Advanced Materials growth the first driver. It is the *narrative* driver and the one management talks about, but at 38% of revenue it cannot move group EBITDA as much as a 200bp price move in the 62% segment. Students systematically rank the growth segment first because that is what the transcript emphasises — which is precisely the error the item detects. The management evasion pattern is the tell, and a strong analyst reads three dodges as information.

---

### M03-E3 — The Falsification Clause

**Topics:** Thesis construction; idea maintenance; pre-mortem.

**Learning objective.** Convert a thesis from an assertion into a falsifiable claim with pre-committed kill criteria — the discipline that prevents thesis creep later.

**Student task.** Given a complete, well-written thesis memo that contains **no falsification conditions**, write: three specific kill criteria (each a named metric, a threshold, and a date by which it resolves); the trading plan (add level, trim level, stop, max size, review date); and a pre-mortem of ≤300 words written from a point 12 months in the future in which the thesis has failed, working backward to the cause. **50 minutes.**

**Tools and environment.** Existing. Templated memo.

**Grading rubric.**
- *Quantitative (35 pts, auto-gradeable from structured fields):* each kill criterion must parse into {metric, threshold, direction, resolution date}. A criterion that cannot be mechanically evaluated at a future date scores zero — "if the competitive environment deteriorates" is not a kill criterion. This is a hard, objective, and genuinely discriminating check.
- *Qualitative (65 pts, LLM panel):* 25 pts — the kill criteria attack the *thesis's load-bearing assumptions* rather than listing generic risks (a grader is given the memo's three key drivers and checks correspondence); 20 pts — the pre-mortem identifies a failure mode **not** already listed in the memo's own risk section, i.e. it generates new information rather than restating; 20 pts — the trading plan's stop level is consistent with the stated bear case rather than an arbitrary round number.
- **The 20-pt "new failure mode" dimension is the most valuable thing in this exercise** and is also the hardest to grade: supply the grader with the memo's risk section verbatim and require it to quote the student's novel failure mode and assert non-overlap.

**Difficulty.** Intermediate. **Build complexity.** Low–medium.

**Example and worked answer.**
> *Thesis excerpt:* "We think consensus underestimates the attach rate of the services bundle. We model 38% attach by FY+2 vs. the Street's implied 29%, worth $0.44 of incremental EPS, and we see $92 fair value vs. $71 today."
>
> **Model kill criteria (full credit):**
> 1. *Metric:* disclosed services attach rate. *Threshold:* below 32% as of the FY+1 Q4 print. *Resolves:* the Q4 release, est. late February. *Rationale:* 32% is the level below which the $0.44 EPS bridge cannot arithmetically close by FY+2 even on a straight-line ramp from there.
> 2. *Metric:* services gross margin disclosed in the segment footnote. *Threshold:* below 55%. *Resolves:* the 10-K. *Rationale:* the thesis assumes attach is accretive; below 55% the mix shift is margin-neutral and the re-rating case fails even if attach hits 38%.
> 3. *Metric:* the two largest channel partners' own disclosed bundled-sales commentary. *Threshold:* either partner guiding bundle attach down. *Resolves:* their Q2 prints, which both precede ours. *Rationale:* a free leading indicator with a date earlier than our own catalyst.
>
> Note what makes criterion 1 strong: the threshold (32%) is **derived from the thesis's own arithmetic**, not picked. A student who writes "below 30%" without showing why 30% breaks the bridge gets partial credit; the derivation is the skill.

---

### M03-E4 — Expectations-Before-Debate (the step 5→6 ordering test)

**Topics:** The nine-step process ordering; FEV's E-leg; model as thinking tool.

**Learning objective.** Demonstrate experientially why the course puts core debate *after* expectations work — students who skip step 5 pick the wrong debate.

**Student task.** Two-phase, with a commitment device. **Phase 1 (20 min):** given only the business description and historical financials, write the core debate and three key drivers. Submit — it locks. **Phase 2 (40 min):** now receive consensus estimates by line item, the current multiple vs. history, the implied growth from a supplied reverse-DCF, and positioning data. Re-write the core debate and drivers. Then write 200 words on what changed and why.

**Tools and environment.** Needs a platform that can lock Phase 1 before revealing Phase 2 — low-to-medium build, or runnable manually in a live cohort session.

**Grading rubric.**
- *Quantitative (40 pts, auto):* Phase 2 drivers scored against the expert key (as M03-E2). Phase 1 is **not** scored for correctness — it is scored only for completion, because its purpose is to create the contrast.
- *Qualitative (60 pts, LLM-graded):* 35 pts — the reflection correctly identifies *which* specific expectations datapoint changed the debate and why (e.g. "the reverse-DCF implies 9% terminal growth, so the debate is not whether they grow but whether the market's duration assumption survives, which is a completely different question from the one I wrote in Phase 1"); 25 pts — intellectual honesty, i.e. the student does not retrofit Phase 1 as having been right all along. **The grader is given both submissions and explicitly instructed to detect retrofitting.**
- This is the rare exercise where **the delta between two submissions is the measured quantity**, which makes it unusually robust to prior knowledge: a student who already knew the name still has to show the reasoning shift.

**Difficulty.** Intermediate. **Build complexity.** Medium (two-phase locking).

**Example.**
> *Phase 1 stimulus (financials only):* revenue 6-yr CAGR 11%, gross margin 68% stable, EBIT margin expanded 14% → 22%, FCF conversion 95%, ROIC 24%, net cash.
> *Typical Phase 1 answer:* "Core debate: can they sustain double-digit growth?" — reasonable, and almost always wrong.
> *Phase 2 stimulus adds:* trades 34x NTM EPS vs. 5-yr range 19–37x; consensus has revenue growth decelerating to 9% then 8%; the supplied reverse-DCF implies 8 years of 12% growth at current margins to justify the price; 94th-percentile hedge-fund crowding.
> **Model Phase 2 answer:** "Core debate: the market is already underwriting *more* growth than consensus publishes — 12% for eight years versus a consensus fading to 8%. So the debate is not whether growth is double-digit; it is whether the **duration** of the growth runway is eight years or four, and the crowding means the stock is priced for the long answer with no margin for a single disappointing print." Full credit requires naming the eight-year implied duration — that is the number that reframes the question, and it was invisible in Phase 1.
## Module 04 — Why Stocks Move Up and Down

### Expected content coverage

**Scope.** The mechanics module: what actually moves a price over different horizons, and how to decompose a move into its parts. Together with M10 this is the analytical heart of the course.

| Topic | What mastery looks like |
|---|---|
| Supply and demand; market price as capital-weighted consensus | Price is the capital-weighted marginal opinion, not the average opinion. The wisdom-of-crowds conditions (cognitive diversity, effective aggregation, meaningful incentives) and the fact that **diversity is the one that breaks** — which is what a crowded trade or a de-grossing is. |
| The four driver families | Fundamentals, expectations, valuation, and non-fundamental factors. Caughran's horizon claim: over short windows price reflects positioning, sentiment and flows; **"fundamentals are all that matter with an investment horizon longer than 3 months."** |
| Stock price vs. business value | Two different objects on two different clocks. The weighing machine is the earnings stream; the voting machine is the multiple. |
| EPS growth, revisions, re-ratings | **Caughran's own evidence (March 2024):** of the top 25 S&P 500 YTD performers, **25 of 25** had positive EPS or revenue revisions; of the bottom 25, **24 of 25** had negative revisions, with P/E change "notable, but not dramatic." Revisions do the work, not re-rating. |
| Return decomposition | Total return = EPS growth + multiple change + the **cross term** (+ shareholder yield). The cross term is negligible over one year and material over three — which is itself the horizon lesson. |
| Risk reduction and visibility | A 50bp fall in the discount rate on a long-duration multiple is worth more than most earnings beats. This is why de-risking events re-rate stocks more than good quarters do. |
| Non-fundamental drivers | Index inclusion/rebalance, passive flows, factor rotations, vol-control and CTA flows, dealer gamma, de-grossing cascades, tax-loss selling, lockups, buyback blackouts. Crucially: **the index effect has decayed** — one study's migration returns fall from ~6.7% (late 1990s) to ~2.7% (2000s) to ~−1.8% (2010s), and another finds the announcement effect has "disappeared." Teaching the 1990s version of this as current is a live error. |
| Inflections and themes | The second derivative is what re-rates a stock; the first derivative is already priced. |

**Proprietary terms — provenance.** **"Focus Five"** is named in the syllabus but **its five components are unverified.** The only recovered trace of Caughran's own words is from a disfluent, machine-generated podcast transcript: *"organic revenue, growth, margin, sort of trajectory, margins, capital intensity, capital deployment, and terminal value visibility"* — which does not cleanly parse into five items. A separate critical distinction surfaced in research and should be preserved: **Focus Five ≠ "the three key drivers."** Focus Five is a universal value-driver taxonomy applied to every name; the three key drivers are the stock-specific subset that is both material *and* contested. Conflating them would look like not having read the material. **"Model linkage," "exceptionalism," "perception shifts"** and **"the 7-Year Test"** likewise have no retrievable definitions. **Recommendation: assess the *function* (decompose value into its drivers; identify which are contested) using the published Rappaport–Mauboussin value-driver set, not the FE label, until FE supplies the list.**

**Prerequisites.** Multiples; forward vs. trailing EPS; CAGR arithmetic; what a consensus estimate and a revision are; the idea that a multiple is shorthand for a DCF.

**Junior vs. strong.** A junior explains a move by finding a news story that matches its direction. A strong analyst decomposes the move into earnings, multiple and flow components, and can say which part is informative about the business and which is not.

---

### M04-E1 — Return Decomposition with the Cross Term

**Topics:** Disaggregating returns; voting vs. weighing; EPS growth and re-ratings.

**Learning objective.** Own the identity cold, including the cross term most analysts drop, and understand why dropping it is harmless over one year and wrong over three.

**Student task.** For six real historical names (dates masked), decompose the total shareholder return into EPS growth, multiple change, cross term and dividend contribution, over both a 1-year and a 3-year window. Then answer: for which names does the cross term exceed 10% of the total return, and what does that tell you about the character of the return? **50 minutes.**

**Tools and environment.** Existing: spreadsheet with a named-output template. Fully auto-gradeable.

**Grading rubric.**
- *Quantitative (85 pts, fully auto):* all decomposition cells against the key, relative tolerance 1e-3; the three components plus cross term must sum **exactly** to the total (a hard tie-check worth 25 pts on its own — if it doesn't tie, the student has made an algebra error, not a rounding error).
- *Qualitative (15 pts, LLM-graded):* the interpretation must connect a large cross term to the co-movement of earnings growth and re-rating, i.e. a "double-barrelled" return where the market both raised numbers and paid more for them — which is the signature of a perception shift rather than a beat.

**Difficulty.** Beginner–intermediate. **Build complexity.** Low.

**Example and worked answer (fully verified).**
> Entry: price $100.00, forward EPS $5.00, so entry multiple **20.0x**. Hold three years. EPS compounds at 12.0%; exit multiple 17.0x.
>
> EPS₃ = 5.00 × 1.12³ = 5.00 × 1.404928 = **$7.02464**. Exit price = 7.02464 × 17.0 = **$119.4189**. Total return = **+19.41888%**.
>
> Cumulative decomposition: EPS growth **+40.49280%**; multiple change (17/20 − 1) **−15.00000%**; cross term 0.4049280 × (−0.15) = **−6.07392%**. Sum: 40.49280 − 15.00000 − 6.07392 = **+19.41888%** ✓ exact.
>
> Annualised: EPS **+12.00000%**, multiple **−5.27318%**, cross **−0.63278%**, total **+6.09404%**. Check: 1.12 × (17/20)^(1/3) = 1.12 × 0.9472682 = 1.0609404 ✓.
>
> **The horizon lesson:** over one year the cross term here would be 0.12 × (−0.0527) = −0.63pp, which you could ignore. Over three years it is −6.07pp, or **31% of the magnitude of the total return**. Over three years you cannot ignore it.
>
> **Note on shareholder yield, which is the trap:** if you add a buyback-driven share-count reduction as a separate "yield" term, you have **double-counted** — buyback accretion is already inside EPS growth. Only *dividends* belong in a separate (1+y)³ term. Getting this wrong inflates expected return by roughly 200–300bp a year, and it is a standard junior error.

---

### M04-E2 — Flow or Information? The Move Diagnostic *(flagship for this module)*

**Topics:** Non-fundamental factors; supply/demand; perception shifts; drivers.

**Learning objective.** The single most practically valuable skill in the module: when a stock moves 8% and you own it, decide in ten minutes whether anything you believe should change.

**Student task.** Twelve vignettes, each a 1-page evidence pack around a single sharp price move (the move itself, sector and market moves over the same window, estimate-revision activity, volume vs. ADV, short-interest and borrow-fee change, option open-interest change, index-event calendar, any news, and whether peers moved). For each: classify the move as **information / flow / factor / mixed**; state the single piece of evidence that most discriminates; and state what you would do with an existing 200bp long. **60 minutes.**

**Tools and environment.** Custom vignette bank. Deliverable is structured fields, so grading is mostly automatic.

**Grading rubric.**
- *Quantitative (60 pts, auto):* classification against a key with accepted alternates for the two deliberately ambiguous vignettes; the "most discriminating evidence" field is scored against a ranked list (full credit for the top discriminator, partial for second).
- *Qualitative (40 pts, LLM-graded):* the action recommendation must follow from the classification — a flow-classified move with an unchanged thesis should produce "add or hold," and an information-classified move should produce "re-underwrite before acting." **Internal inconsistency between classification and action is the main thing being detected** and should cost most of the 40.
- **Design note:** two vignettes have no clean answer, by design, and the key awards full marks for either classification *with correct reasoning*. Tell students this in advance. It prevents the exercise from teaching false confidence, which would be the opposite of the module's lesson.

**Difficulty.** Intermediate. **Build complexity.** Medium (vignette authoring; the grader is simple).

**Example and model answer.**
> *Vignette 7:* Your 200bp long falls 9.1% over four sessions. The S&P is flat; the sector ETF is −0.8%. No company news, no filings. Consensus FY+1 EPS unchanged across all 14 contributors. Volume 3.4x ADV. Borrow fee moved 40bp → 310bp. The stock sits in the 96th percentile of a widely-followed "hedge fund crowded long" basket, and that basket is −6.2% over the same four sessions while the equal-weight market is flat. Next earnings in six weeks. Two other names in your book, in unrelated sectors, are also down sharply.
>
> **Model answer:** Classification **flow** (de-grossing). Most discriminating evidence: **the crowded-long basket being −6.2% while the equal-weight market is flat, combined with unchanged estimates from all 14 contributors.** Not the volume (consistent with either), not the borrow-fee move (a consequence, not a cause), and crucially not the news vacuum — absence of news is weak evidence on its own. The tell that upgrades this from "no news" to "positioning" is the *basket* move plus your own book's unrelated names moving together. Action: hold or add, subject to sleeve risk limits; nothing you believe has changed, and a de-grossing is a liquidity event with a predictable end. State the limits check explicitly.
>
> **The common wrong answer** is to classify this as information on the theory that "the market knows something." Full credit requires noting that all 14 estimate contributors are unchanged — if someone knew something material, the sell-side distribution would normally show at least one mark. **Partial credit** is available for flagging that de-grossing and genuine information can coincide, which is the honest caveat.

---

### M04-E3 — The Visibility Re-Rating

**Topics:** Risk reduction and visibility impact valuations; perception shifts; re-ratings.

**Learning objective.** Quantify why de-risking moves long-duration stocks more than earnings do — the mechanism behind most large re-ratings and the one juniors systematically under-model.

**Student task.** Given a stock's forward EPS, payout, growth and cost of equity, compute the justified forward multiple. Then compute the multiple and price impact of (a) a 50bp fall in the cost of equity with growth unchanged, (b) a 5% beat with the multiple unchanged, (c) both. Rank the three by price impact and write 150 words on which corporate events in practice produce (a) rather than (b). **40 minutes.**

**Tools and environment.** Existing: spreadsheet. Auto-gradeable.

**Grading rubric.**
- *Quantitative (75 pts, auto):* six numeric answers, tolerance ±0.05x on multiples and ±0.1pp on returns.
- *Qualitative (25 pts, LLM-graded):* the written answer must name real de-risking events — a litigation settlement, a refinancing that removes a maturity wall, a long-term contract renewal, a regulatory approval, the end of a strategic review, a major customer re-signing, cessation of a cash drain — and must explain that these change the *denominator*, not the numerator. An answer that lists "good earnings" as de-risking scores zero on this dimension.

**Difficulty.** Intermediate. **Build complexity.** Low.

**Example and worked answer (verified).**
> Forward EPS $4.00, payout 35%, cost of equity 8.5%, growth 7.10%. Justified forward P/E = payout/(r − g) = 0.35/(0.085 − 0.0710) = 0.35/0.0140 = **25.00x**. Price = 25.00 × 4.00 = **$100.00**.
>
> **(a) Cost of equity falls 50bp to 8.00%, growth unchanged.** P/E = 0.35/(0.080 − 0.0710) = 0.35/0.0090 = **38.89x**. Price = 38.89 × 4.00 = **$155.56**, i.e. **+55.6%**.
>
> **(b) A 5% EPS beat, multiple unchanged.** EPS $4.20 × 25.00x = **$105.00**, i.e. **+5.0%**.
>
> **(c) Both:** 38.89 × 4.20 = **$163.33**, i.e. **+63.3%**.
>
> **Ranking: (c) > (a) > (b), and (a) beats (b) by more than eleven times.** Fifty basis points of perceived risk is worth over 55% here, while a 5% beat is worth 5%.
>
> **The caveat that earns the last points:** this sensitivity is an artefact of a *narrow spread* — r − g is only 140bp, so the multiple is enormously convex in r. A student who notes that the same 50bp on a value stock with r − g = 600bp produces only about +9% has understood the real lesson, which is that **long-duration stocks are where visibility is worth the most**, and that is why they also de-rate violently when visibility is withdrawn.

---

### M04-E4 — Index-Effect Vintage Check

**Topics:** Non-fundamental factors; evidence evaluation.

**Learning objective.** A deliberately contrarian item: teach students that a well-known market effect has **decayed**, and that citing its original magnitude is an error. Doubles as training in reading evidence by vintage.

**Student task.** Given four research abstracts on the index-inclusion effect spanning different sample periods, plus a current situation (a stock about to be added to a major index), the student must: state what the evidence implies the trade is worth *today*; identify which abstract a careless analyst would cite and why it would mislead; and state what they would need to check before trading it. **35 minutes.**

**Tools and environment.** Existing. Abstract pack is the build.

**Grading rubric.**
- *Quantitative (30 pts, auto):* a numeric estimate of the expected effect with a stated range, scored for being in the right neighbourhood (the key accepts a wide band and awards zero for a 1990s-magnitude answer).
- *Qualitative (70 pts, LLM-graded):* 30 pts — correctly identifies that the effect has decayed and attributes the decay to a mechanism (index-fund scale, front-running by arbitrageurs, pre-announcement anticipation, improved liquidity); 25 pts — names what else to check (the float-adjusted size of the required buy relative to ADV, whether the add is pre-announced, whether it is a migration between indices rather than a true add, borrow conditions); 15 pts — appropriately hedges rather than asserting a trade.
- **This item's answer key must be re-verified before each cohort.** The decay is itself a moving target, and an assessment that teaches a stale magnitude commits the exact error it is testing for. Flag the key with a review date.

**Difficulty.** Advanced. **Build complexity.** Low.

**Example.**
> **Model answer skeleton:** Evidence across vintages shows migration/addition returns falling from mid-single-digit percentages in the late 1990s to roughly low-single-digit in the 2000s and to approximately zero or negative in the 2010s, with at least one study finding the announcement effect has disappeared and long-run performance is negative. A careless analyst cites the earliest study — it is the most-quoted and has the largest, most attractive number — and sizes a trade for a 5% pop that no longer exists. Before trading: size the required index-fund buy against float-adjusted ADV; check whether the add was pre-announced and how much has already been front-run; check whether this is a true add or an inter-index migration; and check the borrow if any leg is short. **Full credit does not require a precise number — it requires the student to say the effect is small-to-nil now and to explain why.**
## Module 05 — Idea Generation

### Expected content coverage

**Scope.** Where ideas come from, how you decide in minutes whether one deserves days, and how you get a PM to say yes or no fast. Note a boundary: "durable growth algorithms," "melting ice cubes" and "pair trades" sit under **Module 08** in the brochure, not here.

**The quantitative spine — the "10% mindset" as a prior, not a slogan.** Caughran, verbatim: *"At any given time, I believe the majority of stocks in the market are pretty close to fairly valued. The odds that you are going to throw a dart and find a great thesis are slim."* A podcast rendering puts numbers on it: roughly **80% of stocks mostly fairly priced, with ~10% tails each side carrying meaningful mispricing** — *flagged: machine-transcript paraphrase, verify before printing the numbers.* This converts the slogan into the module's mathematical justification: your job is not to value stocks, it is to find the fifth of the universe where valuation is wrong and spend close to zero time on the rest.

**Idea velocity, with real numbers — the most assessment-relevant fact in the module.** Caughran's stated figures: a long-only analyst produces roughly **3 new ideas a year**; a pod analyst roughly **3 a week**. His own standing goal was about 1 a week off ~40 names. **That is a ~50x spread, which means any exercise here must specify the seat** or it is unanswerable.

| Topic | What mastery looks like |
|---|---|
| Efficiency / avoiding premature deep dives | The triage question, verbatim: *"identify the one thing that matters: what will drive the stock up or down by 15–20%?"* |
| FEV as a screen | Fundamentals / Expectations / Valuation applied as a fast three-lens filter — "what is baked in? what do we believe is true / where is the expectations gap?" |
| Compounders and exceptionalism | ROIC + growth + CAP; the reinvestment runway. **Connor Leonard's four-box taxonomy** (no moat / legacy moat / reinvestment moat / capital-light compounder) maps one-to-one onto the value-driver formula and is the sharpest available framework. Akre's three-legged stool. |
| Change / confusion | Almost certainly Caughran's **"equilibrium, disequilibrium"** idea, from his thread "THE 2 C's: CHAOS & CHANGE": *"The best opportunities come from disequilibrium, either at a company level, an industry level, or a broader markets [level]."* |
| Thematic investing | Theme → TAM → value chain → where margins pool. The purest-play test (one usable quantitative definition: ≥50% of revenue from the theme). Themes are used to *falsify* bull cases as often as to generate them. |
| Pattern recognition | Honestly flagged: **structurally un-installable by a 30-hour course.** What a course *can* do is give students reference classes and base rates as a substitute for experience. |
| Cyclical vs. secular | The two symmetrical errors. Normalisation method, including the specifically named common error: **normalising margins without normalising reinvestment.** The structural test: *did the margin improvement survive the last downturn?* |
| Screening | Lenses as *sensors* where the signal is often **membership change**, not membership. The multiplicative destructiveness of stacked filters. Point-in-time data discipline. |
| Idea vetting with PM check-ins | The cheapest kill in the pipeline, and the one juniors skip. |

**Provenance gaps.** Caughran's enumerated **"idea buckets"** list is not recoverable — the thread exists and compounders are confirmed as bucket #2, but neither the list nor the count could be corroborated. **"Exceptionalism"** has no published definition. Named-but-unrecoverable artifacts include a **"7-Year Test"**, **"5 Dimensions of Equity Fragility"** and an **"NVDA Guided Quick Dive."**

**Prerequisites.** M01 (alpha load — you cannot triage without knowing what you are triaging for); basic screening mechanics; knowing your universe's size.

---

### M05-E1 — The 60-Minute Three-Idea Drill *(flagship for this module)*

**Topics:** Efficiency; screening; FEV; ingredients of compelling ideas; idea velocity.

**Learning objective.** Produce real idea flow under a real clock, at the velocity the student's target seat actually demands.

**Student task.** Student is given a 60-name universe extract (point-in-time financials, multiples vs. own history and peers, revision trends, short interest, ownership change, and a one-line business description each) and must produce **three ideas in 60 minutes**: for each, a one-paragraph FEV sketch, the 15–20% driver, a stated expectations gap with a number, and a proposed next step with an hour budget. They must also submit their **kill list** — the names they looked at and rejected, with a one-phrase reason each. **60 minutes, hard stop.**

**Tools and environment.** Custom universe extract (templated and reusable; built from point-in-time data). Spreadsheet plus text.

**Grading rubric.**
- *Quantitative (50 pts, semi-auto):* 20 pts — did the three ideas include any of the key's "live" names (names that subsequently produced a >15% absolute move within four quarters, from the masked historical record)? 15 pts — kill-list coverage: how much of the universe did they actually triage, scored on a curve, because throughput is the skill; 15 pts — the expectations gap is expressed as a number against a named consensus figure (machine-checkable for the presence of both).
- *Qualitative (50 pts, LLM panel):* 20 pts — FEV sketches are genuinely three-legged rather than three restatements of "it's cheap"; 15 pts — the 15–20% driver is a *driver*, not a characteristic; 15 pts — the proposed next step is proportionate to the hour budget.
- **Scoring asymmetry, stated to students:** finding a live name is worth less than correctly killing 50 names. Over-work is penalised harder than a miss. This inverts student instinct and matches the seat.

**Difficulty.** Intermediate. **Build complexity.** Medium (universe extracts + ground-truth tagging).

**Example kill-list entries and how they score.**
> *"Name 23 — killed: trades 19.5x vs 5-yr range 14–21x, consensus revisions flat ±0.3% for six months, no catalyst on the calendar within 2 quarters. No expectations gap."* — **Full credit.** Three lenses applied, conclusion follows, under ten seconds to read.
> *"Name 23 — killed: too expensive."* — **Quarter credit.** 19.5x against a 14–21x range is mid-range, so this is screening on multiple level alone, the largest bucket in the universe.
> *"Name 23 — killed: I ran out of time."* — **Full credit, and this is deliberate.** Honest triage accounting is worth more than a fabricated reason, and the rubric says so explicitly. Students who pad their kill lists with invented rationales score worse than those who admit coverage limits.

---

### M05-E2 — Screen Design and the Stacking Trap

**Topics:** Idea screening using multiple lenses; efficiency; FEV.

**Learning objective.** Teach that a screen is a sensor, not an answer — and that stacking filters destroys the sample multiplicatively.

**Student task.** Given a 1,200-name point-in-time dataset with 25 fields, the student must: (a) design a screen to find candidates for a stated thesis type ("decelerating growth stocks where the Street has not yet cut"), (b) report the surviving count at each filter step, (c) identify the step that destroys the most names and justify keeping or loosening it, and (d) convert one filter from a *level* test to a *change* test and report what that does to the output. **55 minutes.**

**Tools and environment.** Python or spreadsheet, with the dataset provided. Auto-gradeable against a reference implementation.

**Grading rubric.**
- *Quantitative (70 pts, fully auto):* the surviving counts at each step are checked against a reference implementation of the student's own stated filter logic — the grader parses the submitted filter definitions and re-runs them, so it grades whether the student's *reported* counts match what their *stated* screen actually does. This catches the common failure of reporting numbers that the described screen could not produce.
- *Qualitative (30 pts, LLM-graded):* the level-to-change conversion must be correctly motivated (that membership change is usually the signal, so a stock newly entering the "decelerating" set is more informative than one that has been there for three years).

**Difficulty.** Intermediate. **Build complexity.** Medium (dataset + reference grader).

**Example and worked illustration.**
> A student's screen: revenue growth decelerating two consecutive quarters (1,200 → 310) **AND** consensus FY+1 revisions still positive (310 → 96) **AND** multiple above 5-year median (96 → 41) **AND** short interest below 5% of float (41 → 28) **AND** market cap > $2bn (28 → 19).
>
> **The teaching payload:** each filter looks reasonable; together they cut the universe by 98.4%. The multiplicative survival rate here is 19/1,200 = **1.58%**. If each of five filters independently retains ~45%, expected survival is 0.45⁵ = **1.85%** — so this screen is behaving as designed, which is precisely the problem: the student has built a screen so tight that it would have missed most of the thesis type it was built to find. **Full credit requires identifying that the multiple filter and the short-interest filter are the two that should be loosened first**, because they are the two least connected to the stated thesis (which is about *revisions lagging fundamentals*, not about valuation or positioning).

---

### M05-E3 — Cyclical or Secular? The Normalisation Case

**Topics:** Cyclical vs. secular; normalized earnings; compounders; value traps.

**Learning objective.** The module's hardest judgment, and one with a defensible key: distinguish a structurally improved business from one at a cyclical peak.

**Student task.** Given ten years of financials for a business whose margins have doubled, plus industry capacity data, capex/D&A history, competitor margin history and a pricing series: compute normalized EPS under three framings (full-cycle average margin, last-trough margin, and a structural case), state the multiple on each, and deliver a verdict with the single piece of evidence that would most change your mind. **70 minutes.**

**Tools and environment.** Existing spreadsheet + templated data pack.

**Grading rubric.**
- *Quantitative (60 pts, auto):* the three normalized EPS figures and implied multiples, tolerance ±2%. **A specific check worth 20 pts: did the student normalise reinvestment alongside margin?** A normalisation that reverts margin to mid-cycle while holding capex at trough levels is internally inconsistent, and this is the named common error — the grader checks whether the capex line moved.
- *Qualitative (40 pts, LLM panel):* 20 pts — the verdict is argued from the **structural test** (did the improvement survive the last downturn?) rather than from the margin trend; 20 pts — the "what would change my mind" evidence is specific, obtainable and genuinely diagnostic.

**Difficulty.** Advanced. **Build complexity.** Medium.

**Example and worked answer (verified).**
> Reported EPS $1.98 at a 14.2% EBIT margin, a record. Full-cycle average margin over ten years 9.1%; last-trough margin 5.4%. Revenue $4,200m, tax 23%, 310m shares. Capex has run at 0.9x depreciation for three years versus 1.4x across the prior cycle.
>
> Normalized at full-cycle margin: EBIT = 4,200 × 0.091 = $382.2m; net = 382.2 × 0.77 = $294.3m; EPS = 294.3/310 = **$0.9494**. At the current $40.07 price that is **42.2x**, against the 20.2x the market shows on reported EPS.
>
> **But the reinvestment adjustment is the point.** Normalising margin without normalising capex flatters cash earnings: restoring capex to 1.4x depreciation adds roughly $0.14 of per-share cash cost that the EPS figure does not capture, so a cash-based normalisation is worse still. A student who reports $0.9494 and stops has done half the work.
>
> **The structural test:** in the last downturn the margin fell to 5.4%, which is *below* the full-cycle average — evidence the business is cyclical, not structurally re-rated. The bull case requires the improvement to be mix- or price-driven and durable. **Most diagnostic evidence to seek:** segment-level or product-level price realisation through the last downturn, because that separates "we raised price and held it" from "the cycle lifted everything."

---

### M05-E4 — The Five-Minute PM Check-In

**Topics:** Efficient idea vetting with PM check-ins; ingredients of compelling ideas.

**Learning objective.** Get a fast yes/no from a decision-maker, and learn to be killed early without ego.

**Student task.** Live (or AI role-play): the student has **5 minutes** to present an early-stage idea to a PM persona who will kill it on one of eight pre-specified grounds if the student has not pre-empted that ground. The student must then, in 2 minutes, either defend or accept the kill and state what they would need to revive it. **7 minutes per run; run three times with different ideas.**

**Tools and environment.** Voice or text role-play agent (shared engine with M02-E4, M09 and M14). The eight kill grounds are the PM's scripted repertoire: doesn't fit mandate; no catalyst; too illiquid; crowded; factor bet in disguise; thesis is consensus; borrow too expensive; path risk too high for the current risk budget.

**Grading rubric.**
- *Quantitative (50 pts, deterministic from the transcript):* did the student pre-empt the kill ground before the PM raised it (binary, per run)? Did they state the four mandatory fields — expectations gap, catalyst with a date, liquidity, factor footprint — within the 5 minutes (four binaries)? This is a checklist, computed mechanically, and it is reliable precisely because it is binary.
- *Qualitative (50 pts, LLM panel on global rating scales with behavioural anchors):* composure; whether they accepted a correct kill gracefully versus arguing a lost point; whether the revival condition was specific; and **whether they bluffed any number.** One planted question per run has no knowable answer from the pack — fabricating an answer is a **critical failure that caps the run at 40%**, regardless of everything else.
- **Use global ratings, not checklists, for the judgment dimensions** — the evidence is that expert global ratings outperform checklists on inter-station reliability for exactly this kind of task, while checklists penalise expert behaviour like skipping steps.

**Difficulty.** Intermediate (advanced on the third run, where the PM is scripted to be hostile). **Build complexity.** High for the role-play engine — but it is amortised across four modules, which is what makes it worth building.

**Example scripted PM turn.**
> *Student has pitched a decelerating-growth short without mentioning borrow.*
> **PM (turn 3):** "Before you go on — what's the borrow on this, and what's the short interest?"
> *If the student does not know:* PM kills it: "Come back when you know what it costs to hold. You just pitched me a 9-month thesis and you don't know the carry." — **Student loses the pre-emption point for this run but can still score on the recovery dimension** by accepting the kill, naming the specific numbers they will get, and proposing a revised return bar net of carry.
> *If the student bluffs a number:* **critical failure.** The PM is scripted to press once — "where did you get that?" — and the transcript records the fabrication.
## Module 06 — Buyside Modeling

### Expected content coverage

**Scope.** Driver-based operating models built to locate variance versus the Street and to drive stock selection. Explicitly **not** investment-banking modeling: no LBO, no accretion/dilution, no three-statement-for-its-own-sake.

**The framing quote that should govern all assessment here.** Caughran, verbatim: *"The basic act of modeling is a necessary but non-differentiating factor… The model is just **table stakes, a 'thinking tool.'**"* **Implication for assessment: grading mechanics alone grades table stakes.** The model exercises must therefore be scored on what the model *reveals* — the located variance — not only on whether it ties.

| Topic | What mastery looks like |
|---|---|
| Six reasons buy-side analysts build models | **Not published** — reconstruction only. Anchored to the "thinking tool" quote. |
| Raw build (TSLA walk-through) | Segment/driver build from filings: volume × price, units × ASP, subs × ARPU, stores × AUV, backlog → revenue conversion. **Quarterly, not annual** — the buy-side model's defining structural choice, because the bar moves quarterly. |
| Incremental margin | **i = ΔEBIT/ΔRevenue.** Caughran, verbatim: *"businesses with high fixed cost will have high incremental margins, and current incremental margins are a good predictor of future base margins. V and MA are the incremental margin GOATs."* Three identities students should own, all verified below. |
| 2-year stack | **Three conventions in circulation, and sources genuinely conflict.** This ambiguity is the single best assessment item in the module. |
| Consensus & revisions | No single consensus exists — providers differ (the academic citation is Larocque, *Journal of Accounting Research*, "Consensus? An Examination of Differences in Earnings Information Across Forecast Data Providers"). **Bloomberg BEst's documented staleness rule:** an estimate is stale if more than 30 days before the most recent report date, guidance or corporate action. **Visible Alpha** carries line-item consensus — an average of **161 line items per forecast, up to 1,000** — which is why it is the buy-side tool: it tells you *where* your variance is before the print. |
| Seven hacks for variance vs. street | **NOT FOUND — heading only.** Do not build an item keyed to "name the seven." Note also: do not conflate this with Caughran's public "Modeling: 12 Common Buy-Side Approaches" thread, which is a different list. |
| Three statements for stock pickers | Cash-flow quality, accruals, balance-sheet capacity for buybacks/M&A, covenant headroom, leases, deferred revenue as a leading indicator, inventory/receivable builds as red flags. |
| Mental frameworks for forecasting | Base rates and reference classes; outside vs. inside view; the danger of straight-lining; guidance anchoring. Mauboussin's Base Rate Book: top 1,000 global companies since 1950, decile reference classes, full-sample mean sales growth **8.1%/yr (1950–2015)**, and an "operating margin beta" of roughly **0.11**. |
| What your PM looks for | Three numbers that matter, a stated variance, and a sensitivity — not forty tabs. |
| NVST case | **NVST = Envista Holdings**, the Danaher dental spin-off, confirmed from SEC filings: IPO 20 Sep 2019, **30.8m shares at $22.00 (19.4%)**, ~$643m net; Envista paid Danaher ~$2.0bn and issued it 127.9m shares; split-off 18 Dec 2019 exchanging **22,921,984 DHR shares for 127,868,000 NVST shares** (implied ratio **5.578**). Brands: KaVo Kerr, Nobel Biocare, Ormco. **No NVST operating financials were recoverable** — pull EDGAR CIK **1757073** directly before building the case. |

**Prerequisites.** Accounting through the three statements; Excel fluency (and note: **Excel speed is the binding constraint in timed drills** and should be assessed explicitly rather than left as a hidden variable); M04's return decomposition.

**Modeling-test reality.** Published specs are almost entirely IB/PE: LBO tests run **1–3 hours** and are "mostly a speed test"; build-from-10-K at **180 minutes**; one provider publishes a **90-minute** LBO test; one published rubric weights **accuracy 40% / completeness 25% / structure 20% / formatting 15%**; **median scores are often below 50%**; and **no published pass mark exists anywhere.** Grading is characterised as "check the box" — "the reviewer will not be questioning your assumptions." **No published, specified *buy-side* modeling test could be found.** Treat that as confirmed white space and the strongest commercial argument for building this assessment properly.

---

### M06-E1 — The 2-Year Stack Ambiguity *(flagship for this module)*

**Topics:** 2-year stack; bells & whistles; comp effects.

**Learning objective.** Force the student to confront that a metric everyone quotes has three incompatible definitions, and that the most-used one breaks hardest in exactly the case it was adopted for.

**Student task.** Given eight quarters of revenue through a COVID-shaped distortion, compute the 2-year stack under all three conventions (additive, geometric/cumulative, and 2-year CAGR) for every quarter; identify the quarter where the conventions diverge most and quantify the gap; prove algebraically why the additive and geometric conventions differ by exactly the cross-product g₁·g₂; and state which convention you would present to a PM and why. **55 minutes.**

**Tools and environment.** Existing spreadsheet. Fully auto-gradeable.

**Grading rubric.**
- *Quantitative (75 pts, fully auto):* three series of eight values each, tolerance 1e-4; the identified max-divergence quarter; the cross-product proof checked numerically at every quarter.
- *Qualitative (25 pts, LLM-graded):* the recommendation must acknowledge that **no convention is correct** and justify a choice on grounds of what the PM is trying to see through. An answer asserting one convention is simply right scores ≤10.

**Difficulty.** Intermediate. **Build complexity.** Low.

**Example and worked answer (verified).**
> Revenue indexed: 100 → 72 → 115. Year-1 growth = −28.0%; year-2 growth = +59.72%.
>
> **Additive 2-yr stack** = −28.0% + 59.72% = **+31.72%**. **Geometric (cumulative vs. two years ago)** = (0.72 × 1.5972) − 1 = **+15.00%**. **2-year CAGR** = 1.15^(1/2) − 1 = **+7.24%**.
>
> **The spread between additive and geometric is 16.72pp**, and that is exactly the cross-product: g₁ × g₂ = (−0.28) × (0.5972) = **−0.1672** ✓. In normal times the gap is trivial: at +6% and +8%, additive gives 14.00% and geometric gives 14.48%, a gap of 48bp (= 0.06 × 0.08).
>
> **The teaching punchline:** the additive convention — the one most widely used — overstates the recovery by 16.7 points precisely in the COVID-distorted case the convention was popularised to see through. A student who presents "+31.7% two-year stack" to a PM on this data has told them the business is 31.7% bigger than two years ago when it is in fact 15.0% bigger.
>
> **The deeper item for advanced students:** construct an eight-quarter series where year-over-year growth decelerates violently, the geometric stack rises monotonically, and the additive stack shows a **fake peak**. All three are "true"; only one is not actively misleading.

---

### M06-E2 — Incremental Margin and the Operating-Leverage Identity

**Topics:** Incremental margin; bells & whistles; forecasting.

**Learning objective.** Move from computing incremental margin to using it as a forecasting constraint, via three identities that most analysts never see written down.

**Student task.** Given three years of segment revenue and EBIT: compute incremental margin for each period; use the identity m₁ = (m₀ + i·g)/(1+g) to forecast next year's margin from a revenue forecast; state the condition for margin expansion; compute degree of operating leverage and show it equals i/m₀; then compute incremental margin **organically** (stripping an acquisition and FX) and explain why the reported figure understated true operating leverage. **60 minutes.**

**Tools and environment.** Existing spreadsheet with named outputs. Fully auto-gradeable including a perturbation test.

**Grading rubric.**
- *Quantitative (85 pts, fully auto):* all computed values, tolerance 1e-4. **Perturbation test (25 of the 85):** the grader changes the revenue-growth input and checks the forecast margin moves per the identity — this distinguishes a live model from a hardcoded answer.
- *Qualitative (15 pts, LLM-graded):* the explanation of why blending a low-incremental-margin acquisition into the reported figure understates organic operating leverage.

**Difficulty.** Intermediate. **Build complexity.** Low–medium.

**Example and worked answer (all three identities verified numerically).**
> Revenue $1,000m at 15.0% EBIT margin. Revenue grows 12.0%; incremental margin 30.0%.
>
> New revenue $1,120m; EBIT = 150 + 0.30 × 120 = $186m; margin = 186/1,120 = **16.6071%**. Identity check: (0.15 + 0.30 × 0.12)/(1.12) = (0.15 + 0.036)/1.12 = 0.186/1.12 = **0.166071** ✓.
>
> **Condition for margin expansion: i > m₀.** At i = 30% > m₀ = 15%, margin expands. Flip incremental margin to 10%: m₁ = (0.15 + 0.012)/1.12 = **14.4643%**, and margin contracts — verified that the condition holds in both directions.
>
> **DOL = i/m₀.** Here 0.30/0.15 = **2.00x**. Empirical check: %ΔEBIT = 186/150 − 1 = 24.0%; %ΔRevenue = 12.0%; ratio = **2.00** ✓ exact. **Operating leverage and incremental margin are the same fact expressed two ways** — which is worth saying out loud, because students treat them as separate concepts.
>
> **The organic adjustment, which is the real lesson.** Reported revenue +12.50% decomposes to organic +10.25pp, M&A +4.50pp, FX −2.25pp. Recomputing incremental margin **organically** gives **35.85%** versus **30.00%** reported — the reported figure understated true operating leverage by **585bp**, purely because a 10%-incremental-margin acquisition was blended in. An analyst forecasting off the reported 30% will systematically under-forecast margin expansion in every future period.
>
> **Advanced extension — the decremental round trip.** Revenue 4,000 → 4,500 → 4,000 with EBIT 600 → 750 gives an incremental margin of 30.0%. If the down-leg decremental margin is 34%, EBIT returns to **580**, not 600: a full revenue round trip **permanently destroys $20m**. When decremental exceeds incremental, that asymmetry is itself a short signal.

---

### M06-E3 — The Guidance Bridge: Find the Variance

**Topics:** Consensus and revisions; variance vs. street; forecasting; three statements.

**Learning objective.** The module's capstone skill: find where your number differs from the Street's, and whether the difference is in the right place to matter.

**Student task.** Given a company's Q2 release and updated FY guidance, plus the Street's FY model by line item, the student must: build the guidance bridge; compute implied 2H revenue growth and the 2-year stack; attribute the difference between their EPS and the Street's across revenue, margin, tax and share count, with the attribution tying exactly; compute the exit run-rate and the share of next year's consensus growth that is pure annualisation; and state in two sentences where the real variance is. **90 minutes.**

**Tools and environment.** Existing spreadsheet + templated release. Mostly auto-gradeable.

**Grading rubric.**
- *Quantitative (75 pts, auto):* the bridge, the implied 2H figures, the four-way attribution (with a hard tie-check worth 20 pts — the components must sum to the total difference), the exit run-rate, and the annualisation share.
- *Qualitative (25 pts, LLM-graded):* the two-sentence conclusion must identify that offsetting drivers hide inside a small headline difference. An answer that reports "we're in line" without decomposing scores zero.

**Difficulty.** Advanced. **Build complexity.** Medium (templated release + reference model).

**Example and worked answer (verified; both the attribution and the bridge tie exactly).**
> **Part 1 — the raise is smaller than the beat.** Q2 revenue beat by $30m. FY guidance raised by $20m. **Therefore implied 2H revenue falls by $10m**, from $2,030m to $2,020m. 1H growth was +12.71%; implied 2H growth is **−1.46%**. That is **14.17 points of deceleration** embedded in a guidance *raise* — the single most important thing in the release, and invisible to anyone reading the headline.
>
> Decomposing that deceleration: **2.70 points is the harder comp** and **11.47 points is genuine implied slowdown** (2.70 + 11.47 = 14.17 ✓). Two-year stacks fall from 21.42 to 9.95 points additive, or from 10.69% to 4.78% on a 2-year CAGR basis.
>
> **Part 2 — the exit rate kills next year.** Implied Q4 revenue is **−2.86% year-over-year**, while FY+1 consensus requires **+6.16%**. That is a **9-point reacceleration that nobody has underwritten**, derived from pure arithmetic with no view required. Separately, the exit run-rate of 4,800 means **91% of the Street's FY+1 growth is annualisation of Q4** with only **+0.6% in-year progression** — so consensus is far more fragile than its growth rate suggests.
>
> **Part 3 — the headline hides everything.** Student EPS $2.810 vs. Street $2.800 = **+0.37%, "in line."** Stepwise attribution: revenue **+0.692%**, margin **−1.298%**, shares **+0.974%**; net **+0.368%** ✓ ties. Three large offsetting drivers inside a trivial headline. **And the Street's number is simply the guidance midpoint** — which means "consensus ≈ guidance midpoint" is itself the alpha opportunity, because nobody has done this arithmetic.

---

### M06-E4 — Faded Model Build Series

**Topics:** Raw build; three statements; model architecture; PM expectations.

**Learning objective.** Build modeling capability across a heterogeneous cohort without boring the experienced or drowning the career-switcher — by fading scaffolding rather than varying difficulty.

**Student task.** Four exercises on the same company, run in sequence. **(1)** A complete, correct model is supplied; the student annotates why each driver is structured as it is and answers eight questions requiring them to trace dependencies. **(2)** The revenue build is blanked; rebuild it. **(3)** The entire operating section is blanked. **(4)** Raw build from the 10-K with only a blank labelled template. Time limits 30 / 45 / 90 / 180 minutes respectively.

**Tools and environment.** Excel/Sheets with locked submission sheets. The auto-grader is the significant build and is shared with M07, M11 and M13.

**Grading rubric.**
- *Quantitative (70 pts, fully auto):* check cells against the golden model with relative tolerance; three-statement integrity ties (balance sheet balances every period; ending cash ties; sum of segments ties to consolidated); **3–5 perturbation shocks** verifying outputs move correctly; **hardcode detection** (numeric literals outside a whitelist, reported as a hygiene sub-score not a hard fail); **R1C1 formula-consistency** across forecast rows; circular-reference detection.
- *Qualitative (30 pts, LLM-graded):* exercise 1's annotations and, in exercise 4, a required 150-word note on where the variance versus consensus sits. **Per the governing quote, the variance note is worth more than any single mechanical check** — a model that ties perfectly and locates nothing scores in the 60s, which should be stated to students up front.
- **Error-cascade containment is essential:** the grader must limit how far one upstream cell error propagates into downstream wrong answers, or a single early slip zeroes an otherwise competent model. Score each check-cell cluster against the student's *own* upstream values where the dependency is isolable.

**Difficulty.** Beginner (1) through advanced (4). **Build complexity.** Medium–high (the grader); low per additional company once built.

**Example and worked answer (exercise 1, question 4 — the dependency-wiring item).**
> *"Cell D47 (Q3 revenue) — list every input cell it depends on, and state which single input, if changed by 10%, moves it most."*
>
> This question type is the most valuable in the series because it is **ungameable by labelling**. The grader does not read the student's words; it compares the student's claimed dependency list against the actual dependency graph extracted from the golden workbook. A student who writes "volume and price" when the model in fact drives revenue off a single blended ASP line has revealed they did not trace the model — which is exactly the failure that produces analysts who cannot answer "what's your volume assumption?" in a PM meeting.
>
> The same mechanism provides the strongest single check in exercise 4: **"does the revenue line depend on BOTH a volume cell and a price cell?"** A model that drives revenue off one blended growth rate cannot answer a price/volume question, and the dependency graph shows that instantly, regardless of how the rows are labelled.
## Module 07 — Analyze a Business

### Expected content coverage

**Scope.** What you can establish about a business from public documents and a model — **before** you have met management (M09), before you have valued it (M11), and before the print (M13). That carve-out matters: written naively, Modules 07 and 08 double-count against Modules 09, 10, 11, 12 and 13.

| Topic | What mastery looks like |
|---|---|
| Reading the 10-K, calls, sell-side | A strong analyst reads in **model-filling order**, roughly the reverse of the document's own order, with the **segment footnote first.** (Published guides almost all say MD&A first and footnotes last; the model-filling order is a practitioner judgment, flagged as such.) Also: revenue-recognition policy, critical accounting estimates, year-over-year risk-factor diffing, customer concentration, backlog, non-GAAP reconciliation, lease and debt footnotes. Sell-side is used for the model mechanics, the data and the consensus bar — **not for the conclusion.** |
| Business quality | **Helmer's 7 Powers** (Scale Economies, Network Economies, Counter-Positioning, Switching Costs, Branding, Cornered Resource, Process Power) — each with a benefit *and* a barrier, and each with a **financial fingerprint**, which is what makes qualitative moat talk testable. Mauboussin's "Measuring the Moat." Greenwald's two counter-intuitive propositions: **"economies of scale advantages require customer captivity"** and **"fast market growth is a LIABILITY"** — both invert the junior instinct that a big TAM protects an incumbent. |
| ROIC and economic profit | ROIC = NOPAT/Invested Capital, decomposed as **NOPAT margin × invested-capital turns**. Mauboussin's own contrast: Walmart at 12.3% = 3.7% × 3.3x versus a luxury business at ~12% = 20.5% × 0.6x — same ROIC, opposite businesses. ROIIC for the marginal dollar. The intangibles adjustment. |
| Unit and cash economics | Contribution margin, LTV/CAC, payback, cohort retention, NRR; FCF conversion; cash conversion cycle; maintenance-capex estimation. |
| Bull/base/bear and key drivers | Three cases that differ in *drivers*, not in a growth-rate nudge. Focus research on the **three** key drivers — the stock-specific subset that is both material and contested. |
| Peer comparison | Calendarize, capital-structure-adjust, accounting-adjust. The buy-side difference: the comp sheet must be **regressed and the residuals read**, because the residual is the mispricing. |
| Catalysts and risk/reward | Dated, specific, and tied to the key drivers. |

**Scope flags.** Bullet "Evaluate management and capital allocation" is a **near-total overlap with Module 09** — treat it as a pointer, not as content to assess here. "Understand market expectations priced in" overlaps **Module 10**. Six of Caughran's coinages in Modules 07–08 are **reconstructions only**: "viability," the quick/deep-dive time boxes, "durable growth algorithms," "universe tracker," "melting ice cubes" (generic industry usage; no FE definition found) and "connect dots."

**Two things not to teach.** (1) A sibling research pass found **no Mauboussin critique of Porter's Five Forces** — do not attribute one to him. (2) A circulating claim that **ROIIC = Δmargin × Δturnover is not a valid identity** — do not teach it.

**On risk-factor diffing, the evidence is genuinely mixed and should be taught that way.** Kravet & Muslu (peer-reviewed) find risk-disclosure increases predict *volatility and volume*, not direction; Gan et al. find 10-K *file-size* change predicts returns while Item 1A word-count change does **not**. Defensible as hypothesis-generation; **not** defensible as a return signal. This audience will catch over-claiming.

**Prerequisites.** Accounting through the three statements; M06's modeling; the concept of cost of capital.

---

### M07-E1 — The 90-Minute 10-K Brief *(flagship for this module, and the most valid single exercise in the program)*

**Topics:** Reading filings; business quality; key drivers; bull/base/bear.

**Learning objective.** Triage a large document under time pressure and emerge with the *right three things*. The reason this is the most valid exercise available for M07: **driver selection is the actual skill, and it has a defensible expert key** — unlike a price target, which does not.

**Student task.** Student receives ~60 pages (10-K extracts, two transcripts, a comp sheet, an industry data series) and has **90 minutes** to produce a one-page memo containing: a three-sentence business description; the three key drivers **ranked**, each with (a) what the market currently assumes, (b) what you believe, and (c) **a named research plan to resolve it**; the single most important number in the filing and why; and one bull/bear asymmetry observation.

**Tools and environment.** Custom data pack. Existing text tools.

**Grading rubric.**
- *Quantitative (50 pts, semi-auto):* driver identification against an expert key using a controlled vocabulary (3 correct, 4 plausible-secondary, 4 wrong, with partial credit); ranking by rank correlation; the "most important number" against a key with accepted alternates.
- *Qualitative (50 pts, LLM panel, reference-guided):* **the research-plan column carries 25 of the 50 and is nearly impossible to fake** — a plan naming a specific disclosure, a specific competitor's segment data, a specific expert profile, or a specific dated catalyst is distinguishable from "do more diligence" with near-perfect reliability. 15 pts for the market-assumption column being a number against a named consensus line; 10 pts for the asymmetry observation.
- **Do not grade the price target. Do not ask for one.** Grading driver *choice* against an expert key is defensible; grading a 90-minute price target is not.

**Difficulty.** Intermediate–advanced. **Build complexity.** Medium (pack authoring + vocabulary; the pack is reusable indefinitely).

**Example and model answer (driver row).**
> **Model driver #1:** "Realised price in the Industrial segment (58% of revenue, 71% of EBIT). *Market assumes:* consensus FY+1 revenue growth of 4.2% with gross margin flat at 34.1%, which implies roughly 1–2% price and 2–3% volume. *I believe:* price is running negative — the 10-K's MD&A attributes growth to 'higher volumes partially offset by unfavourable price/mix' for the second consecutive year, while the segment footnote shows gross margin down 70bp despite a 310bp fall in input costs. *Research plan:* pull the two listed competitors' segment price commentary from their last four transcripts; obtain the industry price index from the trade association's monthly series; one expert call with a distributor to establish whether discounting is list-price or rebate-driven, because rebates show up in net revenue with a one-quarter lag."
>
> Note what earns the research-plan points: three *named, obtainable* sources with a stated reason each, and an articulated mechanism (rebate lag) that makes the research decision-relevant. Compare the typical weak answer: *"Research plan: talk to industry experts and monitor pricing trends."*
>
> **The "most important number" key for this pack:** the 310bp fall in input costs against a 70bp gross-margin decline. That pairing is the whole thesis — it establishes that price is negative without management ever saying so, and it is available on page 34 to anyone who reads the segment footnote against the MD&A rather than reading either alone.

---

### M07-E2 — ROIC Decomposition and the Intangibles Fork

**Topics:** ROIC; business quality; cash economics.

**Learning objective.** Compute ROIC correctly, decompose it, and understand that the "right" ROIC depends on the question being asked.

**Student task.** From a supplied income statement and balance sheet: compute NOPAT, invested capital, ROIC, and the margin × turns decomposition; recompute ROIC excluding goodwill and excluding all intangibles; compute economic profit two ways; compute ROIIC on the last three years' incremental capital; and write 150 words on which ROIC figure you would put in a pitch and why. **55 minutes.**

**Tools and environment.** Existing spreadsheet. Fully auto-gradeable.

**Grading rubric.**
- *Quantitative (80 pts, fully auto):* all figures, tolerance 1e-3. Economic profit must be computed **both** ways and agree (a 15-pt internal consistency check). The decomposition must tie exactly to the headline ROIC.
- *Qualitative (20 pts, LLM-graded):* full credit requires recognising that **both the including- and excluding-goodwill figures are true answers to different questions** — ROIC including goodwill measures the return on capital *as deployed by this management including what they paid for acquisitions*; excluding goodwill measures the economics of the *operating business*. An answer that calls one "correct" scores ≤8.

**Difficulty.** Intermediate. **Build complexity.** Low.

**Example and worked answer (verified).**
> Revenue $4,200m, EBIT $630m (15.00% margin), tax 23%. NOPAT = 630 × 0.77 = **$485.1m**. Invested capital = (AR 520 + Inventory 410 − AP 380) + net PP&E 1,150 + intangibles 340 = **$2,040m**.
>
> **ROIC = 485.1/2,040 = 23.78%.** Decomposition: NOPAT margin 485.1/4,200 = **11.55%** × invested-capital turns 4,200/2,040 = **2.059x** → 11.55% × 2.059 = **23.78%** ✓ ties exactly.
>
> At WACC 8.5%, the spread is **1,528bp** and economic profit = (0.2378 − 0.085) × 2,040 = **$311.7m**. Cross-check: NOPAT − (WACC × IC) = 485.1 − 173.4 = **$311.7m** ✓.
>
> **The intangibles fork.** On a comparable illustrative company the research produced ROIC of **13.908%** headline, **20.46%** ex-goodwill and **24.18%** ex-all-intangibles. The 10.3-point gap between the first and third is **the price management paid for what it bought.** Both numbers are true. A pitch arguing "this is a high-quality business" should cite the ex-goodwill figure *and disclose that it is ex-goodwill*; a pitch arguing "this management allocates capital well" must cite the inclusive figure, because excluding goodwill excludes precisely the decision being assessed.
>
> **ROIIC is the forward-looking one:** at 22.2% against an average ROIC of 13.9%, the marginal dollar is being deployed far better than the average dollar — which is the single most bullish fact available about this business, and it is invisible in the headline ROIC.

---

### M07-E3 — Cash Economics: When Growth Consumes Cash

**Topics:** Cash economics; unit economics; three statements.

**Learning objective.** Show that profitable growth can be cash-negative, and quantify the working-capital and capex drag per dollar of revenue.

**Student task.** Compute FCF conversion headline and after charging SBC; compute DSO/DIO/DPO and the cash conversion cycle; convert each day of DSO into dollars; estimate maintenance capex by three different methods and reconcile the range; and compute the cash cost of an incremental dollar of revenue. **60 minutes.**

**Tools and environment.** Existing spreadsheet. Auto-gradeable.

**Grading rubric.**
- *Quantitative (80 pts, auto):* all figures, tolerance 1e-3. The three maintenance-capex methods must each be computed and the **range reported** — a student reporting a single figure without the range loses 20 pts, because the method's weakness is the lesson.
- *Qualitative (20 pts, LLM-graded):* must explain why FCF conversion above 100% here comes from **intangible amortisation, not under-investment** (capex is 1.46x depreciation), and must state the cash cost of incremental growth with its sign.

**Difficulty.** Intermediate–advanced. **Build complexity.** Low.

**Example and worked answer (verified).**
> **Cash conversion cycle.** Revenue $4,200m, COGS $2,520m, AR $520m, Inventory $410m, AP $380m. DSO = 520/4,200 × 365 = **45.2 days**; DIO = 410/2,520 × 365 = **59.4 days**; DPO = 380/2,520 × 365 = **55.0 days**. **CCC = 45.2 + 59.4 − 55.0 = 49.5 days.**
>
> **Days into dollars — the move that makes this decision-relevant.** On a comparable illustrative company with a 72.5-day CCC, one day of DSO was worth **$54.8m**, so a five-day DSO slip is worth more in year-one cash than 150bp of gross margin. That reframing is the point: analysts obsess over margin and ignore working capital, which can be larger and moves faster.
>
> **FCF conversion.** Headline **102.6%** falls to **90.8%** once SBC is charged as the real cost it is. The >100% headline comes from intangible amortisation flowing through net income without a cash cost — **not** from under-investing, which the 1.46x capex/depreciation ratio rules out. A student who reads >100% conversion as a red flag for under-investment has the right instinct and the wrong conclusion, and the capex/depreciation check is what separates them.
>
> **Maintenance capex, three ways: 90.8 / 108 / 130.0** — a **43% range on the same company.** Report the range. The Greenwald method (gross PP&E/sales × incremental sales, subtracted from total capex) is the most common and is highly sensitive to the PP&E/sales ratio chosen; on a growth year it can produce a *negative* maintenance figure, which is a signal the method has broken rather than a finding.
>
> **The punchline.** Incremental growth on this business is **cash-negative at −2.5 cents per revenue dollar**: after-tax incremental profit of 23.1 cents is consumed by 21.6 cents of working capital and 4.0 cents of capex. The business is profitable, growing, and each incremental dollar of revenue costs it cash. That is the single most important thing to know about it and it appears nowhere on the income statement.
## Module 08 — Analyze an Industry

### Expected content coverage

**Scope.** The sector-level layer: building an industry P&L, maintaining a universe, and using cross-company read-across to find what single-company analysis cannot see.

| Topic | What mastery looks like |
|---|---|
| Learning an industry | Primers, experts, conferences, trade associations, regulatory dockets. The sequence matters: structure before names. |
| Universe tracker and comp sheets | Which columns, and — the buy-side difference — **the comp sheet is regressed and the residuals read**, because the residual is the mispricing. Three normalisations are mandatory: **calendarization, capital structure, accounting.** |
| Industry P&L | Sector-level revenue pool, aggregate margins, share shifts, industry price vs. volume, capacity utilisation. **Research finding worth knowing: there is essentially no public literature on this technique.** That makes it simultaneously FE's biggest genuine differentiator and the least documentable — build it from practitioner interview and do not expect to cite it. |
| Blocking & tackling | **No defined content anywhere** — the weekly/quarterly maintenance cadence is reconstruction. |
| Inflections and catalysts from the model | The sector model shows you which company is about to be forced to do something. |
| Connecting dots between competitors | A share claim by one company is a share loss claim about named others. This is what makes industry work falsifiable. |
| Quick dives vs. deep dives | Time boxes are **reconstruction only.** |
| Long compounders / short melting ice cubes | **"Short melting ice cubes with structural headwinds" is verbatim Caughran** (this bullet), as is the pairing with durable growth algorithms. |
| Pair trades | Construction, factor/beta matching, sizing to equalise risk rather than notional, and decay. |

**Prerequisites.** M06 (modeling), M07 (single-company analysis), M11's multiples algebra for the comp-sheet regression.

---

### M08-E1 — The Industry P&L Share-Shift Constraint *(flagship for this module)*

**Topics:** Industry P&L; connecting dots between competitors; sector economics.

**Learning objective.** The highest-value item in the module because **it makes share claims falsifiable.** Guidance that is individually plausible becomes collectively impossible once you build the pool.

**Student task.** Given five companies' guidance, their current revenues, and an independent industry-pool growth estimate: build the industry P&L; compute the share shift each company's guidance requires; determine whether the guidance set is collectively feasible; identify which company's guidance is least credible and why; and state the one disclosure that would resolve it. **70 minutes.**

**Tools and environment.** Existing spreadsheet + templated guidance pack. Fully auto-gradeable on the arithmetic.

**Grading rubric.**
- *Quantitative (70 pts, fully auto):* the pool build, each company's implied share, the share deltas, and the **sum-to-zero check** (deltas across all participants including the fringe must net to zero — 20 pts, and it is the check that makes the exercise work).
- *Qualitative (30 pts, LLM-graded):* the least-credible identification must be argued from the arithmetic (who needs the most share from whom, and is there evidence they can take it) rather than from tone; the resolving disclosure must be specific and real.

**Difficulty.** Advanced. **Build complexity.** Low–medium.

**Example and worked answer (verified; deltas sum to zero).**
> Company A guides revenue **+8%** in an industry pool growing **+5%**. A's revenue is $1,200m in a $10,000m pool, so 12.0% share.
>
> A's implied revenue = 1,200 × 1.08 = $1,296m. The pool = 10,000 × 1.05 = $10,500m. A's implied share = 1,296/10,500 = **12.34%**, a gain of **+34bp**... but the exercise's real version works at **100bp** of share: A's guide requires taking a full point of share, which decomposes to **−62.9bp from Company C** and **−37.1bp from the fringe**, with all deltas summing to zero.
>
> **The teaching payload:** C has simultaneously guided to *flat* share. Both guides cannot be true. One of them is wrong, and the arithmetic says so without any judgment about management quality. **Full credit requires naming which specific competitor must lose and by how much** — that is the difference between "A's guidance looks aggressive" (a feeling) and "A's guidance requires 63bp from C, who has guided flat" (a falsifiable claim you can take to a PM).
>
> **Resolving disclosure:** C's segment-level volume disclosure, or the trade association's quarterly unit-shipment series by participant — either one adjudicates it within a quarter.

---

### M08-E2 — The Booby-Trapped Comp Sheet

**Topics:** Comp sheets; universe tracker; normalisation.

**Learning objective.** Build a comp sheet that is actually comparable — and detect the four specific ways comp sheets lie.

**Student task.** Build a comparable multiples table for eight companies from supplied financials. **Four traps are planted and each scores independently:** one company has a June fiscal year-end (requires calendarization); one is lease-heavy (requires a consistent lease treatment); one reports under IFRS (requires an accounting adjustment); one includes SBC in its adjusted EBITDA while the others exclude it. The student must produce adjusted and unadjusted columns, state every adjustment, and identify which company is genuinely cheapest. **80 minutes.**

**Tools and environment.** Existing spreadsheet. Fully auto-gradeable — each trap is a separate check cell.

**Grading rubric.**
- *Quantitative (80 pts, fully auto):* 15 pts per trap correctly handled (60), plus 20 pts for the final adjusted ranking. **Crucially, each trap is scored independently**, so a student who catches three of four gets 45/60 rather than failing the exercise — which is both fairer and more diagnostic.
- *Qualitative (20 pts, LLM-graded):* the adjustment log must state each adjustment and its direction. An unexplained adjustment scores zero even if numerically right.

**Difficulty.** Intermediate–advanced. **Build complexity.** Low–medium.

**Example and worked answer (verified).**
> **The calendarization trap.** A June-year-end company's "FY+1" is six months ahead of its December-year-end peers'. A junior reports **9.19x** EV/EBITDA; properly calendarized to a common December period it is **8.33x** — a **9.3% error**, and in the wrong direction (the stock looked more expensive than it was).
>
> **The lease trap, which is worse than the naive error.** The common mistake is to add the lease liability to enterprise value **without** adding rent back to EBITDA. That gives **9.31x** — *further from the truth than doing nothing at all.* Half an adjustment is worse than none. This is the single best item in the exercise because it punishes the appearance of rigour.
>
> **The SBC trap.** One company's adjusted EBITDA includes SBC as an expense; the others add it back. On a 15%-of-revenue SBC load this is not a rounding difference — it can be several turns. The student must restate all eight to one convention and say which.
>
> **Full credit on the ranking requires the student to conclude that the cheapest name on the unadjusted sheet is not the cheapest on the adjusted sheet.** That inversion is the point of the exercise, and the key is constructed so that it happens.

---

### M08-E3 — Pair Construction and Decay

**Topics:** Pair trades; factor matching; sector relative value.

**Learning objective.** Build a pair that isolates the idiosyncratic view instead of accidentally expressing a factor or beta bet.

**Student task.** Given a stated intra-industry view ("A's margin convergence to B's is not priced"), construct the pair: choose the legs, size them to equalise *risk* rather than notional, compute the residual factor and beta exposure after sizing, state the borrow cost on the short leg and the resulting return hurdle, and specify the two conditions under which you would take the pair off. **55 minutes.**

**Tools and environment.** Existing spreadsheet with supplied betas and factor loadings.

**Grading rubric.**
- *Quantitative (65 pts, auto):* the risk-equalised sizing, residual net beta, residual factor exposure, borrow drag over the stated horizon, and the breakeven convergence required to clear the hurdle.
- *Qualitative (35 pts, LLM-graded):* 20 pts — the take-off conditions must include **one that is thesis-based and one that is market-structure-based** (e.g. the convergence happening, versus the borrow becoming uneconomic or the pair's factor residual drifting beyond a limit); 15 pts — recognises that notional-neutral is not risk-neutral.
- **Research-thin flag:** pair-trade construction and decay was one of the clusters a sibling research pass could not reach before its budget was exhausted, so the key here rests more on practitioner convention than on cited evidence. Treat the sizing mathematics as solid and the *decay* guidance as provisional.

**Difficulty.** Advanced. **Build complexity.** Low.

**Example and worked answer.**
> Long A ($40 stock, beta 1.25, 32% vol), short B ($85 stock, beta 0.95, 24% vol). A naive dollar-neutral pair at $10m per leg carries net beta of 10 × (1.25 − 0.95) = **$3.0m of beta exposure**, i.e. a long market position, plus a long-vol tilt.
>
> **Risk-equalised sizing** scales the legs by inverse volatility: to equalise contribution to risk, the B leg must be larger in notional (24% vol versus 32%), at $10m × (0.32/0.24) = **$13.33m**. That raises gross from $20m to $23.33m and *worsens* the beta mismatch to 10 × 1.25 − 13.33 × 0.95 = 12.50 − 12.67 = **−$0.17m**, which is now effectively beta-flat — the vol-scaling happened to fix the beta here, which is a coincidence worth pointing out to students rather than a rule.
>
> **The hurdle that kills most pairs:** borrow on B at 180bp over a 9-month expected convergence is **135bp of drag**, so the pair must deliver more than 1.35% of relative convergence just to break even, before any factor residual. **Full credit requires netting the carry out of the expected convergence** — the commonest junior error in pair construction is to quote the gross convergence as the return.
## Module 09 — Management & Capital Allocation

### Expected content coverage

**Scope.** Assessing the people allocating the capital, and the capital decisions themselves. Far more quantifiable than the brochure language suggests — 8 of the module's best assessment instruments are substantially arithmetic.

| Topic | What mastery looks like |
|---|---|
| Why management matters (and when it doesn't) | The jockey-vs-horse question. It matters least in commodity businesses and in structurally advantaged or disadvantaged ones; it matters most where reinvestment choices are large relative to the existing asset base. |
| A framework to evaluate management | **Thorndike's *The Outsiders*** — all eight CEOs confirmed (Murphy/Capital Cities, Singleton/Teledyne, Anders/General Dynamics, Malone/TCI, Graham/Washington Post, Stiritz/Ralston Purina, Smith/General Cinema, Buffett/Berkshire), and seven traits: capital allocation as the CEO's primary job; the two-job split; **decentralised operations + centralised capital** (Burke ran Capital Cities' operations, Murphy allocated the cash); per-share value as the yardstick; they did the ROI math themselves; they reduced businesses to a handful of assumptions; frugality, independence, cash-flow focus. **Four commonly-cited traits could NOT be confirmed** — buyback preference, dividend aversion, counter-cyclical leverage, guidance aversion. Do not print those four as Thorndike's. |
| Management deep dive | Guidance-hit-rate analysis; capital-deployment back-testing; M&A track record and goodwill-impairment history; promotional-language scoring; insider ownership as a share of net worth rather than in dollars. |
| Corporate access | **The empirical answer:** Solomon & Soltes (*J. Law & Econ.* 58(2), 2015) find private one-on-ones improve trade timing, **concentrated in hedge funds**, larger when public information is scarce, with alternative explanations ruled out (single-firm caveat). That is the evidence base for "the obsession with corporate access." |
| Structured meeting process | Question hierarchy; process questions over outcome questions; triangulation; **never asking a question whose answer is in the 10-K**. |
| Investor relations and conferences | IR's incentives; 1x1s vs. group meetings; which conference days matter. |
| Stock-based compensation | ASC 718; grant-date fair value vs. expense vs. dilution; the share-count roll-forward; why "buybacks to offset dilution" is not shrinkage. |
| Five options for deployment of cash | Reinvest, M&A, dividends, buybacks, pay down debt (holding cash is a sixth). **Note: Mauboussin's own taxonomy has *seven* uses — the syllabus compresses.** Key sourced facts: **>90% of US corporate capital was internally financed 1980–2015**; M&A is the largest use and is **pro-cyclical with the market** (corporates systematically buy when expensive — the single most damning aggregate fact in the module); buybacks now exceed dividends; shareholder yield beats dividend yield. |
| Buyback analysis | The arithmetic, and the separation of EPS accretion from value creation. |

**Two corrections to carry.** (1) **Rule 10b-18** (the buyback safe harbour) and **Rule 10b5-1** (trading plans) are different rules — "10b5-18" is a conflation and appears in circulation. (2) **The compliance boundary is absent from all ten brochure bullets**, yet four of them are corporate-access bullets. Build MNPI/Reg FD assessment regardless; the CFA Code & Standards item-set format is ready-made technology for it. One genuine ambiguity found and unresolved: law-firm summaries describe Reg FD's 24-hour trigger differently (running from when a senior official *learns* of the disclosure vs. from the *disclosure itself*) — **read the rule before teaching it.**

**Prerequisites.** M06 (modeling), M07 (ROIC and cash economics), basic proxy-statement literacy.

---

### M09-E1 — The Management Scorecard: Guidance, M&A, and Skin

**Topics:** Evaluating management; management deep dive; capital allocation track record.

**Learning objective.** Replace impressions of management with a computed track record.

**Student task.** Given eight years of guidance versus actuals, three completed acquisitions with purchase prices and subsequent segment disclosure, and the proxy's beneficial-ownership table with footnotes: compute the guidance hit rate and mean absolute error for both revenue and EPS; determine whether misses originate above or below the revenue line; back-test the deployed capital's actual return against the WACC and against what was promised at announcement; compute genuine skin in the game after stripping pledged and unvested shares; and produce a 0–100 composite credibility score against a supplied weighting. **85 minutes.**

**Tools and environment.** Existing spreadsheet + templated data pack. Largely auto-gradeable.

**Grading rubric.**
- *Quantitative (80 pts, fully auto):* every computed figure, tolerance 1e-3; the M&A back-test must reconcile two ways (direct NPV and a perpetuity cross-check) — a 15-pt internal consistency check; the composite score must tie to its components.
- *Qualitative (20 pts, LLM-graded):* a 150-word verdict that distinguishes *forecasting ability* from *operating ability* from *capital-allocation ability*, since the three dissociate and the scorecard shows it.

**Difficulty.** Advanced. **Build complexity.** Medium (data pack authoring).

**Example and worked answer (verified).**
> **Guidance track record.** EPS hit rate **3 of 8 = 37.5%**; EPS mean absolute error **10.369%**; revenue MAE **3.798%**. The gap between the two is the finding: **the misses are below the revenue line** — management forecasts demand adequately and controls costs, tax or share count badly. Bias is **−1.789%** over the full sample but **+2.912% excluding 2020**, so the apparent conservatism is one pandemic year, not a habit. Two years show a guide-down that was *still* missed (−0.74%, −0.62%), which is the most damaging pattern available: it means the reset number was not conservative either.
>
> **M&A back-test.** A deal at 12.0x EBITDA / 16.0x EBIT: **the promised ROIC at announcement was 6.325%, already below the 8.5% WACC** — so the deal was value-destructive on management's own numbers before execution. Actual came in at 5.723%, destroying **−$813.5m**, or **−33.9% of the purchase price**, which ties exactly to a perpetuity cross-check and is corroborated independently by a goodwill impairment of 25% of the price. Deal IRR **7.398%**.
>
> **The single best teaching moment in the module.** Blended incremental ROIC across all deployment looks acceptable at **9.63%** — above WACC, nothing to see. Decomposed: **organic reinvestment earned 39.17% but received only 11.1% of the capital**, while **M&A earned 5.94% and received 88.9%.** Management is excellent at reinvesting and terrible at acquiring, and has allocated nine-tenths of the capital to the thing it is bad at. The blended number conceals the entire story, which is why the decomposition is the assessed skill.
>
> **Skin in the game.** $16.0m of reported beneficial ownership becomes **$6.0m outright** once options and unvested awards are stripped; that is **15.0% of estimated net worth**, falling to **5.0% unencumbered** after removing the 66.7% that is pledged against personal borrowings. Zero open-market purchases in eight years. The reported figure overstates alignment by roughly 3x.

---

### M09-E2 — SBC and the Dilution Definition Trap *(flagship for this module)*

**Topics:** Stock-based compensation; buybacks; deployment of cash. Also covers the **"Stock-Based Comp for Investors"** intensive.

**Learning objective.** Make SBC's real cost visible, and show that "net dilution" has competing definitions that can produce **opposite signs in the same year**.

**Student task.** Build the share-count roll-forward; compute gross issuance, issuance net of withholding, and buyback shares; compute net dilution under both definitions and explain the sign conflict; compute SBC as a share of revenue, FCF and market cap; restate FCF yield three ways (reported, charging SBC expense, charging the cash cost of neutralising issuance); compute diluted shares via the treasury-stock method; and compare GAAP to adjusted EPS. **75 minutes.**

**Tools and environment.** Existing spreadsheet, named outputs. Fully auto-gradeable.

**Grading rubric.**
- *Quantitative (85 pts, fully auto):* all figures, tolerance 1e-4. **20 pts specifically for computing net dilution both ways and showing the sign flip** — a student who reports one figure has missed the exercise.
- *Qualitative (15 pts, LLM-graded):* must state which definition they would present and to whom, and why.

**Difficulty.** Intermediate–advanced. **Build complexity.** Low.

**Example and worked answer (verified).**
> Shares 500.0m → 497.0m. Gross issuance 18.0m (**3.600%**); issuance net of shares withheld for taxes 13.0m; buyback 16.0m.
>
> **The trap:** net dilution is **+0.400%** on one definition (gross issuance less buyback, over opening shares: (18.0 − 16.0)/500 = +0.400%) and **−0.600%** on another (the actual change in shares outstanding: (497.0 − 500.0)/500 = −0.600%). **Opposite signs, same year, same company.** The first measures the dilution management created and then repurchased; the second measures what a shareholder experienced. Both are defensible; quoting one without naming it is not.
>
> **What the buyback actually bought.** Of a $1,200m buyback, **81.25% merely offset issuance**; true shrinkage was 3.0m shares, or **0.600%**.
>
> **The money slide.** SBC is 15.00% of revenue and **75.00% of FCF**. Reported FCF yield **2.012%** → **0.503%** charging SBC as an expense → **−0.440%** charging the $975m of cash actually spent neutralising issuance. The business has a negative cash yield to shareholders once you charge what it costs to stop the share count rising.
>
> GAAP diluted EPS **$0.3960** versus adjusted **$1.3465** — a **3.40x** gap, which is **202.0x versus 59.4x** on P/E. Treasury-stock method: 500.0 basic + 4.0 options + 5.6 RSUs + 3.0 PSUs = **512.6m diluted**.

---

### M09-E3 — The Buyback Value Test

**Topics:** Analysing stock buy-backs; deployment of cash.

**Learning objective.** Separate the arithmetic of EPS accretion from the economics of value creation — the distinction juniors most reliably get wrong.

**Student task.** Compute EPS accretion from a stated buyback; compute the break-even pre-tax cost of funds; compute the value created or destroyed at three different intrinsic-value assumptions; compute the buyback IRR static and with growth; compute the maximum justifiable repurchase price; and compute gross and net shareholder yield. Then answer a multiple-choice item on the E/P-versus-cost-of-equity fallacy with a written justification. **50 minutes.**

**Tools and environment.** Existing spreadsheet. Fully auto-gradeable except the justification.

**Grading rubric.**
- *Quantitative (75 pts, auto):* all figures, tolerance 1e-3; the value-creation figure must reconcile two ways.
- *Qualitative (25 pts, LLM-graded, reference-guided):* the justification must correctly reject the E/P-vs-cost-of-equity test as a general value test.

**Difficulty.** Intermediate. **Build complexity.** Low.

**Example and worked answer (verified).**
> Net income $900m, 300m shares, EPS **$3.000**, price $45.00 (**15.00x**), buyback $600m. Shares retired = 600/45 = **13.333m** → 286.667m shares → EPS **$3.1395**, i.e. **+4.65% accretion**. On a comparable illustrative case the research produced **+8.444%** accretion with a break-even pre-tax cost of funds of **8.33%**.
>
> **The value test is a different question.** At an intrinsic value of **$34** against a $40 price, the same buyback **destroys $120m**, cross-checked two ways (20.0m shares × −$6). Running the $45 example: at IV $56 the buyback transfers **+$0.512/share** to remaining holders; at IV $40 it destroys **−$0.233/share**; at IV $45 it is value-neutral. Buyback IRR **6.25% static**, **9.25%** with 3% growth, against a 9% cost of equity; maximum justifiable price **$41.67**. Shareholder yield **12.500% gross / 11.500% net / 12.750%** including debt paydown.
>
> **The multiple-choice item and why it is mis-keyed in most question banks.**
> *"A company earns $3.00/share, trades at $45.00, and has a 9% cost of equity. It announces a buyback. Which is true?"*
> (A) Accretive to EPS and value-creative. (B) Accretive to EPS; value impact depends on intrinsic value. (C) Value-destructive, because E/P of 6.67% is below the 9% cost of equity. (D) Neither accretive nor value-creative.
> **Correct answer: (B).** EPS accretion is guaranteed whenever the earnings yield exceeds the after-tax return forgone on the cash — it is arithmetic, not a value test. **(C) is the attractive distractor and is wrong**: comparing E/P to the cost of equity is a valid value test only for a *no-growth perpetuity*, where justified P/E = 1/r = **11.11x**. For a growing firm, an E/P below r is entirely normal and says nothing about whether the stock is cheap. Here the stock trades at 15.0x against a no-growth justified 11.1x, so the market is pricing growth; whether the buyback creates value depends on the analyst's own intrinsic-value estimate, which is what (B) says.

---

### M09-E4 — The Management Meeting Station *(OSCE-style)*

**Topics:** Structured management meeting process; corporate access; IR; the compliance boundary.

**Learning objective.** Assess **quality of questioning** — otherwise the hardest thing in the syllabus to measure — by making it a binary, logged outcome.

**Student task.** A 15-minute role-play meeting with an AI CFO/IR persona. The student has a pre-read pack and must extract what they need. Afterwards: a 200-word post-meeting note recording what was learned, what remains open, and what changed in the thesis.

**Tools and environment.** Voice or text role-play agent, shared with M02-E4, M05-E4 and M14. The design device is borrowed from medical education's standardised patient: the agent holds a **fact pack** (ground truth), a **disclosure policy** (what it volunteers unprompted versus what it reveals **only if asked a specific question**), a **deflection repertoire** ("we don't guide to that", pivot to a non-answer, cite competitive sensitivity), and a **consistency constraint** (never contradict the fact pack, never invent numbers).

**Grading rubric.**
- *Quantitative (60 pts, deterministic from the transcript):* which **gated facts** did the student extract? Each is binary and logged, which gives this station near-perfect reliability — rare in judgment assessment. Plus a **negative-scored count of "Tier-0" questions** — questions whose answers are already in the 10-K. Each Tier-0 question costs 5 pts, because asking them burns the scarcest resource in the meeting and signals to management that you have not done the work.
- *Qualitative (40 pts, LLM global rating scales, 0–5 per dimension with behavioural anchors):* meeting control; follow-up discipline (did they re-ask when deflected, or accept the non-answer); not-being-sold-to; and the post-meeting note's separation of fact from inference.
- **Plant an MNPI bait.** At a scripted turn, the persona begins to volunteer current-quarter information it should not. **Failure to interrupt is a critical failure that caps the station**, independent of fact extraction. This is the single highest-value design element in the module.
- Use **global ratings, not checklists, for the judgment dimensions**: the evidence (eight 15-minute stations, 53 residents) gives inter-station reliability of **α = 0.79 for a checklist, 0.85 for global ratings alone, and 0.89 for checklist-then-global** — so global ratings beat checklists, and adding a checklist on top of global ratings adds essentially nothing. Note that α = 0.79 is still respectable; checklists are not unreliable, just less good here. Use the checklist for the *objective* fact-extraction half and global ratings for the judgment half, and **never average the two into one number.**

**Difficulty.** Advanced. **Build complexity.** High — but amortised across four modules, and note that the only-if-asked checklist device **already exists commercially** in medical education (Shadow Health / Elsevier's Digital Clinical Experiences score "essential interview components" exactly this way). Cite it as proof of concept rather than claiming novelty.

**Example scripted exchange.**
> **Student:** "Can you talk about how you think about the pricing environment in Industrial?"
> **CFO (deflection 1, scripted):** "We've seen good volume momentum in Industrial and we're pleased with the team's execution there."
> *— The student has been given a non-answer. The graded behaviour is whether they notice and re-ask.*
> **Strong student:** "I appreciate that — but specifically on price rather than volume: was realised price positive or negative in the quarter, and is the direction different in rebates versus list?"
> **CFO (gated fact, releases only to a specific price question):** "Realised price was modestly negative. Most of that is rebate-driven rather than list."
> *— Gated fact extracted. Logged. Worth full marks on that item.*
> **Weak student:** "Great, that's helpful. Moving on to the Advanced Materials segment…"
> *— Non-answer accepted. Fact not extracted. The follow-up-discipline rating drops, and the post-meeting note will reveal whether the student even registered that they did not get an answer — which is the deeper failure.*
## Module 10 — Assessing Expectations

### Expected content coverage

**Scope.** The module that separates a buy-side analyst from a competent accountant: not "what will the numbers be" but "what is already in the price, and where is my view different." Together with M04 this is the analytical core.

| Topic | What mastery looks like |
|---|---|
| Expectations vs. reality | Stocks move on the gap between the two, not on the level of either. |
| Guidance and sell-side estimates | How the published bar forms; GAAP vs. adjusted; the distribution versus the mean; stale estimates; dispersion. |
| Price-implied expectations | **Reverse DCF as a *frontier*, not a point.** The method: estimate what the price implies, identify where your view differs, then buy/sell/hold. Three operating value drivers — **sales growth, operating margin, incremental investment rate** — plus the cash tax rate; **sales is the "turbo" trigger.** |
| Market-implied CAP | Translate an EV/IC multiple into "how many years of excess returns is the market paying for." |
| Buy-side whisper | The published consensus is not the bar. **Honest flag: broker "buy-side bar" survey products have no citable public documentation at all** — a notable hole on a central topic. Teach the concept and the inference method; do not cite a product. |
| Positioning | 13F (and its 45-day lag), short interest, days-to-cover, **utilisation** (the number juniors skip), borrow fee as a crowding signal, options open interest, crowding baskets. |
| Contrarian positioning | Crowding cuts both ways: your best ideas hurt most in a de-grossing because "best" and "most crowded" are correlated. |
| Expectations gap; variant view | The gap must be measured against the *right* bar, which is rarely the published consensus. |
| Core debate and key drivers | Carried from M03. |
| Critical questions | Situation overview, differentiation, monetisation path. |

**Prerequisites.** M04 (return decomposition); M06 (consensus mechanics); M11's multiples algebra. **A real syllabus gap: there is no options primer anywhere in the 15 modules or 9 intensives**, yet implied-move work requires one. Either add a short primer or supply the option mathematics inside the exercise.

**Provenance.** "Spring-loaded," "model linkage," "exceptionalism" and the "7-Year Test" remain **unsourced FE coinages** (the 7-Year Test has a real FE thread — "Terminal Value Debates & the 7 Year Test," describing a payback analysis, with the mechanic truncated in every available extract). On the tails prior, prefer Caughran's better-sourced own words — **"90% of stocks are somewhat fairly valued"** — over the 80/10/10 rendering, which survives only via a machine transcript.

---

### M10-E1 — The Expectations Gap Trap *(flagship for this module and arguably for the program)*

**Topics:** Expectations gap; buy-side whisper; variant view; differentiated view.

**Learning objective.** Destroy the single most common junior error in the entire course: comparing your EPS to published consensus and calling the difference an edge.

**Student task.** A twin-stimulus item. The student receives two situations with **identical fundamentals** — same company financials, same model, same EPS estimate versus published consensus — differing only in the inferred buy-side bar and the positioning data. For each: compute the gap versus published consensus and versus the inferred bar; build a scenario tree; compute expected move, raw and probability-weighted reward/risk; compare to the option-implied move; and give a verdict. Then explain why the two situations have opposite answers. **75 minutes.**

**Tools and environment.** Existing spreadsheet + custom data packs (including an option chain). Mostly auto-gradeable.

**Grading rubric.**
- *Quantitative (70 pts, fully auto):* both gaps, the trees, both reward/risk measures, the implied move, tolerance 1e-3.
- *Qualitative (30 pts, LLM-graded, reference-guided):* the explanation must attribute the divergence to the **bar and the positioning**, not to the fundamentals, and must state that the fundamentals are identical. This is the whole item.
- **Design note:** the twin structure is what makes this robust. A student cannot pattern-match "big beat = buy," because the same beat produces opposite verdicts.

**Difficulty.** Advanced. **Build complexity.** Medium.

**Example and worked answer (both verified).**
> **Situation A.** Published consensus EPS **$2.25**; your model **$2.42**; inferred buy-side bar **$2.40**.
> *Junior:* 2.42/2.25 − 1 = **+7.56%** — "big beat, buy."
> *Strong:* 2.42/2.40 − 1 = **+0.83%**. The junior has **overstated the edge by roughly 9x.**
> Scenario tree: bull p=0.30 at +14.0%; base p=0.45 at −1.0%; bear p=0.25 at −17.0% → **expected move −0.50%**. Raw up/down 0.82:1; probability-weighted +4.20%/−4.70% = **0.89:1**. Option-implied move **9.29%**.
> **Verdict: a +7.6% "beat versus consensus" is a negative-EV long into the print.** The bar is at $2.40, positioning is heavy, and the implied move is wider than your edge.
>
> **Situation B — identical fundamentals, low bar, washed-out positioning.** Bull p=0.35 at +18.0%; base p=0.45 at +3.0%; bear p=0.20 at −12.0% → **expected move +5.25%**; probability-weighted reward/risk **3.19:1**.
>
> **Two tables, identical fundamentals, opposite answers.** That is Module 10 in one item.

---

### M10-E2 — Reverse DCF as a Frontier

**Topics:** Price-implied expectations; what's priced in; the three operating value drivers.

**Learning objective.** Stop treating reverse DCF as "solve for the growth rate." The output is a **frontier** of driver combinations the price can tolerate, and the analyst's job is to judge which point on it is plausible.

**Student task.** Given a price, current financials, WACC and an explicit forecast horizon: solve for implied sales CAGR at the current margin; then hold price constant and solve for the margin required at a lower growth rate, and the growth required at a lower margin, and the growth required at a higher investment rate. Plot the frontier. Compute the steady-state value share of price. Then: build bull/base/bear from your own driver views and value each. **90 minutes.**

**Tools and environment.** Spreadsheet with goal-seek, or Python. Fully auto-gradeable.

**Grading rubric.**
- *Quantitative (80 pts, fully auto):* each solve, tolerance 1e-3; the PV must reconcile to the given price in every case (a hard check — 20 pts); the steady-state share; the three scenario values.
- *Qualitative (20 pts, LLM-graded):* must state which frontier point is most plausible **and name the evidence that would discriminate**. An answer that reports the numbers without a judgment scores ≤8.

**Difficulty.** Advanced. **Build complexity.** Medium.

**Example and worked answer (fully verified; every PV reconciles).**
> Sales $10.0bn, tax 21%, WACC 8%, 8-year explicit horizon, continuing value = NOPAT₈/WACC, EV **$25.0bn** (2.50x sales).
>
> **Steady-state value** = 1.185/0.08 = **$14.812bn = 59% of price.** So **41% of the price is future value creation** — that framing alone reorients most students.
>
> Holding margin at 15.0% and incremental investment rate at 30%: **implied sales CAGR = 9.935%** (PV explicit $7.926bn + PV CV $17.074bn = **$25.000bn** ✓; CV is 68.3% of value).
>
> **The frontier — the actual output:**
> - If sales CAGR is only **4.0%**, the price requires a **20.37% margin**.
> - If margin is only **12.0%**, the price requires a **14.59% CAGR**.
> - If the investment rate rises to **45%**, the price requires a **10.89% CAGR**.
>
> **The "turbo" demonstration:** giving up ~6pp of sales growth requires **+5.4pp of margin** to offset. Sales growth does the heavy lifting, which is why it is the trigger to interrogate first.
>
> Scenarios: bull (11.0% / 16.5%) → $29.41bn = **+17.6%**; base (6.0% / 14.0%) → $18.80bn = **−24.8%**; bear (2.0% / 11.5%) → $12.49bn = **−50.0%**.
>
> **Companion solve — market-implied CAP.** With IC₀ $10.0bn, ROIC 18%, WACC 8% and IC growing 8%, each year's PV of economic profit is constant at $0.926bn, so EV is **linear in CAP**: 0/5/10/15/20/30 years → $10.0 / 14.63 / 19.26 / 23.89 / 28.52 / $37.78bn. **At an EV of $22.0bn the market-implied CAP is 12.96 years** (10.0 + 12.96 × 0.926 = 22.000 ✓). That converts an EV/IC of 2.2x into a falsifiable competitive assertion: *the market is paying for thirteen years of 10-point excess returns.* Ask whether the industry has ever sustained that.

---

### M10-E3 — Positioning Triangulation (with the limits stated)

**Topics:** Assessing positioning; contrarian positioning; crowding.

**Learning objective.** Read positioning from multiple imperfect sources and state what each one cannot tell you.

**Student task.** Given 13F data, short interest, float, ADV, securities-lending data (lendable, on-loan, fee), an options chain and a crowding-basket percentile: compute SI as a share of shares outstanding **and** of float, days-to-cover, utilisation, and the annualised carry; then state a positioning verdict with an explicit list of what the data cannot establish; and quantify 13F staleness at three portfolio-turnover rates. **60 minutes.**

**Tools and environment.** Existing spreadsheet. Fully auto-gradeable except the limits list.

**Grading rubric.**
- *Quantitative (70 pts, fully auto):* all metrics, tolerance 1e-3. **Both SI bases required** — reporting only one costs 10 pts, because the float basis is typically ~33% higher and the choice changes the conclusion.
- *Qualitative (30 pts, LLM-graded):* the limits list must include the 45-day 13F lag, that 13Fs show no shorts and no non-US holders, that short interest is reported with a lag and does not reveal *who*, and that on-loan can exceed short interest because of non-short borrowing.

**Difficulty.** Intermediate. **Build complexity.** Low.

**Example and worked answer (verified).**
> 120m shares outstanding, 30m strategic, so **90m float**. Short interest 13.5m; ADV 1.8m; lendable 20m; on-loan 15.2m; fee 11.5%.
>
> SI as % of shares out = 13.5/120 = **11.25%**; as % of float = 13.5/90 = **15.00%** — the float basis is **33.3% higher**, and 15% reads very differently from 11%. Days-to-cover = 13.5/1.8 = **7.50 days** — but **15.0 days if ADV halves**, which is what happens in a squeeze, so *the risk lives in the denominator.* Utilisation = 15.2/20 = **76.0%**. On-loan exceeds short interest by **12.59%**, which means there is non-short borrowing in the number.
>
> A second verified example: SI 28.4m / float 240m = **11.83%**; DTC 28.4/3.1 = **9.16**; utilisation 28.4/72 = **39.4%**; a 11.5% fee over 90 days = **2.84% carry**. Read: a large short position but **not cornered** — utilisation at 39% says borrow is still available, and utilisation is the number juniors omit.
>
> **13F staleness, quantified.** At the 45-day lag, the share of the book already changed by filing date is **7.1% at 60% annual turnover, 21.9% at 200%, and 38.9% at 400%.** The lesson: 13Fs are nearly harmless for long-only managers and nearly useless for the high-velocity pods you most want to see.

---

### M10-E4 — Expected vs. Implied: Choosing the Instrument

**Topics:** Estimating upside/downside; expectations gap; risk/reward.

**Learning objective.** Decide whether your view is better expressed in stock or in options, by comparing your expected absolute move to the market's.

**Student task.** Given your scenario tree and an option chain, compute your expected absolute move and the option-implied move three ways (raw straddle/spot, the practitioner-adjusted figure, and a true one-standard-deviation figure); compare to the realised-move distribution of the last eight prints; and recommend an expression with sizing. **50 minutes.**

**Tools and environment.** Existing spreadsheet. Auto-gradeable.

**Grading rubric.**
- *Quantitative (75 pts, auto):* all three implied-move computations and the comparison, tolerance 1e-3.
- *Qualitative (25 pts, LLM-graded):* the recommendation must follow from whether the student's expected move exceeds the implied move, and must mention that a wide implied move makes a stock expression safer and an option expression expensive.

**Difficulty.** Advanced. **Build complexity.** Low–medium (needs an option chain in the pack).

**Example and worked answer (verified).**
> Stock **$84.50**; the 85-strike call **$4.05** and put **$3.80**, so the straddle is **$7.85**.
> Raw implied move = 7.85/84.50 = **9.29%**; breakevens **$76.65 / $92.35**. The 0.85x practitioner convention gives **7.90%**. The true one-standard-deviation figure = 9.29% × 1.2533 = **11.64%** (check: 0.7979 × 0.11643 × 84.50 = **$7.850** ✓). A straddle/strangle average using the 87.5 call at $2.95 and the 82.5 put at $2.70 gives **7.99%**.
>
> The relationship worth teaching, because almost nobody does: the Black-Scholes ATM straddle is ≈ **0.7979 × S × σ√T**, and the expected absolute move is **S × σ√T × √(2/π) = 0.7979 × S × σ√T**. **The coefficients are identical, which is why straddle/spot *is* the risk-neutral expected absolute move** — not an approximation of it.
>
> Last eight prints realised 6.1 / 9.4 / 4.2 / 11.8 / 5.5 / 7.0 / 8.9 / 3.6%: mean **7.06%**, median 6.55%. So the raw 9.29% is **modestly rich** against history, and roughly fair on the adjusted basis.
>
> **Recommendation logic:** if your tree's expected absolute move is below ~7%, you are being asked to pay for more movement than you expect — express in stock, or sell the volatility if mandated. If above ~10%, the option is the cheaper expression of your view. **Full credit requires naming which side of the implied move the student's own expectation falls on**, not just computing both.
## Module 11 — Applied Valuation

### Expected content coverage

**Scope.** Valuation as a buy-side working tool on a 12–24 month horizon, not a 10-year academic DCF. The DCF is a thinking device; the working method is a forward-multiple / earnings-power / price-target-with-risk-reward approach. Also covers the **"Valuation Q&A"** and **"The Value of Growth"** intensives.

**The algebra that is the spine of the module.** "Multiples are shorthand for a DCF" is not a slogan, it is a derivation, and the module lives or dies on whether students can do it. From the Gordon growth model P₀ = D₁/(r − g), with D₁ = payout × E₁, and g = b × ROE so that b = g/ROE and payout = 1 − g/ROE:

```
Justified forward P/E  = (1 − g/ROE) / (r_e − g)        [EQUITY: ROE with cost of equity]
Justified trailing P/E = (1 − g/ROE)(1 + g) / (r_e − g)
EV/NOPAT₁              = (1 − g/ROIC) / (WACC − g)      [ENTERPRISE: ROIC with WACC]
EV/EBIT₁               = (1 − t)(1 − g/ROIC) / (WACC − g)
EV/IC₀                 = (ROIC − g) / (WACC − g)
```

**A precision point worth building an item around:** the widely-circulated form "(1 − g/ROIC)/(r − g)" is correct only for an all-equity firm, or when read as **EV/NOPAT with r = WACC**. **Mixing ROIC with a cost of equity is a specific, gradeable error.** The equity version takes ROE and the cost of equity; the enterprise version takes ROIC and WACC.

**The corollary that makes the whole module click:** **ROIC = WACC ⇒ EV/IC = 1.0 for every value of g.** Verified: at ROIC = WACC = 9%, EV/IC is exactly 1.000000 at g = 0, 2, 4, 6 and 8%, and EV/NOPAT is flat at 1/WACC = **11.1111x** — Mauboussin's "commodity multiple." Growth is value-neutral when returns equal the cost of capital, and the algebra says so in one line.

**The grid every student should be able to reproduce** (EV/NOPAT, WACC 9%, all verified):

| | g=0% | g=2% | g=4% | g=6% |
|---|---|---|---|---|
| **ROIC 6%** | 11.11x | 9.52x | 6.67x | 0.00x |
| **ROIC 9% (=WACC)** | 11.11x | 11.11x | 11.11x | 11.11x |
| **ROIC 16%** | 11.11x | 12.50x | 15.00x | 20.83x |
| **ROIC 25%** | 11.11x | 13.14x | 16.80x | 25.33x |

At ROIC below WACC, **growth destroys the multiple** (11.11 → 9.52 → 6.67). At ROIC = WACC the row is flat. The market agrees with the algebra: live medians for the S&P ex-financials/real-estate showed high-spread/high-growth at **19.5x**, high-spread/low-growth **14.0x**, low-spread/high-growth **11.7x**, low-spread/low-growth **11.4x** — **being in the high-ROIC-spread half beats being in the high-growth half.**

**The value of growth, closed form:**
```
GV = NOPAT · g · (ROIC − WACC) / [ROIC · WACC · (WACC − g)]      ⇒   sign(GV) = sign(ROIC − WACC)
```
Verified at NOPAT 180, WACC 9%: (g 4%, ROIC 16%) → **+700.00**, cross-checking exactly against (15.0000 − 11.1111) × 180; (g 4%, ROIC 6%) → **−800.00**; (g 4%, ROIC 9%) → **0.00**; (g 0%, ROIC 16%) → **0.00**. Also: **EPV is the value-driver formula at g = 0, i.e. NOPAT/WACC** — which unifies the earnings-power and multiples sections.

| Other topics | What mastery looks like |
|---|---|
| DCF mechanics | FCFF vs. FCFE and matching discount rates; WACC construction and beta instability; mid-year convention; the enterprise-to-equity bridge. **SBC is not a bridge item** — it is an FCFF expense plus a share-count item. |
| Terminal value "perception" | The word is *perception*, not calculation, which points at the behavioural reading: continuing value is **"commonly in excess of 75 percent"** of DCF value, and *"what drives the DCF model is for the most part a dressed up multiple."* So re-ratings are repricings of the terminal block — which links directly to M04's perception shifts. McKinsey's range across four industries is **56%–125%**, and a high share is not per se a flaw. |
| Choosing a multiple | Which multiple for which business; vs. own history, peers and market; **regress the peer set on growth and ROIC and read the residual.** Mauboussin, verbatim: analysts *"often select a peer group that leads to the desired answer."* And: **"You have to earn the right to use a multiple."** |
| P/E roll-forward | **Flagged vague** — no textbook definition exists. Pin it down explicitly as target multiple × forward EPS at a stated future date, and teach the calendar effect. |
| Disaggregating returns | As M04, with the cross term. |
| Risk/reward and scenario trees | Bull/base/bear with probabilities; expected value; asymmetry; the implied-probability check. |

**Context worth giving students:** roughly **93% of ~2,000 surveyed CFA members use market multiples; 88% use P/E; 77% use an EV multiple; 79% also use a DCF.** Multiples are the working tool and the DCF is the discipline behind it — which is exactly this module's framing.

---

### M11-E1 — Derive the Multiple *(flagship for this module)*

**Topics:** Multiples as shorthand for a DCF; value of growth; choosing a multiple.

**Learning objective.** Make the student derive, not memorise — so that they can answer any "two companies identical except X" question from first principles.

**Student task.** (a) Derive justified forward P/E from the Gordon model, showing every substitution. (b) Derive EV/IC = (ROIC − g)/(WACC − g). (c) Prove that ROIC = WACC makes EV/IC equal 1.0 for all g, and explain in one sentence what that means economically. (d) Build the four-by-four ROIC × growth grid. (e) Verify one cell by brute force against a 200-year explicit DCF. (f) Compute the value of growth at three ROIC levels using the closed form, cross-checking against the difference between the value-driver multiple and 1/WACC. **100 minutes.**

**Tools and environment.** Spreadsheet or Python plus written derivation. Numeric parts auto-gradeable; derivations LLM-graded with the worked key supplied.

**Grading rubric.**
- *Quantitative (70 pts, fully auto):* the grid (16 cells), the brute-force reconciliation (must agree to within 0.01%), the three GV figures and their cross-checks.
- *Qualitative (30 pts, LLM-graded, reference-guided with the full derivation as the reference):* algebraic steps must be present and correct, not asserted. **Per the verification evidence, never let an LLM judge a quantitative derivation without the worked key in context** — reference-guided grading cuts the math-grading failure rate dramatically, and an unreferenced LLM judge has been shown to pass a majority of proofs containing critical errors.
- **Deterministic first, LLM second:** every number is checked arithmetically before any LLM sees the submission, and the LLM grades only the *reasoning*.

**Difficulty.** Advanced. **Build complexity.** Low (the key is the work).

**Example and worked answer.**
> **(b) The EV/IC derivation, in three lines.** EV = NOPAT(1 − g/ROIC)/(WACC − g). Substituting NOPAT = ROIC × IC: EV = ROIC × IC × (1 − g/ROIC)/(WACC − g) = IC × (ROIC − g)/(WACC − g). **Therefore EV/IC = (ROIC − g)/(WACC − g).**
>
> **(c)** Set ROIC = WACC: EV/IC = (WACC − g)/(WACC − g) = **1.0, for every g.** Economically: a business earning exactly its cost of capital is worth exactly the capital invested in it, no matter how fast it grows — growth neither creates nor destroys value, it just moves cash around. *This is the single most important sentence in the module.*
>
> **(e) Brute-force check.** g = 4%, ROIC = 16%, WACC = 9%: value-driver gives (1 − 0.25)/0.05 = **15.00x**. By construction: reinvestment rate b = 25%, FCF₁ = 75 on NOPAT 100, EV = 75/0.05 = **1,500**, so EV/NOPAT = **15.00x** ✓. A 2,000-year explicit DCF gives **1,499.9999** ✓. IC₀ = 625, so EV/IC = 1,500/625 = **2.40** = (0.16 − 0.04)/0.05 ✓. EV/EBIT at t = 25% = 0.75 × 15 = **11.25x**, checked against EBIT₁ = 133.33 → 1,500/133.33 = **11.25x** ✓.

---

### M11-E2 — The P/E Roll-Forward Calendar Trap

**Topics:** P/E roll-forward; disaggregating returns; price targets.

**Learning objective.** Teach a method the course names but no textbook defines — and expose the date error that makes price targets silently wrong by double digits.

**Student task.** Given today's date, a December fiscal year-end, and EPS for FY, FY+1 and FY+2: compute NTM EPS and NTM P/E by day-weighting; then compute the price target three ways (target multiple on FY+1; on FY+2; on NTM-as-of-one-year-forward) and the implied return in each case; compute the price-target jump that occurs on 1 January with no new information; and build the "growing into the multiple" table at a frozen price. **55 minutes.**

**Tools and environment.** Existing spreadsheet. Fully auto-gradeable.

**Grading rubric.**
- *Quantitative (85 pts, fully auto):* the day-weighting, all three targets and returns, the calendar jump, and the four-year multiple decay table, tolerance 1e-4.
- *Qualitative (15 pts, LLM-graded):* must state which convention they would use and why, and must acknowledge the calendar artefact.

**Difficulty.** Intermediate. **Build complexity.** Low.

**Example and worked answer (verified).**
> Today 21 October 2026; December year-end; price **$100**; EPS FY26 **$5.00**, FY27 **$5.75**, FY28 **$6.6125**. Days to year-end = 71, so the NTM weight on FY26 is **w = 0.19452**.
>
> **NTM EPS** = 0.19452 × 5.00 + 0.80548 × 5.75 = **$5.6041**; **NTM P/E = 17.844x**.
>
> At an 18x target: **(i)** 18 × FY27 = **$103.50 (+3.50%)**; **(ii)** 18 × FY28 = **$119.03 (+19.02%)**; **(iii)** 18 × NTM-as-of-Oct-2027 ($6.4447) = **$116.01 (+16.01%)**, plus a 1.5% dividend = **17.51% TSR**.
>
> **Method (i) understates the return by 12.5 points** purely through a date mismatch — it applies a 12-month-forward multiple to a number that is already partly historical by the time the target is supposed to be achieved.
>
> **The calendar artefact.** On 31 December the FY+1-based target is **$103.50**; on 1 January, with the year roll, it becomes **$119.03** — a **+15.00% price-target increase on zero information.** Any analyst publishing targets on an FY+1 convention does this every January, and most do not say so.
>
> **"Growing into the multiple," price frozen at $100:** P/E goes **20.00x → 17.39x → 15.12x → 13.15x** across FY26–FY29. The stock gets cheaper by standing still, which is the entire bull case for a compounder and must be stated as a multiple path, not a feeling.

---

### M11-E3 — Scenario Trees, Implied Probability and the "Theatre" Diagnostic

**Topics:** Scenario trees with weighted outcomes; risk/reward framework; terminal value perception.

**Learning objective.** Build trees that carry information, detect trees that are cosmetic, and back out what probability the market is assigning.

**Student task.** Given a price, a cost of equity and three scenario prices: compute expected value, raw and probability-weighted asymmetry, and the discounted expected return; back out the market-implied bull probability both naively and discounted; apply the "three-scenario theatre" diagnostic; then re-run with a deeper bear case and a de-rated bear multiple and report what changes. Finally, size the position from the bear case. **70 minutes.**

**Tools and environment.** Existing spreadsheet. Fully auto-gradeable.

**Grading rubric.**
- *Quantitative (75 pts, fully auto):* all computations, tolerance 1e-4; both implied-probability methods required.
- *Qualitative (25 pts, LLM-graded):* must explain why the naive and discounted implied probabilities differ, and must state that the bear case drives position size.

**Difficulty.** Advanced. **Build complexity.** Low.

**Example and worked answer (verified).**
> Spot **$50**, 12-month horizon, cost of equity 9%. Bull **$75** (30%), base **$52** (50%), bear **$30** (20%).
>
> EV = **$54.500 = +9.000%**. But upside to *base* is only **+4.00%**. Raw asymmetry 25/20 = **1.250:1 — fails a 2:1 screen.** Probability-weighted 8.500/4.000 = **2.125:1**. And discounting: 54.500/1.09 = **$50.0000**, so **alpha is exactly 0.00%** — the +9% raw upside *is* the 9% cost of equity. The tree looks like an idea and is not one.
>
> **Implied bull probability, two ways.** Naive (EV = spot): 50 = 23p + 47.6 → **p = 10.43%**. Discounted (EV = spot × 1.09): 23p + 47.6 = 54.5 → **p = 30.00%**. **The naive check flatters the analyst by ~20 points of bull probability** because it credits the cost of capital as alpha. Students must use the discounted version.
>
> **Deepen the bear to $38:** EV $56.10, discounted $51.4679, **alpha +2.936%**, asymmetry **2.083:1**, implied bull probability **23.04%** against our 30% — **edge +6.96 points.** Now it is an idea.
>
> **The theatre diagnostic.** A symmetric ±20% tree at 25/50/25 gives EV/base = **1.000** — a literal no-op; the tree contains no information. **If EV/base ≈ 1.00, the tree is cosmetic.** (Here 54.5/52 = 1.0481, so it is doing some work.) A second common cosmetic failure: holding the multiple constant across scenarios. A −25% EPS bear at an unchanged 18x is a −25% price; at a de-rated 13x it is **−45.83%** — **holding the multiple constant halves the measured downside.**
>
> **Sizing from the bear.** The practical rule is size = tolerable NAV loss ÷ bear downside. At 0.50% tolerable and a −40% bear: **1.2500% of NAV** (check: 1.25% × 40% = 0.50% ✓). **The bear case determines position size — not the upside, not conviction.** Note why full Kelly is unusable here: with p = 0.55, +20%/−15%, the correct asset form f* = (p·a − q·b)/(a·b) gives **141.7% of capital in one name** (the gambling form f* = (p·b − q)/b is wrong for assets, which lose a *fraction*, not the whole stake). That absurd output is the argument for fractional Kelly: half-Kelly retains ~75% of the log growth at half the bet, while 2x Kelly earns **approximately zero growth at double the volatility** — strictly dominated, not merely riskier.

---

### M11-E4 — Critique This DCF (eight planted errors)

**Topics:** DCF mechanics; terminal value; WACC; the enterprise-to-equity bridge.

**Learning objective.** Find errors in someone else's valuation — which research consistently suggests is a better-discriminating task than building one from scratch.

**Student task.** A complete, professional-looking DCF with **eight planted errors**, each independently scored: a faulty risk-free rate; a terminal growth rate above the economy's nominal growth; a forecast period too short for the business's competitive position; a terminal value taken from an EV/EBITDA multiple (i.e. "multiples analysis dressed up as a DCF"); a mid-year convention applied to the explicit period but not the terminal value; SBC added back to FCFF while also being excluded from the share count; a pension deficit omitted from the bridge; and a beta sourced from a period that misrepresents the current capital structure. Identify each, state the direction and approximate magnitude of its effect, and produce a corrected value. **100 minutes.**

**Tools and environment.** Existing spreadsheet with the flawed model supplied. Fully auto-gradeable per error.

**Grading rubric.**
- *Quantitative (80 pts, fully auto):* 8 pts per error found and correctly signed (64), plus 16 pts for the corrected value within tolerance. **Independent scoring per error** means partial competence is measured rather than lost.
- *Qualitative (20 pts, LLM-graded):* a ranked list of which errors matter most. Full credit requires identifying the terminal-value errors as dominant and saying why — because continuing value is typically well over 75% of the total.
- **This is the best-sourced assessment artefact in the module:** each planted error maps to a documented, citable DCF failure mode rather than to invented pedantry.

**Difficulty.** Advanced. **Build complexity.** Low–medium.

**Example and worked answer (the reference DCF, verified).**
> FCFF 100 / 110 / 120 / 128 / 135, WACC 9%, terminal g 2.5%. TV₅ = 138.375/0.065 = **2,128.8462**; PV of explicit period **455.409**; PV of TV **1,383.604**; **EV 1,839.013**, with **TV = 75.24% of value.**
>
> **The mid-year trap, which is the one most students miss.** Discounting the terminal value at t = 4.5 instead of t = 5 gives EV **1,919.99**; at t = 5 with a mid-year explicit period, **1,859.07**; fully end-year, **1,839.01**. **The terminal-value exponent choice alone moves the valuation by 4.4%** — more than most of the operating assumptions students spend their time debating.
>
> **The bridge:** 1,839.01 − net debt 500 + associates 120 − minorities 80 + investments 60 − after-tax pension 75 − other 40 + NOLs 30 = **equity 1,354.01**, giving **$13.5401 on basic** but **$12.8954 on diluted (−4.76%)**.
>
> **The implied-exit-multiple cross-check that should be mandatory:** the TV implies an exit EV/EBITDA of **7.10x** on EBITDA of 300. If instead you assert an 8.0x exit multiple, the implied terminal growth is **(0.09 × 2,400 − 135)/(2,400 + 135) = 3.1953%** — so asserting 8.0x is asserting 3.2% perpetual growth. Every DCF should state both numbers so the assumption cannot hide.
>
> **A bonus item worth including, because most question banks get it wrong.** "Does leverage raise P/E?" The condition is exact: with EV 1,000, EBIT 75 and t = 25%, the unlevered equity earnings yield is **5.625%**, so the break-even pre-tax cost of debt is **7.500%**. At 6% debt, P/E *falls* with leverage (17.778 → 16.374 → 13.675x at debt of 0/300/600). At 10% debt, P/E *rises* (→ 20.741 → 35.556x). At exactly 7.5%, **P/E is invariant to leverage at 17.7778x.** **An item keyed "leverage raises P/E" as a general rule is mis-keyed.**
## Module 12 — Short Selling

### Expected content coverage

**Scope.** Mechanics, taxonomy, timing and risk management on the short side — plus using the short mindset to improve long work.

**⚠ Regulatory currency warning — the highest-risk content in the blueprint.** Short-selling rules have moved repeatedly and recently. One fact verified during this work, which a research pass had wrong: the SEC's institutional short-position reporting is on **Form SHO** (not "Form SHORT") under **Rule 13f-2**, and its compliance date has been **deferred to 2 January 2028, with first filings due 14 February 2028**. The Fifth Circuit **remanded the rule to the SEC without vacating it** (August 2025), directing the Commission to quantify the cumulative economic impact of Rule 13f-2 together with the securities-lending rule; the SEC's December 2025 exemptive order extended the dates while it considers its response, which may include proposed amendments. **Design rule: write short-selling regulation items *conceptually*, not factually** — ask "why would a regulator publish aggregated rather than attributed short data?" rather than "when must Form SHO be filed?" Conceptual items survive rule changes; factual ones become wrong silently. Where a factual item is unavoidable, date-stamp the answer key and put it on a review cycle.

| Topic | What mastery looks like |
|---|---|
| Mechanics | Locate and borrow; stock-loan rate and rebate; hard-to-borrow vs. general collateral; Reg T's 150% requirement and portfolio margin; **the short pays the dividend**; recall and buy-in risk; Reg SHO's locate and close-out requirements and the alternative uptick rule's 10%-decline trigger. |
| Challenges and risks | The P&L asymmetry: gains cap at 100%, losses are unbounded, **and the position grows against you** while a losing long shrinks. That is the squeeze engine and it is pure arithmetic. |
| Shorting approaches | Alpha / structural / event-driven / hedging. **The syllabus never states how this axis relates to the separate "short alpha buckets" bullet**; the defensible authoring decision is a 2×2 of *purpose* against *thesis type*. |
| Short alpha buckets | Fraud/accounting; structural decline ("melting ice cubes" — **verbatim Caughran**, from M08); overvaluation/multiple compression; broken-growth/deceleration; cyclical peak; balance-sheet/refinancing; promotional management; serial acquirers; index/flow; hedge and pair legs. **Broken-growth/deceleration is the best bucket for a junior capstone** — modellable, dated catalyst, fits a carry budget. **Overvaluation is the worst** — no catalyst, unbounded carry. |
| Timing and risk management | The carry clock; why shorts need catalysts and tighter stops; the structural headwind of long-run equity drift. |
| Earnings-season tactics for shorts | Pre-print squeeze risk; trimming into catalysts. Overlaps M13. |
| De-grossing | Mechanically, simultaneous risk-limit-driven gross reduction across many pods. The real-time signature matters more than the definition. |
| Quantitative short *selection* | Note the syllabus says **selection**, not "selling" — this implies screening and ranking, not execution. Short-side factor evidence, and why short anomalies are harder to harvest (borrow cost, capacity, squeeze risk). |
| The short mindset applied to longs | Inversion; the disconfirming-evidence habit; "what does the short case look like" as a required section of every long thesis. |

**Scope flag.** Forensic accounting (Beneish, Sloan, the Schilit taxonomy) is **not named anywhere in the Module 12 bullets**. It is genuinely useful here but is a candidate **optional/advanced track** rather than core — decide before building items.

**Provenance.** Caughran's own words for the short alpha buckets and for de-grossing were **not recoverable**; the taxonomy above is assembled, not his. Verified as genuinely his from the syllabus: "Short melting ice cubes with structural headwinds" (M08) and "peak-on-peak"/"spring-loaded" (M13).

---

### M12-E1 — Full Short P&L and the Carry Clock *(flagship for this module)*

**Topics:** Mechanics; timing and risk management; challenges of shorting.

**Learning objective.** Make carry visceral. Most junior short pitches are long pitches with a minus sign and no carry budget.

**Student task.** Compute the complete P&L of a short over a stated holding period, including borrow fee, rebate, dividend liability and margin; compute the return on notional and on posted equity under both Reg T and portfolio margin; compute the carry at a flat price and annualise it; compute the break-even borrow fee; and compute the unhedged return hurdle a beta-1 short must clear. **65 minutes.**

**Tools and environment.** Existing spreadsheet. Fully auto-gradeable.

**Grading rubric.**
- *Quantitative (85 pts, fully auto):* every line, tolerance 1e-3. **Two convention checks worth 20 pts:** the borrow fee must be computed on *average* market value with the entry-value alternative noted, and the day-count basis must be stated — conventions genuinely differ and an answer that does not declare its convention is incomplete, not wrong.
- *Qualitative (15 pts, LLM-graded):* must state the carry at a flat price as an annualised figure and say what it implies for the maximum tolerable time-to-catalyst.

**Difficulty.** Intermediate. **Build complexity.** Low.

**Example and worked answer (verified).**
> Short 10,000 shares at **$50**, cover at **$42**, 90 days, borrow 350bp, rebate 430bp, Act/360, two $0.20 dividends.
>
> Price P&L = (50 − 42) × 10,000 = **+$80,000**. Borrow fee on average market value ($460,000) = **−$4,025** (on the entry-value convention it is −$4,375 — **declare which you used**). Rebate = **+$5,375**. Dividend liability = **−$4,000** (the short pays). **Net $77,350 = 15.47% of notional.** On Reg T equity of $250,000 that is **30.94%**; at a 15% portfolio-margin requirement, **103.13%**.
>
> **The number that matters most: at a flat price the carry is −$3,000, or −2.40% annualised.** Note what produced it — the net rebate is *positive* (rebate 430bp exceeds borrow 350bp), and **the dividend liability alone flips the carry negative.** Students routinely model borrow and forget the dividend.
>
> A second verified case shows the full hurdle: an unhedged beta-1 short must overcome equity drift plus borrow plus dividends, a **10.80%–13.00% annual hurdle**, compounding to **37.01% over five years.** The useful heuristic: **1,200bp of borrow ≈ 1% per month.**

---

### M12-E2 — The Asymmetry Engine and the Forced Rebalance

**Topics:** Challenges and risks; timing; de-grossing.

**Learning objective.** Show arithmetically why shorts require active management that longs do not — the position grows as it goes wrong, forcing you to buy at the worst price.

**Student task.** For a short sized at 3.00% of a $100m NAV: compute the P&L, the new NAV, the new position market value and the new position weight after the stock rises 50% and 100%; compute what fraction of the original share count must be covered to restore the target weight, and at what price; compute the same for a long that falls 40%; and write 150 words on what this implies for stop discipline. **50 minutes.**

**Tools and environment.** Existing spreadsheet. Fully auto-gradeable.

**Grading rubric.**
- *Quantitative (80 pts, fully auto):* all figures, tolerance 1e-4.
- *Qualitative (20 pts, LLM-graded):* must conclude that shorts need *pre-committed* stops because the rebalance trade is forced and happens at the worst available price. An answer that says "shorts are riskier" without the mechanism scores ≤6.

**Difficulty.** Intermediate. **Build complexity.** Low.

**Example and worked answer (verified).**
> Short 3.00% of a $100m NAV: 60,000 shares at $50 = $3.0m.
>
> **Stock rises 50% to $75.** Loss = **$1.5m**. NAV falls to **$98.5m**. Position market value rises to **$4.5m**. New weight = 4.5/98.5 = **4.5685%** — the position has inflated by a factor of **1.523** without a single trade. To restore 3.00% you must **buy back 20,600 of 60,000 shares (34.33%) at $75**, the worst price so far.
>
> **At +100%:** you must **cover 51.50% at the top.**
>
> **The mirror long, falling 40%:** 3.00% becomes **1.8219%** — it shrinks, and no action is forced.
>
> **The asymmetry stated plainly:** a short that goes to zero returns +100%; a short that triples returns −200%. **The long shrinks as it goes wrong; the short grows.** That is why short stops must be pre-committed and mechanical: by the time you are deciding whether to cover, the position is already larger than you sized it, and the decision is being made under duress at the worst price.

---

### M12-E3 — Forensic Screen and the Three-Lens Convergence *(optional/advanced track)*

**Topics:** Identifying short ideas; quantitative short selection; fundamentals leg of FEV.

**Learning objective.** Compute the standard forensic scores correctly, and — the real lesson — recognise when three "independent" lenses are detecting one underlying event.

**Student task.** From a full two-year income statement and balance sheet: compute all eight Beneish components and the M-score; compute Sloan accruals and the CFO/net-income ratio; compute the five-variable Beneish variant; then state in 150 words whether the three lenses constitute independent evidence. **70 minutes.**

**Tools and environment.** Existing spreadsheet. Fully auto-gradeable.

**Grading rubric.**
- *Quantitative (80 pts, fully auto):* all eight components plus the score, tolerance 1e-4; accruals and CFO/NI.
- *Qualitative (20 pts, LLM-graded):* **full credit requires recognising that the lenses are not independent** — a receivables-driven revenue overstatement shows up as a high DSRI, as high accruals, and as collapsing CFO/NI, because all three are measuring the same gap between revenue and cash. A student who reports "three independent red flags" has misread the evidence and scores ≤6.

**Difficulty.** Advanced. **Build complexity.** Low.

**Example and worked answer (verified).**
> Components: DSRI **1.666667**, GMI **1.111111**, AQI **1.066667**, SGI **1.400000**, DEPI **1.142857**, SGAI **0.944444**, TATA **0.072222**, LVGI **1.030303**.
>
> M = −4.84 + 0.920(1.666667) + 0.528(1.111111) + 0.404(1.066667) + 0.892(1.400000) + 0.115(1.142857) − 0.172(0.944444) + 4.679(0.072222) − 0.327(1.030303) = **−1.070264**.
>
> **Threshold: the commonly cited cutoff is −1.78, and −1.070 exceeds it, so the company is flagged.** But state the caveat in the key: **sources genuinely conflict on the threshold (−1.78 vs −2.22)**, and Beneish's own paper frames the cutoff as depending on the relative cost of Type I versus Type II errors rather than as a fixed line. On either threshold this company flags, which is why it is a good teaching case — but a question keyed to a single threshold is fragile, and the five-variable variant gives **−1.928048**, which flags on one cutoff and not the other. **Teach the ambiguity; it is the more useful lesson.**
>
> The score is driven by **DSRI (+1.533 contribution) and SGI (+1.249)**. The same financials give Sloan accruals of **8.67%** and **CFO/net income collapsing from 0.9167 to 0.1333**.
>
> **The convergence point.** DSRI is the receivables tell. Accruals are the same gap expressed as a balance-sheet change. CFO/NI is the same gap expressed as a cash ratio. **These are three views of one event, not three independent confirmations** — and an analyst who treats them as independent will overstate their confidence by a wide margin.

---

### M12-E4 — De-Grossing Recognition, in Real Time

**Topics:** De-grossing; contrarian positioning; earnings-season tactics for shorts.

**Learning objective.** Distinguish a positioning event from an information event while it is happening — the decision that most often destroys a pod analyst's year.

**Student task.** A timed, staged exercise. Over four releases of information spaced 10 minutes apart (simulating four hours of a trading day), the student receives market, sector, factor, basket and single-name data and must, at each stage, state: what is happening, their confidence, and what they would do with a stated book of three longs and two shorts. They cannot revise earlier answers. **50 minutes.**

**Tools and environment.** Needs staged release and answer locking — medium build, or runnable live. Shares the event-clock engine with M13.

**Grading rubric.**
- *Quantitative (50 pts, auto):* classification at each stage against a key, with the key **changing as evidence accumulates** — a student who calls de-grossing at stage 1 on insufficient evidence scores *lower* than one who says "unclear" and calls it at stage 2. Premature confidence is penalised, which is the opposite of how students expect to be graded.
- *Qualitative (50 pts, LLM-graded):* 25 pts for action consistency with the stated classification; 25 pts for a **calibration-style confidence statement** that updates monotonically with evidence. Score the confidence trajectory, not just the final answer.

**Difficulty.** Advanced. **Build complexity.** Medium.

**Example staged evidence and the signature to teach.**
> **Stage 1:** your market-neutral book is −1.8% on the day; the index is +0.1%. *Correct answer: unclear. Could be idiosyncratic.*
> **Stage 2:** both legs are losing — your longs are down and your shorts are **up**. The index is still flat. *Now it is diagnostic.* **"Index flat, market-neutral book down, both legs losing" is the de-grossing signature**, because information cannot move both your longs and your shorts against you simultaneously; only forced position unwinding does that.
> **Stage 3:** a widely-followed crowded-long basket is −4.2%, a crowded-short basket is +3.1%, and momentum is sharply negative. **Confirmed.** Note the corollary students find counter-intuitive: **your best shorts hurt most, because "best short" and "most crowded short" are correlated.**
> **Stage 4:** borrow fees on your two shorts have spiked. *This is a consequence, not new information* — and a student who upgrades their confidence on it has double-counted.
>
> **The action key:** in a confirmed de-grossing with theses intact, the correct action is to **do nothing or add within limits**, and explicitly to *not* cover shorts into the squeeze — which is precisely what the risk system and the P&L pressure are pushing you to do. Full credit requires naming that tension.
## Module 13 — Earnings Season

### Expected content coverage

**Scope.** The operational module: what an analyst does hour by hour around a print. The most simulatable content in the course, and the natural home for the program's highest-fidelity exercise.

| Topic | What mastery looks like |
|---|---|
| Why earnings drives volatility | Concentrated information release against a dated bar. |
| Expectations gap and catalyst framework | Carried from M10. |
| Preparing for earnings | **The preview memo**, with eight sections: a header strip carrying the implied move and the realised-move history of the last eight prints; a three-column bar per line item (consensus / inferred buy-side bar / our number); **the forward bar as its own section**; key debates; positioning; a risk/reward table; **a written pre-commitment of what we do in each outcome**; and what we need from the call. |
| Updating models and assessing results | **A two-step update, and step 2 is the one juniors skip:** step 1 updates the model to the actuals; step 2 **re-sets the forward bar, the multiple and the gap.** An analyst who does step 1 only has a current model and a stale thesis. |
| Surprise factor and algorithmic shifts | SUE; post-earnings-announcement drift; the five reasons stocks fall on beats. On "algorithmic shifts": machines price the extractable numbers within seconds, so **the fundamental analyst's edge is entirely in the second wave** — which is the argument against reacting in minute five. |
| Estimating upside/downside | Implied move from the straddle, and the relationship that makes it exact rather than approximate. |
| Tactics for earnings day and beyond | Pre-print positioning; the 15-minute first read; the 48-hour discipline. |
| Read-throughs | The read-through map and the arithmetic of translating a peer's print into your numbers. **The key insight: after a peer print the bar moves before consensus does**, so your gap can go to zero with no published estimate changing. |
| Spring-loaded and peak-on-peak | **Both are verbatim Caughran terms with no recoverable definitions.** |
| Reacting to prints; fading overreactions | An overreaction is defined by the move **relative to the change in forward numbers and relative to the implied move** — not by its size. |

**⚠ Two honest flags.**
1. **"Peak-on-peak" is genuinely ambiguous and unresolved.** It can mean *peak earnings against a peak comp base* (a comparison problem) or *a peak multiple on peak earnings* (a valuation problem). These imply different assessment items. **Ask FE before building.**
2. **The PEAD-versus-reversal tension is real** and should be taught as such rather than resolved. They are not contradictory because they measure different things — drift is measured over weeks, cross-sectionally, sorted on surprise; reversal is measured over hours to days, on single names, sorted on move magnitude. Retrievable PEAD magnitudes conflict badly across secondary sources, and at least one commonly quoted figure appears to be mis-attributed. **Do not put a PEAD magnitude in an answer key without opening the primary paper.**

**Prerequisites.** M06 (modeling), M10 (expectations), M11 (multiples). **And the options gap again:** implied-move work needs option basics that the curriculum does not supply.

---

### M13-E1 — The Earnings Event Clock *(flagship exercise for the whole program)*

**Topics:** All ten bullets. The module's integrative exercise.

**Learning objective.** Run a complete earnings event end to end, under a clock, with pre-commitment — and be graded on process fidelity rather than on whether the trade worked.

**Student task.** A staged, timed simulation over a 20-step event clock from T−5 days to T+60 days, with **five timed deliverables**: (1) the preview memo, due T−2, including the pre-commitment table; (2) a **15-minute first read** immediately after the release, structured as a fixed five-stage sequence beginning with the guidance paragraph; (3) the updated model plus the **re-set forward bar**, due 90 minutes after the release; (4) the action decision with sizing, due at the next open; (5) a post-mortem at T+60 scored against the student's own pre-commitment. Total student time roughly 4 hours across the sequence.

**Tools and environment.** **Custom — this is the historical case engine (INF-1).** Real historical print, real transcript, real option chain, point-in-time consensus, dates masked. Model template supplied.

**Grading rubric.**
- *Quantitative (55 pts, auto):* model-update accuracy against the golden model via check cells and perturbation; the implied-move and bar arithmetic; **trap detection** — the case contains planted items, each independently scored (see below); and the forward-bar re-set.
- *Qualitative (45 pts, LLM panel, reference-guided, 0–5 per dimension with behavioural anchors):* preview-memo quality; **pre-commitment consistency** — did the action at step 4 match what the student committed to at step 1, and if not, is the deviation *justified by new information* rather than by the price? This is the single most valuable dimension and the closest thing in the program to measuring thesis-creep resistance; first-read discipline; post-mortem honesty.
- **Explicitly do NOT grade on the outcome.** The stock's actual move is revealed and is used only to score the *calibration* of the student's probability estimates (Brier), aggregated across the cohort and across cases. Grading a single outcome would be grading noise and would teach resulting.
- **Fourteen traps to plant, each independently scored:** a tax-rate-driven beat; a guidance raise smaller than the quarter's beat; a comp-base effect; a GAAP/adjusted mismatch; guidance given only on the call and not in the release; an after-hours overshoot that retraces by the open; an inventory tell; a DSO tell; a quietly redefined non-GAAP metric; a peer share-gain claim that conflicts with this company's; a non-answer in the Q&A; a disclosure that appears only in the 10-Q weeks later; a kitchen-sink quarter; and an exit-rate gap versus next year's consensus.

**Difficulty.** Four-level ladder from intermediate to advanced, by how many traps are planted and whether the model template is pre-built or blank. **Build complexity.** High — but it is the engine that supports the most exercises in the program.

**Example and worked answer (the guidance-bridge trap, fully verified).**
> Q2 revenue beats by **$30m**. FY guidance is raised by **$20m**. Management's call language is confident.
>
> **The arithmetic nobody does:** the raise is $10m *smaller* than the beat, so **implied 2H revenue falls** from $2,030m to $2,020m. 1H growth was **+12.71%**; implied 2H growth is **−1.46%** — **14.17 points of deceleration embedded in a guidance raise.**
>
> Decomposing it: **2.70 points is a harder comp** and **11.47 points is genuine implied slowdown** (2.70 + 11.47 = 14.17 ✓). Two-year stacks fall from 21.42 to 9.95 points additive, or 10.69% → 4.78% on a 2-year CAGR basis — and reporting both conventions is required, because the additive figure overstates the deceleration here.
>
> **The exit rate is the kill shot.** Implied Q4 is **−2.86% year-over-year**, while FY+1 consensus requires **+6.16%** — a **9-point reacceleration that nobody has underwritten**, derived from arithmetic alone with no view required.
>
> **The graded behaviour:** did the student's first read catch that the raise was smaller than the beat? That is a binary, auto-detectable check — it either appears in the 15-minute deliverable or it does not — and it is the single highest-signal item in the station.

---

### M13-E2 — Beat Decomposition: How Much of This Was Real?

**Topics:** Surprise factor; updating models; quality of a beat.

**Learning objective.** Decompose an EPS surprise into its drivers so that "they beat" becomes "they beat on tax and share count, and missed on margin."

**Student task.** Given consensus and actual values for revenue, gross margin, operating expense, tax rate and share count, build the EPS surprise bridge; confirm it ties exactly; classify each contributor as high or low quality; and state in two sentences what the beat implies for the forward bar. **45 minutes.**

**Tools and environment.** Existing spreadsheet. Fully auto-gradeable.

**Grading rubric.**
- *Quantitative (80 pts, fully auto):* each contributor plus a **hard tie-check (25 pts)** — the components must sum to the total surprise to floating-point tolerance.
- *Qualitative (20 pts, LLM-graded):* the quality classification and the forward-bar implication. An answer calling a tax-driven beat "a beat" without qualification scores ≤5.

**Difficulty.** Intermediate. **Build complexity.** Low.

**Example and worked answer (verified; the bridge closes exactly).**
> Consensus: revenue $1,000m, gross margin 40.0%, opex $250m, tax 21%, shares 100m → EPS **$1.1850**. Actual: revenue $1,030m, gross margin 39.2%, opex $256m, tax 19%, shares 98.5m → EPS **$1.2151**. Surprise **+$0.0301 (+2.54%)**.
>
> Sequential bridge: revenue **+$0.0948**; gross margin **−$0.0651**; opex **−$0.0474**; tax **+$0.0296**; share count **+$0.0182**. Sum = **+$0.0301** ✓ ties exactly.
>
> **The reading:** the company beat on revenue and then gave back more than two-thirds of it on margin and opex. The *entire* reported beat is accounted for by **tax and share count (+$0.0478 combined)** — items with no bearing on business momentum and no forward durability. A second verified case shows the same shape: **31.6% of a beat being low-quality**, split revenue +31.9% / margin +36.5% / tax +20.6% / shares +11.0%.
>
> **Forward-bar implication for full credit:** the tax rate will not repeat at 19%, and the share count benefit is finite, so next year's consensus — which will be built off this reported EPS — now embeds a quality of earnings the business did not deliver. **This is a sell-side upgrade cycle and a buy-side short setup at the same time.**

---

### M13-E3 — The Read-Through Translation

**Topics:** Read-throughs; adapting the expectations bar; connecting dots.

**Learning objective.** Convert a peer's print into a quantified change to *your* numbers — and know when not to.

**Student task.** Given a peer's reported organic growth, the historical spread between the peer's and your company's growth in the overlapping segment, segment weights, FX and M&A contributions: translate to your company's expected reported growth; compare to consensus; convert the revenue delta to EPS using incremental margin, tax and share count; attach an uncertainty band; then run the 11-point naive-read-through risk checklist and state which items apply. **60 minutes.**

**Tools and environment.** Existing spreadsheet + templated peer release. Auto-gradeable.

**Grading rubric.**
- *Quantitative (70 pts, auto):* the four-step translation, the EPS delta, and the uncertainty band, tolerance 1e-3.
- *Qualitative (30 pts, LLM-graded):* the checklist application. **Full credit requires identifying at least two reasons the read-through might fail here** and saying how much of the estimated delta each could erase.

**Difficulty.** Advanced. **Build complexity.** Low–medium.

**Example and worked answer (verified).**
> Peer reports **+8.0% organic**. The historical spread (you minus peer) in the overlapping segment is **−2.0 points**, implying **6.0%** for you in that segment. The overlapping segment is **70%** of your revenue; the non-overlapping 30% is tracking **+3.0%**. Weighted organic = 0.70 × 6.0% + 0.30 × 3.0% = **+5.1%**. Add FX **+1.6%** and M&A **+0.8%** → **+7.5% reported** versus consensus **+6.2%**.
>
> Revenue delta = **+$10.4m (+1.22%)**. At a 35% incremental margin, 22% tax and 120m shares: **+$0.0237 of EPS, a 2.3% beat.** Uncertainty band: **±$5m of revenue**, derived from the historical stability of the −2.0 point spread.
>
> **The checklist items that bite here:** different geographic mix (the peer's growth may be concentrated in a region where you are under-indexed, which would erase most of the delta); and **sell-in versus sell-through** — if the peer sells into the same channel you do, their strong quarter may be channel inventory build that becomes your headwind next quarter, which flips the sign of the read-through entirely.
>
> **The strategic point that earns the last marks:** after the peer's print, **the buy-side bar for your company has already moved to roughly +7.5%**, even though published consensus still reads +6.2%. So your +1.3-point "beat versus consensus" is **no longer an edge** — it is the new expectation. A student who concludes "we're set up to beat" has missed the entire module.
## Module 14 — Pitch Like a Pro

### Expected content coverage

**Scope.** Turning a thesis into a decision someone else makes. The module with the richest published assessment precedent — and four bullets that nothing in the world currently tests.

| Topic | What mastery looks like |
|---|---|
| Turning an idea into a compelling thesis | Lead with the conclusion. Caughran: a thesis is "distilled to its key elements, highlighting where the research is differential, communicated to the decision maker succinctly." |
| Firm's preferred format | Formats differ; the discipline of fitting one is itself the skill. |
| Key elements | Summary, thesis points, risks, valuation. **SumZero's published write-up standard is the most explicit public specification available:** business/product analysis, valuation, **target price justification**, risks, **timeline/horizon**, and **trade feasibility (liquidity and inventory)**; must be forward-looking; explicitly long or short; and **ideas with less than 5–10% expected upside tend to be rejected.** |
| Telling a story with data | The data serves the argument, not the reverse. |
| Anticipating questions | Pre-build the answers to the five questions you least want asked. |
| Delivery: confidence and humility | "I don't know, I'll find out by 4pm" beats a bluffed number, and should be scored that way. |
| Follow-up | **Externally unassessed.** |
| Avoiding thesis creep with a trading plan | The best-sourced bullet in the module, in Caughran's own voice: thesis creep is **"the great killer of performance"**; the diagnosis is sunk cost — *"a lot of brain damage to get an idea into a book… you don't want to admit that you are wrong"*; **"Trading Plans are the best way I've learned to avoid 'thesis creep'"**; kill criteria mean pre-defining *"the specific outcomes that would demolish my thesis,"* and the rule is **"if the thesis breaks, I'm out"**; he runs a **monthly/quarterly "thesis creep meeting"** where you *"pull our initial trading plans"* and test whether positions are *"tracking to our ex-ante view"*; and **"quite often, your first sale is your best sale."** |
| Pre-mortem and post-mortem | **Citation correction:** the pre-mortem is Klein, "Performing a Project Premortem," *HBR*, September 2007 — prospective hindsight, imagine the project **has already failed**, work backward; runs 30–60 minutes in groups of 3–10; and Klein's own stated purpose is that it **"makes it safe for knowledgeable dissenters to speak up,"** which is the part usually dropped. **The widely-quoted "+30%" improvement figure is routinely mis-attributed to Klein; the underlying evidence is Mitchell, Russo & Pennington (1989).** Fix this if you cite it. |
| Evaluating pitches / poking holes | **Externally unassessed**, and the highest-value gap. |

**The published rubric to build against.** The **CFA Institute Research Challenge** splits 50/50 between written report and presentation. Written report, 100 points: Business Description **5**, Industry & Competitive Positioning **10**, Investment Summary **15**, **Valuation 20**, **Financial Analysis 20**, Investment Risks **15**, ESG **15**. Report capped at **10 A4 pages** plus a ≤20-page appendix, cover excluded. Presentation, 100 points: Financial Analysis **20**, Valuation **20**, ESG **10**, Presentation **20**, **Q&A 20**, Team Involvement **5**, Materials **5**. Local rounds run **10 minutes plus 10 minutes of Q&A**.

**The structural insight most people miss, and it should shape your design:** **50 of the 100 presentation points are substantive content** (financial analysis, valuation, ESG) — so the artefact and the defence are **deliberately double-scored on the same constructs**, with only 20 points for delivery. The lesson is not "weight the presentation"; it is *test the same analytical claims twice, once in writing and once under questioning*, because the second test is what detects a memo the candidate cannot actually defend.

**Four bullets nothing public tests.** Follow-up, trading plans/thesis creep, pre/post-mortems, and evaluator-side hole-poking are untested anywhere, because every competition and interview format is **single-shot**. That is simultaneously the biggest research gap and the clearest opening for proprietary instruments — all three of the exercises below exploit it.

---

### M14-E1 — The Capstone Pitch and Defence *(the program's terminal assessment)*

**Topics:** All of M14, integrating M03, M10, M11 and M13.

**Learning objective.** Produce and defend a complete investment recommendation to the standard the student's target seat actually demands.

**Student task.** Student chooses their own name (the **exploration** step — no scaffolding). Deliverables: a **page-limited memo** with mandatory structured fields; an operating model with explicit bull/base/bear; optional slides to a stated cap; then a live **10-minute pitch plus 20–40 minutes of adversarial Q&A**. Two weeks for the artefact; the defence is scheduled.

**Mandatory structured fields — the single most important technical decision in the blueprint:** target price, horizon, conviction, catalyst **with a date**, falsification condition, position size, liquidity (days to exit at a stated participation rate), factor footprint, and borrow cost if short. **Free-form memos are not scoreable at scale; structured fields make both auto-grading and later calibration scoring free**, because every submission becomes a timestamped, horizon-bounded forecast at no extra student effort.

**Tools and environment.** Existing tools for the artefact; the role-play engine or a live human for the defence. Page limits enforced **mechanically before grading**.

**Grading rubric — two separate instruments, never averaged.**
- *Artefact (100 pts, human double-scored, LLM pre-screen).* Built on **ICD 203's nine analytic tradecraft standards**, which are a published government standard for analytic product quality and the closest thing in existence to an official rubric for an investment memo. Mapped and weighted: (1) describes quality and credibility of sources, data and methodologies — **12**; (2) expresses and explains uncertainties — **15**; (3) distinguishes underlying information from the analyst's assumptions and judgments — **15**; (4) incorporates analysis of alternatives (the bear case) — **12**; (5) demonstrates customer relevance and addresses implications (what the PM should *do*) — **10**; (6) clear and logical argumentation — **12**; (7) explains change to or consistency of analytic judgments — **10**; (8) makes accurate judgments and assessments — **4**; (9) effective visual information — **10**.
  - **Standard 2 is scored on two separate axes, not one** — the likelihood of the outcome *and* the analyst's confidence in the basis for that judgment. Two fields. This is the detail that makes the standard powerful and it is what most finance rubrics collapse.
  - **Standard 7 is the thesis-creep dimension** and is graded by no finance course anywhere.
  - **Standard 8 — accuracy — deliberately carries the smallest weight (4 points).** In a low-validity domain, outcome accuracy over a single idea is mostly noise; weighting it heavily would teach resulting.
- *Defence (100 pts, human, global rating scales 0–5 per dimension with behavioural anchors):* knows their own numbers without notes; concedes when wrong; distinguishes what they know from what they assume; updates on new evidence **without abandoning the thesis** (the thesis-creep-versus-appropriate-updating distinction); composure; and **bluffing is a critical failure.** Plant one question whose answer is not knowable from the available information and grade whether the student fabricates. **That single planted item is the highest-signal thing in the station.**
- **Reliability commitment:** double-score every capstone, report quadratic weighted kappa, and target **≥0.75 on the artefact's near-objective dimensions and ≥0.60 on the holistic defence dimensions.** Those are honest targets — professional essay scoring rarely beats 0.7–0.8 human-to-human. Publishing your own inter-rater reliability would be a genuine differentiator; no competitor in finance training does it.

**Difficulty.** Advanced. **Build complexity.** Medium for the artefact rubric and anchors; high if the defence is AI-driven.

**Example — the planted unknowable question.**
> **PM:** "What's the attach rate on the enterprise tier specifically, as opposed to the blended number you've shown me?"
> The company does not disclose it, and nothing in the public record contains it.
> **Full credit:** "They don't break it out. I've triangulated a range of roughly 30–40% from the two channel partners' commentary and the pricing differential, but it's an estimate and the thesis doesn't depend on it — if you want it tightened, two expert calls would do it and I'd have it by Thursday."
> **Critical failure:** any specific number asserted without that hedge. The PM is scripted to press once — *"where did you get that?"* — and the transcript records whether the student invented it.

---

### M14-E2 — The Forced Re-Underwrite (longitudinal; tests what nothing else does)

**Topics:** Thesis creep; trading plans; pre- and post-mortems; idea maintenance.

**Learning objective.** The one instrument that can actually measure thesis-creep resistance — because it is **not single-shot**.

**Student task.** Three sittings, spaced weeks apart, on the student's own capstone name.
- **Sitting 1 (at submission):** lock the thesis, the trading plan, and the kill criteria.
- **Sitting 2 (weeks later):** the student is shown real subsequent tape — the next print, the price action, and two news items, drawn from masked historical data so ground truth exists. They must state whether any kill criterion has triggered, and either exit, hold with an unchanged thesis, or hold with an explicitly amended thesis — **and if amended, state precisely what new information justifies the amendment.**
- **Sitting 3:** full post-mortem against the sitting-1 document, including whether the *process* was sound independent of the outcome.

**Tools and environment.** Requires the historical case engine plus a locked-submission store. Medium build on top of INF-1.

**Grading rubric.**
- *Quantitative (40 pts, auto):* did a kill criterion objectively trigger, and did the student correctly identify that it had? This is **binary and mechanical**, because sitting 1's criteria were stored as structured {metric, threshold, direction, date} records and the subsequent tape either crosses them or does not. **This is the cleanest measurement in the entire program.**
- *Qualitative (60 pts, LLM panel + human on disagreement):* 30 pts — if the thesis was amended, is the amendment **justified by new information rather than by the price**? The grader receives both documents and the intervening tape and must quote the specific new information the student cited. 20 pts — post-mortem quality, specifically whether the student distinguishes a bad decision from a bad outcome. 10 pts — whether they acted on their own plan at all.
- **Critical-failure marker:** a student whose kill criterion triggered, who did not exit, and who amended the thesis in the direction that justified holding, has demonstrated textbook thesis creep. Flag it explicitly in feedback with their own two documents side by side. **That feedback is the most valuable single output of the program** and it is impossible to produce without a longitudinal instrument.

**Difficulty.** Advanced. **Build complexity.** Medium–high.

**Example.**
> *Sitting 1 kill criterion:* "Exit if services attach is below 32% at the FY+1 Q4 print."
> *Sitting 2 tape:* attach reported at **29.5%**. Stock is **up 11%** on a strong revenue beat elsewhere in the business.
> **The trigger has objectively fired.** The honest answers are to exit per plan, or to hold with an amendment that explicitly identifies what *new* information changes the analysis — for example, a disclosure that the attach definition changed, or evidence the shortfall is timing rather than demand, with the revised bridge shown.
> **The failure mode the item is built to catch:** "Attach came in at 29.5%, but revenue beat and the stock is working, so the thesis is intact and the attach ramp is just delayed a quarter." That is thesis creep, it is in the student's own handwriting against their own pre-commitment, and the price is doing the arguing. Caughran's own ENDP loss is a ready-made teaching companion here: opioid regulation and generic price deflation were both identified risks, and in his words **"BOTH happened, and I ignored both."**

---

### M14-E3 — Poke Holes: The Evaluator Seat

**Topics:** Evaluating pitches; anticipating questions; intellectual honesty.

**Learning objective.** Train the skill from the other side of the table — the only public precedent for which is Value Investors Club's requirement that members **rate 20 ideas a year**, not merely post their own.

**Student task.** The student receives three peer memos (or curated anchor memos at known quality levels) and must, for each: identify the single weakest load-bearing assumption; write the three questions that would most efficiently test it; state what answer would kill the thesis; and give a two-axis rating separating **"do I agree with this"** from **"is this good work"** — a separation SumZero's own ratings make and that juniors reliably conflate. **70 minutes.**

**Tools and environment.** Existing. Needs a memo bank with pre-scored anchors.

**Grading rubric.**
- *Quantitative (45 pts, semi-auto):* the identified weakest assumption against an expert key with accepted alternates; **and — the clever part — the student's two-axis ratings are scored against the known quality level of the anchor memos**, so rating a deliberately well-argued memo you disagree with as "bad work" is a detectable, scorable error.
- *Qualitative (55 pts, LLM panel):* 30 pts — question *efficiency*: do the three questions actually discriminate, or are they generic diligence? 15 pts — the kill answer is specific. 10 pts — the written critique is something you could send a colleague without causing offence, which is a real professional skill.
- **Guard against the known failure mode:** peer ratings in enthusiast communities drift upward and correlate with length and author reputation rather than quality. Mitigations: seed pre-scored anchor memos invisibly into the queue as validity checks; use **pairwise comparison against anchors rather than absolute rating** for high-stakes scoring; and weight each student's peer ratings by that student's own demonstrated rating accuracy.

**Difficulty.** Advanced. **Build complexity.** Low–medium (the anchor memo bank is the build, and it doubles as the golden set for every LLM grader in the program).

**Example.**
> *Memo under review argues a 35% upside on margin expansion from a cost programme.*
> **Model answer — weakest load-bearing assumption:** that the $180m of announced savings flows to the EBIT line rather than being competed away in price. The memo asserts flow-through without evidence.
> **Three discriminating questions:** (1) In the last two cost programmes, what share of announced savings showed up in reported EBIT margin twelve months later? (2) Is the industry's pricing mechanism cost-plus or market-based — i.e. do customers have contractual visibility into the cost base? (3) What did the two closest competitors' margins do after *their* cost programmes?
> **What would kill it:** evidence that the prior programme's savings produced no margin improvement, which would establish competitive give-back as the house pattern.
> **Two-axis rating:** this can legitimately be "I disagree" and "good work" simultaneously — well-sourced, clearly argued, one unexamined assumption. **A student who marks it down on both axes because they disagree has made the exact error the item measures.**
## Module 15 — Wrapping Up / Bringing It All Together

### Expected content coverage

**Scope.** The capstone module. It mixes three things that should be assessed differently: **review** (the FEV / MIC / ETIK callbacks), **genuinely new portfolio-management content** (ranking, the idea stack, risk management, portfolio construction — the only rigorously assessable material here), and **career framing** (analyst progression), which is not assessable at all. Bullet 8 ("communicate idea with structured pitch script") duplicates M14 almost entirely, and bullet 4 duplicates the risk intensive.

**The course's own acronyms, with provenance now resolved.**

| Acronym | Status |
|---|---|
| **FEV** | **Fundamentals, Expectations, Valuation.** Confirmed; Caughran's own origin post calls it "a simple stock selection framework." |
| **MIC** | **Market view, Internal view, Convergence.** **Settled on "convergence"** from FE's own page; a course listing rendering the C as "catalyst for convergence" is wrong — "catalyst" belongs to M13's separate expectations-gap-and-catalyst framework. Structurally, MIC is near-identical to Steinhardt's own four-part test from *No Bull* (the idea / the consensus view / the variant perception / a trigger that unlocks value) — **teach them as one object.** |
| **ETIK** | **"Everything There Is to Know."** **Now confirmed verbatim** as a lesson title in the Caughran-taught Wall Street Prep course: *"Key Drivers — Everything There Is to Know (ETIK)."* The **expansion** is public; the **method** — what achieving ETIK on a driver actually requires — is not. Note the scoping logic that makes the bullet coherent: you cannot know everything about everything, so you achieve ETIK **scoped to the key drivers**, which dovetails with M07's "focus research on 3 key drivers." |
| **KDs** | **Key Drivers.** Confirmed. |
| **Idea stack** | Named, not defined beyond "long and short book rankings." |
| **Three-year double** | Named, partially defined ("EPS growth and P/E expansion"); no threshold or hurdle given. |
| **"Full stack" partner** | Named, not defined. |

**The biggest curriculum gap in the whole course, flagged plainly:** **sleeve risk management is essentially absent from the syllabus.** Gross and net exposure, beta and factor neutrality, correlation limits, stop-outs, drawdown governors and contribution-to-risk appear nowhere across the 15 modules, apart from one line in M15 bullet 9 and M12's "de-grossing." For a program training pod analysts that is a real hole — or the brochure badly understates the recorded content. Either way, **the assessment layer should cover it, because the seat demands it.** There is also **no stated prerequisite maths level**, despite the risk-models intensive needing linear algebra and the audience being explicitly bimodal.

---

### M15-E1 — The Idea Stack, and Why Price Alone Re-Ranks It *(flagship for this module)*

**Topics:** Ranking stocks; idea stack; portfolio construction; risk/reward.

**Learning objective.** Build a ranked book, map rank to size under real constraints, and discover that the stack is not a one-time exercise because **price movement alone re-orders it.**

**Student task.** Given 10 longs and 8 shorts, each with bull/base/bear targets, probabilities, betas, factor loadings, ADV and borrow: build the stack ranked on probability-weighted expected value and reward/risk; map rank to position size subject to a single-name cap, a gross target and a net target; compute contribution-to-risk per position and confirm the contributions sum to portfolio volatility; then **re-run after a stated set of price moves with all targets unchanged** and report what changed in the ranking and the book. **100 minutes.**

**Tools and environment.** Existing spreadsheet or Python. Fully auto-gradeable.

**Grading rubric.**
- *Quantitative (80 pts, fully auto):* the stack, the sizing under constraints, the contribution-to-risk decomposition (**with a hard check that CTRs sum exactly to portfolio volatility** — 20 pts), and the full re-rank.
- *Qualitative (20 pts, LLM-graded):* must state the implication — that the stack requires continuous maintenance because price alone invalidates it, and that a rallying name with an unchanged target is mechanically a worse idea than it was.

**Difficulty.** Advanced. **Build complexity.** Low–medium.

**Example and worked answers (all verified).**
> **The re-rank, which is the single best assessment item in this module.** A name rallies **20% toward an unchanged target.** Its reward/risk falls from **2.00 to 0.24**; its expected value falls from **+11.2% to −7.3%**; and it **drops out of the stack entirely.** No new information arrived. **Price alone re-ranked the book** — and an analyst who only revisits the stack when news breaks will carry a book of positions that have silently become bad ideas.
>
> **Rank-weighting versus equal-weighting:** on the 10-long book, rank-weighting adds **+2.21% of NAV** of expected value over equal-weighting the same names. Conviction dispersion is worth real money.
>
> **Two honest failures the arithmetic exposes, and both should be kept in the exercise:**
> 1. **A negative-EV short gets a negative weight** — i.e. a naive rank-to-size model silently flips your short into a long. **Negative-EV ideas must be *rejected*, not sized.** The constraint has to be explicit or the optimiser does something absurd.
> 2. **When the single-name cap binds on every name, rank-weighting came out *worse* than equal-weighting.** The lesson is sharp: **when caps bind everywhere, your stack has no effect on your portfolio** — the ranking work is wasted effort and the constraint is the real portfolio manager.
>
> **Contribution-to-risk:** a position at **60% of notional** can be **77.4% of risk**. Notional weights and risk weights are different objects, and CTRs sum exactly to portfolio volatility, which is the check that proves the student did it right.

---

### M15-E2 — The Three-Year Double Grid

**Topics:** Three-year double; return decomposition; feasibility screening.

**Learning objective.** A 60-second feasibility filter usable at the quick-dive stage: what does a double actually require, and is this stock on a row you can defend?

**Student task.** Build the full solution grid for (1+g)³ × k = 2; compute the pure-EPS-growth case; compute the required multiple change at eight growth rates and the required growth at six multiple changes; add a dividend-yield variant; then apply it to three real situations and state which is feasible and what each requires you to defend. **45 minutes.**

**Tools and environment.** Existing spreadsheet. Fully auto-gradeable.

**Grading rubric.**
- *Quantitative (85 pts, fully auto):* the grid, tolerance 1e-5. **Precision matters and is scored:** rounding 1.15³ to 1.52 before dividing introduces visible drift.
- *Qualitative (15 pts, LLM-graded):* must state, for each real situation, **which term the analyst is being asked to defend** — the earnings or the multiple.

**Difficulty.** Beginner–intermediate. **Build complexity.** Low.

**Example and worked answer (verified).**
> Pure EPS growth, flat multiple: **g = 2^(1/3) − 1 = 25.992105%** (and note this is also the three-year IRR of any double, which is the same number).
>
> | EPS CAGR | 3-yr EPS multiple | Required M_exit/M_entry | Required multiple change |
> |---|---|---|---|
> | 5% | 1.157625 | 1.727675 | **+72.8%** |
> | 8% | 1.259712 | 1.587686 | **+58.8%** |
> | 10% | 1.331000 | 1.502630 | **+50.3%** |
> | 12% | 1.404928 | 1.423560 | **+42.4%** |
> | 15% | **1.520875** | **1.315032** | **+31.5%** |
> | 18% | 1.643032 | 1.217262 | **+21.7%** |
> | 20% | 1.728000 | 1.157407 | **+15.7%** |
> | 25% | 1.953125 | 1.024000 | **+2.4%** |
> | 30% | 2.197000 | 0.910332 | **−9.0%** (can de-rate and still double) |
>
> Inverse: a 1.25x re-rating needs **16.96%** EPS CAGR; 1.40x needs **12.62%**; 1.50x needs **10.06%**; 2.00x needs **0%**. Worked check at 15%: 15.0x on $4.00 EPS = $60; EPS₃ = $6.08350; required exit multiple 19.7255x → **$120.0000 = +100.0000%** ✓. At 20%: 6.91200 × 17.3611x = **$120.0000** ✓.
>
> **Two precision points that are themselves assessable.** (1) With a 2% dividend yield the requirement becomes (1+g)³ × k = 2/1.02³ = **1.884645**. (2) **Buybacks must NOT enter as a separate yield term** — buyback accretion is already inside EPS growth, and double-counting it inflates expected return by roughly 200–300bp a year. **Only dividends belong in the (1+y)³ term.**
>
> **The teaching payload:** a "three-year double" on a 15% grower is not a fundamental call, it is a **+31.5% re-rating call** — so the analyst must defend the *multiple*, which means defending a change in perceived durability or risk, not just the EPS line. Every pitch claiming a double should state which row of this table it is on.

---

### M15-E3 — Attribute This P&L

**Topics:** Risk management; MIC; analyst progression; alpha vs. factor.

**Learning objective.** Answer the question a pod risk meeting actually asks: *what did you get paid for?*

**Student task.** Given a year of position-level returns, factor exposures and realised factor returns: decompose total P&L into factor and residual components; compute the systematic and specific variance split and confirm they sum; compute batting average, slugging ratio and expectancy; compute the information ratio and compare it to IC × √breadth with and without a transfer coefficient; and state how many years of this record would be needed to establish skill statistically. **80 minutes.**

**Tools and environment.** Existing spreadsheet or Python. Fully auto-gradeable.

**Grading rubric.**
- *Quantitative (85 pts, fully auto):* all decompositions with summation checks, tolerance 1e-4.
- *Qualitative (15 pts, LLM-graded):* must state the years-to-significance figure and draw the correct inference — that this is why process accountability exists.

**Difficulty.** Advanced. **Build complexity.** Low.

**Example and worked answers (all verified).**
> **Factor risk decomposition.** Systematic variance **0.002641** + specific variance **0.006125** = total **0.008766** → total volatility **9.3627%**; **30.13% systematic / 69.87% specific**, summing to 100%. Two teaching points fall out: the cross-term can be *positive* despite a negative factor correlation when exposures are opposite-signed; and **volatilities do not add** — 5.14% + 7.83% = 12.97% ≠ 9.36%, so a junior who adds vols **overstates risk by 39%**.
>
> **IR = IC × √BR.** At IC 0.05 and breadth 200: **0.7071**. With a transfer coefficient of 0.60: **0.4243** — **a 40% haircut from constraints alone**, which is the quantitative case for pitching ideas the mandate can actually express. And the sobering version for this audience: a concentrated analyst with ~25 independent bets needs **IC ≈ 0.14–0.17** to reach IR 0.75, which is enormous. **The fundamental analyst's business model is high-IC/low-breadth, and it is far more fragile than the quant's.**
>
> **Batting versus slugging — the killer case.** Three analysts. Analyst B: 35% hit rate, **+3.100% EV per position**. Analyst C: **65% hit rate, 0.545 slugging ratio, +0.050% EV per position** — right about two-thirds of the time and **0.29 percentage points from losing money.** Break-even batting average = 1/(1+slugging ratio). **Hit rate without the payoff ratio is a personality trait, not skill.**
>
> **The punchline that justifies the whole process-over-outcome architecture:** at **IR 0.50 it takes 15.37 years to establish skill at 95% confidence.** No training program, and few analyst tenures, run that long. Therefore the program cannot validly assess whether a student will make money — only whether their process is sound and their forecasts are calibrated. Say this to students explicitly in week one.

---

## Topical Intensives (TI1–TI9)

The nine guest intensives are recorded sessions whose **content, length and instructors are unknown** — scope below is inferred from titles, and all of it is lower-confidence than the core modules. Treat these as a **thin assessment layer** (retrieval items plus one computational exercise each), not as full modules.

| # | Intensive | Expected coverage | Recommended assessment |
|---|---|---|---|
| **TI1** | Introduction to Equity Risk Models | Factor model structure (factor returns × exposures + specific risk); fundamental vs. statistical models; style and industry factors; predicted vs. historical beta; tracking error; VaR and expected shortfall; factor P&L attribution; why multi-manager risk desks force factor neutrality. **Do not print a specific style-factor list as any vendor's without a source — model generations change.** | **Risk-tearsheet reading** (a provided tearsheet, 12 questions, auto-graded) + **parametric VaR and expected shortfall computation** + Kupiec backtest. *Verified worked example:* $100m at 20% annual vol → daily σ **1.2599%**; 1-day 99% VaR **$2.931mm**; ES multiplier φ(z)/(1−α) = 2.66521 → **ES $3.358mm**. Kupiec: 9 breaches in 250 days → LR **10.2290** > 3.841, **reject the model.** |
| **TI2** | Quantitative Approaches to Stock Selection | Factor investing; the main anomalies and **their replication problems**; backtest hygiene (look-ahead, survivorship, p-hacking, multiple testing, costs, capacity); IC/IR; the quantamental workflow. | **Backtest critique** — give students a backtest with planted methodological errors and score each find independently. Plus a multiple-testing item: *20 tests at α = 0.05 gives a **64.15%** chance of at least one false positive* — verified, and the single most useful number in the intensive. |
| **TI3** | Making Sense of Macro | What a bottom-up stock picker needs: the discount-rate channel and equity duration; FX translation; input costs; the credit cycle; inflation pass-through and pricing power; the consumer; inventory cycles; neutralising macro within a sleeve. | **The 100bp drill**, verified: at g = 3%, a 100bp rate rise takes the multiple **16.667x → 14.286x = −14.29%**; at g = 6%, **33.333x → 25.000x = −25.00%**; at g = 0%, −10.00%. The Macaulay duration of a 6%-growth perpetuity is **~36 years — longer than a 30-year Treasury.** And the item that earns the lesson: **if the risk-free rate rises 100bp but the equity risk premium falls 100bp, the multiple does not move at all.** |
| **TI4** | Analyst Toolkit: Field Research | Expert calls and how to run one; channel checks; survey design; alternative data and its biases and decay; regulatory-database mining; **and the compliance perimeter.** | **Survey-statistics item** (verified): n = 400 gives **±4.90pp**; ±3pp needs **n = 1,068**. The high-value part: **a 6pp wave-over-wave move at n = 400 per wave is NOT significant** — MoE on the *difference* is 6.92pp, z = 1.700, p = 0.0890; you need **534 per wave**. Note the asymmetry — MoE on a difference exceeds MoE on a level, so **the comparisons analysts care about most are the ones their samples support least.** Plus an **alt-data critique** exercise and the MNPI vignette sort from M02-E4. |
| **TI5** | Your Market Mindset | Documented biases that cost analysts money; decision journals; **calibration training**; process-vs-outcome accountability; handling drawdowns and public wrongness. | **The calibration battery — the single best-evidenced instrument in the program.** Pre- and post-course, 20+ resolvable questions, Brier-scored with the Murphy decomposition. *Verified example:* BS **0.1700** = reliability 0.0035 − resolution 0.0826 + uncertainty 0.2491; skill score **+0.3175**. The contrast cases are what teach: a coin-flipper scores **0.2500**, and **always saying 0.90 scores 0.3860 — worse than the coin-flipper.** **De-weight bias-recognition quizzes** (low validity) and **do not run P&L-scored trading sims** (outcome-dominated; they reward exactly the overconfidence you are training out). |
| **TI6** | The Value of Growth | Growth is only valuable above the cost of capital; the ROIC/growth matrix; duration and CAP. | Folded into **M11-E1**; add 6–8 retrieval items on the grid. |
| **TI7** | Wisdom From 30 Years on the Street | Career and judgment narrative. | **Not assessable.** Use as reflective prompts in the decision journal; do not score. |
| **TI8** | Valuation Q&A | **No published content** — treat as free-response/oral. | Folded into **M11**; use as the question bank for the capstone defence. |
| **TI9** | Stock-Based Comp for Investors | ASC 718; expense vs. dilution; FCF treatment; the share-count roll-forward. | Folded into **M09-E2**, which already covers it in full. |

**A cross-cutting design principle that emerged repeatedly across the intensives and is worth stating generally: "here is a flawed artefact — find the flaws" beats "produce an artefact" on almost every axis** — it is faster to grade, more reliable, more discriminating, and it maps better onto what analysts actually do all day.
# Part 4 — Shared Infrastructure

Seven pieces of infrastructure carry almost every exercise in this blueprint. They are ordered by value per unit of build effort.

## INF-1 — The Historical Case Engine *(the keystone; build this first)*

**You asked whether a full market simulator is worth building. My answer is no — and the reasoning matters more than the verdict.**

Fundamental analysis runs on a quarters-to-years clock. A real-time trading simulator is a category error for this syllabus: it optimises for execution and price feedback, when the skills in these fifteen modules are thesis formation, expectations inference, and position maintenance. Worse, **the one thing a trading simulator uniquely supplies — price feedback — is the least valid assessment signal available** (§2.1). You would spend the most money to buy the least useful measurement.

What you should build instead is a **historical case engine**: a replay harness over point-in-time data.

**The core insight: the simulator's value is not realism. It is time compression plus free ground truth.** Freeze a date, serve only what was knowable then, and a three-year holding period collapses into a 40-minute exercise in which the correct answer already exists.

**Core features.**
1. Freeze a date **T** for a real company.
2. Serve **only** information available at T — as-filed financials, transcripts, the then-prevailing consensus, the then-prevailing price, option chain and positioning data.
3. Demand a thesis, a model, a price target, scenario probabilities and a sizing recommendation, with structured fields.
4. Advance the clock to T+1 quarter, release the actual print, and demand an updated view — which *is* the Module 13 drill.
5. At T+N, reveal the outcome and force a **post-mortem against the student's own original thesis document.**
6. Score on process fidelity and calibration; score outcome only as a small, explicitly noisy component.

**Exercises it supports:** M13-E1 (the event clock), M14-E2 (the forced re-underwrite — impossible without it), M10-E1/E2/E3, M07-E1, M05-E1, M12-E4, M01-E3, M01-E6, M06-E3, and the calibration ledger's resolution engine. **That is roughly half the blueprint.**

**MVP versus full version.**

| | MVP | Full |
|---|---|---|
| Cases | 8–12, hand-built | 30–40 across sectors and situation types |
| Clock | Static before/after reveal | Staged intra-day release with answer locking |
| Consensus | Hand-curated from contemporaneous coverage | Licensed historical estimate data |
| Positioning | Hand-assembled | Automated from vendor feeds |
| Grading | Check cells + LLM rubric | Full perturbation testing + dependency-graph comparison |
| Delivery | Files plus a form | Web app with timers and locking |

**Point-in-time data: the one real engineering problem.** Four distinct look-ahead leaks must each be closed — **restated financials** (today's database shows restatements; the analyst at T saw as-first-reported numbers and often a different segment structure); **index-membership survivorship**; **delisting survivorship** in prices (cheap APIs usually drop dead tickers, so the worst outcomes silently vanish from your case set); and **historical consensus estimates**, which is both the hardest and the one Modules 10 and 13 most need.

**SEC EDGAR is the free backbone and it solves the hardest leak for nothing.** The Financial Statement Data Sets (2009Q2 onward) and the `data.sec.gov` XBRL APIs — `companyconcept`, `companyfacts`, and the **`frames` API** for cross-sections — tie **every fact to an accession number and a filing date**, so "what did the filing say when it was filed" is always reconstructible. Free, no licence, redistributable. Requirements: a 10 requests/second limit and a User-Agent that **must contain an email address** — a URL-only User-Agent is rejected with HTTP 403 (verified).

**One correction from prototyping this layer** (see `case-engine/SPEC.md`): `frames` rows carry no `filed` field, so **frames is not point-in-time safe on its own** — use it for discovery and screening, and use `companyconcept`, which does carry `filed`, for actual values. Also note `data.sec.gov` and `www.sec.gov` are separate hosts with separate reachability: you can end up with every number and no documents. Limits: XBRL coverage starts around 2009–2011, so pre-2009 cases need manual construction; no prices, no index membership, no estimates; US only; and tag inconsistency across filers makes normalisation real work.

**Historical consensus is the unsolved gap, and the recommended workaround is deliberately low-tech:** hand-curate a consensus table for a fixed case library. For 20–40 cases that is a few hundred data points, and historical consensus figures are frequently quoted verbatim in contemporaneous coverage and in the transcripts themselves ("versus the Street's $1.42"). Labour-intensive, legally clean, sufficient. The alternative — using **management guidance as the bar instead of consensus** — is free, point-in-time, unambiguous, and supports most of what Modules 10 and 13 teach; the guidance-versus-consensus gap can then be taught conceptually.

**On the data vendors: do not budget from the figures circulating in secondary sources.** Verification found that **Sharadar SF1 no longer publishes pricing** (quote-based, and its non-professional/professional tiering means a paid training product very likely needs the professional tier — the **licensing question matters more than the price**); **Norgate pricing could not be found at all**; and EODHD and Tiingo tiers conflict badly across sources. Treat all of these as "request a quote," not as line items. Confirmed public prices: **Stock-Trak at $12–$49.95 per student** depending on tier, and **Polygon.io at $0 / $29 / $79 / $199** (note it rebranded to "Massive" in late 2025).

**The apparent limitation is the design virtue.** A *fixed* case library is **better assessment** than a dynamic any-company-any-date simulator, because identical stimuli across students is the OSCE property that makes scores comparable — and it lets you reuse answer keys, anchor papers and golden sets. A dynamic simulator would be more impressive, cost far more, and measure worse.

**Build complexity: high** (the highest in the blueprint, and worth it). **MVP: medium.**

## INF-2 — The Model Auto-Grader

**What it does.** Ingests an uploaded workbook and scores it on four independent axes: correctness, liveness, structure and hygiene.

**The techniques that actually work, in descending value:**
1. **Named-range submission contracts.** Require students to name output cells, or supply a template with a locked, pre-labelled `SUBMISSION` sheet they link into. **This single decision eliminates roughly 80% of autograding fragility** — you stop having to find the EPS cell.
2. **Perturbation / shock testing.** Change an *input*, recalculate, and verify the *outputs moved the right way by the right amount*. **This is the only way to distinguish a genuinely live, correctly-linked model from one with the right numbers hardcoded** — no static value check can do it. Run 3–5 shocks per model against deltas from the golden model.
3. **Three-statement integrity ties.** Balance sheet balances every period; ending cash ties; net income ties from P&L to cash flow to retained earnings; sum of segments ties to consolidated. Objective, high-signal, fully automatable — **the best value per engineering hour in the whole stack.**
4. **R1C1 formula-consistency across forecast rows.** Convert formulas to R1C1 and check that every cell in a forecast row shares one string. Inconsistency along a time axis is the classic model bug and what a PM spots in five seconds.
5. **Hardcode detection**, as a hygiene sub-score rather than a hard fail (some hardcodes are correct), with a whitelist for legitimate constants.
6. **Circular-reference detection** via the dependency graph, distinguishing intentional circularity with iterative calc enabled from accidental.
7. **Dependency-wiring tests** — "does the revenue line depend on **both** a volume cell and a price cell?" **Ungameable by labelling**, and the single best check for whether a student built a real driver model.
8. **Error-cascade containment.** Limit how far one upstream error propagates into downstream wrong answers, or a single early slip zeroes an otherwise competent model. Score check-cell clusters against the student's *own* upstream values where the dependency is isolable.

**Tooling.** `openpyxl` as the structural backbone (reads formulas but does not compute them); **`formulas`** or **`pycel`** to build the dependency DAG and actually evaluate — these are what make perturbation testing possible without Excel (note `pycel`'s last release was a 2021 beta, so test coverage before committing); LibreOffice headless for free recalculation with imperfect fidelity on edge cases; or the **Microsoft Graph Workbook API** for real-Excel fidelity without local Excel, which is the best fidelity-per-ops-effort option if M365 licensing is acceptable.

**Commercial precedent that this works at scale:** **McGraw Hill's "Integrated Excel"** runs inside their platform with no file transfer and lets instructors choose to auto-grade **by formula accuracy or by solution value** — which answers "results only or formulas too?" with "both, instructor's choice." Pearson's MyLab Grader Projects use a download/upload model, and have one feature worth stealing: **different starting values per student.** The **Financial Modeling World Cup** proves high-stakes competitive spreadsheet assessment is viable, and its scoring mechanics are richer than usually described — 1,000 points per stage, with a **time bonus of 10 points per minute for the first 10 minutes saved then 1 point per minute, gated on scoring at least 90% of the regular points.** That 90% gate is a genuinely good mechanic to borrow: it rewards speed only once accuracy is established. (The "designated submission cells, tolerance-matched" mechanic is widely described but **could not be confirmed** — do not cite it as sourced.)

**Why hygiene deserves its own score:** field audits converge on **cell error rates of roughly 1–5%** in operational spreadsheets, with a large majority of substantial real-world spreadsheets containing at least one error; an analysis of ~15,770 spreadsheets from the Enron corpus found roughly **24% of those containing formulas had at least one error value.** Given those base rates, scoring hygiene teaches a skill the industry demonstrably lacks. **It also means your own golden models will contain errors — budget for independent review of every answer key.**

**Exercises supported:** M06-E1/E2/E3/E4, M07-E2/E3, M08-E1/E2, M09-E1/E2/E3, M10-E2/E3/E4, M11-E1/E2/E3/E4, M12-E1/E2/E3, M13-E1/E2/E3, M15-E1/E2/E3. **Nearly every quantitative exercise in the blueprint.**

**Build complexity: medium.** **This is the highest-ROI build in the program** and should be second after the MVP case library.

## INF-3 — The Role-Play Station Engine

**What it does.** Runs two station types against a scripted persona: a **management meeting** (CFO/IR) and a **PM grilling**.

**The design device, borrowed from medical education's standardised patient:** give the agent a **fact pack** (ground truth), a **disclosure policy** (what it volunteers unprompted versus what it releases **only if asked a specific question**), a **deflection repertoire**, and a **consistency constraint** (never contradict the pack, never invent numbers). Because extraction of gated facts is **binary and logged**, the station achieves near-perfect reliability — rare in judgment assessment.

**Honest positioning, corrected from an earlier assumption.** This is **less of a moat than it first appears.** Generic AI role-play with custom personas *and custom scoring rubrics* is now close to a commodity — several products offer it, some with explicit financial-services positioning and user-defined rubrics. The medical analogue is a mature commercial product that **already scores "essential interview components" on exactly the only-if-asked pattern**, so the device is proven rather than novel. And a 2026 study of an AI pitch simulator playing a VC investor, scored on an 8-point rubric, found participants valued the repeatable structured practice but noted reduced emotional and non-verbal fidelity. **What remains defensible is the content, not the capability:** the case library, the only-if-asked disclosure scripts, the behaviourally-anchored rubrics, and the golden set. Build on a commodity engine; invest in the scripts.

**Technical requirements.** Speech-native APIs or an orchestration framework handling turn-taking, VAD and interruption. **Barge-in matters more than raw latency for adversarial role-play — a PM who cannot interrupt you is not a PM.** Natural turn gaps are ~200ms; under 500–800ms voice-to-voice is acceptable; cascaded ASR→LLM→TTS stacks land at 1–2.5s and feel stilted. Accept slightly higher latency to get interruption.

**Two design elements that carry most of the value:** the **planted unknowable question** (grading whether the student fabricates — a critical failure), and the **planted MNPI bait** in the management meeting. And run **unlimited ungraded practice plus one graded instance on a fresh scenario** — the aviation training/evaluation split. Unlimited practice is nearly free and is the actual product value; the graded run is what the certificate rests on. It also defuses the desirable-difficulties complaint problem.

**Exercises supported:** M02-E4, M05-E4, M09-E4, M14-E1 (defence), M14-E3.

**Build complexity: high.** Amortised across five exercises in four modules.

## INF-4 — The Calibration Ledger and Forecast Resolution Engine

**What it does.** Every module ends with 5–10 resolvable questions carrying a stated resolution date. Students submit probabilities. The system resolves them automatically from filings and prices and returns Brier, reliability, resolution, and a skill score against a base-rate forecast.

**Why it is the highest-value-per-dollar item in the blueprint:** it is cheap, fully automatic, generates 75–150 scored forecasts per student, is the only valid outcome measure available (§2.2), and produces the program's one defensible efficacy claim. Because the case engine serves masked historical data, **resolution is instant** — you do not wait a quarter for ground truth.

**It also comes free from a decision made elsewhere.** Because the idea ledger and capstone enforce **mandatory structured fields** (target, horizon, conviction, catalyst with date, falsification condition), every student submission is *already* a timestamped, horizon-bounded forecast. No extra student effort. **This is why structured fields are the single most important technical design decision in the blueprint** — free-form memos are not scoreable at scale, and structured fields make both auto-grading and calibration scoring essentially free.

**Exercises supported:** all 15 modules, plus the TI5 pre/post battery.

**Build complexity: low–medium.** **Build this second or third.**

## INF-5 — The Fake-Company Data Generator

**What it does.** Generates internally consistent synthetic companies — three statements that tie, plausible segment structure, a comp set, consensus estimates, an ownership profile — with **planted defects drawn from a defect register.**

**Why synthetic as well as historical.** Real cases have ground truth but are finite, effortful, and googleable. Synthetic cases are unlimited, cheaply parameterised, and let you plant a *specific* defect to test a *specific* skill. Use real cases where ground truth matters (calibration, the event clock, the re-underwrite) and synthetic where you need volume and control (forensic screens, comp-sheet traps, the booby-trapped DCF, the planted-error exercises).

**The key asset is the defect register.** Research for Module 06 alone produced a 25-item register of which **18 are fully auto-detectable.** Each defect maps to an exercise, a check, and a curriculum section — which also lets feedback point students back at the right video.

**Exercises supported:** M08-E2, M11-E4, M12-E3, M06-E1/E2, M01-E3, M01-E6, M03-E1, M14-E3, plus all vignette item sets.

**Build complexity: medium.**

## INF-6 — The Golden Set and Rubric Store

**What it does.** Holds, for every rubric: behaviourally anchored scale definitions, pre-scored anchor submissions at each score point with written rationales, a human-scored golden set of ≥100 submissions per rubric, and seeded validity items for drift monitoring.

**Why it is infrastructure rather than content.** It is what makes every LLM grader trustworthy, what lets you swap models without re-validating from scratch, and what lets you publish reliability coefficients. **Build the golden set before the graders that depend on it.**

**Where the anchors come from, cheaply:** run a behaviourally-anchored-rating-scale development process with Caughran, Carr and the guest speakers, harvesting **real critical incidents** — "the analyst who said 'I don't know, I'll find out by 4pm'" versus "the analyst who bluffed a number." Concrete behavioural anchors in PM vernacular are also what make an LLM judge reliable; vague anchors like "demonstrates strong analysis" produce wide variance.

**Build complexity: low technically, high in expert time.** The expert time is the point — it is the thing a competitor cannot copy.

## INF-7 — The Idea Ledger

**What it does.** A continuous, tracked paper book. Every student idea is logged with mandatory structured fields, timestamped, and tracked to a fixed horizon, producing per-student attribution: hit rate, slugging ratio, expectancy, factor-adjusted residual, and sizing-versus-conviction alignment.

**Precedent.** This is the industry's own answer to assessing someone before outcomes exist — juniors run shadow books. The industrialised version is an alpha-capture platform, where contributors submit ideas with conviction and horizon and are size-weighted by measured skill. Value Investors Club supplies the community mechanics worth copying: membership is gated on a write-up, members must post **2 ideas a year *and rate 20***, and ideas are released publicly after **45 days**. (Its rating scale is reported as 1–5 by third parties only, so **the 1–5 versus 1–10 question is unresolved**, and the FAQ is roughly eight years old while a 2026 profile says "2 to 6 ideas/year" — verify before copying the quota.) SumZero requires business/product analysis, valuation, **target price justification**, risks, **timeline/horizon** and **trade feasibility**, and **rejects ideas with less than 5–10% expected upside.**

**Guard against the known failure mode:** peer ratings in enthusiast communities drift upward and correlate with length and author reputation rather than accuracy. Mitigate by weighting each student's ratings by their own demonstrated rating accuracy, using **pairwise comparison against anchors** rather than absolute scores for anything high-stakes, and seeding pre-scored validity items invisibly.

**Exercises supported:** M05-E1, M12 ideas, M15-E1, M14-E2, and the calibration ledger.

**Build complexity: medium.**

## What NOT to build

- **A real-time market or trading simulator.** Category error, as above. If you want students to touch borrow mechanics and order types, a free paper-trading account at a real broker does it for nothing.
- **A P&L-scored trading competition.** Outcome-dominated, and it rewards precisely the overconfidence the program should be training out. Research for Module 15 recommended explicitly de-weighting these.
- **A bias-recognition quiz.** Low validity. Students learn to name biases without becoming less biased.
- **Your own data terminal.** Licensing for a commercial trainer is the blocker, not the engineering — academic-rate access to the gold-standard datasets is generally unavailable to a for-profit training company, which is a hard constraint worth knowing before anyone scopes it.
- **Video or facial analysis of pitches.** Fairness liability, marginal signal, and there is a well-known cautionary precedent of a hiring vendor withdrawing exactly this capability after external audit.
# Part 5 — Suggested Build Roadmap

Sequenced by value to students per unit of effort. The ordering principle: **build the things that make other things gradable before building the things that get graded.**

## Phase 0 — Before you build anything (2–3 weeks, no engineering)

Three blocking items. All three are cheap and all three invalidate work done without them.

1. **Resolve the proprietary-framework gaps with Caughran directly.** The following are named in the syllabus and **not published anywhere**: the **four reasons markets are not efficient** (M01); the **seven hacks for identifying variance vs. street** (M06); the **substance of the nine thesis-development steps** (M03 — the step names are confirmed, the content is not); **"spring-loaded" and "peak-on-peak"** (M13, and peak-on-peak has **two materially different readings** that imply different items); **"exceptionalism," "model linkage," "alpha load," "10% mindset," "durable growth algorithm," "viability"**; the **idea buckets** (count confirmed as nine, contents not); the **5 Dimensions of Equity Fragility**; and the **7-Year Test** mechanic. An hour of his time removes a dozen caveats from this document.
   - Already resolved and *not* needing his time: **ETIK = "Everything There Is to Know"** (confirmed); **MIC's C = "convergence"** (confirmed); **FEV** (confirmed); **"Focus Five"** resolved to five items but single-sourced to a machine transcript — worth a 30-second confirmation.
2. **Run the verification queue in Part 7.** Roughly 25 fetches. Several currently-quoted numbers in circulation are wrong or stale, and this document flags which.
3. **Decide the two scoring presets.** Long-only houses weight written durability and multi-year earnings power; pods weight catalyst density, expectations gaps and sizing. **The same capstone artefact should be scorable under either preset**, and students should choose their target seat at intake. Modules 11/12/13/15 lean pod; 07/08/09 lean long-only.

## Phase 1 — Foundation (weeks 1–10): make things gradable

| Build | Why first |
|---|---|
| **INF-6 Golden Set and Rubric Store** (skeleton) | Every grader depends on it. Start harvesting critical incidents from Caughran and Carr immediately — it is the long-lead item and the only one a competitor cannot copy. |
| **INF-2 Model Auto-Grader** | Highest ROI in the program. Unlocks ~30 exercises across 10 modules. Start with the three cheapest, highest-signal checks: named-range contracts, three-statement integrity ties, and perturbation testing. |
| **INF-4 Calibration Ledger** | Cheap, fully automatic, and it is the program's one defensible efficacy claim. |
| **Layer A + B content: retrieval drills and vignette item sets** | ~95% of assessment volume at ~5% of cost. The CFA Level II item-set format — a 1–2 page case with exhibits and **4 questions** — is the right default: it is the only MCQ format that tests judgment rather than recall, it is 100% auto-gradable, and it amortises one expensive stimulus across four items. |

**Phase 1 deliverable:** every module has auto-graded retrieval and vignette assessment, the modelling modules have working auto-graded exercises, and the calibration ledger is running. **This alone is more assessment than any comparable program offers**, and it is achievable without the hard builds.

## Phase 2 — The keystone (weeks 8–20, overlapping): time compression

| Build | Why now |
|---|---|
| **INF-1 Historical Case Engine, MVP** | 8–12 hand-built cases. Unlocks roughly half the blueprint, including M13-E1 (the program's flagship) and M10's expectations work. |
| **INF-5 Fake-Company Data Generator** + the defect register | Gives unlimited volume and controlled defect planting where real cases are scarce. |
| **The flagship exercises** | M13-E1 (event clock), M10-E1 (expectations gap trap), M07-E1 (90-minute 10-K brief), M11-E1 (derive the multiple), M06-E3 (guidance bridge). |

**Sequencing note:** build the case engine as **files plus a form** first. Do not build the web app until the cases have been run with real students twice. The content is the asset; the delivery layer is replaceable.

## Phase 3 — Differentiation (weeks 18–32)

| Build | Why now |
|---|---|
| **INF-7 Idea Ledger** | Turns the cohort into a continuous assessment stream and feeds the calibration ledger. |
| **Layer J: the capstone** with the ICD-203-derived artefact rubric and the separate defence rubric | The terminal assessment. Needs the golden set to be mature. |
| **INF-3 Role-Play Engine** | The highest-cost build and the one with the least defensible moat — which is exactly why it comes after the content that *is* defensible. Start with **text** before voice; text role-play is a fraction of the cost and tests the same questioning discipline. |
| **Layer K: the entrustment report** | The credential. Only meaningful once A–J are producing evidence. |

## Phase 4 — Maturity (ongoing)

- **Publish your inter-rater reliability.** Double-score capstones, report quadratic weighted kappa per station type, target ≥0.75 on near-objective dimensions and ≥0.60 on holistic ones. **No competitor in finance training does this**, and it is the concrete form of the "structure, not modality" argument.
- **Post-program spaced retrieval.** Optimal review gaps of 3–8 weeks mean the assessment layer must outlive the 15 modules — which is also the commercial argument for a renewable subscription.
- **Run the drift monitoring.** Seeded validity items, pinned model versions, and a refusal to ship a grader change that drops measured agreement.
- **Expand the case library** toward 30–40, prioritising situation diversity over sector coverage.

## If the budget is much smaller than assumed

Build, in this order, and stop wherever the money runs out: **(1)** the vignette item-set bank for all 15 modules; **(2)** the calibration ledger; **(3)** the model auto-grader with three checks; **(4)** six historical cases; **(5)** the capstone rubric plus anchor memos. That is perhaps 25% of the full effort and captures most of the student value, because layers A, B, C, D and F are where the volume lives.

## The three things I would not compromise on

1. **The calibration ledger**, because it is the only honest outcome measure and the only defensible efficacy claim.
2. **Perturbation testing in the model grader**, because without it you are grading answers rather than models, and a hardcoded workbook scores identically to a live one.
3. **Mandatory structured submission fields**, because they are free to implement, they make everything downstream gradable, and retrofitting them later means re-authoring every exercise.
# Part 6 — Sources, by topic

**Provenance reminder:** none of these were opened as documents (see the front matter). URLs are the canonical locations to verify each claim, reached via search-result extraction. Deliberately excluded: pirated course-material hosts (a CliffsNotes-hosted confidential FE deck, several Scribd re-uploads, and a site offering the Academy as a free download) and low-reliability aggregators.

## Fundamental Edge / Caughran primary
fundamentedge.com/analyst-academy · fundamentedge.com/blog/the-market-is-broken-why-stocks-move · fundament-edge.squarespace.com/s/FE-x-IC-Info-Session-Deck.pdf · fundament-edge.squarespace.com/s/FExIC-Syllabus-Outline-5.pdf · fundamental-edge.teachable.com/p/academy-april-2026 · **wallstreetprep.com/self-study-programs/buy-side-financial-modeling/** (the Caughran-taught course lesson list — the source that confirms **ETIK = "Everything There Is to Know"**) · wallstreetprep.com/knowledge/hedge-fund-course · x.com/FundamentEdge status 1554829073636999169 (FEV), 1570836119687921671 ("Blown out of a pod"), 1700232675477618707 ("Beat the pods"), 1617893298278133760 ("Is this interesting?"), 2036140329125241210 (AI and alpha), 1575857342754627585 (incremental margin), 2016546337953853872 (the model as "table stakes"), 1564408743533547521 (buy-side whisper), 1561856044392796160 (idea generation), 1562165424199835648 (idea buckets), 1561856070993055744 (chaos & change), 1600581222530359296 (idea velocity), 1771239097769816091 (why stocks move) · threadreaderapp.com/user/FundamentEdge · threadreaderapp.com/thread/1563563047465103365.html ("a thesis is not a book report") · aima.org/article/ep-70-how-to-survive-and-thrive-as-a-buy-side-analyst.html · podcasts.apple.com/podcast/fundamental-edges-brett-caughran-on-setting-up-for (YAVP #220) · yetanothervalueblog.com/p/fundamental-edges-brett-caughran · institutionalinvestor.com/article/2bstq4h4e2sqjx0fre9s0 · wpcarey.asu.edu (Caughran bio, FIN 494) · pennwitg.com/competition and avicasu.com/stock-pitch-competition (FE-judged competitions — FE's revealed rubric)

## M01 — Market efficiency, mispricing, Pareto returns
papers.ssrn.com/sol3/papers.cfm?abstract_id=2900447 (Bessembinder 2018) · econpapers.repec.org/RePEc:eee:jfinec:v:129:y:2018:i:3:p:440-457 · datagolf.com/static/blogs/fl_bias/fama_1970.pdf (Fama 1970) · knowledge.wharton.upenn.edu/article/the-lasting-impact-of-a-1976-paper-on-stock-information-and-prices/ (Grossman–Stiglitz) · nber.org/papers/w5167 and ms.mcmaster.ca/~grasselli/ShleiferVishny97.pdf (Shleifer & Vishny 1997) · dspace.mit.edu/bitstream/1721.1/75362/1/Lo_Adaptive%20Markets.pdf · institutionalinvestor.com/article/2bsxcauvaxemsst5us9a8 (paradox of skill) · quoteinvestigator.com/2020/01/09/market/ (the voting/weighing provenance trap) · morganstanley.com/im/publication/insights/articles/article_whoisontheotherside.pdf (BAIT) · cfainstitute.org/insights/professional-learning/refresher-readings/2026/market-efficiency

## M02 — Buy-side structure, LPs, fees, compliance perimeter
hfr.com/media/market-commentary/global-hedge-fund-industry-capital-surges-nears-historic-5-trillion-milestone/ · thepluto.substack.com/p/multi-manager-or-multi-strategy-or · hedgeweek.com/hedge-funds-charging-billions-in-no-limit-passthrough-fees/ · bloomberg.com/graphics/2025-hedge-fund-investment-fees/ · sec.gov/Archives/edgar/data/2026275/000139834424023275/fp0091372-1_n2aixbrl.htm · ib.barclays/our-insights/3-point-perspective/2025-hedge-fund-outlook.html · aima.org/article/the-great-manager-hunt-key-highlights-from-the-hedgeweek-aima-mid-year-allocator-sentiment-report-2025.html · morningstar.com/funds/how-active-etfs-are-reshaping-fund-fees · depot.som.yale.edu/icf/papers/fileuploads/2370/original/06-14.pdf (Cremers–Petajisto, active share) · evidenceinvestor.com/wp-content/uploads/2019/01/faj.v69.n4.7.pdf · **govinfo.gov/content/pkg/FR-2000-08-24/pdf/00-21156.pdf and ecfr.gov/current/title-17/chapter-II/part-243/section-243.100 (Reg FD)** · sec.gov/files/rules/final/33-7881.htm · wilmerhale.com/-/media/files/.../csld082300.pdf (Reg FD is an issuer-disclosure rule, not an antifraud rule) · dechert.com/content/dam/dechert files/knowledge/publication/2018/4/SRLRRegFD.pdf · justice.gov/usao-sdny/pr/sac-capital-portfolio-manager-mathew-martoma-found-guilty-manhattan-federal-court · sec.gov/news/press/2011/2011-233.htm · caselaw.findlaw.com/court/us-2nd-circuit/1871789.html (*Newman*) · tuckerellis.com/lingua-negoti-blog/is-the-mosaic-theory-as-a-defense-to-insider-trading-dead/ · analystprep.com/study-notes/cfa-level-2/standard-ii-material-nonpublic-information/

## M03, M14 — Thesis development, pitching, published rubrics
**cfainstitute.org/sites/default/files/-/media/documents/support/research-challenge/challenge/rc-written-report-guidelines.pdf** and **.../research-challenge-official-rules.pdf** (the written-report and presentation rubrics, with weights) · cfasociety.org/phoenix/Pages/GradingCriteria.aspx (a superseded season — useful for seeing that weights move) · cfainstitute.org/programs/research-challenge · static1.squarespace.com/.../Stock-Pitch-Rules-2025.pdf (McGill) · yis.org/programs/stock-pitch-competition/stock-pitch-report/ · **sumzero.com/quality_guidelines** · **valueinvestorsclub.com/help/faq** · umichmbef.org/competition/ · gatton.uky.edu/uk-stock-pitch-competition · smeal.psu.edu/bires/reit-stock-pitch-competition · sohnconference.org · moiglobal.com · **hbr.org/2007/09/performing-a-project-premortem** (Klein) · valueinvestorindia.com/2005/11/22/concept-of-variant-perception/ (Steinhardt) · richard-toad.ghost.io/how-to-craft-a-winning-stock-pitch/ · l3vlup.com/guides/hedge-fund-case-study-interview

## M04, M10 — Why stocks move, expectations investing
**expectationsinvesting.com/the-book** (Tutorial 8 carries the book's own price-implied-expectations spreadsheet — the highest-value artefact still unfetched) · morganstanley.com/im/publication/insights/articles/article_marketexpectedreturnoninvestment_en.pdf · .../article_theneglectedvaluedriver_ltr.pdf (competitive advantage period) · .../article_totalshareholderreturns.pdf · eatonvance.com/.../article_everythingisadcfmodel_us.pdf · sorfis.com/wp-content/uploads/2021/09/The-Base-Rate-Book-...-September-2016.pdf · morganstanley.com/content/dam/im/.../article_thewisdomofcrowds_ltr.pdf · www-stat.wharton.upenn.edu/~steele/Courses/434/434Context/Momentum/MomentumStrategiesJF96.pdf (Chan–Jegadeesh–Lakonishok) · academia.edu/119586135 (Bernard & Thomas) · hillsdaleinv.com/uploads/The_Russell_Reconstitution_Effect... (Madhavan 2003) · hbs.edu/ris/Publication Files/23-025_...pdf (Greenwood–Sammon, index-effect decay) · ruf.rice.edu/~yxing/option-skew-FINAL.pdf · msci.com/downloads/web/msci-com/data-and-analytics/crowding-solutions/MSCI-Factor-Crowding-Model-cfs-en-2019.pdf · cdn.ihs.com/www/pdf/Shining_the_Light_on_Short_Interest.pdf · visiblealpha.com/products/consensus-only-insights/ · cfainstitute.org/sites/default/files/-/media/documents/study-session/2025-l2-los-t5.pdf

## M05 — Idea generation, quality, base rates
cuhk.edu.hk 1996TAR (Sloan accruals) · pubsonline.informs.org/doi/fpi/10.1287/mnsc.1110.1320 · en.wikipedia.org/wiki/Beneish_M-score and gmtresearch.com/beneishs-m-score · corporatefinanceinstitute.com/resources/accounting/piotroski-f-score · accountingtools.com/articles/the-altman-z-score-formula.html · nber.org/papers/w15940 · eatonvance.com article_measuringthemoat.pdf · hedgefundalpha.com/investment-strategy/michael-mauboussin-roic-patterns-and-shareholder-returns · rpc.cfainstitute.org/research/multimedia/2017/capital-light-compounders-and-reinvestment-moats-with-connor-leonard · basehitinvesting.substack.com/p/importance-of-roic-reinvestment-vs-legacy-moats · novelinvestor.com/chuck-akres-three-legged-stool · themarket.ch scale-economies-shared-ld.14926 · nber.org/papers/w23075 and fairmodel.econ.yale.edu/ec439/shiller1.pdf (Shiller, narrative) · ubs.com thematic-investing/pure-play · morganstanley.com/im dispersion-and-alpha-conversion.pdf · alphatheory.com/blog/batting-and-slugging-sensitivity

## M06 — Buy-side modeling
sec.gov/Archives/edgar/data/1757073/... (Envista/NVST separation filings; **CIK 1757073** for the operating financials) · sec.gov/Archives/edgar/data/313616/... (Danaher split-off) · onlinelibrary.wiley.com/doi/10.1111/1475-679x.70072 (Larocque, provider differences in consensus) · spglobal.com/market-intelligence/en/solutions/visible-alpha · hedgenordic.com/2023/06/demystifying-consensus-estimates/ · wallstreetoasis.com/forum/investment-banking/what-is-a-2-year-stack and freightwaves.com/news/choosing-between-year-over-year-and-sequential-comps and upfina.com/demystifying-the-confusing-retail-sales-report/ (the three conflicting 2-year-stack conventions) · mergersandinquisitions.com/lbo-modeling-test/ · fe.training/free-resources/careers-in-finance/90-minute-lbo-modeling-test/ · wallstreetprep.com/knowledge/leveraged-buyout-lbo-modeling-1-hour-practice-test/ · peer.asee.org/automated-grading-of-microsoft-excel-spreadsheets.pdf · aisel.aisnet.org/cgi/viewcontent.cgi?article=1012&context=siged2018 · exprep.com

## M07, M08 — Business and industry analysis
safalniveshak.com/wp-content/uploads/2017/01/Measuring-the-Moat-Mauboussin-2016.pdf · shareholderforum.com/returns/Library/20140604_Mauboussin-Callahan.pdf (calculating ROIC) · morganstanley.com/im/publication/insights/articles/article_roicandintangibleassets_us.pdf · covestreetcapital.com/wp-content/uploads/2015/07/Mauboussin-June-2015.pdf · pages.stern.nyu.edu/~adamodar/pdfiles/eqnotes/cap.pdf · adambrandenburger.com/aux/material/ssf-06-27-24.pdf · theinvestorspodcast.com/episodes/7-powers-by-hamilton-helmer (Helmer's 7 Powers) · alphaarchitect.com/book-review-competition-demystified-radically-simplified-approach-business-strategy (Greenwald) · link.springer.com/article/10.1007/s11142-013-9228-9 (Kravet & Muslu, risk-factor disclosure) · onlinelibrary.wiley.com/doi/10.1111/irfi.12324 · nber.org/system/files/working_papers/w30032/w30032.pdf · wallstreetprep.com/knowledge/cash-conversion-cycle-ccc · qualityequities.substack.com/p/maintenance-capex · vigilantllc.com/risk-alert-investment-adviser-mnpi-compliance-issues · stat.wharton.upenn.edu PairsTradingGGR.pdf

## M09 — Management and capital allocation, SBC
onlinelibrary.wiley.com/doi/abs/10.1111/jacf.12090 and academia.edu/41831740 (Mauboussin & Callahan, *Capital Allocation*) · ideas.repec.org/a/eee/jfinec/v124y2017i2p307-330.html and corpgov.law.harvard.edu/2017/06/11/compensation-goals-and-firm-performance (Bennett/Bettis/Gopalan/Milbourn — compensation-goal bunching) · ideas.repec.org/a/ucp/jlawec/doi10.1086-684038.html and library.hbs.edu/working-knowledge/private-meetings-of-public-companies-thwart-disclosure-rules (Solomon & Soltes — private meetings) · researchgate.net/publication/256557208_Market_Underreaction_to_Open_Market_Share_Repurchases (Ikenberry/Lakonishok/Vermaelen) · quartr.com/insights/business-philosophy/unconventional-ceos-william-thorndike-s-book-the-outsiders and blas.com/the-outsiders/ · berkshirehathaway.com/letters/letters.html and berkshirehathaway.com/ownman.pdf · asc.fasb.org (ASC 718) · ecfr.gov/current/title-17/chapter-II/part-229

## M11 — Applied valuation
**morganstanley.com/im/publication/insights/articles/article_valuationmultiples.pdf** (Mauboussin & Callahan, 23 Apr 2024 — the verbatim Gordon-growth→multiples derivation; continuing value "commonly in excess of 75 percent") · **eatonvance.com/.../article_everythingisadcfmodel_us.pdf** ("what drives the DCF model is for the most part a dressed up multiple"; "you have to earn the right to use a multiple") · morganstanley.com/im/.../article_themathofvalueandgrowth.pdf · strawman.com/member/uploads/objects/... (*What Does a P/E Multiple Mean?*, Credit Suisse 2014) · pages.stern.nyu.edu/~adamodar/pdfiles/papers/ERPcurrent.pdf · aswathdamodaran.substack.com/p/the-price-of-risk-with-equity-risk · cfainstitute.org/insights/professional-learning/refresher-readings/2026/free-cash-flow-valuation · kellogg.northwestern.edu/faculty/jagannathan/teaching/practicum/2006/files/Week3/VI_Lecture_3.pdf (Greenwald EPV) · research.hhs.se/.../Technical-Note-Value-Driver-Formulas · wallstreetprep.com/knowledge/terminal-value/

## M12 — Short selling (regulatory content: verify before every cohort)
**morganlewis.com/pubs/2025/12/short-sale-reporting-on-form-sho-compliance-date-further-extended-to-2028** and **mofo.com/resources/insights/260107-u-s-sec-further-delays-compliance-dates** and sec.gov/newsroom/press-releases/2025-37 and regulatoryandcompliance.com/2025/12/sec-again-extends-short-sale-and-securities-lending-rules-compliance-deadlines-to-2028-while-it-considers-response-to-court-ruling/ (**Form SHO deferred to 2028; Fifth Circuit remand without vacatur**) · natlawreview.com/article/sec-announces-one-year-extension-rule-13f-2-form-sho-compliance · sec.gov (Reg SHO, Rule 201) · finra.org (Rule 4560 short-interest reporting) · federalreserve.gov (Reg T) · ortex.com/understanding-the-mechanics-and-metrics-of-short-selling/ · papers.ssrn.com (Stambaugh–Yu–Yuan, arbitrage asymmetry; D'Avolio 2002, the market for borrowing stock) · aqr.com (QMJ, BAB) · sec.gov staff report on the January 2021 episode

## M13 — Earnings season
jstor.org/stable/2491062 (Bernard & Thomas 1989) · doi.org/10.1016/0165-4101(90)90008-R (Bernard & Thomas 1990) · doi.org/10.1111/jofi.12885 (Cohen–Malloy–Nguyen, "Lazy Prices") · nber.org/papers/w13090 (Frazzini & Lamont, the earnings-announcement premium) · criticalfinancereview.org (Martineau on PEAD decay) · sraf.nd.edu/loughranmcdonald-master-dictionary/ · insight.factset.com/topic/earnings (current beat rates) · sec.gov/fast-answers/answers-form8khtm.html and sec.gov/corpfin/secg-accelerated-filer-and-large-accelerated-filer-definitions · cboe.com/insights/ · quartr.com

## M15 and the intensives — portfolio construction, risk, calibration
msci.com (Barra model handbooks) · simcorp.com (Axioma) · northinfo.com · garp.org/frm · doi.org/10.1093/rfs/hhy131 (Hou–Xue–Zhang, *Replicating Anomalies*) · doi.org/10.1093/rfs/hhv059 (Harvey–Liu–Zhu) · doi.org/10.1111/jofi.12530 (Harvey, presidential address) · doi.org/10.1111/jofi.12365 (McLean & Pontiff) · doi.org/10.1016/j.jfineco.2013.10.005 (Frazzini–Pedersen) · Grinold (1989) and Clarke–de Silva–Thorley (2002) on the fundamental law · Kupiec (1995); Artzner et al. (1999) doi:10.1111/1467-9965.00068 · journals.ametsoc.org (Brier 1950; Murphy 1973) · fred.stlouisfed.org, bls.gov/opub/hom, bea.gov/resources/methodologies, ismworld.org · open.fda.gov, clinicaltrials.gov, patentsview.org, fcc.gov/oet/ea/fccid (regulatory-database mining) · annieduke.com/books · goodjudgment.com

## Assessment design and grading technology
psycnet.apa.org/record/1993-40718-001 (Ericsson 1993) · journals.sagepub.com/doi/10.1177/0956797614535810 (Macnamara 2014) · **psycnet.apa.org/record/2009-15733-001 (Kahneman & Klein 2009 — the architectural spine)** · journals.sagepub.com/doi/10.1111/j.1467-9280.2006.01693.x (Roediger & Karpicke) · psycnet.apa.org/record/2015-01462-001 (Rohrer, interleaving) · bjorklab.psych.ucla.edu/publications · files.eric.ed.gov/fulltext/ED284181.pdf and aft.org/ae (Collins, Brown & Newman — cognitive apprenticeship) · journals.lww.com/academicmedicine (Regehr et al. 1998 — checklists vs global ratings) · link.springer.com/journal/10459 and Van der Vleuten & Schuwirth (2005) *Med Educ* 39:309–317 · onlinelibrary.wiley.com/journal/13652923 (ten Cate 2005 — entrustable professional activities) · **intelligence.gov/assets/documents/intelligence-community-directives/ICD_203.pdf (the nine analytic tradecraft standards)** · cia.gov/resources/csi/books-monographs/psychology-of-intelligence-analysis · faa.gov/regulations_policies/advisory_circulars (LOFT/LOE) · journals.sagepub.com/doi/10.1177/0956797614524255 (Mellers 2014) and journal.sjdm.org (Chang et al. 2016 — the Brier training effect) · psycnet.apa.org/record/1998-10661-006 (Schmidt & Hunter 1998) and **psycnet.apa.org/record/2021-77453-001 (Sackett et al. 2022 — the re-ranking)** · cfainstitute.org/programs/cfa/exam/structure · garp.org/frm/exam-details · fmworldcup.com · eusprig.org and panko.shidler.hawaii.edu/ssr (spreadsheet error rates) · arxiv.org/abs/2306.05685, /2303.16634, /2305.17926, /2404.13076, /2404.18796 (LLM-as-judge; **note the 2026 work contesting the panel finding**) · openpyxl.readthedocs.io, github.com/vinci1it2000/formulas, github.com/stephenrauch/pycel, learn.microsoft.com/en-us/graph/api/resources/excel · sec.gov/edgar/sec-api-documentation and sec.gov/dera/data/financial-statement-data-sets.html · evolve.elsevier.com (Shadow Health — the only-if-asked precedent) · stocktrak.com · polygon.io/pricing · eeoc.gov/laws/guidance/employment-tests-and-selection-procedures, nyc.gov/site/dca/about/automated-employment-decision-tools.page, artificialintelligenceact.eu
# Part 7 — Verification Queue

Everything below should be checked before it reaches a paying student. Ordered by value. The first group carries almost all the externally-quotable numbers in this document; the second group is content the course itself owns and only Fundamental Edge can supply.

## A. Blocking — ask Caughran (no research will close these)

These are named in the syllabus and published nowhere. An hour of his time removes a dozen caveats from this blueprint.

| # | Item | Module | Why it blocks |
|---|---|---|---|
| A1 | **The four reasons markets are not efficient** | M01 | The heading is verbatim in FE's own free syllabus PDF; the list exists only inside the paid video. M01-E6 is written to be robust to this, but an item keyed to "name his four" cannot be built. |
| A2 | **The seven hacks for identifying variance vs. street** | M06 | Heading only. Do not conflate with his public "Modeling: 12 Common Buy-Side Approaches" thread — different list. |
| A3 | **The substance of each of the nine thesis-development steps** | M03 | Step *names* are confirmed from two independent sources; the content of each step is unpublished. |
| A4 | **"Spring-loaded" and "peak-on-peak"** | M13 | **Peak-on-peak has two materially different readings** — peak earnings on a peak comp base (a comparison problem) versus a peak multiple on peak earnings (a valuation problem). They imply different assessment items. This is the single most consequential ambiguity in the document. |
| A5 | **"Alpha load," "10% mindset," "exceptionalism," "model linkage," "viability," "durable growth algorithm"** | M01, M04, M05, M07, M08 | Headings only. Exercises are written around the *function* rather than the label. |
| A6 | **The nine idea buckets** | M05 | Count confirmed as nine from FE's own X account; only buckets 2 (compounders) and 3 (mispriced catalysts) recovered. |
| A7 | **"Focus Five" — confirm the five items** | M04 | Resolved to organic revenue growth / margin trajectory / capital intensity / capital deployment / terminal value visibility, but **single-sourced to a machine-generated podcast transcript.** A 30-second confirmation. Also confirm that Focus Five ≠ the three key drivers. |
| A8 | **The "5 Dimensions of Equity Fragility"** and the **7-Year Test** mechanic | M11, M04 | Both have real FE threads; both truncate before the mechanic. |
| A9 | **"Coverage models impact thesis development latency"** | M03 | Genuinely ambiguous between your seat's coverage model and sell-side coverage density. Both readings are useful; they need different items. |
| A10 | **Is there any options content anywhere in the curriculum?** | M10, M13 | Implied-move and hedging content requires it and the brochure shows none. Either it exists and the brochure understates it, or the assessment layer must supply a primer. |
| A11 | **Is there any sleeve risk-management content?** | M15 | Gross/net, factor neutrality, stop-outs and contribution-to-risk appear almost nowhere, despite the program training pod analysts. |
| — | *Already resolved — do not spend his time:* **ETIK = "Everything There Is to Know"** (confirmed via the Wall Street Prep lesson list); **MIC's C = "convergence"** (confirmed from FE's own page); **FEV** (confirmed) | | |

## B. High value — one fetch each

| # | Item | Why |
|---|---|---|
| B1 | **Appendix E of the current (2026-27) CFA Research Challenge rules**, read directly | Both rubrics were recovered, but **the appendix letter moves by season** (E in 2026-27, D previously) and weights have changed across seasons (an older version had Corporate Governance at 5; the current has ESG at 15). Lock the current season's split before building the capstone rubric. |
| B2 | **Van der Vleuten & Schuwirth (2005), *Med Educ* 39:309–317, Table 1 cell values** | This is what would let the blueprint state a *defensible station count* rather than deriving it arithmetically from "3–4 hours." Currently the document derives it and says so. |
| B3 | **Expectations Investing Tutorial 8** (expectationsinvesting.com) | Carries the book's own price-implied-expectations spreadsheet. Would upgrade M10-E2 from my construction to the canonical worked example. |
| B4 | **ICD 203 PDF, to confirm version** | The nine standards were recovered verbatim and in order, but **revision history conflicts** across sources (ODNI shows Jan 2015 + Jun 2023; a legal summary says "amended 21 Jan 2022"). State which version your rubric derives from. |
| B5 | **Bernard & Thomas (1989/1990) PEAD magnitudes** | Retrievable secondary figures conflict badly (8–9%/quarter vs 4.2%/60 days vs ±2%) and at least one appears mis-attributed. **Do not put a PEAD magnitude in an answer key until the primary is open.** Also get recent evidence on whether PEAD has decayed. |
| B6 | **Current FactSet Earnings Insight beat rate** | Quoted constantly, easy to get wrong, and it moves every quarter. Date-stamp it. |
| B7 | **Beneish's original paper on the threshold** | Sources genuinely conflict (−1.78 vs −2.22) and the original frames the cutoff as depending on the relative cost of Type I vs Type II errors. M12-E3 currently teaches the ambiguity, which is defensible, but the primary would let you do it properly. |
| B8 | **Envista/NVST operating financials — EDGAR CIK 1757073** | The separation mechanics are confirmed from filings; **zero operating financials were recovered.** The M06 NVST case cannot be built without them. |
| B9 | **The four unconfirmed *Outsiders* traits** | Buyback preference, dividend aversion, counter-cyclical leverage and guidance aversion are widely attributed to Thorndike and **could not be confirmed.** Do not print them as his. |
| B10 | **Mauboussin's per-use capital-allocation evidence** | The taxonomy and the aggregate facts are sourced; the per-use academic evidence — the most useful part for M09 — is not. |
| B11 | **Reg FD's 24-hour trigger** | Two law-firm summaries describe it differently (running from when a senior official *learns* of the disclosure versus from the disclosure itself). Read the rule. |
| B12 | **SEC Rule 13f-2 / Form SHO status, re-check each cohort** | Verified as deferred to **2 Jan 2028** with first filings **14 Feb 2028**, and remanded without vacatur in Aug 2025 — but the SEC may propose amendments. **Put this on a standing review cycle.** |
| B13 | **Current LLM-grader agreement literature** | This moves in months. The 2026 findings already overturned the 2024 panel-of-judges recommendation. Re-check before committing grader architecture. |

## C. Counsel review required

Every legal and compliance item in Modules 02, 09 and 12 and intensive TI4 needs review by qualified counsel before it reaches students, independent of whether the research is sourced. Two specific hazards found:

- **A conviction described in one research pass as standing was in fact vacated on appeal** (*US v. Newman*, 2d Cir. 2014, later partially overruled by *Salman*, 2016). Teaching a vacated conviction as a conviction in a compliance module would be a serious credibility failure at this price point. Get the case outcomes right from DOJ/SEC releases and the opinions themselves.
- **Reg FD is an issuer-disclosure rule, not an antifraud rule** — so it does not protect the analyst. Students routinely assume the opposite.

## D. Strike or caveat — currently unsupportable

| Item | Status |
|---|---|
| **Sharadar SF1 pricing** | No longer published; quote-based. Its non-professional/professional tiering means a paid training product very likely needs the professional tier — **the licensing question matters more than the price.** Strike any "$100–$300/month" figure. |
| **Norgate Data pricing** | Not found. Strike. |
| **EODHD / Tiingo pricing** | Sources conflict badly. Do not budget from them. |
| **Bloomberg Market Concepts pricing** | Not retrieved. Strike. |
| **Citadel Associate Program details** | Nothing official — forum anecdote only. Do not print. |
| **FMWC "designated submission cells, tolerance-matched"** | Widely described, **could not be confirmed.** The points/time-bonus mechanics *were* confirmed. |
| **Any firm's drawdown stop-out, net-exposure band, single-name or ADV cap, payout percentage, PM turnover, comp split, AUM or pod count** | Crowd-sourced and firm-unconfirmed; sources conflict (e.g. net exposure −20/+20 vs −10/+10). **State limits in the exercise prompt as hypotheticals and have students compute consequences.** Never ask "what is firm X's stop-out?" |
| **Active Share thresholds (60%/80%)** | Unconfirmed. Do not put a threshold in an answer key. |
| **"400–600% gross exposure" attributed to Caughran** | Unconfirmed. |
| **Bessembinder's 4.31% / 0.33% percentages, and his named top-5 wealth creators** | The percentages do not reconcile against the 25,967 sample; the named list could not be sourced. Use the paper's own framings. |
| **Value Investors Club's rating scale** | 1–5 is third-party only; the 1–5 vs 1–10 question is **unresolved**, the FAQ is roughly eight years old, and a 2026 profile says "2 to 6 ideas/year" against the FAQ's 2. Verify before copying the quota. |
| **Any verbatim Graham attribution for the voting/weighing line** | No primary source exists. |

## E. Known-thin areas, stated plainly

- **Firm-specific assessment internals** are the thinnest category in the project and will stay thin — funds do not publish them. The honest output is a composite funnel plus journalistic colour, which is what Part 2 gives. One genuinely useful find: a competitor program aimed at exactly this blueprint's target learner (6 months, 1–4 years' research experience, lateral to the buy side, covering modelling, valuation, pitching, Python and AI) is worth studying directly.
- **No published, specified *buy-side* modeling test exists anywhere.** Every documented instrument is investment-banking or private-equity. **Treat this as confirmed white space** and the strongest commercial argument for building this assessment properly.
- **The industry-P&L technique has essentially no public literature.** That makes it simultaneously FE's biggest genuine differentiator and the least documentable — build it from practitioner interview and do not expect to cite it.
- **Four Module-14 bullets are tested nowhere publicly** — follow-up, trading plans/thesis creep, pre/post-mortems, and evaluator-side hole-poking — because every competition and interview format is single-shot. The three M14 exercises exploit exactly that gap.
- **Adversarial role-play is less of a moat than it first appears.** Generic AI role-play with custom personas and custom rubrics is close to a commodity, and the medical analogue already implements the only-if-asked device commercially. **The defensible asset is the content — the case library, the disclosure scripts, the anchored rubrics, the golden set — not the capability.**
- **The nine intensives' content, length and instructors are unknown.** All scope for TI1–TI9 is inferred from titles alone and is the lowest-confidence material in this document.
