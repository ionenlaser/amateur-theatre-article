"""Add Internet Archive snapshots to generated articles and QuickStatements batches.

For every <ref>...</ref> whose first external link is not a Wikimedia site, ask the
Wayback Machine for a snapshot and append a link to it. A snapshot from the last
six months is reused; otherwise Save Page Now is asked for a fresh capture:

    <ref name="site">[https://example.de/ Über uns], Example e.V., retrieved 14 October 2026.</ref>
 -> <ref name="site">[https://example.de/ Über uns], Example e.V., retrieved 14 October 2026. [https://web.archive.org/web/20261014120000/https://example.de/ Archived] on 14 October 2026.</ref>

The QuickStatements files next to each article (<base>.qs, <base>.award-items.qs,
<base>.pending.qs) get the same snapshots: every reference block with an S854
reference URL and no S1065 gets an S1065 archive URL and an S2960 archive date.

Afterwards the batch files of every touched folder are rebuilt: the "## Batches"
section of each <base>.qs-report.md (with its QuickStatements 3.0 URLs) and the
folder-wide 000_all.qs, 000_all.qs.url, 000_all.award-items.qs(.url),
000_all.pending.qs and 000_all.qs-report.md.

Refs and reference blocks that already have an archive link are left alone, so the
script can be re-run safely. If a capture fails, the most recent existing snapshot
is used regardless of age; if there is none, the ref is left unchanged and reported.

All Wayback requests are paced; on HTTP 429 (Too Many Requests) the script waits
(Retry-After, or exponential backoff), doubles the pause between requests and slowly
speeds up again after successful calls.

Captures use the authenticated Save Page Now 2 API, which needs archive.org S3 keys
(https://archive.org/account/s3.php) in IA_ACCESS_KEY and IA_SECRET_KEY:

    IA_ACCESS_KEY=... IA_SECRET_KEY=... python3 archive_refs.py

Usage:
    python3 archive_refs.py [--dry-run] [PATH ...]   # PATH: .wiki files or folders (default: articles)
"""

import argparse
import datetime as dt
import json
import os
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
QS_URL_RE = re.compile(r'\tS854\t"([^"]+)"')
QS_BLOCK_RE = re.compile(r"(?=\t!S\d)")  # a second reference block starts with !S
QS_BASE_URL = "https://qs-dev.toolforge.org/batch/new?v1="
QS_SUFFIXES = (".award-items.qs", ".pending.qs", ".qs")
REQUEST_DELAY = 6  # minimum seconds between Wayback requests
MAX_DELAY = 120  # upper bound for the pause after repeated 429s
MAX_BACKOFF = 600  # upper bound for a single wait before retrying
RETRY_CODES = (429, 500, 502, 503, 504)
IA_KEYS = (os.environ.get("IA_ACCESS_KEY"), os.environ.get("IA_SECRET_KEY"))
MAX_SNAPSHOT_AGE = timedelta(days=183)  # reuse snapshots up to six months old


def utcnow():
    return datetime.now(UTC).replace(tzinfo=None)  # Wayback timestamps are naive UTC


def is_wikimedia(url):
    host = urllib.parse.urlsplit(url).hostname or ""
    return any(host == d or host.endswith("." + d) for d in WIKIMEDIA_DOMAINS)


pace = REQUEST_DELAY  # current pause between requests; grows on 429
last_request = 0.0


def http_open(url, data=None, headers=None, timeout=120):
    # Percent-encode non-ASCII characters (e.g. /über-uns/); http.client only sends ASCII.
    url = urllib.parse.quote(url, safe=":/?#[]@!$&'()*+,;=%~")
    headers = {"User-Agent": USER_AGENT, **(headers or {})}
    req = urllib.request.Request(url, data=data, headers=headers)
    return urllib.request.urlopen(req, timeout=timeout)


def retry_after(error):
    try:
        return int(error.headers.get("Retry-After", ""))
    except ValueError:
        return None


def request(url, data=None, headers=None, timeout=120, tries=5):
    """Paced http_open that waits and retries on 429, 5xx and network errors."""
    global pace, last_request
    for attempt in range(tries):
        time.sleep(max(0, last_request + pace - time.monotonic()))
        last_request = time.monotonic()
        try:
            resp = http_open(url, data, headers, timeout)
            pace = max(REQUEST_DELAY, pace * 0.9)  # recover slowly after a slowdown
            return resp
        except urllib.error.HTTPError as e:
            if e.code not in RETRY_CODES or attempt == tries - 1:
                raise
            if e.code == 429:
                pace = min(pace * 2, MAX_DELAY)
            wait = retry_after(e) or min(30 * 2**attempt, MAX_BACKOFF)
            reason = f"HTTP {e.code}"
        except (urllib.error.URLError, TimeoutError) as e:
            if attempt == tries - 1:
                raise
            wait = min(30 * 2**attempt, MAX_BACKOFF)
            reason = str(e)
        print(
            f"    {reason}; waiting {wait} s (attempt {attempt + 1}/{tries}, "
            f"pause now {pace:.0f} s)",
            file=sys.stderr,
        )
        time.sleep(wait)


