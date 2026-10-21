"""
Parse BLUEPRINT.md and case-engine/SPEC.md into structured data.

The markdown is written to a consistent shape, so parsing is reliable rather
than heuristic. Verified against the source: 15 modules, 58 exercises, 7
infrastructure items, 7 parts. The parser asserts those counts so a future
edit to the markdown that breaks the shape fails the build loudly instead of
silently dropping content.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field, asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BLUEPRINT = ROOT / "BLUEPRINT.md"
SPEC = ROOT / "case-engine" / "SPEC.md"

# Expected counts — the parser's own smoke test.
EXPECT = {"modules": 15, "exercises": 58, "infra": 7, "parts": 7}


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class Exercise:
    eid: str                 # "M07-E1"
    module: str              # "M07"
    module_num: int
    name: str
    flagship: bool
    topics: str = ""
    objective: str = ""
    task: str = ""
    tools: str = ""
    rubric_md: str = ""
    difficulty: str = ""
    difficulty_tier: int = 0     # 1 beginner .. 3 advanced, for sorting
    build: str = ""
    build_tier: int = 0
    example_md: str = ""
    time_limit: str = ""
    grading_tags: list[str] = field(default_factory=list)
    body_md: str = ""            # the whole block, for the detail view


@dataclass
class Module:
    mid: str                 # "M07"
    num: int
    title: str               # "Analyze a Business"
    coverage_md: str
    exercises: list[Exercise] = field(default_factory=list)


@dataclass
class Infra:
    iid: str                 # "INF-1"
    name: str
    tagline: str
    body_md: str
    build: str = ""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _field(block: str, label: str) -> str:
    """
    Pull a '**Label.** text' field. Matches on prefix so label variants
    ('Grading rubric — two separate instruments...') still resolve.
    """
    pat = re.compile(
        r"\*\*" + re.escape(label) + r"[^*]*\*\*\s*(.*?)(?=\n\n\*\*|\n\n###|\n\n---|\Z)",
        re.S,
    )
    m = pat.search(block)
    return m.group(1).strip() if m else ""


_DIFF_TIERS = [
    (re.compile(r"intermediate\s*[–-]\s*advanced", re.I), 3, "Intermediate–Advanced"),
    (re.compile(r"beginner\s*[–-]\s*intermediate", re.I), 1, "Beginner–Intermediate"),
    (re.compile(r"advanced", re.I), 3, "Advanced"),
    (re.compile(r"intermediate", re.I), 2, "Intermediate"),
    (re.compile(r"beginner", re.I), 1, "Beginner"),
]

_BUILD_TIERS = [
    (re.compile(r"medium\s*[–-]\s*high", re.I), 3, "Medium–High"),
    (re.compile(r"low\s*[–-]\s*medium", re.I), 1, "Low–Medium"),
    (re.compile(r"high", re.I), 3, "High"),
    (re.compile(r"medium", re.I), 2, "Medium"),
    (re.compile(r"low", re.I), 1, "Low"),
]


def _classify(text: str, table) -> tuple[str, int]:
    for pat, tier, label in table:
        if pat.search(text):
            return label, tier
    return "", 0


def _grading_tags(rubric: str) -> list[str]:
    tags = []
    low = rubric.lower()
    if "fully auto" in low:
        tags.append("Fully auto-gradeable")
    elif "semi-auto" in low:
        tags.append("Semi-automatic")
    elif "auto" in low:
        tags.append("Auto-graded component")
    if "llm" in low:
        tags.append("LLM-graded")
    if re.search(r"\bhuman\b", low):
        tags.append("Human marking")
    if "checklist" in low:
        tags.append("Checklist")
    if "global rating" in low:
        tags.append("Global ratings")
    if "critical" in low and "failure" in low:
        tags.append("Critical-failure marker")
    if "perturbation" in low:
        tags.append("Perturbation test")
    return tags


_TIME = re.compile(r"\*\*(\d+(?:\s*[–-]\s*\d+)?)\s*(minutes|hours|min)\b", re.I)


def _time_limit(task: str) -> str:
    m = _TIME.search(task)
    if m:
        return f"{m.group(1)} {m.group(2).lower().replace('min','minutes') if m.group(2).lower()=='min' else m.group(2).lower()}"
    for pat, label in ((r"two weeks", "two weeks"), (r"three sittings", "3 sittings"),
                       (r"7 minutes per run", "7 min × 3")):
        if re.search(pat, task, re.I):
            return label
    return ""


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

def parse_blueprint() -> dict:
    src = BLUEPRINT.read_text(encoding="utf-8")

    # Top-level parts
    part_chunks = re.split(r"\n(?=# Part \d)", src)
    front = part_chunks[0]
    parts: dict[str, str] = {}
    for chunk in part_chunks[1:]:
        head = chunk.split("\n", 1)[0]
        num = re.search(r"# Part (\d)", head).group(1)
        parts[num] = chunk

    # Modules live inside Part 3
    p3 = parts["3"]
    mod_chunks = re.split(r"\n(?=## Module \d\d )", p3)
    modules: list[Module] = []
    for chunk in mod_chunks[1:]:
        head = chunk.split("\n", 1)[0]
        m = re.match(r"## Module (\d\d) — (.+)", head)
        num, title = int(m.group(1)), m.group(2).strip()
        mid = f"M{num:02d}"

        ex_split = re.split(r"\n(?=### M\d\d-E\d)", chunk)
        coverage = ex_split[0]
        # strip the module heading line from coverage
        coverage = coverage.split("\n", 1)[1].strip() if "\n" in coverage else ""
        # drop a trailing '---' separator
        coverage = re.sub(r"\n---\s*$", "", coverage).strip()
        # the page template supplies its own "Expected content coverage" heading,
        # so strip the markdown's duplicate
        coverage = re.sub(r"^###\s*Expected content coverage\s*\n+", "", coverage).strip()

        exercises: list[Exercise] = []
        for ex_block in ex_split[1:]:
            ex_head = ex_block.split("\n", 1)[0]
            em = re.match(r"### (M\d\d-E\d+) — (.+)", ex_head)
            if not em:
                continue
            eid = em.group(1)
            raw_name = em.group(2).strip()
            flagship = bool(re.search(r"\*\(.*flagship.*\)\*|terminal assessment", raw_name, re.I))
            name = re.sub(r"\s*\*\(.*?\)\*\s*$", "", raw_name).strip()
            name = name.replace("*", "").strip()

            body = ex_block.split("\n", 1)[1] if "\n" in ex_block else ""
            body = re.sub(r"\n---\s*$", "", body).strip()

            diff_raw = _field(body, "Difficulty")
            # difficulty and build share one line
            build_raw = ""
            bm = re.search(r"\*\*Build complexity\.?\*\*\s*(.*?)(?=\n\n|\Z)", body, re.S)
            if bm:
                build_raw = bm.group(1).strip()
            diff_only = re.split(r"\*\*Build complexity", diff_raw)[0]

            d_label, d_tier = _classify(diff_only, _DIFF_TIERS)
            b_label, b_tier = _classify(build_raw, _BUILD_TIERS)
            rubric = _field(body, "Grading rubric")
            task = _field(body, "Student task")

            exercises.append(Exercise(
                eid=eid, module=mid, module_num=num, name=name, flagship=flagship,
                topics=_field(body, "Topics:").rstrip("."),
                objective=_field(body, "Learning objective"),
                task=task,
                tools=_field(body, "Tools and environment"),
                rubric_md=rubric,
                difficulty=d_label, difficulty_tier=d_tier,
                build=b_label, build_tier=b_tier,
                example_md=(_field(body, "Example and worked answer")
                            or _field(body, "Example and model answer")
                            or _field(body, "Example task prompt")
                            or _field(body, "Example")),
                time_limit=_time_limit(task),
                grading_tags=_grading_tags(rubric),
                body_md=body,
            ))

        modules.append(Module(mid=mid, num=num, title=title,
                              coverage_md=coverage, exercises=exercises))

    # Intensives table (inside Part 3, after Module 15)
    ti_m = re.search(r"## Topical Intensives \(TI1[^\n]*\n(.*?)$", p3, re.S)
    intensives_md = ti_m.group(1).strip() if ti_m else ""

    # Infrastructure (Part 4)
    p4 = parts["4"]
    infra: list[Infra] = []
    for chunk in re.split(r"\n(?=## INF-\d)", p4)[1:]:
        head = chunk.split("\n", 1)[0]
        im = re.match(r"## (INF-\d) — (.+)", head)
        iid = im.group(1)
        raw = im.group(2).strip()
        tagline = ""
        tm = re.search(r"\*\((.*?)\)\*", raw)
        if tm:
            tagline = tm.group(1)
        name = re.sub(r"\s*\*\(.*?\)\*\s*$", "", raw).replace("*", "").strip()
        body = chunk.split("\n", 1)[1].strip()
        bc = re.search(r"\*\*Build complexity:?\s*(.*?)\*\*", body)
        infra.append(Infra(iid=iid, name=name, tagline=tagline, body_md=body,
                           build=(bc.group(1).strip().rstrip('.') if bc else "")))

    # "What NOT to build" sits at the end of Part 4
    notbuild_m = re.search(r"## What NOT to build\n(.*?)$", p4, re.S)

    data = {
        "front_md": front,
        "exec_md": parts["1"],
        "architecture_md": parts["2"],
        "modules": [asdict(m) for m in modules],
        "intensives_md": intensives_md,
        "infra": [asdict(i) for i in infra],
        "not_build_md": notbuild_m.group(1).strip() if notbuild_m else "",
        "roadmap_md": parts["5"],
        "sources_md": parts["6"],
        "verification_md": parts["7"],
    }

    # Assertions: fail loudly rather than silently dropping content.
    got = {
        "modules": len(modules),
        "exercises": sum(len(m.exercises) for m in modules),
        "infra": len(infra),
        "parts": len(parts),
    }
    for key, want in EXPECT.items():
        assert got[key] == want, f"parser expected {want} {key}, found {got[key]}"
    for m in modules:
        assert m.coverage_md, f"{m.mid} has no coverage block"
        for e in m.exercises:
            assert e.objective, f"{e.eid} missing learning objective"
            assert e.difficulty, f"{e.eid} missing difficulty"
            assert e.build, f"{e.eid} missing build complexity"
    return data


def parse_spec() -> dict:
    src = SPEC.read_text(encoding="utf-8")
    header, _, rest = src.partition("\n---\n")
    sections = []
    for chunk in re.split(r"\n(?=## \d+\. )", rest):
        head = chunk.split("\n", 1)[0]
        m = re.match(r"## (\d+)\. (.+)", head)
        if not m:
            continue
        body = chunk.split("\n", 1)[1].strip() if "\n" in chunk else ""
        sections.append({"num": m.group(1), "title": m.group(2).strip(), "body_md": body})

    # Example cases live in section 9 as '### Case X — "Title"'
    cases = []
    sec9 = next((s for s in sections if s["num"] == "9"), None)
    if sec9:
        for chunk in re.split(r"\n(?=### Case [A-E] )", sec9["body_md"])[1:]:
            head = chunk.split("\n", 1)[0]
            cm = re.match(r'### Case ([A-E]) — [“"](.+?)[”"]', head)
            if not cm:
                continue
            body = chunk.split("\n", 1)[1].strip()
            serves = _field(body, "Serves:").rstrip(".")
            cases.append({
                "letter": cm.group(1), "title": cm.group(2),
                "serves": serves,
                "situation": _field(body, "Situation type:").rstrip("."),
                "data": _field(body, "Data:").rstrip("."),
                "body_md": body,
            })
        assert len(cases) == 5, f"expected 5 example cases, found {len(cases)}"
    return {"header_md": header, "sections": sections, "cases": cases}


if __name__ == "__main__":
    bp = parse_blueprint()
    sp = parse_spec()
    print(f"modules      {len(bp['modules'])}")
    print(f"exercises    {sum(len(m['exercises']) for m in bp['modules'])}")
    print(f"infra items  {len(bp['infra'])}")
    print(f"spec sections {len(sp['sections'])}  example cases {len(sp['cases'])}")
    flag = [e['eid'] for m in bp['modules'] for e in m['exercises'] if e['flagship']]
    print(f"flagship     {len(flag)}: {', '.join(flag)}")
    from collections import Counter
    print("difficulty  ", dict(Counter(e['difficulty'] for m in bp['modules'] for e in m['exercises'])))
    print("build       ", dict(Counter(e['build'] for m in bp['modules'] for e in m['exercises'])))
