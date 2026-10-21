#!/usr/bin/env python3
"""
Generate the static site from BLUEPRINT.md and case-engine/SPEC.md.

    pip install markdown
    python3 build.py          # writes ./public

Output is plain static HTML/CSS/JS with no runtime dependencies, which is why
`public/` is committed: Vercel then needs no build step at all. Re-run this
whenever the markdown changes.
"""

from __future__ import annotations

import html
import json
import re
import shutil
from pathlib import Path

import markdown

from parse import parse_blueprint, parse_spec

HERE = Path(__file__).resolve().parent
OUT = HERE / "public"
STATIC = HERE / "static"

SITE_TITLE = "Analyst Academy — Assessment Blueprint"
SITE_DESC = ("A research-backed assessment and exercise blueprint for Fundamental Edge's "
             "Analyst Academy: 58 specified exercises across 15 modules, with rubrics, "
             "shared infrastructure and a build roadmap.")

MD_EXT = ["tables", "fenced_code", "sane_lists", "attr_list", "md_in_html"]


# ---------------------------------------------------------------------------
# Markdown
# ---------------------------------------------------------------------------

def md(text: str) -> str:
    if not text:
        return ""
    return markdown.markdown(text, extensions=MD_EXT, output_format="html5")


def md_inline(text: str) -> str:
    """Render a short fragment without wrapping it in <p>."""
    out = md(text).strip()
    if out.startswith("<p>") and out.endswith("</p>") and out.count("<p>") == 1:
        out = out[3:-4]
    return out


