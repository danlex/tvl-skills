#!/usr/bin/env python3
"""verify_pointers.py — ground an audit's EVIDENCE CHECK with a tool.

Resolve the pointers a draft cites and print CONFIRMED / NOT-FOUND /
UNVERIFIABLE for each, so the audit is backed by a check instead of a guess.

Pointer forms (one per line, via args or stdin):
  https://example.com/x     URL            -> HEAD request (UNVERIFIABLE if offline)
  path/to/file.py           file exists
  path/to/file.py:120       file + line number exists
  path/to/file.py:my_func   file contains the symbol / text

Rules:
  - REFUTED is never emitted here: contradiction needs semantic judgment, not a
    resolver. This tool only answers "does the cited target exist / resolve?".
  - Never raises. Anything uncheckable is UNVERIFIABLE.

Usage:
  python3 verify_pointers.py "src/app.py:42" "https://a.com" < pointers.txt
"""
from __future__ import annotations

import sys
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


def _classify_file(raw: str) -> tuple[str, str]:
    p = Path(raw)
    if p.exists():
        return "CONFIRMED", "path exists" if p.is_file() else "directory exists"
    return "NOT-FOUND", "no such path"


def _classify_file_line(path: str, line: int) -> tuple[str, str]:
    p = Path(path)
    if not p.exists():
        return "NOT-FOUND", "file does not exist"
    try:
        n = sum(1 for _ in p.open(encoding="utf-8", errors="replace"))
    except OSError as exc:  # unreadable
        return "UNVERIFIABLE", f"unreadable: {exc.__class__.__name__}"
    if 1 <= line <= n:
        return "CONFIRMED", f"file has {n} lines"
    return "NOT-FOUND", f"line {line} beyond EOF ({n} lines)"


def _classify_file_symbol(path: str, symbol: str) -> tuple[str, str]:
    p = Path(path)
    if not p.exists():
        return "NOT-FOUND", "file does not exist"
    try:
        text = p.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return "UNVERIFIABLE", f"unreadable: {exc.__class__.__name__}"
    hits = [i + 1 for i, ln in enumerate(text.splitlines()) if symbol in ln]
    if hits:
        preview = ",".join(map(str, hits[:5]))
        return "CONFIRMED", f"found on line(s) {preview}"
    return "NOT-FOUND", "symbol/text not present in file"


def _classify_url(url: str) -> tuple[str, str]:
    req = Request(url, method="HEAD", headers={"User-Agent": "tvl-audit/1.0"})
    try:
        with urlopen(req, timeout=6) as resp:  # noqa: S310 (intended)
            return "CONFIRMED", f"HTTP {resp.status}"
    except HTTPError as exc:
        if exc.code in (404, 410):
            return "NOT-FOUND", f"HTTP {exc.code}"
        if exc.code in (405, 403):  # HEAD refused / forbidden, existence unclear
            return "UNVERIFIABLE", f"HTTP {exc.code} (HEAD refused)"
        return "UNVERIFIABLE", f"HTTP {exc.code}"
    except (URLError, TimeoutError, ValueError, OSError) as exc:
        return "UNVERIFIABLE", f"offline/blocked: {exc.__class__.__name__}"


def classify(raw: str) -> tuple[str, str]:
    raw = raw.strip()
    if not raw:
        return "UNVERIFIABLE", "empty"
    if raw.startswith(("http://", "https://")):
        return _classify_url(raw)
    if ":" in raw:
        path, _, tail = raw.rpartition(":")
        if path and tail:
            if tail.isdigit():
                return _classify_file_line(path, int(tail))
            # only treat as file:symbol when the left side looks like a real path
            if Path(path).exists() or "/" in path or path.endswith(
                (".py", ".js", ".ts", ".md", ".html", ".css", ".json", ".yaml", ".yml", ".txt")
            ):
                return _classify_file_symbol(path, tail)
    return _classify_file(raw)


def main(argv: list[str]) -> int:
    pointers = list(argv)
    if not pointers and not sys.stdin.isatty():
        pointers = [ln for ln in sys.stdin.read().splitlines() if ln.strip()]
    if not pointers:
        print(__doc__)
        return 0

    rows = [(p, *classify(p)) for p in pointers]
    width = min(max((len(p) for p, _, _ in rows), default=8), 60)
    print(f"{'POINTER':<{width}}  {'RESULT':<12}  NOTE")
    for ptr, result, note in rows:
        shown = ptr if len(ptr) <= width else ptr[: width - 1] + "…"
        print(f"{shown:<{width}}  {result:<12}  {note}")

    counts: dict[str, int] = {}
    for _, result, _ in rows:
        counts[result] = counts.get(result, 0) + 1
    summary = " ".join(f"{k}={v}" for k, v in sorted(counts.items()))
    print(f"\n{len(rows)} pointer(s): {summary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
