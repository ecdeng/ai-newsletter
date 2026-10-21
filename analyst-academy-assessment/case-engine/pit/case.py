"""
Case manifests and the point-in-time safety validator.

A case is a frozen date T plus everything an analyst could have known at T,
plus the deliverables, plus the answer key, plus the resolution data revealed
later. The manifest is JSON so cases are reviewable, diffable and portable.

The most important thing in this module is `validate_pit_safety`. Authoring a
case by hand WILL leak future information — it is the single most likely way to
ruin a case, and it is silent. So leakage is checked mechanically against the
SEC's own filing dates rather than left to the author's discipline.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import date
from pathlib import Path
from typing import Any

from . import client as c


@dataclass
class ServedFact:
    """A financial fact served to the student, with its provenance."""
    tag: str
    period_start: str | None
    period_end: str
    value: float
    filed: str          # the SEC filing date this value came from
    accn: str           # accession number — the audit trail
    form: str


@dataclass
class CalibrationQuestion:
    """A resolvable forecast question. Resolution is held back from the student."""
    qid: str
    text: str
    kind: str                      # "binary" | "categorical"
    options: list[str] = field(default_factory=lambda: ["yes", "no"])
    resolves_on: str = ""
    resolution: str | None = None  # withheld at serve time
    resolution_source: str = ""


@dataclass
class Deliverable:
    did: str
    name: str
    due_at_step: int
    time_limit_minutes: int
    artifact: str                  # "memo" | "workbook" | "numeric" | "recording"
    max_words: int | None = None


@dataclass
class Trap:
    """A planted item. Each is scored independently so partial credit works."""
    tid: str
    description: str
    detect: str                    # how the grader detects it
    points: int


@dataclass
class CaseManifest:
    case_id: str
    title: str
    entity_name: str
    cik: int
    freeze_date: str               # T
    reveal_steps: list[dict[str, Any]]
    served_facts: list[ServedFact]
    served_filings: list[dict[str, str]]
    curated_consensus: dict[str, Any]
    deliverables: list[Deliverable]
    traps: list[Trap]
    check_cells: dict[str, dict[str, float]]
    calibration: list[CalibrationQuestion]
    notes: str = ""

    def to_json(self, path: str | Path) -> None:
        Path(path).write_text(json.dumps(asdict(self), indent=2))

    def student_view(self) -> dict[str, Any]:
        """What the student receives: no key, no traps, no resolutions."""
        d = asdict(self)
        d.pop("traps", None)
        d.pop("check_cells", None)
        for q in d.get("calibration", []):
            q.pop("resolution", None)
            q.pop("resolution_source", None)
        # reveal steps beyond the first are withheld until the clock advances
        d["reveal_steps"] = d["reveal_steps"][:1]
        return d


# ---------------------------------------------------------------------------
# The validator that matters
# ---------------------------------------------------------------------------

class PITLeak(Exception):
    pass


def validate_pit_safety(manifest: CaseManifest, *, strict: bool = True) -> list[str]:
    """
    Assert that nothing served to the student was filed after the freeze date.

    Checks, in order of how likely each is to bite:
      1. Every served fact's `filed` date is <= freeze_date.
      2. Every served fact actually exists in the SEC record with that value
         AND that filing date (catches transcription errors and silently
         restated figures pasted from a current database).
      3. Every served filing was filed on or before T.
      4. No calibration question resolves on or before T (that would make it
         answerable from information already served).

    Returns a list of problem strings. Raises on the first problem when strict.
    """
    problems: list[str] = []
    T = manifest.freeze_date

    def fail(msg: str) -> None:
        problems.append(msg)
        if strict:
            raise PITLeak(msg)

    # 1 + 2: served facts
    by_tag: dict[str, dict] = {}
    for sf in manifest.served_facts:
        if sf.filed > T:
            fail(
                f"LEAK: fact {sf.tag} {sf.period_start}..{sf.period_end} was filed "
                f"{sf.filed}, after the freeze date {T}."
            )
        if sf.tag not in by_tag:
            by_tag[sf.tag] = c.company_concept(manifest.cik, sf.tag)
        rows = by_tag[sf.tag].get("units", {}).get("USD", [])
        match = [
            r for r in rows
            if r.get("start") == sf.period_start
            and r["end"] == sf.period_end
            and r["accn"] == sf.accn
        ]
        if not match:
            fail(
                f"UNVERIFIED: {sf.tag} {sf.period_start}..{sf.period_end} accn "
                f"{sf.accn} not found in the SEC record."
            )
        elif abs(float(match[0]["val"]) - float(sf.value)) > 1.0:
            fail(
                f"MISMATCH: {sf.tag} {sf.period_end} manifest says {sf.value:,.0f} "
                f"but accn {sf.accn} reports {match[0]['val']:,.0f}. This is the "
                f"signature of a value copied from a CURRENT database rather than "
                f"from the as-filed document."
            )

    # 3: served filings
    for f in manifest.served_filings:
        fd = f.get("filingDate", "")
        if fd and fd > T:
            fail(f"LEAK: filing {f.get('form')} {f.get('accessionNumber')} filed {fd} > {T}.")

    # 4: calibration questions must resolve in the future
    for q in manifest.calibration:
        if q.resolves_on and q.resolves_on <= T:
            fail(
                f"DEGENERATE: calibration question {q.qid} resolves {q.resolves_on}, "
                f"on or before the freeze date {T} — it is already knowable."
            )

    return problems


def facts_from_sec(
    cik: int | str,
    tags: list[str],
    cutoff: str | date,
    *,
    min_days: int = 300,
) -> list[ServedFact]:
    """
    Build served facts directly from the SEC record at `cutoff`.

    Authoring cases this way rather than by hand makes a point-in-time leak
    close to impossible, because the filing date travels with the value.
    """
    cut = cutoff.isoformat() if isinstance(cutoff, date) else cutoff
    out: list[ServedFact] = []
    for tag in tags:
        try:
            concept = c.company_concept(cik, tag)
        except RuntimeError:
            continue
        for (start, end), row in c.latest_as_of(concept, cut).items():
            if start is None:
                continue
            span = (date.fromisoformat(end) - date.fromisoformat(start)).days
            if span < min_days:
                continue
            out.append(
                ServedFact(
                    tag=tag, period_start=start, period_end=end,
                    value=float(row["val"]), filed=row["filed"],
                    accn=row["accn"], form=row["form"],
                )
            )
    return sorted(out, key=lambda s: (s.tag, s.period_end))