def strip_md(text: str) -> str:
    """Plain text, for search indexes and meta descriptions."""
    t = re.sub(r"`{1,3}", "", text)
    t = re.sub(r"\*\*|\*|_", "", t)
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)
    t = re.sub(r"[#>|]", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def slug(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", strip_md(text).lower()).strip("-")
    return s[:60]


# ---------------------------------------------------------------------------
# Navigation
# ---------------------------------------------------------------------------

NAV = [
    ("Start", [
        ("index.html", "Overview", None),
        ("approach.html", "The approach", None),
    ]),
    ("The blueprint", [
        ("modules.html", "Modules", "15"),
        ("exercises.html", "Exercise catalogue", "58"),
        ("intensives.html", "Topical intensives", "9"),
    ]),
    ("Build", [
        ("infrastructure.html", "Shared infrastructure", "7"),
        ("case-engine.html", "Case engine spec", None),
        ("roadmap.html", "Build roadmap", None),
    ]),
    ("Appendix", [
        ("provenance.html", "Provenance & corrections", None),
        ("verification.html", "Verification queue", None),
        ("sources.html", "Sources", None),
    ]),
]


def nav_html(current: str, modules: list[dict], root: str = "") -> str:
    out = []
    for label, items in NAV:
        out.append(f'<div class="nav-group"><p class="nav-label">{label}</p><nav class="nav">')
        for href, text, badge in items:
            active = " active" if href == current else ""
            b = f'<span class="n">{badge}</span>' if badge else ""
            out.append(
                f'<a class="{active.strip()}" href="{root}{href}">{b}{html.escape(text)}</a>'
            )
            # expand the module list underneath when we are inside it
            if href == "modules.html" and current.startswith("modules/"):
                out.append('</nav><nav class="nav" style="margin:.2rem 0 .4rem .5rem">')
                for m in modules:
                    mh = f"modules/{m['mid'].lower()}.html"
                    a = " active" if mh == current else ""
                    out.append(
                        f'<a class="{a.strip()}" href="{root}{mh}">'
                        f'<span class="n">{m["num"]:02d}</span>{html.escape(m["title"])}</a>'
                    )
                out.append('</nav><nav class="nav">')
        out.append("</nav></div>")
    return "".join(out)


# ---------------------------------------------------------------------------
# Page shell
# ---------------------------------------------------------------------------

def page(path: str, title: str, body: str, modules: list[dict],
         desc: str = SITE_DESC, prev_next: tuple | None = None) -> None:
    depth = path.count("/")
    root = "../" * depth
    full_title = title if title == SITE_TITLE else f"{title} · Analyst Academy Blueprint"

    pn = ""
    if prev_next:
        prev, nxt = prev_next
        left = (f'<a href="{root}{prev[0]}"><span class="dir">← Previous</span>{html.escape(prev[1])}</a>'
                if prev else "<span></span>")
        right = (f'<a href="{root}{nxt[0]}" style="text-align:right"><span class="dir">Next →</span>{html.escape(nxt[1])}</a>'
                 if nxt else "<span></span>")
        pn = f'<div class="pagenav">{left}{right}</div>'

    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(full_title)}</title>
<meta name="description" content="{html.escape(desc[:300])}">
<meta name="color-scheme" content="light dark">
<meta property="og:title" content="{html.escape(full_title)}">
<meta property="og:description" content="{html.escape(desc[:300])}">
<meta property="og:type" content="website">
<link rel="stylesheet" href="{root}static/style.css">
<link rel="icon" href="{root}static/favicon.svg" type="image/svg+xml">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="topbar">
  <button class="iconbtn" data-nav-toggle aria-label="Open navigation">☰</button>
  <a class="brand" href="{root}index.html">Assessment Blueprint</a>
  <span class="spacer"></span>
  <button class="iconbtn" data-theme-toggle>☾</button>
</div>
<div class="shell">
  <aside class="sidebar">
    <a class="brand" href="{root}index.html">Assessment&nbsp;Blueprint</a>
    <p class="brand-sub">Fundamental Edge · Analyst Academy
      <button class="iconbtn" data-theme-toggle style="float:right;margin-top:-.3rem">☾</button>
    </p>
    {nav_html(path, modules, root)}
  </aside>
  <main class="main" id="main">
    <div class="wrap">
      {body}
      {pn}
      <footer class="site">
        <p>Assessment blueprint for the Fundamental Edge Analyst Academy syllabus.
        Every quantitative example was independently verified; see
        <a href="{root}provenance.html">provenance &amp; corrections</a> for what is
        sourced, what is unpublished, and what still needs checking.</p>
      </footer>
    </div>
  </main>
</div>
<script src="{root}static/app.js" defer></script>
</body>
</html>
"""
    target = OUT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(doc, encoding="utf-8")


# ---------------------------------------------------------------------------
# Shared fragments
# ---------------------------------------------------------------------------

TIER_CLASS = {1: "chip-t1", 2: "chip-t2", 3: "chip-t3"}


def ex_chips(e: dict, link_module: bool = False, root: str = "") -> str:
    bits = []
    if e["flagship"]:
        bits.append('<span class="chip chip-flag">★ Flagship</span>')
    if e["difficulty"]:
        bits.append(f'<span class="chip {TIER_CLASS.get(e["difficulty_tier"],"chip-neutral")}">'
                    f'{html.escape(e["difficulty"])}</span>')
    if e["build"]:
        bits.append(f'<span class="chip chip-neutral">Build: {html.escape(e["build"])}</span>')
    if e["time_limit"]:
        bits.append(f'<span class="chip chip-neutral">{html.escape(e["time_limit"])}</span>')
    for t in e["grading_tags"][:3]:
        bits.append(f'<span class="chip chip-accent">{html.escape(t)}</span>')
    return '<div class="exrow-meta">' + "".join(bits) + "</div>"


def field(label: str, body_md: str, inline: bool = False) -> str:
    if not body_md:
        return ""
    body = md_inline(body_md) if inline else md(body_md)
    return (f'<div class="field"><p class="field-label">{html.escape(label)}</p>'
            f'<div class="field-body">{body}</div></div>')


def disclose(label: str, body_md: str) -> str:
    if not body_md:
        return ""
    return (f'<details class="disclose"><summary>{html.escape(label)}</summary>'
            f'<div class="disclose-inner">{md(body_md)}</div></details>')


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------

def build_landing(bp: dict, sp: dict, modules: list[dict]) -> None:
    n_ex = sum(len(m["exercises"]) for m in modules)
    flagships = [e for m in modules for e in m["exercises"] if e["flagship"]]
    top5 = [e for e in flagships if e["eid"] in
            ("M13-E1", "M10-E1", "M14-E2", "M07-E1", "M09-E4")]
    # M14-E2 is not flagged flagship; pull it explicitly
    byid = {e["eid"]: e for m in modules for e in m["exercises"]}
    top5 = [byid[i] for i in ("M13-E1", "M10-E1", "M14-E2", "M07-E1", "M09-E4") if i in byid]

    cards = ""
    for e in top5:
        mnum = e["module_num"]
        cards += (
            f'<a class="card" href="modules/{e["module"].lower()}.html#{slug(e["eid"]+e["name"])}">'
            f'<p class="card-eyebrow">{e["eid"]} · Module {mnum:02d}</p>'
            f'<p class="card-title">{html.escape(e["name"])}</p>'
            f'<p class="card-body">{html.escape(strip_md(e["objective"])[:190])}…</p>'
            f'<div class="card-foot">{ex_chips(e)}</div></a>'
        )

    mod_cards = ""
    for m in modules[:6]:
        mod_cards += (
            f'<a class="card" href="modules/{m["mid"].lower()}.html">'
            f'<p class="card-eyebrow">Module {m["num"]:02d}</p>'
            f'<p class="card-title">{html.escape(m["title"])}</p>'
            f'<p class="card-body">{len(m["exercises"])} exercises</p></a>'
        )

    body = f"""
<div class="hero">
  <p class="eyebrow">Assessment &amp; exercise blueprint</p>
  <h1>How to test whether a buy-side analyst is actually getting better</h1>
  <p class="lede">A research-backed assessment design for Fundamental Edge's
  <strong>Analyst Academy</strong> — {n_ex} specified exercises across 15 modules and
  9 intensives, each with a rubric, a difficulty rating and a build-complexity
  estimate, plus the shared infrastructure to run them and a roadmap to build it.</p>
</div>

<div class="statgrid">
  <div class="stat"><div class="stat-n">{n_ex}</div><div class="stat-l">exercises specified, with rubrics</div></div>
  <div class="stat"><div class="stat-n">15</div><div class="stat-l">core modules covered</div></div>
  <div class="stat"><div class="stat-n">7</div><div class="stat-l">shared infrastructure proposals</div></div>
  <div class="stat"><div class="stat-n">5</div><div class="stat-l">worked example cases</div></div>
  <div class="stat"><div class="stat-n">13/13</div><div class="stat-l">data-layer tests passing on live SEC data</div></div>
</div>

<h2>The argument in one paragraph</h2>
<p><strong>Investing is a low-validity domain.</strong> Deliberate practice needs
well-defined tasks, immediate feedback, repetition and error correction — and stock
picking natively supplies none of them. Accumulated practice explains under 1% of
performance variance in the professions. And at an information ratio of 0.50,
establishing skill at 95% confidence takes <strong>15.37 years</strong>: longer than
the program, longer than most analyst tenures.</p>

<div class="callout">
<p class="callout-title">So the design conclusion is</p>
<p>The program <em>cannot</em> validly assess whether a student will make money. Any
assessment that tries is grading noise and teaching students to confuse outcomes with
decisions. What it <em>can</em> assess rigorously is <strong>process fidelity</strong>
and <strong>forecast calibration</strong> — and roughly 95% of the assessment volume
can be auto-graded at about 5% of the cost, concentrating human judgment on one
capstone artefact and its live defence.</p>
</div>

<p><a href="approach.html">Read the full approach →</a></p>

<h2>The five highest-value exercises</h2>
<p class="prose">Chosen for validity and discriminating power rather than coverage.
Each links into its module, where the full task, rubric and worked answer sit.</p>
<div class="cards cards-2">{cards}</div>
<p><a href="exercises.html">Browse and filter all {n_ex} exercises →</a></p>

<h2>On the market simulator</h2>
<p class="prose">The brief asked whether a full market simulator is worth building.
<strong>It is not</strong> — and the reason is instructive rather than budgetary.
Fundamental analysis runs on a quarters-to-years clock; a real-time trading simulator
optimises for execution and price feedback, and price feedback is the <em>least</em>
valid assessment signal available here. You would spend the most to measure the least.</p>
<p class="prose">Build a <strong>historical case engine</strong> instead: freeze a date,
serve only what was knowable then, advance the clock, force a post-mortem against the
student's own original thesis. Its value is not realism — it is
<strong>time compression plus free ground truth</strong>.</p>
<div class="cards cards-2">
  <a class="card" href="case-engine.html">
    <p class="card-eyebrow">INF-1 · Prototyped &amp; tested</p>
    <p class="card-title">Historical case engine</p>
    <p class="card-body">Full technical spec: architecture, data sourcing, the four
    look-ahead leaks and how each is closed, the case manifest, and five worked example
    cases. The point-in-time layer is built and tested against live SEC data.</p>
  </a>
  <a class="card" href="infrastructure.html">
    <p class="card-eyebrow">INF-1 … INF-7</p>
    <p class="card-title">All shared infrastructure</p>
    <p class="card-body">Seven pieces carry nearly every exercise, ordered by value per
    unit of build effort — plus an explicit list of what <em>not</em> to build.</p>
  </a>
</div>

<h2>Start reading</h2>
<div class="cards cards-3">{mod_cards}</div>
<p><a href="modules.html">All 15 modules →</a></p>

<div class="callout callout-warn">
<p class="callout-title">Before you quote a number from this</p>
<p>Research for this blueprint ran under two hard tool constraints: no source could be
opened as a document, and web-search budget was pooled across parallel research passes.
Every piece of arithmetic was independently verified — the mathematics is the most
trustworthy content here, the citations the least. Eleven of the course's own frameworks
are unpublished and only Fundamental Edge can supply them.
<a href="provenance.html">See provenance, corrections and research depth by module →</a></p>
</div>
"""
    page("index.html", SITE_TITLE, body, modules,
         desc=SITE_DESC)


def build_approach(bp: dict, modules: list[dict]) -> None:
    arch = bp["architecture_md"]
    arch = re.sub(r"^# Part 2 — The Assessment Architecture\s*", "", arch).strip()
    # build an in-page TOC from the h2s
    heads = re.findall(r"^## (.+)$", arch, re.M)
    toc = "".join(f'<li><a href="#{slug(h)}">{md_inline(h)}</a></li>' for h in heads)
    rendered = md(arch)
    for h in heads:
        rendered = rendered.replace(f"<h2>{md_inline(h)}</h2>",
                                    f'<h2 id="{slug(h)}">{md_inline(h)}</h2>', 1)
    body = f"""
<h1>The approach</h1>
<p class="lede">Why the exercises are shaped the way they are. Read this before the
module detail, or the rubrics will look arbitrary.</p>
<div class="toc"><p class="toc-title">On this page</p><ul>{toc}</ul></div>
<div class="prose">{rendered}</div>
"""
    page("approach.html", "The approach", body, modules,
         desc="The evidence base behind the assessment design: low-validity domains, "
              "calibration as the one honest outcome measure, OSCE station design, and "
              "what the assessment layer actually sells.",
         prev_next=(("index.html", "Overview"), ("modules.html", "Modules")))


def build_modules_index(bp: dict, modules: list[dict]) -> None:
    rows = ""
    for m in modules:
        exs = m["exercises"]
        flag = next((e for e in exs if e["flagship"]), None)
        adv = sum(1 for e in exs if e["difficulty_tier"] == 3)
        rows += (
            f'<a class="card" href="modules/{m["mid"].lower()}.html">'
            f'<p class="card-eyebrow">Module {m["num"]:02d} · {len(exs)} exercises</p>'
            f'<p class="card-title">{html.escape(m["title"])}</p>'
            + (f'<p class="card-body"><strong>★ {html.escape(flag["name"])}</strong></p>' if flag else "")
            + f'<div class="card-foot"><div class="chips">'
              f'<span class="chip chip-neutral">{adv} advanced</span>'
              f'</div></div></a>'
        )
    body = f"""
<h1>The 15 core modules</h1>
<p class="lede">The course's own structure and naming are preserved. Each module page
gives the expected content coverage — what a student should actually master, with
provenance flagged where the course's frameworks are unpublished — followed by its
exercises in full detail.</p>
<div class="cards cards-2">{rows}</div>
<h2>Also</h2>
<div class="cards cards-2">
<a class="card" href="intensives.html"><p class="card-eyebrow">TI1 … TI9</p>
<p class="card-title">Topical intensives</p>
<p class="card-body">Nine guest sessions whose content, length and instructors are
unknown — scope is inferred from titles, so this is the lowest-confidence material.
A thin assessment layer is recommended, not full modules.</p></a>
<a class="card" href="exercises.html"><p class="card-eyebrow">Cross-module</p>
<p class="card-title">Exercise catalogue</p>
<p class="card-body">All 58 exercises in one filterable view — by module, difficulty,
build complexity and grading method. The most useful view if you are deciding what to
build first.</p></a>
</div>
"""
    page("modules.html", "Modules", body, modules,
         desc="All 15 core modules of the Analyst Academy syllabus with expected content "
              "coverage and specified exercises.",
         prev_next=(("approach.html", "The approach"), ("exercises.html", "Exercise catalogue")))


def build_module_pages(bp: dict, modules: list[dict]) -> None:
    for i, m in enumerate(modules):
        prev = (f"modules/{modules[i-1]['mid'].lower()}.html",
                f"Module {modules[i-1]['num']:02d} — {modules[i-1]['title']}") if i else \
               ("modules.html", "All modules")
        nxt = (f"modules/{modules[i+1]['mid'].lower()}.html",
               f"Module {modules[i+1]['num']:02d} — {modules[i+1]['title']}") \
              if i + 1 < len(modules) else ("intensives.html", "Topical intensives")

        ex_toc = "".join(
            f'<li><a href="#{slug(e["eid"]+e["name"])}">'
            f'{"★ " if e["flagship"] else ""}{e["eid"]} — {html.escape(e["name"])}</a></li>'
            for e in m["exercises"])

        blocks = ""
        for e in m["exercises"]:
            anchor = slug(e["eid"] + e["name"])
            blocks += f"""
<section class="exercise" id="{anchor}">
  <h3>{"★ " if e["flagship"] else ""}{e["eid"]} — {html.escape(e["name"])}</h3>
  {ex_chips(e)}
  {field("Topics covered", e["topics"], inline=True)}
  {field("Learning objective", e["objective"])}
  {field("Student task", e["task"])}
  {field("Tools and environment", e["tools"])}
  {field("Grading rubric", e["rubric_md"])}
  {disclose("Example and worked answer", e["example_md"])}
</section>"""

        body = f"""
<p class="eyebrow">Module {m["num"]:02d}</p>
<h1>{html.escape(m["title"])}</h1>
<p class="lede">{len(m["exercises"])} exercises.
{sum(1 for e in m["exercises"] if e["difficulty_tier"]==3)} rated advanced.</p>

<div class="toc"><p class="toc-title">Exercises in this module</p><ul>{ex_toc}</ul></div>

<h2 id="coverage">Expected content coverage</h2>
<div class="prose">{md(m["coverage_md"])}</div>

<h2 id="exercises">Exercises</h2>
{blocks}
"""
        page(f"modules/{m['mid'].lower()}.html",
             f"Module {m['num']:02d} — {m['title']}", body, modules,
             desc=strip_md(m["coverage_md"])[:280],
             prev_next=(prev, nxt))


def build_exercise_catalogue(bp: dict, modules: list[dict]) -> None:
    all_ex = [e for m in modules for e in m["exercises"]]
    mod_opts = "".join(
        f'<option value="{m["mid"]}">{m["num"]:02d} — {html.escape(m["title"])}</option>'
        for m in modules)
    diffs = ["Beginner", "Beginner–Intermediate", "Intermediate",
             "Intermediate–Advanced", "Advanced"]
    builds = ["Low", "Low–Medium", "Medium", "Medium–High", "High"]
    grads = ["Fully auto-gradeable", "Auto-graded component", "Semi-automatic",
             "LLM-graded", "Human marking", "Checklist", "Global ratings",
             "Perturbation test", "Critical-failure marker"]

    rows = ""
    for e in sorted(all_ex, key=lambda x: (x["module_num"], x["eid"])):
        search = strip_md(" ".join([e["eid"], e["name"], e["topics"], e["objective"],
                                    e["task"], " ".join(e["grading_tags"])])).lower()
        rows += (
            f'<article class="exrow" data-module="{e["module"]}" '
            f'data-difficulty="{html.escape(e["difficulty"])}" '
            f'data-build="{html.escape(e["build"])}" '
            f'data-grading="{html.escape("|".join(e["grading_tags"]))}" '
            f'data-flagship="{"1" if e["flagship"] else "0"}" '
            f'data-search="{html.escape(search)}">'
            f'<div class="exrow-head">'
            f'<span class="exrow-id">{e["eid"]}</span>'
            f'<span class="exrow-name">{"★ " if e["flagship"] else ""}{html.escape(e["name"])}</span>'
            f'</div>'
            f'<p class="exrow-obj">{html.escape(strip_md(e["objective"])[:260])}</p>'
            f'{ex_chips(e)}'
            f'<p style="margin:.6rem 0 0;font-size:.82rem">'
            f'<a href="modules/{e["module"].lower()}.html#{slug(e["eid"]+e["name"])}">'
            f'Full task, rubric and worked answer →</a></p>'
            f'</article>'
        )

    body = f"""
<h1>Exercise catalogue</h1>
<p class="lede">All {len(all_ex)} exercises in one place. Filter by module, difficulty,
build complexity or grading method — useful if you are deciding what to build first, or
looking for everything that can be auto-graded.</p>

<div class="filters">
  <div class="fgroup"><span>Search</span>
    <input type="search" id="f-q" placeholder="e.g. guidance bridge, borrow, calibration"></div>
  <div class="fgroup"><span>Module</span>
    <select id="f-module"><option value="">All modules</option>{mod_opts}</select></div>
  <div class="fgroup"><span>Difficulty</span>
    <select id="f-difficulty"><option value="">Any</option>
    {"".join(f'<option>{d}</option>' for d in diffs)}</select></div>
  <div class="fgroup"><span>Build complexity</span>
    <select id="f-build"><option value="">Any</option>
    {"".join(f'<option>{b}</option>' for b in builds)}</select></div>
  <div class="fgroup"><span>Grading</span>
    <select id="f-grading"><option value="">Any</option>
    {"".join(f'<option>{g}</option>' for g in grads)}</select></div>
  <div class="fgroup"><span>&nbsp;</span>
    <label style="font-size:.85rem;display:flex;align-items:center;gap:.4rem;padding:.4rem 0">
      <input type="checkbox" id="f-flagship"> Flagship only</label></div>
  <div class="fgroup"><span>&nbsp;</span>
    <button class="btn-reset" id="f-reset" type="button">Reset</button></div>
  <p class="fcount" id="f-count">{len(all_ex)} exercises</p>
</div>

<div class="exlist" id="exlist">{rows}</div>
<p class="empty" id="f-empty" hidden>No exercises match those filters.</p>
"""
    page("exercises.html", "Exercise catalogue", body, modules,
         desc=f"All {len(all_ex)} specified exercises, filterable by module, difficulty, "
              "build complexity and grading method.",
         prev_next=(("modules.html", "Modules"), ("intensives.html", "Topical intensives")))


def build_intensives(bp: dict, modules: list[dict]) -> None:
    body = f"""
<h1>Topical intensives</h1>
<p class="lede">Nine recorded guest sessions. Their content, length and instructors are
unknown — all scope below is inferred from titles alone, which makes this the
lowest-confidence material in the blueprint. The recommendation is a thin assessment
layer (retrieval items plus one computational exercise each), not full modules.</p>
<div class="prose">{md(bp["intensives_md"])}</div>
"""
    page("intensives.html", "Topical intensives", body, modules,
         desc="The nine topical intensives, with a recommended thin assessment layer each.",
         prev_next=(("exercises.html", "Exercise catalogue"),
                    ("infrastructure.html", "Shared infrastructure")))


def build_infrastructure(bp: dict, modules: list[dict]) -> None:
    cards = ""
    for inf in bp["infra"]:
        cards += (
            f'<a class="card" href="#{inf["iid"].lower()}">'
            f'<p class="card-eyebrow">{inf["iid"]}'
            + (f' · {html.escape(inf["tagline"])}' if inf["tagline"] else "")
            + f'</p><p class="card-title">{html.escape(inf["name"])}</p>'
            + (f'<div class="card-foot"><span class="chip chip-neutral">'
               f'Build: {html.escape(inf["build"])}</span></div>' if inf["build"] else "")
            + "</a>")

    sections = ""
    for inf in bp["infra"]:
        extra = ""
        if inf["iid"] == "INF-1":
            extra = ('<p><a href="case-engine.html"><strong>Full technical spec for the '
                     'case engine, including five worked example cases →</strong></a></p>')
        sections += f"""
<section id="{inf["iid"].lower()}">
<h2>{inf["iid"]} — {html.escape(inf["name"])}
{f'<span class="chip chip-accent" style="vertical-align:middle;margin-left:.5rem">{html.escape(inf["tagline"])}</span>' if inf["tagline"] else ""}</h2>
<div class="prose">{md(inf["body_md"])}{extra}</div>
</section>"""

    body = f"""
<h1>Shared infrastructure</h1>
<p class="lede">Seven pieces of infrastructure carry almost every exercise in the
blueprint. They are ordered by value per unit of build effort — not by how interesting
they are to build.</p>
<div class="cards cards-2">{cards}</div>
{sections}
<hr>
<h2 id="not-build">What <em>not</em> to build</h2>
<div class="prose">{md(bp["not_build_md"])}</div>
"""
    page("infrastructure.html", "Shared infrastructure", body, modules,
         desc="Seven shared-infrastructure proposals ordered by value per unit of build "
              "effort, plus an explicit list of what not to build.",
         prev_next=(("intensives.html", "Topical intensives"),
                    ("case-engine.html", "Case engine spec")))


def build_case_engine(sp: dict, modules: list[dict]) -> None:
    case_cards = ""
    for c in sp["cases"]:
        free = "✅" in c["data"]
        case_cards += (
            f'<a class="card" href="#case-{c["letter"].lower()}">'
            f'<p class="card-eyebrow">Case {c["letter"]}</p>'
            f'<p class="card-title">{html.escape(c["title"])}</p>'
            f'<p class="card-body">{md_inline(c["situation"])}</p>'
            f'<div class="card-foot"><div class="chips">'
            f'<span class="chip {"chip-t1" if free else "chip-t2"}">'
            f'{"Free data" if free else "Needs paid data"}</span>'
            f'<span class="chip chip-neutral">{html.escape(strip_md(c["serves"])[:48])}</span>'
            f'</div></div></a>')

    secs = ""
    for s in sp["sections"]:
        if s["num"] == "9":
            # render example cases as anchored sections
            intro = re.split(r"\n(?=### Case [A-E] )", s["body_md"])[0]
            inner = f'<div class="prose">{md(intro)}</div><div class="cards cards-2">{case_cards}</div>'
            for c in sp["cases"]:
                inner += (f'<section id="case-{c["letter"].lower()}">'
                          f'<h3>Case {c["letter"]} — {html.escape(c["title"])}</h3>'
                          f'<div class="prose">{md(c["body_md"])}</div></section>')
            secs += (f'<section id="s{s["num"]}"><h2>{s["num"]}. '
                     f'{md_inline(s["title"])}</h2>{inner}</section>')
        else:
            secs += (f'<section id="s{s["num"]}"><h2>{s["num"]}. {md_inline(s["title"])}</h2>'
                     f'<div class="prose">{md(s["body_md"])}</div></section>')

    toc = "".join(f'<li><a href="#s{s["num"]}">{s["num"]}. {md_inline(s["title"])}</a></li>'
                  for s in sp["sections"])

    body = f"""
<p class="eyebrow">INF-1 · Technical specification</p>
<h1>The historical case engine</h1>
<p class="lede">A replay harness. Freeze a date, serve only what was knowable then, make
the student produce a thesis and a position, advance the clock, reveal what happened.
<strong>The value is not realism — it is time compression plus free ground truth.</strong></p>

<div class="callout">
<p class="callout-title">Status</p>
<p>The point-in-time data layer is a <strong>working prototype, tested against the live
SEC XBRL API</strong> — 13/13 smoke tests passing. Layers 3 and 4 (runtime clock,
grading integration) are specified but unbuilt. Code lives in
<code>case-engine/pit/</code> with tests in <code>case-engine/test_pit.py</code>.</p>
</div>

<div class="toc"><p class="toc-title">On this page</p><ul>{toc}</ul></div>
{secs}
"""
    page("case-engine.html", "Case engine spec", body, modules,
         desc="Technical specification for the historical case engine: architecture, data "
              "sourcing, point-in-time discipline, case manifest, and five worked example cases.",
         prev_next=(("infrastructure.html", "Shared infrastructure"),
                    ("roadmap.html", "Build roadmap")))


def build_simple(bp: dict, modules: list[dict], key: str, path: str, title: str,
                 lede: str, strip_head: str, desc: str, prev_next) -> None:
    text = re.sub(r"^#\s*" + re.escape(strip_head) + r"\s*", "", bp[key]).strip()
    heads = re.findall(r"^## (.+)$", text, re.M)
    rendered = md(text)
    for h in heads:
        rendered = rendered.replace(f"<h2>{md_inline(h)}</h2>",
                                    f'<h2 id="{slug(h)}">{md_inline(h)}</h2>', 1)
    toc = ("".join(f'<li><a href="#{slug(h)}">{md_inline(h)}</a></li>' for h in heads)
           if len(heads) > 2 else "")
    tochtml = (f'<div class="toc"><p class="toc-title">On this page</p><ul>{toc}</ul></div>'
               if toc else "")
    body = f"""
<h1>{html.escape(title)}</h1>
<p class="lede">{lede}</p>
{tochtml}
<div class="prose">{rendered}</div>
"""
    page(path, title, body, modules, desc=desc, prev_next=prev_next)


def build_provenance(bp: dict, modules: list[dict]) -> None:
    text = bp["front_md"]
    # drop the title block and the "how to read" section — both are site chrome now
    m = re.search(r"## Confidence and provenance.*", text, re.S)
    text = m.group(0) if m else text
    text = re.sub(r"^## Confidence and provenance[^\n]*\n", "", text).strip()
    heads = re.findall(r"^## (.+)$", text, re.M)
    rendered = md(text)
    for h in heads:
        rendered = rendered.replace(f"<h2>{md_inline(h)}</h2>",
                                    f'<h2 id="{slug(h)}">{md_inline(h)}</h2>', 1)
    body = f"""
<h1>Provenance &amp; corrections</h1>
<p class="lede">What is sourced, what is unpublished, and what was corrected along the
way. Read this before quoting any number from the blueprint.</p>
<div class="prose">{rendered}</div>
"""
    page("provenance.html", "Provenance & corrections", body, modules,
         desc="Research constraints, depth by module, and the corrections made during this "
              "work — including several where the widely-circulated version is wrong.",
         prev_next=(("roadmap.html", "Build roadmap"),
                    ("verification.html", "Verification queue")))


def write_static() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    dst = OUT / "static"
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(STATIC, dst)
    (dst / "favicon.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">'
        '<rect width="32" height="32" rx="7" fill="#1a5f59"/>'
        '<path d="M7 22V10m0 12h18M11 18l4-6 4 4 5-8" stroke="#fff" stroke-width="2.2" '
        'fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>',
        encoding="utf-8")


def main() -> None:
    bp = parse_blueprint()
    sp = parse_spec()
    modules = bp["modules"]

    if OUT.exists():
        shutil.rmtree(OUT)
    write_static()

    build_landing(bp, sp, modules)
    build_approach(bp, modules)
    build_modules_index(bp, modules)
    build_module_pages(bp, modules)
    build_exercise_catalogue(bp, modules)
    build_intensives(bp, modules)
    build_infrastructure(bp, modules)
    build_case_engine(sp, modules)
    build_simple(bp, modules, "roadmap_md", "roadmap.html", "Build roadmap",
                 "Sequenced by value to students per unit of effort. The ordering "
                 "principle: build the things that make other things gradable before "
                 "building the things that get graded.",
                 "Part 5 — Suggested Build Roadmap",
                 "A phased build roadmap, what to do if the budget is smaller than "
                 "assumed, and the three things not to compromise on.",
                 (("case-engine.html", "Case engine spec"),
                  ("provenance.html", "Provenance & corrections")))
    build_provenance(bp, modules)
    build_simple(bp, modules, "verification_md", "verification.html", "Verification queue",
                 "Everything that should be checked before it reaches a paying student, "
                 "ordered by value — plus the eleven things only Fundamental Edge can supply.",
                 "Part 7 — Verification Queue",
                 "A prioritised verification queue: blocking items, high-value fetches, "
                 "counsel review, and claims to strike.",
                 (("provenance.html", "Provenance & corrections"),
                  ("sources.html", "Sources")))
    build_simple(bp, modules, "sources_md", "sources.html", "Sources",
                 "Grouped by topic. None were opened as documents — see provenance — so "
                 "these are the canonical locations to verify each claim.",
                 "Part 6 — Sources, by topic",
                 "Sources grouped by module and topic.",
                 (("verification.html", "Verification queue"), None))

    # search/debug index
    (OUT / "exercises.json").write_text(json.dumps(
        [{k: e[k] for k in ("eid", "module", "name", "flagship", "difficulty",
                            "build", "grading_tags", "time_limit")}
         for m in modules for e in m["exercises"]], indent=2), encoding="utf-8")

    pages = sorted(p.relative_to(OUT).as_posix() for p in OUT.rglob("*.html"))
    print(f"wrote {len(pages)} pages to {OUT}")
    for p in pages:
        print("  ", p)


if __name__ == "__main__":
    main()
