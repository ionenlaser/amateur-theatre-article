# Feedback report (`<base>.report.md`)

For the person reviewing the `{{AIGenerated}}` page. Not uploaded
(`upload_articles.py` only takes `.wiki` files). Build it from the ledger's
`PROBLEM` lines.

- Be specific: the claim, the sources (title + URL), what the article does with it.
  Not "Founding year unclear", but "Founding year: Chronik says 1946, Kreiszeitung
  2021 says 1947; article uses 1946 (own chronicle, more detailed)".
- One or two lines per point. No summary of the article.
- Keep every heading; write "None found." under an empty one.
- Report Wikidata problems here; fixes belong in Step 5.
- A well-sourced fact belongs in the article, not here.
- For a Wikidata-only stub, list the searches run under "Leads".

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
- Venue section dropped: no source names the playing space.

## Leads for further research
- Festschrift "50 Jahre …" (2010) mentioned in the press, not online; the group or the local library may have it.
- Kreiszeitung articles behind a paywall: <URLs>.
```
