# Weekly AI-in-Legal and AI-in-Finance brief: plan (draft 1, 2026-10-29)

Goal: a skill that runs once a week, sweeps a fixed and verified set of sources plus open-ended search, and writes two executive newsletters (legal, finance) with key takeaways. Recall is the first design goal; writing quality is the second. Research behind this plan is in `newsletter/research/`.

## 1. What we learned from the research

- **Most high-value sources have working feeds.** About 40 RSS/Atom feeds were verified live from the cloud sandbox (Artificial Lawyer, LawNext, Legal IT Insider, Law360 Pulse, Finextra, Banking Dive, Bank Automation News, SEC, Fed, CFPB, OpenAI news, DeepMind, Mistral, HF, latent.space AI News, Zvi, Import AI, and more).
- **Google News RSS with a `when:7d` filter works** and returns dated, sourced items for arbitrary queries. That turns an entity watchlist (every firm, bank, vendor, regulator) into deterministic weekly queries without a search API.
- **A set of important pages has no feed and must be snapshot-diffed**: anthropic.com/news, Claude and OpenAI release notes, Gemini API changelog, Vals AI, Scale SEAL, Artificial Analysis changelog, Harvey/Legora/Hebbia/Rogo blogs, Charlotin's hallucination-case CSV.
- **Some sites block bots** (Bloomberg, Reuters, FT, WSJ, The Information, Law.com articles, Reddit, x.ai, arena.ai, American Banker). These are reachable only through search-engine snippets and through the aggregators that cite them.
- **X is pay-to-read now.** Nitter and xcancel are dead, the public syndication endpoints rate-limit datacenter IPs. Working routes: official X API pay-per-use (~$30-65/month for 100 accounts, ToS-clean), twitterapi.io (~$3/month, scraped upstream), and a free Bluesky fallback via verified mirror bots for the lab accounts. Details in `research/sources-x-twitter.md`.
- **Competing weeklies exist in both verticals** (Legal AI Weekly, The Redline, Legaltech Week, Fintech Brainfood, BankingNewsAI, Tom Fox's "5 Stories", AI News, Zvi). We should read them every run as a recall audit: anything they cover that we missed is a measurable miss.
- **Style:** the newsletters executives actually read share a small set of conventions (headline carries the news with a number; bold bottom line first; labelled "Why it matters" of ~60 words; one primary source per item; fact/report/rumour separated by verb; fixed weekly slots; dated "what to watch"). Full rules and a template are in `research/style-exemplars.md`.

## 2. Architecture

Three collection layers, then triage, then writing, then an editorial pass. Each layer writes to disk so a failure in one does not lose the others.

```
sweep.py (deterministic)        search sweep (agentic)        recall audit (agentic)
  RSS feeds (~40)                 ~30 vertical queries           read 8 competing weeklies
  Google News RSS (watchlist)     entity queries for             diff their items vs ours
  HTML snapshot diffs (~15)         bot-blocked outlets          add misses, flag them
  HN Algolia, HF API
  Bluesky mirrors + X provider
          \                 |                  /
           v                v                 v
                 candidates.jsonl  (url, title, date, source, snippet, tags)
                          |
                 dedupe against state/seen.jsonl (prior weeks) + cluster same story
                          |
                 triage: classify {legal, finance, both, frontier}, score importance,
                         fetch primary source for anything that will be written up
                          |
                 write legal.md and finance.md from the template; shared "Frontier" block
                          |
                 editor pass: style checklist, every number traced to a fetched source,
                         confidence labels, cut to length; write audit.md
                          |
                 commit to repo (+ optional Google Doc / artifact / email)
```

### 2.1 Deterministic sweep (`scripts/sweep.py`)

- Reads `references/sources.yaml`: feeds, snapshot pages, Google News queries, HN queries, HF orgs, Bluesky handles, X handles/list id.
- Window: last 8 days (one day of overlap so late-published items are not lost).
- Snapshot-diff pages: store the extracted text in `state/snapshots/<slug>.txt`; emit new headings/links as candidates.
- Google News RSS: one query per watchlist entity and per topic (about 120 queries, cheap). Watchlist is the entity list in `sources.yaml`: labs, legal vendors, finance vendors, AmLaw 50 and Magic Circle firms, G-SIBs and top asset managers, regulators.
- X: provider chosen by which secret is present (`X_BEARER_TOKEN` for official, `TWITTERAPI_IO_KEY` for the reseller); otherwise Bluesky mirrors only. Persist `since_id`.
- Output: `candidates.jsonl` plus `sweep-log.md` listing every source, item count, and any fetch failure, so a silent source outage shows up in the audit rather than as a quiet recall drop.

### 2.2 Agentic search sweep

Claude runs the ~30 queries in `sources-legal.md`, `sources-finance.md`, and `sources-lab-launches.md` with a past-week filter, plus "<entity> AI" for any watchlist entity whose Google News query returned nothing. Purpose: catch coverage from bot-blocked outlets and from sources not on the list. Results are appended to `candidates.jsonl` with `source: websearch`.

### 2.3 Recall audit

Fetch this week's issue of each competing weekly. For every item they cover, check whether our candidate set has it. Add misses with a `recall_miss` flag and name the source that caught it. Over time this tells us which sources to add; `audit.md` reports the miss rate each week.

### 2.4 Triage and classification

- Classify each cluster: `legal`, `finance`, `both`, `frontier` (model and lab launches, benchmarks, enterprise-AI signals relevant to both audiences).
- Importance rubric (0-5), in `references/rubric.md`: frontier model or major product GA; a lab's legal or finance vertical move; AmLaw 100 / Magic Circle or G-SIB / top-20 asset manager deployment with numbers; funding ≥ $50M or acquisition; regulation, enforcement, court ruling, or bar guidance; benchmark leaderboard change on a legal/finance index; credible survey with new numbers. Lower: vendor feature updates, opinion pieces, event promotion.
- Anything scored ≥3 gets its primary source fetched (press release, filing, blog post, ruling) before writing. No item is written from a secondary headline alone.

### 2.5 Writing

Template per newsletter (from `research/style-exemplars.md`), target 1,500-2,500 words:

1. Subject line (≤10 words, biggest fact + number)
2. The week in one paragraph (≤80 words, bold first sentence)
3. Three takeaways (decisions, each with a verb aimed at the reader)
4. Big stories (2-4 × 200-300 words): bold headline → what happened, dated and attributed → **Why it matters** (≤60 words) → **Our read** (confidence stated) → **Source**
5. Frontier models and labs (shared block, written once, trimmed per vertical)
6. Deals and launches (one-liners: actor, action, number, source)
7. Regulation and policy (each tagged law / proposal / guidance / enforcement, with dates)
8. People and moves
9. What to watch (dated, checkable)
10. Sources (numbered primary documents)

Slow-week and busy-week rules are in the style reference. House rules: sentences ≤25 words, active voice, no hype words, hedge once and precisely, numbers as comparisons, confirmed vs reported vs rumoured marked by verb, Google's own launches held to the same scrutiny as everyone else's.

### 2.6 Editor pass

A second agent reviews each draft against a checklist: every number traces to a fetched source in this run; every big story has all five parts; no item repeats a prior week unless there is new information; takeaways are decisions not summaries; word count in range; style rules. It writes `audit.md`: sources checked, failures, recall-audit misses, items cut and why.

## 3. Repository layout

```
.claude/skills/ai-weekly-brief/
  SKILL.md                 orchestration: the steps above, in order, with stop conditions
  references/sources.yaml  feeds, pages, queries, watchlist entities, handles (machine-readable)
  references/style.md      house style, template, checklists, before/after examples
  references/rubric.md     classification, importance scoring, confidence labels
  scripts/sweep.py         deterministic collector → candidates.jsonl + sweep-log.md
  scripts/social.py        Bluesky + X provider adapters (official / twitterapi.io)
  scripts/dedupe.py        canonical URLs, clustering, seen-state update
newsletter/
  research/                the verified source maps and style research (done)
  issues/YYYY-Www/         legal.md, finance.md, candidates.jsonl, audit.md
  state/                   seen.jsonl, snapshots/, since_ids.json
```

## 4. Schedule and delivery

- Scheduled task on this account, fresh cloud session each week, prompt `/ai-weekly-brief`. Proposed time: Sunday 18:00 Pacific, so the run catches Friday's legal wraps, Thursday's Zvi, and Sunday's Fintech Brainfood, and the brief is ready for Monday morning in London and California. Alternative: Friday 15:00 Pacific if you want it before the weekend and accept missing Brainfood.
- Output committed to the repo on a `weekly/YYYY-Www` branch or straight to main (your call). Optional: also publish each issue as a Google Doc via the Drive connector, or as a claude.ai artifact, for forwarding.
- Cost: a thorough run (sweep, ~30 searches, ~20 primary-source fetches, two drafts, editor pass) will likely cost several dollars of usage per week. One of your existing scheduled tasks mentions a $5/day cap; the weekly run should be sized to fit, or the cap raised for that session.

## 5. Build order

1. **Sources and sweep (first).** Write `sources.yaml` from the research files, build `sweep.py`, run it for this week, inspect `candidates.jsonl` and `sweep-log.md`. Check recall against this week's Legal AI Weekly, The Redline, Brainfood, and AI News by hand.
2. **Style and rubric.** Write `style.md` and `rubric.md`; produce a first issue of both newsletters for the week of Oct 23-29 so we can edit the voice on real material.
3. **SKILL.md and editor pass.** Encode the full procedure, run it end to end once manually, fix what breaks.
4. **X provider and schedule.** Add the chosen X key as an environment secret, create the scheduled task, run two or three weeks and track the recall-audit miss rate before trusting it.

## 6. Decisions needed from you

1. **X budget.** (a) Free: Bluesky mirrors for lab accounts only. (b) ~$3/month: twitterapi.io on a private X List (scraped upstream, could vanish). (c) ~$50/month: official X API pay-per-use (ToS-clean). My recommendation: start with (a) now, add (c) once the rest works, since researcher and commentator chatter is where X adds the most and (a) misses most of it.
2. **Delivery.** Markdown in the repo only, or also Google Doc and/or an artifact link each week.
3. **Run time.** Sunday evening Pacific (recommended) or Friday afternoon.
4. **Scope edges.** Insurance and accounting/audit under finance? Include UK/EU/Asia regulators at parity with US? Treat frontier launches as a shared block in both issues (recommended) or a third newsletter?
5. **Paywalled outlets.** Bloomberg, FT, WSJ, The Information, Law.com and American Banker cannot be fetched from the sandbox. The plan reaches them through search snippets and the aggregators that cite them. If you have logins and want full text, that needs a separate route (Remote Control from your machine, or a reader service).
6. **Watchlist.** I will seed the entity list (labs, vendors, firms, banks, regulators) from the research; tell me names you specifically want tracked and anyone to exclude.
