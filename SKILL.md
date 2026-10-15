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
  links for generic topics, and local links for amateur-theatre topics. Can also
  propose referenced Wikidata statements (inception, awards, aliases, social
  media) as a QuickStatements V1 batch URL. Trigger even when templates are not named. Do
  NOT use for general Wikidata reconciliation or authority-file lookups
  (normdata-search) or the Baroque ceiling-painting corpus (deckenmalerei-lab).
---

# Amateur Theatre Wiki article from a Wikidata QID

Turn a single Wikidata QID into a finished, referenced MediaWiki article about an
amateur theatre group, suitable for pasting into the Amateur Theatre Wiki.

The wiki's `{{DynamicInfobox}}` template pulls the *structured* facts (founding
date, location, members, website, identifiers) straight from Wikidata when the
page renders. So your job is **not** to re-key that structured data. Your job is
to read the item just enough to know *what the group is called* and *where to go
looking*, then write the prose, the context, and the citations that Wikidata and
the infobox cannot supply on their own.

Work in four steps. Read `references/wikidata.md` before step 1,
`references/article-format.md` before step 3 and `references/report-format.md`
before step 4, which ends with a feedback report. Step 5 (Wikidata enrichment) is
optional and runs only when the user asks for it; read
`references/quickstatements.md` before it.

## Step 1 — Read the Wikidata item

Goal: get the group's **name**, a one-line **description**, and every
**outbound link** you can use as a research seed (official website, social media,
and the title of any linked Wikipedia article).

**Read Wikidata through the Wikidata MCP — and use the MCP *only* for Wikidata.**
The web research in step 2 is plain `web_search` / `web_fetch`; the MCP is not a
general web tool. The MCP tools are deferred, so load them once with `tool_search`
(e.g. `tool_search("wikidata get statements")`), then call them directly.

The whole read is usually a single call:

```
Wikidata:get_statements(entity_id="Q122798923", include_external_ids=true)
```

It returns one statement per line with labels already resolved, plus the item's
description and aliases — for example the name, `official website (P856)`,
`headquarters location (P159)`, `member of (P463)`, and `instance of (P31)`. That
is everything you need: the name, the description, and the official-website seed.
`references/wikidata.md` lists the properties worth reading and the few cases that
need a follow-up call (`get_statement_values` for a property's qualifiers/sources,
`search_items` if you were given a name instead of a QID, `execute_sparql` only
for genuine graph questions).

Always confirm `instance of (P31)` denotes a theatre group / troupe / ensemble,
not an unrelated entity that happens to share the id. If it clearly is not (e.g.
it resolves to a person or a place with no theatrical sense), stop and check with
the user rather than writing an article about the wrong subject.

Note: the structured facts you read (location, inception, members) are rendered
on-wiki by `{{DynamicInfobox}}` from the same QID, so you only need them to verify
and phrase the prose — the name and a seed URL or two are enough to proceed.

## Step 2 — Research the group on the web

Using the name and the seed links, gather the material a neutral article needs:
founding and history, the kind of theatre it does (Low German / `Plattdeutsch`,
improvisation, puppetry, youth, senior, open-air, etc.), notable productions,
its venue, legal form (`e.V.`), and any festival participation, association
membership, or press coverage.

- `web_fetch` the **official website** and the **linked Wikipedia article**
  first; these are your strongest sources.
- Run a handful of targeted `web_search` queries (name + "Theater", name +
  town, name + "gegründet", name + "Premiere"/"Inszenierung"). Scale to the
  group's footprint: a long-running stage with press coverage warrants more
  searches than a small village `Laienspielgruppe` with only its own homepage.
- **Cast a wide net for independent sources and cite each useful one.** Beyond the
  group's own site and Wikipedia, look for local and regional newspaper articles
  (premiere reviews, anniversary reports), city or regional wikis (e.g. a
  Stadtwiki), municipal culture pages, umbrella-association member pages,
  festival programmes, and the group's social-media pages. Each extra source
  that confirms or adds a fact makes the article more verifiable. Prefer it over
  the group's own site for the same claim, and add it as a ref even when the fact
  is already cited once. Social-media pages are primary sources: fine for plain
  facts like a premiere date or venue, never for evaluative claims.
