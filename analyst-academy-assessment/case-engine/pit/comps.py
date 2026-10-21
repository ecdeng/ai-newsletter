"""
Point-in-time comp sets.

A correction worth knowing, established by testing the live API rather than
reading the docs: the `frames` endpoint returns a de-duplicated cross-section
whose rows carry only {cik, entityName, loc, end, val, accn} — there is NO
`filed` field. So a frame is NOT point-in-time safe on its own: you cannot tell
from the payload whether a given entity's value was filed before or after your
cutoff date, and SEC has already chosen which filing to surface.

Therefore the design rule:
    * use `frames` for DISCOVERY (who exists, rough scale, screening);
    * use `companyconcept` for VALUES, because it carries `filed` per fact.

A comp set is ~8-15 names, so the per-name cost is trivial. Resolving 6,000+
frame rows to filing dates would not be.
"""

from __future__ import annotations

from datetime import date
from typing import Iterable, Sequence

from . import client as c


def pit_series(
    cik: int | str,
    tag: str,
    cutoff: str | date,
    *,
    taxonomy: str = "us-gaap",
    unit: str = "USD",
) -> dict[tuple[str | None, str], dict]:
    """As-reported values per period for one company, as visible at `cutoff`."""
    concept = c.company_concept(cik, tag, taxonomy)
    return c.latest_as_of(concept, cutoff, unit)


def pit_annual(
    cik: int | str,
    tag: str,
    cutoff: str | date,
    *,
    taxonomy: str = "us-gaap",
    unit: str = "USD",
    min_days: int = 300,
) -> dict[str, float]:
    """
    Annual (≈365-day duration) as-reported values, keyed by period end date.

    `min_days` filters out quarterly and year-to-date durations that share the
    same tag. XBRL mixes durations under one tag, which is a standard trap.
    """
    out: dict[str, float] = {}
    for (start, end), row in pit_series(cik, tag, cutoff, taxonomy=taxonomy, unit=unit).items():
        if start is None:
            continue
        span = (date.fromisoformat(end) - date.fromisoformat(start)).days
        if span >= min_days:
            out[end] = float(row["val"])
    return dict(sorted(out.items()))


def build_comp_set(
    ciks: Sequence[int | str],
    tags: Iterable[str],
    cutoff: str | date,
) -> dict[str, dict[str, dict[str, float]]]:
    """
    A point-in-time comp table: {entity: {tag: {period_end: value}}}.

    Every value is as-reported at `cutoff`. Tags that a filer does not use are
    omitted rather than zero-filled, because tag coverage genuinely varies and
    silently zero-filling would corrupt a comp sheet.
    """
    table: dict[str, dict[str, dict[str, float]]] = {}
    for cik in ciks:
        name = None
        per_tag: dict[str, dict[str, float]] = {}
        for tag in tags:
            try:
                concept = c.company_concept(cik, tag)
            except RuntimeError:
                continue  # filer does not report this tag
            name = name or concept.get("entityName", str(cik))
            series = pit_annual(cik, tag, cutoff)
            if series:
                per_tag[tag] = series
        if name:
            table[name] = per_tag
    return table


def leak_report(
    cik: int | str,
    tag: str,
    analyst_date: str | date,
    today: str | date | None = None,
    *,
    unit: str = "USD",
) -> list[dict]:
    """
    Quantify the restatement leak for one tag: what an analyst saw at
    `analyst_date` versus what a current database shows.

    Use this when authoring a case to check whether building it from current
    data would have handed the student numbers the market never saw.
    """
    today = today or date.today().isoformat()
    concept = c.company_concept(cik, tag)
    then = c.latest_as_of(concept, analyst_date, unit)
    now = c.latest_as_of(concept, today, unit)
    rows = []
    for key, then_row in then.items():
        now_row = now.get(key)
        if not now_row or now_row["val"] == then_row["val"]:
            continue
        rows.append(
            {
                "start": key[0],
                "end": key[1],
                "as_seen": then_row["val"],
                "as_seen_filed": then_row["filed"],
                "today": now_row["val"],
                "today_filed": now_row["filed"],
                "delta": now_row["val"] - then_row["val"],
                "delta_pct": (now_row["val"] - then_row["val"]) / abs(then_row["val"]) * 100,
            }
        )
    return sorted(rows, key=lambda r: r["end"])
