#!/usr/bin/env python3
"""Validate the generated site: leaked markdown, broken links, empty pages."""
import re, sys
from pathlib import Path
from html.parser import HTMLParser

OUT = Path(__file__).resolve().parent / "public"
problems = []

class Stripper(HTMLParser):
    def __init__(self):
        super().__init__(); self.text=[]; self.skip=0
    def handle_starttag(self,t,a):
        if t in ("script","style","pre","code"): self.skip+=1
    def handle_endtag(self,t):
        if t in ("script","style","pre","code"): self.skip=max(0,self.skip-1)
    def handle_data(self,d):
        if not self.skip: self.text.append(d)

pages = sorted(OUT.rglob("*.html"))
ids_by_page = {}
links = []

for p in pages:
    rel = p.relative_to(OUT).as_posix()
    src = p.read_text(encoding="utf-8")

    if "<h1" not in src: problems.append(f"{rel}: no <h1>")
    if "<title>" not in src: problems.append(f"{rel}: no <title>")

    s = Stripper(); s.feed(src); text = "".join(s.text)

    # leaked markdown in visible prose
    for pat, label in [
        (r"\*\*[A-Za-z]", "bold markers **"),
        (r"^\s*#{2,}\s", "heading markers ##"),
        (r"\]\(http", "raw link syntax ](http"),
        (r"\|\s*---", "raw table pipes"),
    ]:
        for m in re.finditer(pat, text, re.M):
            frag = text[max(0,m.start()-45):m.start()+55].replace("\n"," ")
            problems.append(f"{rel}: leaked {label} → …{frag.strip()}…")
            break

    ids_by_page[rel] = set(re.findall(r'id="([^"]+)"', src))
    for href in re.findall(r'href="([^"]+)"', src):
        if href.startswith(("http://","https://","mailto:")): continue
        links.append((rel, href))

# resolve internal links
for page, href in links:
    base = (OUT / page).parent
    frag = ""
    if "#" in href:
        href, frag = href.split("#", 1)
    if href in ("", "."):
        target_rel = page
    else:
        t = (base / href).resolve()
        try: target_rel = t.relative_to(OUT.resolve()).as_posix()
        except ValueError:
            problems.append(f"{page}: link escapes site root → {href}"); continue
        if not t.exists():
            problems.append(f"{page}: dead link → {href}"); continue
    if frag and target_rel in ids_by_page and frag not in ids_by_page[target_rel]:
        problems.append(f"{page}: dead anchor → {href}#{frag}")

# content sanity
for p in pages:
    rel = p.relative_to(OUT).as_posix()
    s = Stripper(); s.feed(p.read_text(encoding="utf-8"))
    n = len("".join(s.text).split())
    if n < 120: problems.append(f"{rel}: suspiciously short ({n} words)")

print(f"checked {len(pages)} pages, {len(links)} internal links")
if problems:
    print(f"\n{len(problems)} PROBLEM(S):")
    for x in problems[:40]: print("  -", x)
    sys.exit(1)
print("all checks passed")