- **Look explicitly for member counts and activity status.** Club pages, annual
  reports, chronicles, anniversary press articles and association member lists
  often give a number of members for a stated year ("117 Mitglieder, Stand 2019").
  Note **every dated count** you find, with its year and source, not just the
  latest. Also note any evidence that the group is no longer active: a
  dissolution notice (Auflösung, Liquidation) in the register of associations or
  the press, an announcement on its own site, or an umbrella association listing it
  as dissolved. A dead website or a long gap in productions alone is not evidence of
  dissolution; mention it in the article only if a source says so.
- **Look explicitly for awards and prizes the group received** (`Preis`,
  `Auszeichnung`, `Kulturpreis`, festival prizes, amateur-theatre awards such as
  those of umbrella associations or regional culture prizes). For each one, note
  the **exact award name**, the **year**, the **awarding body**, the **production**
  it was given for (if any), any **category or rank** (1st prize, audience award),
  and the source. Press reports, the group's chronicle, the awarding body's list of
  winners, and festival pages are typical sources; prefer the awarding body's own
  list when you can find it. Nominations and shortlists are not awards; mention
  them only as such.
- **Try to assemble the complete repertoire.** Aim for a list of *every*
  production the group has staged, each with year, title and author, not just a
  few highlights. Look for the group's own production history first: pages
  titled `Chronik`, `Archiv`, `Rückblick`, `Bisherige Stücke`, `Unsere Stücke`,
  `Aufführungen` or `Historie`, and anniversary brochures (Festschrift) as PDFs.
  If the current site only shows recent seasons, check older snapshots of the
  site on the Wayback Machine (`web.archive.org/web/*/<domain>*`) for earlier
  seasons. Fill gaps from the German Wikipedia article, press reviews,
  umbrella-association and festival pages, and the group's social media. Merge
  the sources into one list, sorted by year, and keep track of which source
  covers which rows. If the history stays incomplete after a reasonable search
  (missing years, productions without title or author), keep what you found and
  note the gaps; never fill them by guessing.
- **Note problems as you go** for the feedback report (Step 4): sources that
  contradict each other or the Wikidata item, pages that fail to load, and
  claims you could only source from the group itself.
- **Record the URL, title, and site of every source you will cite.** You need
  these for the `<ref>` tags. Capture them as you go rather than reconstructing
  them later.

Treat the group's own website as a primary source: fine for plain facts
(founding year, repertoire, venue), but attribute or omit anything evaluative or
promotional. Do not inflate a thin evidence base — it is better to write three
well-sourced sentences than a page of unverifiable filler.

**If nothing turns up besides the Wikidata item** (no website, no Wikipedia
article, no press, no association or festival page, no social media), write a
**Wikidata-only stub**: a short lead built from the item's statements, cited to
the item itself, and marked with `{{Stub}}`. Don't pad it with general text about
the town or the genre. See "Wikidata-only stubs" in `references/article-format.md`.

## Step 3 — Write the article

Read `references/article-format.md` for the exact skeleton, the link-routing
rules, the citation style, and a full worked example. The essentials:

1. The article **must** begin with both templates, in this order:
   ```
   {{AIGenerated}}
   {{DynamicInfobox|qid=Q1747746}}
   ```
   When the only source is the Wikidata item, add `{{Stub}}` between them
   (`{{AIGenerated}}`, `{{Stub}}`, `{{DynamicInfobox|…}}`). It shows a notice
   asking readers to contribute and adds the page to `Category:Stub`. Don't use
   it when any other source was found, however thin.
   Use the *input* QID in the infobox — double-check it matches. `{{AIGenerated}}`
   flags the page for human review, which is exactly why every non-obvious claim
   below it needs a citation.
2. Write in a **neutral, encyclopedic, research register**: third person, no
   promotional adjectives, evaluative claims attributed to a source. Only state
   what the sources support; never invent dates, member counts, or award names.
   **Awards the group received** go in their own `== Awards ==` section (prose
   for one or two, a short list for more), each with year, awarding body, the
   production it honoured, and a ref. See the reference file.
3. Don't restate the whole infobox in prose. Mention the key facts a reader needs
   for the narrative, and spend the body on context the infobox can't show.
   In the **Repertoire** section, when the sources list about five or more dated
   productions, present them as a `wikitable sortable` (Year / Title / Author /
   Notes) below a short prose summary. Include **every production you found**,
   not a selection; caption it "Productions" when the list is complete and
   "Productions (incomplete)" when it has known gaps. Cite it once in the caption
   when one source covers all rows, otherwise per row for the rows from other
   sources. Keep a few productions, or ones without dates, as prose. See the
   reference file.
