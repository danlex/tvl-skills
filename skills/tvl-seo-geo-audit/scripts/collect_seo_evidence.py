#!/usr/bin/env python3
"""Collect deterministic SEO/GEO evidence for one URL.

The collector records observations only. It does not decide findings.
"""

from __future__ import annotations

import argparse
import hashlib
import html.parser
import ipaddress
import json
import platform
import re
import socket
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


MAX_BYTES = 2_000_000
MAX_REDIRECTS = 5
TIMEOUT = 10
USER_AGENT = "tvl-seo-geo-audit/2.0 (+https://github.com/danlex/tvl-skills)"
AI_AGENTS = (
    "OAI-SearchBot",
    "GPTBot",
    "ChatGPT-User",
    "Claude-SearchBot",
    "ClaudeBot",
    "Claude-User",
    "PerplexityBot",
    "Perplexity-User",
)


class UnsafeUrlError(ValueError):
    """Raised when a URL is unsafe to fetch."""


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


def validate_public_http_url(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        raise UnsafeUrlError("Only http and https URLs are allowed")
    if not parsed.hostname:
        raise UnsafeUrlError("URL must include a host")

    host = parsed.hostname
    try:
        addresses = socket.getaddrinfo(host, parsed.port or (443 if parsed.scheme == "https" else 80))
    except socket.gaierror as exc:
        raise UnsafeUrlError(f"Cannot resolve host: {host}") from exc

    for addr in addresses:
        ip = ipaddress.ip_address(addr[4][0])
        if (
            ip.is_private
            or ip.is_loopback
            or ip.is_link_local
            or ip.is_multicast
            or ip.is_reserved
            or ip.is_unspecified
        ):
            raise UnsafeUrlError(f"Refusing private or unsafe address: {ip}")
    return urllib.parse.urlunparse(parsed)


def read_limited(response: urllib.response.addinfourl) -> bytes:
    data = response.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        return data[:MAX_BYTES]
    return data


def fetch_url(url: str, *, method: str = "GET") -> dict[str, Any]:
    current = validate_public_http_url(url)
    redirects: list[dict[str, Any]] = []
    failures: list[str] = []

    for _ in range(MAX_REDIRECTS + 1):
        req = urllib.request.Request(
            current,
            method=method,
            headers={"User-Agent": USER_AGENT, "Accept": "text/html,application/xhtml+xml,*/*;q=0.8"},
        )
        try:
            opener = urllib.request.build_opener(NoRedirectHandler)
            response = opener.open(req, timeout=TIMEOUT)
            status = getattr(response, "status", response.getcode())
            headers = dict(response.headers.items())
            body_bytes = b"" if method == "HEAD" else read_limited(response)
            encoding = response.headers.get_content_charset() or "utf-8"
            body = body_bytes.decode(encoding, errors="replace")
            return {
                "ok": True,
                "url": current,
                "status": status,
                "headers": headers,
                "body": body,
                "body_bytes": len(body_bytes),
                "truncated": len(body_bytes) >= MAX_BYTES,
                "content_hash": sha256_text(body),
                "redirect_chain": redirects,
                "failures": failures,
            }
        except urllib.error.HTTPError as exc:
            status = exc.code
            location = exc.headers.get("Location")
            if status in {301, 302, 303, 307, 308} and location:
                next_url = urllib.parse.urljoin(current, location)
                validate_public_http_url(next_url)
                redirects.append({"from": current, "to": next_url, "status": status})
                current = next_url
                continue
            body_bytes = exc.read(MAX_BYTES)
            body = body_bytes.decode(exc.headers.get_content_charset() or "utf-8", errors="replace")
            return {
                "ok": True,
                "url": current,
                "status": status,
                "headers": dict(exc.headers.items()),
                "body": body,
                "body_bytes": len(body_bytes),
                "truncated": False,
                "content_hash": sha256_text(body),
                "redirect_chain": redirects,
                "failures": failures,
            }
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            failures.append(str(exc))
            if len(failures) < 2:
                continue
            return {
                "ok": False,
                "url": current,
                "status": None,
                "headers": {},
                "body": "",
                "body_bytes": 0,
                "truncated": False,
                "content_hash": None,
                "redirect_chain": redirects,
                "failures": failures,
            }

    return {
        "ok": False,
        "url": current,
        "status": None,
        "headers": {},
        "body": "",
        "body_bytes": 0,
        "truncated": False,
        "content_hash": None,
        "redirect_chain": redirects,
        "failures": ["redirect limit exceeded"],
    }


class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):  # type: ignore[no-untyped-def]
        return None


class SeoHtmlParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title_parts: list[str] = []
        self.in_title = False
        self.current_heading: str | None = None
        self.heading_parts: list[str] = []
        self.meta: list[dict[str, str]] = []
        self.links: list[dict[str, str]] = []
        self.anchors: list[dict[str, str]] = []
        self.images: list[dict[str, str]] = []
        self.json_ld_raw: list[str] = []
        self.in_json_ld = False
        self.json_ld_buf: list[str] = []
        self.headings: list[dict[str, str]] = []
        self.text_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {k.lower(): (v or "") for k, v in attrs}
        tag = tag.lower()
        if tag == "title":
            self.in_title = True
        elif tag in {"h1", "h2", "h3"}:
            self.current_heading = tag
            self.heading_parts = []
        elif tag == "meta":
            self.meta.append(attr)
        elif tag == "link":
            self.links.append(attr)
        elif tag == "a" and attr.get("href"):
            self.anchors.append({"href": attr.get("href", ""), "text": ""})
        elif tag == "img":
            self.images.append({"src": attr.get("src", ""), "alt": attr.get("alt", "")})
        elif tag == "script" and attr.get("type", "").lower() == "application/ld+json":
            self.in_json_ld = True
            self.json_ld_buf = []

    def handle_data(self, data: str) -> None:
        text = " ".join(data.split())
        if not text:
            return
        if self.in_title:
            self.title_parts.append(text)
        if self.current_heading:
            self.heading_parts.append(text)
        if self.in_json_ld:
            self.json_ld_buf.append(data)
        else:
            self.text_parts.append(text)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "title":
            self.in_title = False
        elif tag in {"h1", "h2", "h3"} and self.current_heading == tag:
            self.headings.append({"level": tag, "text": " ".join(self.heading_parts)})
            self.current_heading = None
            self.heading_parts = []
        elif tag == "script" and self.in_json_ld:
            self.json_ld_raw.append("".join(self.json_ld_buf).strip())
            self.in_json_ld = False
            self.json_ld_buf = []


def meta_value(meta: list[dict[str, str]], key: str, value: str) -> str | None:
    for item in meta:
        if item.get(key, "").lower() == value.lower():
            return item.get("content")
    return None


def parse_html(html: str, base_url: str) -> dict[str, Any]:
    parser = SeoHtmlParser()
    parser.feed(html)
    canonical = None
    hreflang: list[dict[str, str]] = []
    stylesheets: list[str] = []
    for link in parser.links:
        rel = set(link.get("rel", "").lower().split())
        href = link.get("href", "")
        if "canonical" in rel and href:
            canonical = urllib.parse.urljoin(base_url, href)
        if "alternate" in rel and link.get("hreflang") and href:
            hreflang.append({"hreflang": link["hreflang"], "href": urllib.parse.urljoin(base_url, href)})
        if "stylesheet" in rel and href:
            stylesheets.append(urllib.parse.urljoin(base_url, href))

    json_ld = []
    for block in parser.json_ld_raw:
        try:
            parsed = json.loads(block)
            types = []
            candidates = parsed if isinstance(parsed, list) else [parsed]
            for item in candidates:
                if isinstance(item, dict) and "@type" in item:
                    types.append(item["@type"])
            json_ld.append({"valid": True, "types": types, "raw_hash": sha256_text(block)})
        except json.JSONDecodeError as exc:
            json_ld.append({"valid": False, "error": str(exc), "raw_hash": sha256_text(block)})

    return {
        "title": " ".join(parser.title_parts),
        "meta_description": meta_value(parser.meta, "name", "description"),
        "robots_meta": meta_value(parser.meta, "name", "robots"),
        "lang": re.search(r"<html[^>]*\slang=[\"']?([^\"'\s>]+)", html, re.I).group(1)
        if re.search(r"<html[^>]*\slang=[\"']?([^\"'\s>]+)", html, re.I)
        else None,
        "canonical": canonical,
        "hreflang": hreflang,
        "headings": parser.headings,
        "open_graph": {m.get("property", ""): m.get("content", "") for m in parser.meta if m.get("property", "").startswith("og:")},
        "twitter": {m.get("name", ""): m.get("content", "") for m in parser.meta if m.get("name", "").startswith("twitter:")},
        "json_ld": json_ld,
        "links": [{"href": urllib.parse.urljoin(base_url, a["href"]), "text": a.get("text", "")} for a in parser.anchors[:500]],
        "images": parser.images[:200],
        "stylesheets": stylesheets,
        "text_excerpt": " ".join(parser.text_parts)[:4000],
        "initial_html_text_length": len(" ".join(parser.text_parts)),
    }


