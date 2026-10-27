---
name: amateur-theatre-article
description: >-
  Create a neutral, referenced MediaWiki article about an amateur theatre group
  from a Wikidata QID. Use whenever the user gives a Q-id (e.g. "Q1747746") and
  wants a wiki article, page, or stub about a theatre troupe / ensemble / Bühne /
  Theaterverein / Laienspielgruppe / Speeldeel, or says "write the Amateur
  Theatre Wiki page for this troupe" or "turn this QID into a wiki article".
  Reads the Wikidata item, researches the group online, and outputs MediaWiki
  markup with {{DynamicInfobox|qid=...}} and {{AIGenerated}}, enwiki interwiki
  links for generic topics, and local links for amateur-theatre topics. Then
  writes referenced Wikidata statements (inception, awards, aliases, social
  media) as a QuickStatements V1 batch. Trigger even when templates are not named. Do
  NOT use for general Wikidata reconciliation or authority-file lookups
  (normdata-search) or the Baroque ceiling-painting corpus (deckenmalerei-lab).
---

# Amateur Theatre Wiki article from a Wikidata QID

Input: one QID. `<base>` = the group's name with spaces as underscores
(`Kellertheater_Hamburg`). Output, all in one folder:

| File | Written in | Spec |
|---|---|---|
| `<base>.wiki` | Step 3 | `references/article-format.md` |
| `<base>.report.md` | Step 4 | `references/report-format.md` |
| `<base>.qs`, `<base>.qs-report.md` | Step 5 | `references/quickstatements.md` |
| `<base>.award-items.qs`, `<base>.pending.qs` | Step 5, only for awards needing a new item | `references/award-items.md` |

`{{DynamicInfobox}}` renders the item's structured data on the wiki. The article
adds prose, context and citations; it does not re-key the infobox.

## Working rules

- Run Steps 1–6 in one go. Stop only at the ⛔ points.
- Read each reference file once, when its step starts. Don't re-read files.
- Send independent calls in parallel (searches, fetches, lookups).
- Never fetch the same URL or run the same query twice.
- Record facts in the **ledger** (below) as you find them. Steps 3–5 work from
  the ledger, not from memory or new research.
- Where a rule gives a default, apply it and move on. Put open doubts in the
  report; don't keep weighing them.
- Never invent facts, dates, titles, QIDs or PIDs.

**Ledger**: keep it terse, one line per source, plus one line per problem:

```
SRC chronik | https://…/chronik | Chronik | Theatergruppe X e. V. | founded 1951; e. V. 1962; 117 members (2019); plays 1951–2024
SRC press1  | https://…/artikel | 70 Jahre … | Kreiszeitung, 12 Mar 2021 | founded 1950 (!); Kulturpreis Achim 2018 for "Krug"
SOCIAL facebook.com/xyz ; instagram.com/xyz ; youtube.com/@xyz   (from site footer)
PROBLEM conflict | founding 1951 (chronik) vs 1950 (press1)
PROBLEM error    | https://…/archiv 404
PROBLEM weak     | venue only on own site
PROBLEM lead     | Festschrift 2001, print only
```

## Step 1 — Read the Wikidata item

