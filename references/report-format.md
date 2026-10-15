# Feedback report format

Every article gets a feedback report: a Markdown file in the same folder as the
`.wiki` file, named `<base>.report.md`. It is for the person who reviews the
`{{AIGenerated}}` page before or after upload. It is not uploaded
(`upload_articles.py` only picks up `.wiki` files).

The report records what you noticed while researching and writing that the
article itself doesn't show: where sources disagree, what may be wrong, and what
rests on thin evidence. Collect these points during Step 2 rather than
reconstructing them at the end.

## Rules

- **Be specific.** Name the claim, the sources involved (title and URL) and what
  the article does with it. "Founding year unclear" is not useful; "Founding
  year: Chronik says 1946, Kreiszeitung 2021 says 1947; article uses 1946
  (group's own chronicle, more detailed)" is.
- **Keep every heading**, and write "None found." under one with nothing to
  report, so the reviewer sees it was checked.
- One or two lines per point. No prose summary of the article.
- Report problems on Wikidata here; don't fix them in this step. Fixes belong in
  the QuickStatements step or by hand.
- Don't put anything in the report that should have gone into the article: if a
  fact is well sourced, use it there.

## Template

```markdown
# Feedback report: <Group name> (<QID>)

Article: `<base>.wiki`, generated <date>.

## Data conflicts
- <Fact>: <source A> says X, <source B> says Y. Article uses X because …
- <Fact>: Wikidata has X (P571), sources say Y. Article follows the sources.

## Possible errors on Wikidata
- P31 is "theatre" (building), but the item describes the group.
- P856 http://old-site.de/ is dead; current site is https://new-site.de/.

## Errors during research
- https://example.de/chronik returned 404; used the Wayback snapshot of 2019.
- `[[wikipedia:Volksstück]]` dropped: no English Wikipedia article.

## Weak or missing sources
- Founding year sourced only from the group's own site.
- Repertoire: no productions found for 1990–2004; table marked incomplete.
- Member count "about 80" (website, undated): not used.
- Venue section dropped: no source names the playing space.

## Leads for further research
- Festschrift "50 Jahre …" (2010) is mentioned in the press but not online;
  the group or the local library may have it.
- Kreiszeitung articles behind a paywall: <URLs>.
```
