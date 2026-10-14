# amateur-theatre-article

A Claude skill that turns a Wikidata QID for an amateur theatre group into a
neutral, referenced MediaWiki article. It can also propose Wikidata statements
as a QuickStatements batch. See [SKILL.md](SKILL.md) for the full instructions.

## Repository layout

| Path | Purpose |
| --- | --- |
| `SKILL.md` | Skill definition (frontmatter + instructions) |
| `references/` | Reference docs the skill loads on demand |
| `amateur-theatre-article.skill` | Packaged skill, ready to upload |
| `theaterlist.csv` | List of theatre groups on Wikidata (not part of the skill) |

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

## Requirements

- **Wikidata MCP connector**: the skill reads the Wikidata item through it.
  Enable it in Claude.ai under **Settings → Connectors**.
- **Web search / web fetch**: needed for researching the group online.

## License

See [LICENSE](LICENSE).