def robots_allowed(robots_text: str, target_url: str) -> dict[str, Any]:
    lines = robots_text.splitlines()
    result = {}
    for agent in AI_AGENTS:
        result[agent] = {"state": "NOT_TESTED", "reason": "robots parser unavailable"}
    try:
        import urllib.robotparser

        rp = urllib.robotparser.RobotFileParser()
        rp.parse(lines)
        for agent in AI_AGENTS:
            result[agent] = {"state": "CONFIRMED", "allowed": rp.can_fetch(agent, target_url)}
    except Exception as exc:  # pragma: no cover - defensive
        for agent in AI_AGENTS:
            result[agent] = {"state": "UNVERIFIABLE", "reason": str(exc)}
    sitemaps = []
    for line in lines:
        if line.lower().startswith("sitemap:"):
            sitemaps.append(line.split(":", 1)[1].strip())
    return {"agents": result, "sitemaps": sitemaps}


def audit_agent_allowed(robots_text: str, target_url: str) -> bool:
    try:
        import urllib.robotparser

        rp = urllib.robotparser.RobotFileParser()
        rp.parse(robots_text.splitlines())
        return rp.can_fetch(USER_AGENT, target_url)
    except Exception:
        return True


def collect_sitemap(urls: list[str], target_url: str) -> dict[str, Any]:
    memberships = []
    for sitemap_url in urls[:5]:
        fetched = fetch_url(sitemap_url)
        if not fetched["ok"] or not fetched["body"]:
            memberships.append({"sitemap": sitemap_url, "state": "NOT_TESTED", "reason": fetched["failures"]})
            continue
        try:
            root = ET.fromstring(fetched["body"])
            ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
            found = False
            lastmod = None
            for url_node in root.findall(".//sm:url", ns):
                loc = url_node.findtext("sm:loc", default="", namespaces=ns)
                if loc.rstrip("/") == target_url.rstrip("/"):
                    found = True
                    lastmod = url_node.findtext("sm:lastmod", default=None, namespaces=ns)
                    break
            memberships.append({"sitemap": sitemap_url, "state": "CONFIRMED", "found": found, "lastmod": lastmod})
        except ET.ParseError as exc:
            memberships.append({"sitemap": sitemap_url, "state": "UNVERIFIABLE", "reason": str(exc)})
    return {"memberships": memberships}