4. **Link routing** — this is the rule the user cares about most:
   - generic, general-knowledge topics → **interwiki link to English Wikipedia**
     using the `wikipedia:` prefix, e.g.
     `[[wikipedia:Improvisational theatre|improvisational theatre]]`,
     `[[wikipedia:Low German|Low German]]`, `[[wikipedia:Hanover|Hanover]]`.
   - topics that live inside the Amateur Theatre Wiki's own scope (other troupes,
     scene-specific festivals, associations the wiki documents) → **local
     wikilink**, e.g. `[[Niedersächsische Amateurtheatertage]]`.
   When unsure, ask "would a general encyclopedia have this article?" — if yes,
   interwiki; if it's specific to the amateur-theatre world this wiki covers,
   local. Don't over-link; link a term once, on first mention.
   **Verify every `wikipedia:` target actually exists before linking it.** A
   plausible-looking English title is often a dead link — English Wikipedia has no
   `Volksstück` article, for instance, so `[[wikipedia:Volksstück|Volksstück]]`
   would be broken. Confirm the page resolves first: a quick `web_search` for the
   title usually suffices (check that a real `en.wikipedia.org/wiki/<Title>`
   article for *that* concept comes up, not a German-Wikipedia page or a redirect
   to something unrelated), or look the concept up on Wikidata and confirm an
   English-Wikipedia sitelink. If the exact title is missing, link a broader or
   synonymous article you have confirmed exists, or leave the term as plain text —
   never ship a `wikipedia:` link to a non-existent page. Local wikilinks need no
   such check: a missing local target is a normal, useful redlink.
5. **Reference** every cited claim with `<ref>` tags and close with a references
   section. **Don't repeat the same ref after every sentence**: when several
   sentences or a whole paragraph come from one source, cite it once after the
   last of them (paragraph-wide citation). Repeat a ref only where the source
   changes or a single claim is surprising, contested or quoted. **Define each named ref exactly once, with content** —
   `<ref name="x">[URL Title], Site, retrieved DATE.</ref>` — and reuse it
   elsewhere with the self-closing form `<ref name="x" />`. A self-closing
   `<ref name="x" />` whose name has **no content definition anywhere** (including
   a self-closing tag sitting inside the `<references>` block) triggers the
   MediaWiki error *Cite error: `<ref>` tag with name "x" ... has no content*, so
   make sure every name carries its content exactly once. Use the **basic ref
   format only** (`<ref name="x">[URL Title], Site, retrieved DATE.</ref>`); do not
   use `{{cite web}}`, `{{cite news}}`, or other citation templates yet — they are
   not implemented on the wiki. When citing a **Wikipedia article** (any
   language), cite the exact revision you read with an `oldid` permalink —
   `https://de.wikipedia.org/w/index.php?title=<Title>&oldid=<revid>` — never the
   plain `/wiki/<Title>` URL; get the current revid from the wiki's API
   (`action=query&prop=revisions&rvprop=ids&titles=<Title>`). This applies only to
   references, not to `wikipedia:` interwiki links. The `oldid` rule is **only for
   Wikimedia projects** (Wikipedia, Wikisource, Commons, …). Other MediaWiki sites,
   such as regional or city wikis (AW-Wiki, Stadtwikis), are ordinary websites:
   cite their plain page URL like any other web source, so the page can be
   archived and referenced normally. Details are in the reference file.

## Step 4 — Deliver and self-check

Before handing it over, verify:
- [ ] `{{AIGenerated}}` present, and `{{DynamicInfobox|qid=...}}` carries the
      **input** QID.
- [ ] `{{Stub}}` follows `{{AIGenerated}}` if, and only if, the Wikidata item
      is the article's only source.
- [ ] Lead sentence bolds the group's native name and says what/where it is.
- [ ] Every non-obvious factual claim is covered by a `<ref>`, and the same ref
      isn't repeated sentence after sentence where one paragraph-end citation
      would do. **Each named ref is defined
      exactly once with content**, every reuse is self-closing, and no self-closing
      tag is left without a content definition (a contentless name — e.g. a
      self-closing `<ref name="x" />` in the body plus a self-closing
      `<references />` — is what causes the "has no content" cite error). All use
      the **basic ref format** (no `{{cite ...}}` templates). Wikipedia sources
      are cited with an `oldid` permalink, not a `/wiki/<Title>` URL; non-Wikimedia
      wikis are cited with their plain page URL, never an `oldid` link.
