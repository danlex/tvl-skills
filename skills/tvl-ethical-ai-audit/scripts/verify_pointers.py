#!/usr/bin/env python3
"""verify_pointers.py — existence check for an audit's cited pointers.

Resolve the pointers a draft cites and print PASS / FAIL for each:
  PASS = the pointer resolves (the target exists).
  FAIL = it does not resolve, or could not be reached (see the NOTE column).

This is existence only. A PASS is NOT `CONFIRMED`: you must still read the
source and judge whether it supports the claim (that is the auditor's job).
Treating a PASS here as confirmation is automation bias.

Pointer forms (one per line, via args or stdin):
  https://example.com/x     URL            -> HEAD request
  path/to/file.py           file exists
  path/to/file.py:120       file + line number exists
  path/to/file.py:my_func   file contains the symbol / text

Never raises. Anything uncheckable is FAIL with a "could not verify" note.

Usage:
  python3 verify_pointers.py "src/app.py:42" "https://a.com" < pointers.txt
"""
from __future__ import annotations

import sys
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


def _file(raw: str) -> tuple[str, str]:
    p = Path(raw)
    if p.exists():
        return "PASS", "path exists" if p.is_file() else "directory exists"
    return "FAIL", "no such path"


def _file_line(path: str, line: int) -> tuple[str, str]:
    p = Path(path)
    if not p.exists():
        return "FAIL", "file does not exist"
    try:
        n = sum(1 for _ in p.open(encoding="utf-8", errors="replace"))
    except OSError as exc:
        return "FAIL", f"could not verify: unreadable ({exc.__class__.__name__})"
    if 1 <= line <= n:
        return "PASS", f"file has {n} lines"
    return "FAIL", f"line {line} beyond EOF ({n} lines)"


def _file_symbol(path: str, symbol: str) -> tuple[str, str]:
    p = Path(path)
    if not p.exists():
        return "FAIL", "file does not exist"
    try:
        text = p.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return "FAIL", f"could not verify: unreadable ({exc.__class__.__name__})"
    hits = [i + 1 for i, ln in enumerate(text.splitlines()) if symbol in ln]
    if hits:
        return "PASS", f"found on line(s) {','.join(map(str, hits[:5]))}"
    return "FAIL", "symbol/text not present in file"


def _url(url: str) -> tuple[str, str]:
    req = Request(url, method="HEAD", headers={"User-Agent": "tvl-audit/1.0"})
    try:
        with urlopen(req, timeout=6) as resp:  # noqa: S310 (intended)
            return "PASS", f"HTTP {resp.status}"
    except HTTPError as exc:
        if exc.code in (404, 410):
            return "FAIL", f"HTTP {exc.code} (not found)"
        return "FAIL", f"could not verify: HTTP {exc.code}"
    except (URLError, TimeoutError, ValueError, OSError) as exc:
        return "FAIL", f"could not verify: offline/blocked ({exc.__class__.__name__})"


def classify(raw: str) -> tuple[str, str]:
    """Return (PASS|FAIL, note) for one pointer. Existence only, never CONFIRMED."""
    raw = raw.strip()
    if not raw:
        return "FAIL", "empty"
    if raw.startswith(("http://", "https://")):
        return _url(raw)
    if ":" in raw:
        path, _, tail = raw.rpartition(":")
        if path and tail:
            if tail.isdigit():
                return _file_line(path, int(tail))
            if Path(path).exists() or "/" in path or path.endswith(
                (".py", ".js", ".ts", ".md", ".html", ".css", ".json", ".yaml", ".yml", ".txt")
            ):
                return _file_symbol(path, tail)
    return _file(raw)


def main(argv: list[str]) -> int:
    pointers = list(argv)
    if not pointers and not sys.stdin.isatty():
        pointers = [ln for ln in sys.stdin.read().splitlines() if ln.strip()]
    if not pointers:
        print(__doc__)
        return 0

    rows = [(p, *classify(p)) for p in pointers]
    width = min(max((len(p) for p, _, _ in rows), default=8), 60)
    print(f"{'POINTER':<{width}}  {'RESULT':<6}  NOTE")
    for ptr, result, note in rows:
        shown = ptr if len(ptr) <= width else ptr[: width - 1] + "…"
        print(f"{shown:<{width}}  {result:<6}  {note}")

    passed = sum(1 for _, r, _ in rows if r == "PASS")
    print(f"\n{len(rows)} pointer(s): PASS={passed} FAIL={len(rows) - passed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
