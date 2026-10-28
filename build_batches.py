"""Build the QuickStatements batch files of article folders.

Run this after archive_refs.py, or after changing a .qs file by hand. For every
folder it rewrites the "## Batches" section of each <base>.qs-report.md (file names
and counts; the QuickStatements 3.0 URLs go only into .url files) and rebuilds the folder-wide 000_all.qs, 000_all.qs.url,
000_all.award-items.qs(.url), 000_all.pending.qs and 000_all.qs-report.md.

Usage:
    python3 build_batches.py [PATH ...]   # PATH: folders or files in them (default: articles)
"""

import argparse
import datetime as dt
import re
import urllib.parse
from pathlib import Path

QS_BASE_URL = "https://qs-dev.toolforge.org/batch/new?v1="
QS_SUFFIXES = (".award-items.qs", ".pending.qs", ".qs")


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
        out.append(f"- Main batch: `{main.name}`, {len(cmds)} commands")
    if awards.exists() and (cmds := commands(awards)):
        n = sum(l == "CREATE" for l in cmds)
        out.append(f"- Award items: `{awards.name}`, {n} new items")
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
            f"- Main batch: `000_all.qs`, {n} commands from {len(main)} groups; "
            "open `000_all.qs.url`"
        )
        print(f"  {folder / '000_all.qs'}: {n} commands, URL {len(url)} characters")
    if awards:
        n, url = write_batch(folder, "000_all.award-items.qs", awards)
        out.append(
            f"- Award items: `000_all.award-items.qs`, {n} commands from {len(awards)} groups; "
            "open `000_all.award-items.qs.url`"
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
        help="folders, or files whose folder is rebuilt",
    )
    args = parser.parse_args()
    for folder in sorted(
        {p if p.is_dir() else p.parent for p in map(Path, args.paths)}
    ):
        print(folder)
        rebuild_batches(folder)


if __name__ == "__main__":
    main()