def save_page_now(url, poll=5, max_wait=300):
    """Capture url via the Save Page Now 2 API and return the snapshot URL, or None."""
    headers = {
        "Accept": "application/json",
        "Authorization": "LOW {}:{}".format(*IA_KEYS),
    }
    try:
        data = urllib.parse.urlencode({"url": url}).encode()
        with request("https://web.archive.org/save", data, headers) as resp:
            job = json.load(resp)
        if "job_id" not in job:
            print(f"    capture refused: {job.get('message', job)}", file=sys.stderr)
            return None
        status_url = "https://web.archive.org/save/status/" + job["job_id"]
        for _ in range(max_wait // poll):
            time.sleep(poll)
            with request(status_url, headers=headers) as resp:
                status = json.load(resp)
            if status.get("status") == "success":
                return (
                    f"https://web.archive.org/web/{status['timestamp']}/"
                    f"{status['original_url']}"
                )
            if status.get("status") != "pending":
                print(
                    f"    capture failed: {status.get('message', status)}",
                    file=sys.stderr,
                )
                return None
        print(f"    capture still pending after {max_wait} s", file=sys.stderr)
    except (urllib.error.URLError, TimeoutError, ValueError, KeyError) as e:
        print(f"    capture failed: {e}", file=sys.stderr)
    return None


def latest_snapshot(url):
    """Return the closest existing snapshot URL, or None."""
    try:
        query = urllib.parse.urlencode(
            {"url": url, "timestamp": utcnow().strftime("%Y%m%d%H%M%S")}
        )
        api = "https://archive.org/wayback/available?" + query
        with request(api, timeout=60) as resp:
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
    m = SNAPSHOT_RE.search(snapshot_url)
    if not m:
        raise ValueError(f"not a Wayback snapshot URL: {snapshot_url}")
    return datetime.strptime(m.group(1), "%Y%m%d%H%M%S")


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
    return cache[url]


def process_wiki(path, cache, dry_run):
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


def process_qs(path, cache, dry_run):
    """Add S1065/S2960 to every reference block that has an S854 but no S1065."""
    text = path.read_text(encoding="utf-8")
    missing = []

    def archive_block(block):
        link = QS_URL_RE.search(block)
        if not link or "\tS1065\t" in block or is_wikimedia(link.group(1)):
            return block
        url = link.group(1)
        if dry_run:
            print(f"  would archive {url}")
            return block
        snap = archive(url, cache, dry_run)
        if not snap:
            missing.append(url)
            return block
        date = snapshot_time(snap).strftime("+%Y-%m-%dT00:00:00Z/11")
        return f'{block}\tS1065\t"{snap}"\tS2960\t{date}'

    lines = [
        "".join(archive_block(b) for b in QS_BLOCK_RE.split(line))
        for line in text.splitlines()
    ]
    new_text = "\n".join(lines) + "\n"
    if new_text != text and not dry_run:
        path.write_text(new_text, encoding="utf-8")
        print(f"  updated {path}")
    return missing


def qs_kind(path):
    """Return (base name, suffix) of a group's QuickStatements file, or None."""
    if path.name.startswith("000_"):
        return None
    for suffix in QS_SUFFIXES:
        if path.name.endswith(suffix):
            return path.name[: -len(suffix)], suffix
    return None


def group_files(folder, suffix):
    return sorted(
        p
        for p in folder.glob("*" + suffix)
        if (qs_kind(p) or (None, None))[1] == suffix
    )


def commands(path):
    return [l for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def batch_url(lines):
    return QS_BASE_URL + urllib.parse.quote("\n".join(lines), safe="")


def placeholders(lines):
    return sorted(set(re.findall(r"Q<NEW: ([^>]+)>", "\n".join(lines))))


def creator_of(folder, label):
    """Return the award-items file whose CREATE block has this Lde label."""
    for p in group_files(folder, ".award-items.qs"):
        if f'LAST\tLde\t"{label}"' in p.read_text(encoding="utf-8"):
            return p.name
    return None


def update_report(folder, base):
    """Rewrite the "## Batches" section of <base>.qs-report.md from its batch files."""
    report = folder / (base + ".qs-report.md")
    if not report.exists():
        return
    out = []
    main = folder / (base + ".qs")
    awards = folder / (base + ".award-items.qs")
    pending = folder / (base + ".pending.qs")
    if main.exists() and (cmds := commands(main)):
        out.append(
            f"- Main batch: `{main.name}`, {len(cmds)} commands, "
            f"[open in QuickStatements]({batch_url(cmds)})"
        )
    if awards.exists() and (cmds := commands(awards)):
        n = sum(l == "CREATE" for l in cmds)
        out.append(
            f"- Award items: `{awards.name}`, {n} new items, "
            f"[open in QuickStatements]({batch_url(cmds)})"
        )
    if pending.exists() and (cmds := commands(pending)):
        for label in placeholders(cmds):
            creator = creator_of(folder, label)
            source = f" (created by `{creator}`)" if creator else ""
            out.append(
                f"- Pending: `{pending.name}`, {len(cmds)} lines waiting for: {label}{source}. "
                f'After running that batch, tell Claude "{label} is Q…" to fill in the placeholder.'
            )
    section = "## Batches\n" + "\n".join(out) + "\n\n" if out else ""
    text = report.read_text(encoding="utf-8")
    if re.search(r"^## Batches\n", text, re.MULTILINE):
        new_text = re.sub(
            r"^## Batches\n.*?(?=^## |\Z)",
            section,
            text,
            flags=re.MULTILINE | re.DOTALL,
        )
    elif m := re.search(r"^## ", text, re.MULTILINE):
        new_text = text[: m.start()] + section + text[m.start() :]
    else:
        new_text = text.rstrip("\n") + "\n\n" + section
    if new_text != text:
        report.write_text(new_text, encoding="utf-8")


def write_batch(folder, name, files):
    cmds = [l for p in files for l in commands(p)]
    (folder / name).write_text("\n".join(cmds) + "\n", encoding="utf-8")
    url = batch_url(cmds)
    (folder / (name + ".url")).write_text(
        f"[InternetShortcut]\nURL={url}\n", encoding="utf-8"
    )
    return len(cmds), url


def rebuild_batches(folder):
    """Update every group report's batch links and rebuild the 000_all.* files."""
    bases = sorted({qs_kind(p)[0] for p in folder.glob("*.qs") if qs_kind(p)})
    for base in bases:
        update_report(folder, base)
    for p in folder.glob("000_all.*"):
        if p.name != "000_all.tasks.md":
            p.unlink()
    main = group_files(folder, ".qs")
    awards = group_files(folder, ".award-items.qs")
    pending = group_files(folder, ".pending.qs")
    reports = sorted(
        p for p in folder.glob("*.qs-report.md") if not p.name.startswith("000_")
    )
    if not (main or awards or pending or reports):
        return
    out = [
        (
            f"# QuickStatements report: all groups\n\nGenerated {dt.date.today()} "
            f"from {len(reports)} group reports.\n\n## Batches"
        )
    ]
    if main:
        n, url = write_batch(folder, "000_all.qs", main)
        out.append(
            f"- Main batch: `000_all.qs`, {n} commands from {len(main)} groups, "
            f"[open in QuickStatements]({url})"
        )
        print(f"  {folder / '000_all.qs'}: {n} commands, URL {len(url)} characters")
    if awards:
        n, url = write_batch(folder, "000_all.award-items.qs", awards)
        out.append(
            f"- Award items: `000_all.award-items.qs`, {n} commands from {len(awards)} groups, "
            f"[open in QuickStatements]({url})"
        )
    if pending:
        cmds = [l for p in pending for l in commands(p)]
        (folder / "000_all.pending.qs").write_text(
            "\n".join(cmds) + "\n", encoding="utf-8"
        )
        out.append(
            f"- Pending: `000_all.pending.qs`, waiting for: {', '.join(placeholders(cmds))}. "
            'Run the award-items batch, then tell Claude "<award label> is Q…" to fill in the placeholders.'
        )
    for p in reports:
        text = p.read_text(encoding="utf-8").strip()
        out.append("\n" + re.sub(r"^(#+) ", r"#\1 ", text, flags=re.MULTILINE))
    (folder / "000_all.qs-report.md").write_text(
        "\n".join(out) + "\n", encoding="utf-8"
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument(
        "paths",
        nargs="*",
        default=["articles"],
        help=".wiki files or folders (their .qs files are included)",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="list URLs without archiving"
    )
    args = parser.parse_args()
    if not args.dry_run and not all(IA_KEYS):
        parser.error("IA_ACCESS_KEY and IA_SECRET_KEY must be set")

    wikis, batches = [], []
    for p in map(Path, args.paths):
        if p.is_dir():
            wikis += sorted(p.glob("*.wiki"))
            batches += sorted(q for q in p.glob("*.qs") if qs_kind(q))
        else:
            wikis.append(p)
            batches += [
                q for s in QS_SUFFIXES if (q := p.with_name(p.stem + s)).exists()
            ]

    cache, missing = {}, []
    for f in wikis:
        print(f)
        missing += [(f, u) for u in process_wiki(f, cache, args.dry_run)]
    for f in batches:
        print(f)
        missing += [(f, u) for u in process_qs(f, cache, args.dry_run)]

    if not args.dry_run:
        for folder in sorted({f.parent for f in wikis + batches}):
            rebuild_batches(folder)

    if missing:
        print("\nNo snapshot available for:", file=sys.stderr)
        for f, u in missing:
            print(f"  {f}: {u}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
