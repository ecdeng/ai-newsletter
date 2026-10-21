# Case engine — point-in-time layer

Working prototype of the data foundation for INF-1 (see `SPEC.md`, and
`../BLUEPRINT.md` for the exercises it serves).

**Status:** the point-in-time layer is built and tested against live SEC data —
13/13 smoke tests passing as of 21 Oct 2026. Layers 3 and 4 (runtime clock,
grading) are specified in `SPEC.md` but not built.

## Quickstart

```bash
# The SEC requires an EMAIL-STYLE User-Agent. A URL alone returns HTTP 403.
export SEC_CONTACT="Your Organisation you@yourdomain.com"
export PIT_CACHE=.pit-cache

python3 test_pit.py
```

Expect `13 passed, 0 failed`. The first run hits the SEC API (polite, 8 req/s,
under the stated 10/s ceiling); afterwards everything is served from the cache,
so runs are offline and reproducible.

## What's here

| File | Purpose |
|---|---|
| `pit/client.py` | SEC XBRL client with as-of filtering, restatement detection and rate limiting |
| `pit/comps.py` | Point-in-time comp sets, annual-duration filtering, and `leak_report()` for authoring safety |
| `pit/case.py` | `CaseManifest` schema, `facts_from_sec()`, and `validate_pit_safety()` |
| `test_pit.py` | Live smoke tests |
| `SPEC.md` | The full specification, including five worked example cases |

## The thirty-second version of why this matters

Envista Holdings reported FY2019 revenue of **$2.7516bn** in its 2020 and 2021
10-Ks, then **$2.2848bn** in its 2022 10-K — a 17% restatement, almost
certainly a discontinued-operations reclassification.

An analyst on 30 June 2021 saw $2.75bn. A current database shows $2.28bn. A
case built from current data would hand a student a revenue base the market
never saw, and every growth rate, margin and multiple derived from it would be
wrong.

The SEC stamps every reported fact with the filing date it came from, so this
is fixable for free — and `validate_pit_safety()` fails the build if you get it
wrong:

```
MISMATCH: Revenues 2019-12-31 manifest says 2,284,800,000 but accn
0001628280-20-001914 reports 2,751,600,000. This is the signature of a value
copied from a CURRENT database rather than from the as-filed document.
```

## Two access gotchas

1. **`SEC_CONTACT` must contain an email address.** A descriptive User-Agent
   carrying only a project URL is rejected with HTTP 403. Verified both ways.
2. **`data.sec.gov` and `www.sec.gov` are different hosts.** The XBRL APIs are
   on `data.sec.gov`; the actual filing documents are on
   `www.sec.gov/Archives/`. In a restricted network you may reach one and not
   the other, which means all the numbers and none of the documents. Check both
   before scoping.
