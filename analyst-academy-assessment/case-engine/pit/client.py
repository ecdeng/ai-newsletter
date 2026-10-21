"""
Point-in-time client for the SEC XBRL "frames"/companyfacts APIs.

Why this module exists
----------------------
A case engine must serve ONLY what an analyst could have known on a frozen
date T. The SEC's XBRL API is uniquely suited to this because every reported
fact carries the accession number and the FILING DATE of the document it came
from. That means "what did the filings say as of T" is always reconstructible,
which closes the restatement look-ahead leak for free.

Verified against live SEC data on 2026-10-21: the companyconcept endpoint for
Envista (CIK 1757073) returns the SAME fiscal period (FY2018 revenue) from two
different filings, filed 2020-02-21 and 2021-02-19. That duplication is the
point-in-time signal, not noise.

SEC fair-access requirements (https://www.sec.gov/os/webmaster-faq#developers):
  * Declare a real User-Agent with contact information.
  * Stay at or below 10 requests/second.
Both are enforced here. SET YOUR OWN CONTACT in SEC_CONTACT before use; the
module refuses to run with the placeholder.
"""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path
from typing import Any, Iterable

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# REQUIRED: replace with your own organisation and contact address, or set the
# SEC_CONTACT environment variable. The SEC blocks unidentified traffic.
SEC_CONTACT = os.environ.get("SEC_CONTACT", "CHANGE-ME contact@example.com")

MAX_REQUESTS_PER_SECOND = 8          # under the SEC's stated 10/s ceiling
CACHE_DIR = Path(os.environ.get("PIT_CACHE", ".pit-cache"))

_DATA_HOST = "https://data.sec.gov"


class SECContactNotSet(RuntimeError):
    pass


class _RateLimiter:
    """Simple blocking rate limiter. Shared across all calls in a process."""

    def __init__(self, per_second: float) -> None:
        self._min_interval = 1.0 / per_second
        self._last = 0.0

    def wait(self) -> None:
        now = time.monotonic()
        gap = now - self._last
        if gap < self._min_interval:
            time.sleep(self._min_interval - gap)
        self._last = time.monotonic()


_limiter = _RateLimiter(MAX_REQUESTS_PER_SECOND)


def _check_contact() -> None:
    """
    The SEC requires an EMAIL-STYLE User-Agent. Verified empirically on
    2026-10-21: a descriptive User-Agent carrying only a project URL
    ("analyst-academy-case-engine (github.com/...)") is rejected with
    HTTP 403, while the same request with "Name email@domain" returns 200.
    So an "@" is not cosmetic here — it is the difference between working
    and not. Fail fast rather than letting a caller debug a 403.
    """
    if "CHANGE-ME" in SEC_CONTACT or "example.com" in SEC_CONTACT:
        raise SECContactNotSet(
            "Set SEC_CONTACT (or the SEC_CONTACT env var) to your own "
            "organisation and a reachable email address before calling the "
            "SEC API, e.g. 'Fundamental Edge data@yourdomain.com'."
        )
    if "@" not in SEC_CONTACT:
        raise SECContactNotSet(
            "SEC_CONTACT must contain an email address. A User-Agent carrying "
            "only a URL is rejected by the SEC with HTTP 403 (verified)."
        )


def cik10(cik: int | str) -> str:
    """Zero-pad a CIK to the 10 digits the XBRL endpoints require."""
    return f"{int(cik):010d}"


