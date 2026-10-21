#!/usr/bin/env python3
"""
Live smoke tests for the point-in-time layer.

These hit the real SEC API, so they need network access and a contact address:

    export SEC_CONTACT="Your Org you@yourdomain.com"
    export PIT_CACHE=.pit-cache
    python3 test_pit.py

Every assertion below was verified passing on 2026-10-21 against live data.
Results are cached, so re-runs are offline and fast.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pit import case as k
from pit import client as c
from pit import comps

NVST = 1757073                      # Envista Holdings, the Danaher dental spin-off
FY19 = ("2019-01-01", "2019-12-31")

PASS, FAIL = 0, 0


def check(label: str, cond: bool, detail: str = "") -> None:
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"  PASS  {label}")
    else:
        FAIL += 1
        print(f"  FAIL  {label}  {detail}")


def main() -> int:
    print("=" * 74)
    print("Point-in-time layer — live smoke tests")
    print("=" * 74)

    rev = c.company_concept(NVST, "Revenues")
    check("companyconcept reachable", rev.get("entityName", "").startswith("ENVISTA"),
          rev.get("entityName", "<none>"))

    # The as-of filter must be monotonic in the cutoff date.
    n20 = len(c.as_of(rev, "2020-06-30"))
    n21 = len(c.as_of(rev, "2021-06-30"))
    n26 = len(c.as_of(rev, "2026-10-21"))
    check("as_of is monotonic in cutoff", n20 < n21 < n26, f"{n20}/{n21}/{n26}")

    # The headline point-in-time property: FY2019 revenue as seen in 2020 is
    # the ORIGINAL figure, not the later restated one.
    snap20 = c.latest_as_of(rev, "2020-06-30")
    check("FY2019 revenue as-filed at 2020-06-30 is 2.7516bn",
          abs(snap20[FY19]["val"] - 2_751_600_000) < 1e6,
          f"{snap20[FY19]['val']:,.0f}")

    snap26 = c.latest_as_of(rev, "2026-10-21")
    check("FY2019 revenue in the current record is 2.2848bn",
          abs(snap26[FY19]["val"] - 2_284_800_000) < 1e6,
          f"{snap26[FY19]['val']:,.0f}")

    # ...and therefore the leak is real and material.
    leak = (snap26[FY19]["val"] - snap20[FY19]["val"]) / snap20[FY19]["val"]
    check("the restatement leak on this tag exceeds 15%", abs(leak) > 0.15,
          f"{leak:+.1%}")

    rs = c.restatements(rev)
    check("restatement detector finds >= 2 restated periods", len(rs) >= 2, str(len(rs)))

    # Duration filtering: annual values only.
    ann = comps.pit_annual(NVST, "Revenues", "2020-06-30")
    check("pit_annual returns only annual periods at T", set(ann) == {
        "2017-12-31", "2018-12-31", "2019-12-31"}, str(sorted(ann)))

    # Filing history must respect the cutoff.
    fl = c.filings_before(NVST, "2020-06-30")
    check("no served filing is dated after T",
          all(f["filingDate"] <= "2020-06-30" for f in fl), "")

    # frames: useful for discovery, but NOT point-in-time safe on its own.
    fr = c.frame("Assets", "CY2019Q4I")
    check("frames returns a large cross-section", len(fr.get("data", [])) > 1000,
          str(len(fr.get("data", []))))
    check("frames rows carry NO 'filed' field (so frames is not PIT-safe alone)",
          "filed" not in fr["data"][0], str(sorted(fr["data"][0])))

    # The validator.
    facts = k.facts_from_sec(NVST, ["Revenues", "GrossProfit"], "2020-06-30")
    good = k.CaseManifest(
        case_id="smoke", title="smoke", entity_name="ENVISTA HOLDINGS CORPORATION",
        cik=NVST, freeze_date="2020-06-30", reveal_steps=[{"step": 1}],
        served_facts=facts, served_filings=c.filings_before(NVST, "2020-06-30")[:5],
        curated_consensus={}, deliverables=[], traps=[], check_cells={},
        calibration=[k.CalibrationQuestion("Q1", "x", "binary", resolves_on="2021-02-19")],
    )
    check("validator passes a correctly authored case",
          k.validate_pit_safety(good, strict=False) == [], "")

    bad = k.CaseManifest(**{**good.__dict__, "case_id": "bad"})
    bad.served_facts = [k.ServedFact(
        "Revenues", "2019-01-01", "2019-12-31", 2_284_800_000.0,
        "2020-02-21", "0001628280-20-001914", "10-K")]
    probs = k.validate_pit_safety(bad, strict=False)
    check("validator catches a current-database value pasted into a frozen case",
          any("MISMATCH" in p for p in probs), str(probs))

    bad2 = k.CaseManifest(**{**good.__dict__, "case_id": "bad2"})
    bad2.calibration = [k.CalibrationQuestion(
        "Q9", "already knowable", "binary", resolves_on="2020-01-01")]
    check("validator catches a question resolving before T",
          any("DEGENERATE" in p for p in k.validate_pit_safety(bad2, strict=False)), "")

    print("=" * 74)
    print(f"{PASS} passed, {FAIL} failed")
    return 1 if FAIL else 0


if __name__ == "__main__":
    raise SystemExit(main())
