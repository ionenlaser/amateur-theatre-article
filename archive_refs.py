"""Add Internet Archive snapshots to the references of generated .wiki articles.

For every <ref>...</ref> whose first external link is not a Wikimedia site, ask the
Wayback Machine for a snapshot and append a link to it. A snapshot from the last
six months is reused; otherwise Save Page Now is asked for a fresh capture:

    <ref name="site">[https://example.de/ Über uns], Example e.V., retrieved 14 October 2026.</ref>
 -> <ref name="site">[https://example.de/ Über uns], Example e.V., retrieved 14 October 2026. [https://web.archive.org/web/20261014120000/https://example.de/ Archived] on 14 October 2026.</ref>

Refs that already contain a web.archive.org link are left alone, so the script can
be re-run safely. If a capture fails, the most recent existing snapshot is used
regardless of age; if there is none, the ref is left unchanged and reported.

Usage:
    python3 archive_refs.py [--dry-run] [PATH ...]   # PATH: .wiki files or folders (default: articles)
"""

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import UTC, datetime, timedelta
from pathlib import Path

USER_AGENT = "amateur-theatre-article-archiver/1.0 (+https://amateur-theatre-wiki.gwi.uni-muenchen.de/)"
WIKIMEDIA_DOMAINS = (
    "wikipedia.org",
    "wikimedia.org",
    "wikidata.org",
    "wiktionary.org",
    "wikisource.org",
    "wikibooks.org",
    "wikiquote.org",
    "wikinews.org",
    "wikiversity.org",
    "wikivoyage.org",
    "mediawiki.org",
    "archive.org",
)
REF_RE = re.compile(r"(<ref(?:\s+name=\"[^\"]*\")?\s*>)(.*?)(</ref>)", re.DOTALL)
LINK_RE = re.compile(r"\[(https?://[^\s\]]+)")
SNAPSHOT_RE = re.compile(r"/web/(\d{14})/")
SAVE_DELAY = 6  # seconds between captures; anonymous Save Page Now is rate-limited
MAX_SNAPSHOT_AGE = timedelta(days=183)  # reuse snapshots up to six months old


def utcnow():
    return datetime.now(UTC).replace(tzinfo=None)  # Wayback timestamps are naive UTC


def is_wikimedia(url):
    host = urllib.parse.urlsplit(url).hostname or ""
    return any(host == d or host.endswith("." + d) for d in WIKIMEDIA_DOMAINS)


def http_get(url, timeout=120):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    return urllib.request.urlopen(req, timeout=timeout)


def save_page_now(url, retries=3):
    """Capture url and return the snapshot URL, or None."""
    for attempt in range(retries):
        try:
            with http_get("https://web.archive.org/save/" + url) as resp:
                for candidate in (
                    resp.headers.get("Content-Location", ""),
                    resp.geturl(),
                ):
                    if SNAPSHOT_RE.search(candidate):
                        return urllib.parse.urljoin(
                            "https://web.archive.org", candidate
                        )
        except urllib.error.HTTPError as e:
            print(
                f"    save attempt {attempt + 1} failed: HTTP {e.code}", file=sys.stderr
            )
            if e.code not in (429, 500, 502, 503, 504, 520, 523):
                break
        except (urllib.error.URLError, TimeoutError) as e:
            print(f"    save attempt {attempt + 1} failed: {e}", file=sys.stderr)
        time.sleep(SAVE_DELAY * (attempt + 2))
    return None


def latest_snapshot(url):
    """Return the closest existing snapshot URL, or None."""
    try:
        query = urllib.parse.urlencode(
            {"url": url, "timestamp": utcnow().strftime("%Y%m%d%H%M%S")}
        )
        api = "https://archive.org/wayback/available?" + query
        with http_get(api, timeout=60) as resp:
            closest = json.load(resp).get("archived_snapshots", {}).get("closest", {})
        if closest.get("available") and str(closest.get("status", "200")).startswith(
            ("2", "3")
        ):
            return closest["url"].replace(
                "http://web.archive.org", "https://web.archive.org"
            )
    except (urllib.error.URLError, TimeoutError, ValueError) as e:
        print(f"    availability lookup failed: {e}", file=sys.stderr)
    return None


def snapshot_time(snapshot_url):
    return datetime.strptime(SNAPSHOT_RE.search(snapshot_url).group(1), "%Y%m%d%H%M%S")


def snapshot_date(snapshot_url):
    d = snapshot_time(snapshot_url)
    return f"{d.day} {d.strftime('%B %Y')}"


def archive(url, cache, dry_run):
    if url not in cache:
        if dry_run:
            cache[url] = None
        else:
            print(f"  archiving {url}")
            existing = latest_snapshot(url)
            if existing and utcnow() - snapshot_time(existing) <= MAX_SNAPSHOT_AGE:
                print(f"    reusing snapshot from {snapshot_date(existing)}")
                cache[url] = existing
            else:
                snap = save_page_now(url)
                if not snap and existing:
                    print("    capture failed; using existing snapshot")
                    snap = existing
                cache[url] = snap
                time.sleep(SAVE_DELAY)
    return cache[url]


def process_file(path, cache, dry_run):
    text = path.read_text(encoding="utf-8")
    missing = []

    def replace(m):
        open_tag, body, close_tag = m.groups()
        link = LINK_RE.search(body)
        if not link or "web.archive.org" in body or is_wikimedia(link.group(1)):
            return m.group(0)
        url = link.group(1)
        if dry_run:
            print(f"  would archive {url}")
            return m.group(0)
        snap = archive(url, cache, dry_run)
        if not snap:
            missing.append(url)
            return m.group(0)
        body = body.rstrip()
        if not body.endswith("."):
            body += "."
        return (
            f"{open_tag}{body} [{snap} Archived] on {snapshot_date(snap)}.{close_tag}"
        )

    new_text = REF_RE.sub(replace, text)
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        print(f"  updated {path}")
    return missing


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument(
        "paths", nargs="*", default=["articles"], help=".wiki files or folders"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="list URLs without archiving"
    )
    args = parser.parse_args()

    files = []
    for p in map(Path, args.paths):
        files += sorted(p.glob("*.wiki")) if p.is_dir() else [p]

    cache, missing = {}, []
    for f in files:
        print(f)
        missing += [(f, u) for u in process_file(f, cache, args.dry_run)]

    if missing:
        print("\nNo snapshot available for:", file=sys.stderr)
        for f, u in missing:
            print(f"  {f}: {u}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