- [ ] Generic terms use `wikipedia:` interwiki links **whose target pages were
      confirmed to exist on English Wikipedia**; amateur-theatre-scene terms use
      local links; nothing is over-linked.
- [ ] No `{{Wikipedia article}}` template: the infobox links Wikipedia from
      Wikidata.
- [ ] Every award found in research is in the `Awards` section with its exact
      name, year, awarding body and a ref; nominations aren't presented as wins.
- [ ] The Repertoire table lists every production found in research (not a
      selection), each row is covered by a ref, and the caption says whether the
      list is complete or incomplete.
- [ ] Tone is neutral and verifiable — no promotional language, no invented facts.
- [ ] The feedback report `<base>.report.md` sits next to the article and lists
      every conflict, error and weak source you noticed while writing.

When file tools are available, save the wikitext to a `.wiki` file in the
outputs directory (with the feedback report next to it, see below) and present
it, so the user can copy it straight into the wiki.
Otherwise return it in a single fenced code block. The Amateur Theatre Wiki is
**English-language**, so write the prose and section headings in English by
default, while keeping every proper name in its native form (e.g.
`Plattdütsche Vereen Visselhövede`, not a translation). For local wikilinks, match
the wiki's existing page titles exactly — including the legal form, as in
`[[Amateurtheaterverband Niedersachsen e. V.]]`; a target that doesn't exist yet
is a normal redlink, not a problem.

### Write the feedback report

After the article, write a feedback report as a Markdown file **in the same
folder**, with the article's base name plus `.report.md`
(`Kellertheater_Hamburg.wiki` → `Kellertheater_Hamburg.report.md`). It is for the
human reviewer who checks the `{{AIGenerated}}` page, so be specific: name the
claim, the sources involved and their URLs, and what you would check. Read
`references/report-format.md` for the template. It covers:

- **Data conflicts**: facts on which sources disagree (founding year, names,
  production years, member counts), and facts where the Wikidata item disagrees
  with the sources. Say which version the article uses and why.
- **Possible errors on Wikidata**: statements that look wrong or outdated
  (wrong P31, wrong town, a dead official website, a merged or duplicate item).
  Report them; don't fix them here.
- **Errors and problems in the research**: pages that failed to load, dead or
  redirected links, a source you could only read partly, a `wikipedia:` link
  you dropped because the target doesn't exist.
- **Weak or missing sources**: claims that rest only on the group's own site or
  social media, sections or facts you dropped because no source supported them,
  and gaps such as missing repertoire years or an undated member count.
- **Leads for further research**: sources you found but could not access
  (print articles, Festschrift, paywalled press), and who might hold them. For a
  Wikidata-only stub, list the searches you ran, so the next person doesn't
  repeat them.

Keep each point to a line or two. Write "None found." under a heading rather
than dropping it, so the reviewer sees it was checked. The report is not
uploaded: `upload_articles.py` only picks up `.wiki` files.

### Recommend the next steps (do not run them)

After delivering the article, tell the user what can follow, in this order, and
stop there:

