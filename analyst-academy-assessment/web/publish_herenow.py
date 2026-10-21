#!/usr/bin/env python3
"""
Publish ./public to here.now via its three-step API (create -> upload -> finalize).

No installer and no bundled scripts: this calls the documented public API
directly. Without an API key the Site is anonymous and expires in 24 hours;
set HERENOW_API_KEY for a permanent one.

    python3 publish_herenow.py [--slug SLUG]
"""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "public"
API = "https://here.now/api/v1/publish"
CLIENT = "claude-code"
KEY = os.environ.get("HERENOW_API_KEY")


def req(url: str, *, method="GET", data=None, headers=None, raw=False):
    h = {"X-HereNow-Client": CLIENT}
    if KEY:
        h["Authorization"] = f"Bearer {KEY}"
    if headers:
        h.update(headers)
    body = data
    if data is not None and not raw:
        body = json.dumps(data).encode()
        h["Content-Type"] = "application/json"
    r = urllib.request.Request(url, data=body, headers=h, method=method)
    with urllib.request.urlopen(r, timeout=120) as resp:
        payload = resp.read()
    return payload if raw else json.loads(payload or b"{}")


def main() -> int:
    slug = None
    if "--slug" in sys.argv:
        slug = sys.argv[sys.argv.index("--slug") + 1]

    files = sorted(p for p in ROOT.rglob("*") if p.is_file())
    manifest = [{"path": p.relative_to(ROOT).as_posix(), "size": p.stat().st_size}
                for p in files]
    total = sum(f["size"] for f in manifest)
    print(f"publishing {len(manifest)} files, {total/1024:.0f} KB")
    assert any(f["path"] == "index.html" for f in manifest), \
        "index.html must be at the root of the published directory"

    url = f"{API}/{slug}" if slug else API
    created = req(url, method="PUT" if slug else "POST", data={"files": manifest})
    up = created["upload"]
    print(f"  slug      {created['slug']}")
    print(f"  url       {created['siteUrl']}")
    ps = created.get("publishStatus", {})
    print(f"  ownership {ps.get('ownership')}  persistence {ps.get('persistence')}"
          + (f"  expires {ps.get('expiresAt')}" if ps.get("expiresAt") else ""))

    by_path = {u["path"]: u for u in up["uploads"]}
    for i, f in enumerate(manifest, 1):
        u = by_path.get(f["path"])
        if not u:
            print(f"  !! no upload target for {f['path']}")
            return 1
        blob = (ROOT / f["path"]).read_bytes()
        try:
            req(u["url"], method=u.get("method", "PUT"), data=blob,
                headers=u.get("headers") or {}, raw=True)
        except urllib.error.HTTPError as e:
            print(f"  !! upload failed {f['path']}: HTTP {e.code} {e.read()[:200]!r}")
            return 1
        if i % 10 == 0 or i == len(manifest):
            print(f"  uploaded {i}/{len(manifest)}")

    final = req(up["finalizeUrl"], method="POST", data={"versionId": up["versionId"]})
    print("\nfinalize:", json.dumps(
        {k: final.get(k) for k in
         ("isLive", "status", "siteUrl", "primaryUrl", "unchanged", "missingFiles")},
        indent=2))
    live = final.get("primaryUrl") or final.get("siteUrl") or created["siteUrl"]
    print(f"\nLIVE: {live}")
    return 0 if final.get("isLive") else 1


if __name__ == "__main__":
    raise SystemExit(main())