def _get_json(path: str, *, cache_key: str) -> dict[str, Any]:
    """GET a JSON document, with an on-disk cache so case builds are reproducible."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cached = CACHE_DIR / f"{cache_key}.json"
    if cached.exists():
        return json.loads(cached.read_text())

    _check_contact()
    _limiter.wait()
    req = urllib.request.Request(
        f"{_DATA_HOST}{path}",
        headers={
            "User-Agent": SEC_CONTACT,
            "Accept-Encoding": "gzip, deflate",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read()
            if resp.headers.get("Content-Encoding") == "gzip":
                import gzip
                raw = gzip.decompress(raw)
            payload = json.loads(raw)
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"SEC returned HTTP {exc.code} for {path}") from exc

    cached.write_text(json.dumps(payload))
    return payload


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def company_concept(cik: int | str, tag: str, taxonomy: str = "us-gaap") -> dict[str, Any]:
    """Every reported value of one concept, each stamped with its filing date."""
    c = cik10(cik)
    return _get_json(
        f"/api/xbrl/companyconcept/CIK{c}/{taxonomy}/{tag}.json",
        cache_key=f"concept_{c}_{taxonomy}_{tag}",
    )


def company_facts(cik: int | str) -> dict[str, Any]:
    """All facts for one company. Large (tens of MB for big filers)."""
    c = cik10(cik)
    return _get_json(f"/api/xbrl/companyfacts/CIK{c}.json", cache_key=f"facts_{c}")


def submissions(cik: int | str) -> dict[str, Any]:
    """Filing history, including filing dates and accession numbers."""
    c = cik10(cik)
    return _get_json(f"/submissions/CIK{c}.json", cache_key=f"subs_{c}")


def frame(tag: str, period: str, unit: str = "USD", taxonomy: str = "us-gaap") -> dict[str, Any]:
    """
    One fact per entity for one period — the cross-sectional endpoint.

    `period` looks like "CY2023Q1I" (instantaneous) or "CY2023Q1" (duration).
    Useful for building a point-in-time comp set rather than a single company.
    """
    return _get_json(
        f"/api/xbrl/frames/{taxonomy}/{tag}/{unit}/{period}.json",
        cache_key=f"frame_{taxonomy}_{tag}_{unit}_{period}",
    )


def as_of(
    concept: dict[str, Any],
    cutoff: str | date,
    unit: str = "USD",
) -> list[dict[str, Any]]:
    """
    Filter a companyconcept payload to facts an analyst could have seen on `cutoff`.

    This is the core point-in-time operation: drop every fact whose `filed`
    date is after the cutoff. What remains is the as-filed record at T.
    """
    cut = cutoff.isoformat() if isinstance(cutoff, date) else cutoff
    rows = concept.get("units", {}).get(unit, [])
    return [r for r in rows if r.get("filed") and r["filed"] <= cut]


def latest_as_of(
    concept: dict[str, Any],
    cutoff: str | date,
    unit: str = "USD",
) -> dict[tuple[str | None, str], dict[str, Any]]:
    """
    For each (start, end) period, the most recently FILED value as of `cutoff`.

    Keyed by period so you can see the as-reported figure for each fiscal
    period exactly as it stood at T — including a period that had already been
    restated by then.
    """
    out: dict[tuple[str | None, str], dict[str, Any]] = {}
    for r in as_of(concept, cutoff, unit):
        key = (r.get("start"), r["end"])
        prev = out.get(key)
        if prev is None or r["filed"] > prev["filed"]:
            out[key] = r
    return out


def restatements(
    concept: dict[str, Any],
    unit: str = "USD",
) -> list[dict[str, Any]]:
    """
    Periods reported more than once with DIFFERENT values — i.e. restated.

    This is the leak a naive database silently introduces: today's value for a
    2018 period is not what the 2018 filing said. Use this to find cases where
    the restatement itself is the teaching point, and to assert in tests that
    your engine is serving as-filed rather than as-restated numbers.
    """
    by_period: dict[tuple[str | None, str], list[dict[str, Any]]] = {}
    for r in concept.get("units", {}).get(unit, []):
        by_period.setdefault((r.get("start"), r["end"]), []).append(r)

    found = []
    for (start, end), rows in by_period.items():
        values = {r["val"] for r in rows}
        if len(values) > 1:
            found.append(
                {
                    "start": start,
                    "end": end,
                    "versions": sorted(
                        ({"filed": r["filed"], "val": r["val"], "form": r["form"],
                          "accn": r["accn"]} for r in rows),
                        key=lambda d: d["filed"],
                    ),
                }
            )
    return sorted(found, key=lambda d: d["end"])


def filings_before(cik: int | str, cutoff: str | date,
                   forms: Iterable[str] = ("10-K", "10-Q", "8-K")) -> list[dict[str, str]]:
    """The filings available to an analyst at T, newest first."""
    cut = cutoff.isoformat() if isinstance(cutoff, date) else cutoff
    recent = submissions(cik).get("filings", {}).get("recent", {})
    keys = ("form", "filingDate", "accessionNumber", "primaryDocument", "reportDate")
    rows = zip(*(recent.get(k, []) for k in keys))
    want = set(forms)
    out = [
        dict(zip(keys, row))
        for row in rows
        if row[0] in want and row[1] <= cut
    ]
    return sorted(out, key=lambda d: d["filingDate"], reverse=True)