1. **Archive the references.** If the user has the `archive_refs.py`
   post-processing script (see the skill repository's README), recommend running
   it on the output folder. It adds archive.org snapshot links to the references.
2. **Wikidata enrichment.** Offer to generate a QuickStatements batch from the
   finished article (Step 5), ideally after archiving, so the archive links can be
   used as references.

Do **not** start Step 5 on your own after writing the article; wait for the user.

## Step 5 — Wikidata enrichment via QuickStatements (on request only)

Read `references/quickstatements.md` first. Do not start a new research round,
except for awards that need a new Wikidata item (point 4).
Work from the finished `.wiki` article (re-read it, in case the archive script has
updated it), anything already gathered earlier in the conversation with a recorded
source URL, and one `get_statements` call for the item.

1. Extract the facts the item does **not** already have: inception (`P571`; with two
   relevant dates, add both with `P1013` criterion used = `Q132555` de jure for the
   e. V. founding or registration and `Q712144` de facto for the group's actual
   start, and add a task for the user to set one as preferred after the upload),
   headquarters town (`P159`) and a registered-seat street address (`P6375`
   qualifier on `P159`), official name (`P1448`), **legal form** (`P1454`, usually `Q9299236`
   registered association for an e. V.; not for a section of a larger club), **member counts** (`P2124`, one
   statement per dated count, each with a `P585` point-in-time qualifier; sum
   split counts such as adults + youth, date an undated count to the current
   year, and add vague counts like "about 80" with `P1480` = `Q5727902` circa),
   **dissolution** (`P576`, only with explicit evidence), **awards received**
   (`P166`, one statement per award and year, with `P585` and, where the item
   exists, `P1027` conferred by and `P1686` for work), aliases, **every official website
   found** (`P856`, including a new domain or an extra site), and social-media
   profiles. Facts may be stated in the article or **directly implied** by it (e.g.
   a founding year from "1900" in the name plus a cited 125th anniversary in 2025).
   Websites and social-media profiles count as part of the article because
   `{{DynamicInfobox}}` displays them; if they aren't in the research context, one
   fetch of the official homepage to read its profile links is allowed. Skip
   anything already on the item, and never add person-valued statements.
2. **Reference the non-trivial statements** (dates, locations, addresses, names,
   awards) from the ref the article attaches to that fact: `S854` reference URL + `S813`
   retrieved, plus **`S1065` archive URL and `S2960` archive date when the ref has
   an archive.org link**. Facts sourced from Wikipedia or another Wikimedia project
   get only `S143` (imported from Wikimedia project), with no URL or dates.
   Identifiers (website, social media) and aliases get no reference.
3. Build the V1 command block, percent-encode it programmatically onto
   `https://qs-dev.toolforge.org/batch/new?v1=` (QS 3.0, for every batch: the
   classic tool has no URL import), save the commands to a `.qs` file
   beside the article, and show the user both. The link opens a draft the user
   reviews and runs while logged in; nothing is saved automatically.
4. **Awards without a Wikidata item.** An award becomes a `P166` statement only
   if the award has an item. When it has none (checked with `search_items` on
   the native and the English name), decide whether it deserves one: it must be
   an **official, concrete prize**, with a fixed name, an identifiable awarding
   body, and evidence that it is awarded as such (a winners list, a statute, press
   about the award itself). Generic or one-off honours (a certificate of thanks,
   "Sonderapplaus", a festival invitation, an unnamed jury mention) don't
   qualify. For each qualifying award, research the award itself (this is the one
   new research round allowed in Step 5), then write a separate creation batch,
   `<base>.award-items.qs`, with the typical award statements listed in
   `references/quickstatements.md`. Write the group's `P166` lines for it to
   `<base>.pending.qs` with the placeholder `Q<NEW: <Lde label>>`, and list them
   in the report. If another group in the folder already proposed the same
   award, reuse its placeholder instead of writing a second `CREATE` block.
   Never create items for the awarding body or for people.
5. **Write the QuickStatements report** next to the article as
   `<base>.qs-report.md` (template in `references/quickstatements.md`): what the
   batch adds, what was skipped and why, conflicts between the item and the
   article, the award items proposed for creation (and awards rejected as not
   concrete enough), possible errors on the item that need a manual fix, and
   facts outside the default set.
6. **Regenerate the folder-wide batch files** (see "Folder-wide batch files" in
   `references/quickstatements.md`): `000_all.qs` with its `000_all.qs.url`,
   `000_all.award-items.qs` with its `.url` if any group has award items,
   `000_all.pending.qs` if any lines wait for a new award, and the combined
   `000_all.qs-report.md`, and `000_all.tasks.md` if any report has tasks for
   after the upload. The `000_` prefix sorts them before every
   group's files. Rebuild them from all groups in the folder, not only the
   current one.

**When the user reports a created award** ("<award label> is Q…"), resolve its
placeholder across the whole output folder as described in "Resolving
placeholders after the award item is created" in `references/quickstatements.md`:
verify the item, move the pending lines into each group's `.qs`, delete the run
`CREATE` block, update the reports and regenerate the `000_` files. When
presenting award-items batches, always tell the user this is the next step.

If the article holds a useful fact of a type outside the default set (e.g.
described at URL `P973`, a member organisation `P463`), propose it and ask whether
it should become part of the default set.
