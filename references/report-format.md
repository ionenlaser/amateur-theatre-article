# Feedback report (`<base>.report.md`)

For the person reviewing the `{{AIGenerated}}` page. Not uploaded
(`upload_articles.py` only takes `.wiki` files). Build it from the ledger's
`PROBLEM` lines. Only what needs a human: problems, doubts, unread sources.

- One line per point: the claim, the source, what the article does with it.
  Not "Founding year unclear", but "Founding year: Chronik 1946, Kreiszeitung
  2021 1947; article uses 1946".
- No summary of the article, no list of what went well.
- Leave out empty sections (no "None found.").
- Report Wikidata problems here; fixes belong in Step 5.
- For a Wikidata-only stub, list the searches run under "Leads".

```markdown
# Feedback report: <Group name> (<QID>)

## Data conflicts
- <Fact>: <source A> says X, <source B> says Y. Article uses X.

## Possible errors on Wikidata
- P856 http://old-site.de/ is dead; current site is https://new-site.de/.

## Cited but not read
- Kreiszeitung, 12 Mar 2015, <URL>: paywall; cited for the 2015 premiere from the teaser. Check the full text.

## Weak or missing sources
- Founding year only on the group's own site.
- Repertoire: nothing found for 1990–2004; table marked incomplete.

## Leads for further research
- Festschrift "50 Jahre …" (2010), print only.
```
