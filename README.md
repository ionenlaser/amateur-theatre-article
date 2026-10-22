# amateur-theatre-article

A Claude skill that turns a Wikidata QID for an amateur theatre group into a
neutral, referenced MediaWiki article, and proposes the matching Wikidata
statements as a QuickStatements batch in the same run. See [SKILL.md](SKILL.md) for the full instructions.

## Repository layout

| Path | Purpose |
| --- | --- |
| `SKILL.md` | Skill definition (frontmatter + instructions) |
| `references/` | Reference docs the skill loads on demand (`award-items.md` only when an award needs a new item) |
| `amateur-theatre-article.skill` | Packaged skill, ready to upload |
| `theaterlist.csv` | List of theatre groups on Wikidata (not part of the skill) |
| `articles/` | Generated articles (`.wiki`), ready to paste into the wiki, with their feedback reports (`.report.md`), QuickStatements batches (`.qs`, `.award-items.qs`, `.pending.qs`) and reports (`.qs-report.md`), and the folder-wide `000_all.*` batch files |
| `archive_refs.py` | Post-processing: adds Internet Archive snapshots to references and QuickStatements batches |
| `build_batches.py` | Post-processing: writes the batch URLs and the folder-wide `000_all.*` files |
| `upload_articles.py` | Uploads the articles to the wiki |

## Building the `.skill` file

A `.skill` file is a plain zip archive with `SKILL.md` and `references/` at the
archive root. Rebuild it after editing either one:

```sh
rm -f amateur-theatre-article.skill
zip -r amateur-theatre-article.skill SKILL.md references
```

## Installing

### Claude.ai / Claude desktop app

1. Open **Settings → Capabilities** and make sure **Skills** is enabled.
2. Click **Upload skill** and choose `amateur-theatre-article.skill`.
3. To update the skill, delete the old version and upload the new file.

### Claude Code

Claude Code reads skills from folders instead of `.skill` files. Copy or symlink
this repository into a skills directory:

```sh
# for all your projects
ln -s "$PWD" ~/.claude/skills/amateur-theatre-article

# or for a single project only
mkdir -p /path/to/project/.claude/skills
ln -s "$PWD" /path/to/project/.claude/skills/amateur-theatre-article
```

Restart Claude Code; the skill then appears in the skills list.

## Archiving references and building the batches

After generating articles, run `archive_refs.py` to snapshot every cited web page
in the [Internet Archive](https://web.archive.org/) and add the snapshot links to
the articles and QuickStatements batches, then `build_batches.py` to build the
batch URLs. Both are separate steps, not part of the skill, and need only
Python 3 (standard library). Archiving needs archive.org S3 keys
(https://archive.org/account/s3.php):

```sh
export IA_ACCESS_KEY=… IA_SECRET_KEY=…
python3 archive_refs.py --dry-run   # list the URLs it would archive (no keys needed)
python3 archive_refs.py             # archive and update articles/ in place
python3 archive_refs.py articles/Foo.wiki other-folder/   # specific files or folders
python3 build_batches.py            # build the batch files of articles/
python3 build_batches.py other-folder/
```

For each `<ref>`, the script takes the first external link. Wikimedia links
(Wikipedia, Wikidata, …) are skipped, because those are cited with `oldid`
permalinks already. It asks Save Page Now for a capture (reusing one from the last
six months) and appends the result:

```mediawiki
<ref name="site">[https://example.de/ Über uns], Example e.V., retrieved 14 October 2026. [https://web.archive.org/web/20261014120000/https://example.de/ Archived] on 14 October 2026.</ref>
```

If a capture fails, it falls back to the most recent existing snapshot. URLs with
no snapshot at all are listed at the end, and the script exits with status 1.
Refs that already contain a `web.archive.org` link are skipped, so it's safe to
re-run. Requests are paced, so expect roughly 20–60 seconds per URL.

The skill writes the QuickStatements batches with reference URL (S854) and
retrieved date (S813) only. `archive_refs.py` adds archive URL (S1065) and
archive date (S2960) to every reference block in `<base>.qs`,
`<base>.award-items.qs` and `<base>.pending.qs` that has an S854 and no S1065,
reusing the snapshot it took for the article. `build_batches.py` then:

1. writes the `## Batches` section of each `<base>.qs-report.md`, with command
   counts and [QuickStatements 3.0](https://qs-dev.toolforge.org/) links;
2. rebuilds the folder-wide `000_all.qs`, `000_all.qs.url`,
   `000_all.award-items.qs(.url)`, `000_all.pending.qs` and
   `000_all.qs-report.md` from every group in the folder.

Re-run `build_batches.py` after changing a `.qs` file by hand (or after Claude resolved an award
placeholder) to refresh the links and the `000_` files.

## Uploading articles to the wiki

`upload_articles.py` creates one wiki page per `.wiki` file in a folder. The page
title is the file name with underscores as spaces (`Kellertheater_Hamburg.wiki` →
"Kellertheater Hamburg"). It logs in with your normal wiki account (no bot
password needed) and uses only the Python standard library.

```sh
python3 upload_articles.py                 # upload articles/, asks for username and password
WIKI_USER=Name WIKI_PASSWORD=… python3 upload_articles.py
python3 upload_articles.py --overwrite     # also replace pages that already exist
python3 upload_articles.py other-folder/ --summary "New article"
```

Pages that already exist are skipped unless you pass `--overwrite`. Run
`archive_refs.py` first, so the uploaded references include archive links.

## Requirements

- **Wikidata MCP connector**: the skill reads the Wikidata item through it.
  Enable it in Claude.ai under **Settings → Connectors**.
- **Web search / web fetch**: needed for researching the group online.