def build_evidence(url: str, mode: str, sample: list[str]) -> dict[str, Any]:
    timestamp = now_iso()
    limitations: list[str] = ["rendered DOM not collected by this stdlib collector"]
    validate_public_http_url(url)
    parsed_url = urllib.parse.urlparse(url)
    origin = f"{parsed_url.scheme}://{parsed_url.netloc}"
    robots_url = urllib.parse.urljoin(origin, "/robots.txt")
    robots_fetch = fetch_url(robots_url)
    robots_observations: dict[str, Any] = {"agents": {}, "sitemaps": []}
    may_fetch_page = True
    if robots_fetch["ok"] and robots_fetch["body"]:
        robots_observations = robots_allowed(robots_fetch["body"], url)
        may_fetch_page = audit_agent_allowed(robots_fetch["body"], url)
    else:
        limitations.append("robots.txt not collected")

    if may_fetch_page:
        page_fetch = fetch_url(url)
    else:
        limitations.append("target URL not fetched because robots.txt disallows this audit user agent")
        page_fetch = {
            "ok": False,
            "url": url,
            "status": None,
            "headers": {},
            "body": "",
            "body_bytes": 0,
            "truncated": False,
            "content_hash": None,
            "redirect_chain": [],
            "failures": ["blocked by robots.txt"],
        }
    final_url = page_fetch.get("url")

    html_observations: dict[str, Any] = {}
    if page_fetch["body"]:
        html_observations = parse_html(page_fetch["body"], final_url or url)

    sitemap_urls = robots_observations.get("sitemaps") or [urllib.parse.urljoin(origin, "/sitemap.xml")]
    sitemap_observations = collect_sitemap(sitemap_urls, final_url or url) if mode in {"PAGE", "MULTILINGUAL_PAIR", "SITE_SAMPLE"} else {"memberships": []}

    evidence_records = [
        {
            "id": "http.final_url",
            "state": "CONFIRMED" if page_fetch["ok"] else "NOT_TESTED",
            "origin": "MEASURED",
            "value": final_url,
        },
        {
            "id": "http.status",
            "state": "CONFIRMED" if page_fetch["status"] else "NOT_TESTED",
            "origin": "MEASURED",
            "value": page_fetch["status"],
        },
        {
            "id": "robots_meta",
            "state": "CONFIRMED" if html_observations.get("robots_meta") else "NOT_FOUND",
            "origin": "MEASURED",
            "value": html_observations.get("robots_meta"),
        },
        {
            "id": "x_robots_tag",
            "state": "CONFIRMED" if page_fetch["headers"].get("X-Robots-Tag") else "NOT_FOUND",
            "origin": "MEASURED",
            "value": page_fetch["headers"].get("X-Robots-Tag"),
        },
        {
            "id": "canonical",
            "state": "CONFIRMED" if html_observations.get("canonical") else "NOT_FOUND",
            "origin": "MEASURED",
            "value": html_observations.get("canonical"),
        },
        {
            "id": "rendered_dom",
            "state": "NOT_TESTED",
            "origin": "MEASURED",
            "value": None,
        },
    ]

    return {
        "manifest": {
            "requested_url": url,
            "final_url": final_url,
            "retrieval_timestamp": timestamp,
            "audit_mode": mode,
            "selected_sample": sample,
            "tool": "collect_seo_evidence.py",
            "tool_version": "2.0",
            "python_version": platform.python_version(),
            "limitations": limitations + page_fetch.get("failures", []),
        },
        "fetches": {
            "page": {k: v for k, v in page_fetch.items() if k != "body"},
            "robots": {k: v for k, v in robots_fetch.items() if k != "body"},
        },
        "page": html_observations,
        "robots": robots_observations,
        "sitemap": sitemap_observations,
        "evidence_records": evidence_records,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect SEO/GEO evidence for a public URL")
    parser.add_argument("url")
    parser.add_argument("--mode", choices=("PAGE", "MULTILINGUAL_PAIR", "SITE_SAMPLE", "CONTENT_BRIEF"), default="PAGE")
    parser.add_argument("--sample", action="append", default=[])
    parser.add_argument("--output")
    args = parser.parse_args()

    try:
        evidence = build_evidence(args.url, args.mode, args.sample)
    except UnsafeUrlError as exc:
        print(f"Refused URL: {exc}", file=sys.stderr)
        return 2

    data = json.dumps(evidence, indent=2, sort_keys=True)
    if args.output:
        Path(args.output).write_text(data + "\n", encoding="utf-8")
    else:
        print(data)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