1. Load the Wikidata MCP tools once with `tool_search` (e.g. "wikidata get
   statements"). Use the MCP only for Wikidata; web research uses
   `web_search` / `web_fetch`.
2. Call `get_statements(entity_id=<QID>, include_external_ids=true)`. Keep the
   result: Step 5 reuses it.
3. Fetch the sitelinks:
   `https://www.wikidata.org/w/api.php?action=wbgetentities&ids=<QID>&props=sitelinks&format=json`
4. Note: name, description, aliases, P31, P856 (main research seed), P159,
   P571, P1454 (legal form), P463 (umbrella association), P749 (parent
   organisation), social media
   (P2013 Facebook, P2003 Instagram, P2002 X, P2397/P11245 YouTube, P4033
   Mastodon), and Wikipedia sitelink titles.
5. ⛔ P31 is clearly not a theatre group (a person, a place) → stop and ask
   the user.
   ⛔ MCP unavailable or the item can't be read → say so and stop. Never
   fabricate item contents.

Other MCP calls, only if needed: `get_statement_values` for a statement's
qualifiers or references; `search_items` when given a name instead of a QID;
`execute_sparql` for real graph questions only.

## Step 2 — Research

Find every item in the checklist, or confirm it can't be found. Log each find
in the ledger with its URL, title and site.

| Find | Details |
|---|---|
| History | founding (both the group's start and the e. V. founding or registration, if different), milestones, renamings, breaks |
| Kind of theatre | language/dialect (Low German, Bavarian …), genre (comedy, open-air, improv, puppetry, youth, senior) |
| Repertoire | **every** production: year, title, author. Not a selection |
| Venue | named playing space |
| Organisation | legal form (e. V., or a section of a larger club), registered address, umbrella associations, parent organisation: for Wikidata (Step 5), shown by the infobox. Festivals, cooperations, other activities: for the article. Not website operators, imprint names or board members |
| Members | **every dated** member count with its year; split counts (adults + youth) |
| Status | explicit dissolution evidence (register notice, press, own announcement, association list) |
| Awards | exact name, year, awarding body, production, category/rank. Nominations are not awards |
| Websites, social media | every official site; profile links from the site's footer or header |

Order, with each batch sent in parallel:

1. **Seeds**: official homepage plus its subpages `Chronik`, `Archiv`,
   `Rückblick`, `Bisherige Stücke`, `Unsere Stücke`, `Aufführungen`,
   `Historie`, `Über uns`, `Verein`, `Impressum` (whichever exist), and each
   Wikipedia sitelink article.
2. **Searches**: `"<name>"`, `"<name>" Theater <town>`, `"<name>" gegründet`,
   `"<name>" Premiere`, `"<name>" Preis OR Auszeichnung`, `"<name>"
   Mitglieder`, `"<name>" Jubiläum`. Then follow promising results: local and
   regional press (reviews, anniversary reports), city or regional wikis,
   municipal culture pages, umbrella-association member pages, festival
   programmes, awarding bodies' winners lists, Festschrift PDFs.
3. **Repertoire gaps**: list old snapshots with the CDX API instead of the
   Wayback calendar:
   `https://web.archive.org/cdx/search/cdx?url=<domain>/*&output=json&fl=timestamp,original&filter=statuscode:200&collapse=urlkey&limit=200`,
   then fetch the snapshots of history and production pages
   (`https://web.archive.org/web/<timestamp>/<original>`). Fill remaining gaps
   from Wikipedia, press, association and festival pages, and social media.

Scale the depth to the group: a long-running stage with press coverage gets
many more follow-ups than a village group with only a homepage. **Stop
condition**: a checklist item is done when it is found, or when its likely
sources (own site and archive, Wikipedia, targeted searches) have been tried
and the last two searches for it turned up nothing new. Log what's missing as
`PROBLEM weak`.

Source rules:
- The group's own site and social media are primary sources. Use them for
  plain facts (dates, venue, repertoire), never for evaluative claims.
- Add an independent source for a fact even when it is already cited to the
  group's own site.
- A dead website or a gap in productions is not evidence of dissolution.
- Log contradictions, failed pages and own-site-only claims as `PROBLEM` lines.

**No source besides the Wikidata item** → write a Wikidata-only stub (see
`references/article-format.md`). Log the searches you ran as `PROBLEM lead`.

## Step 3 — Write the article

Read `references/article-format.md`, then write `<base>.wiki` from the ledger:

1. Head: `{{AIGenerated}}`, then `{{Stub}}` (only for a Wikidata-only stub),
   then `{{DynamicInfobox|qid=<input QID>}}`.
2. English prose and headings; proper names in their native form. Neutral,
   third person, no promotional wording.
3. Sections: lead, History, Repertoire (table if there are about five or more
   dated productions), Venue, Organisation, Awards, References. Leave out a
   section you can't source. Legal form, address, umbrella associations and
   parent organisation go to Wikidata (Step 5) for the infobox, not into the
   prose; Organisation only holds what the infobox can't show (see the format
   reference).
4. Links: generic topics → `[[wikipedia:Title|text]]`, amateur-theatre topics
   → local `[[Title]]`. Check all `wikipedia:` targets in **one** batched API
   call; drop or replace any that are missing.
5. Refs: basic format, all definitions in the `<references>` block, Wikipedia
   cited by `oldid` (revids fetched in one batched call per language).

## Step 4 — Self-check and feedback report

Check the article; fix any failing point before you go on:

- [ ] Template order and the **input** QID in the infobox; `{{Stub}}` if and only if Wikidata is the only source.
- [ ] Lead bolds the native name and says what and where the group is.
- [ ] Every non-obvious claim is referenced (claims taken only from Wikidata stay unreferenced); no ref repeated sentence after sentence.
- [ ] Every body ref is `<ref name="x" />`, and each name is defined exactly once inside `<references>…</references>`. No purely numeric names (`"2016"`, `"50"`); use e.g. `"season2016"`. No `{{cite …}}` templates.
- [ ] No ref cites Wikidata (no `wikidata.org` URL in any ref). Wikipedia refs use `oldid` permalinks; non-Wikimedia wikis use plain URLs.
- [ ] Every `wikipedia:` target was confirmed by the API; each term is linked once; no `{{Wikipedia article}}`, no External links section, no categories.
- [ ] Every award from the ledger is in Awards with name, year, body and ref.
- [ ] The repertoire table holds every production from the ledger, and its caption says complete or incomplete. No sentence about missing years or productions not found.
- [ ] Organisation has no legal form, address, umbrella association or parent organisation that has a Wikidata item, and no website operators, imprint names or board members. Dropped if nothing else remains.

Then read `references/report-format.md` and write `<base>.report.md` from the
`PROBLEM` lines.

## Step 5 — QuickStatements batch

Read `references/quickstatements.md`. Work only from the article, the ledger and
the Step 1 `get_statements` result; no new research, except:
- no social-media links in the ledger → fetch the homepage once for its profile links;
- an award without an item → read `references/award-items.md` and follow it.

1. List the facts missing from the item (property table in the reference file).
2. Reference each one from the article's ref for that fact.
3. Fix clear errors on the item (`SWITCH_VALUE`, ranks); never remove statements.
4. Write `<base>.qs` and `<base>.qs-report.md` (and the award files, if any).
   Write no batch URLs, no `## Batches` section and no `000_*` files.

## Step 6 — Hand over

In the final message:
1. Name the files written.
2. Tell the user to run `archive_refs.py` and then `build_batches.py` on the
   output folder next. The first adds archive links to refs and `.qs` files, the
   second writes the batch URLs and rebuilds the `000_all.*` files. The batches
   are only ready after that.
3. If award items were proposed: run the award-items batch, then tell Claude
   "<award label> is Q…".
4. List facts outside the default property set (e.g. P973) and ask
   whether to add them to the default set.

Then stop.

## Follow-up: "<award label> is Q…"

Read `references/award-items.md`, section "Resolving placeholders", and follow it
for the whole output folder. No new research.
