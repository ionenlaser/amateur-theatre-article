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
  propose referenced Wikidata statements (inception, aliases, social media) as a
  QuickStatements V1 batch URL. Trigger even when templates are not named. Do
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

Work in four steps. Read `references/wikidata.md` before step 1 and
`references/article-format.md` before step 3. Step 5 (Wikidata enrichment) is
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
- **Record the URL, title, and site of every source you will cite.** You need
  these for the `<ref>` tags. Capture them as you go rather than reconstructing
  them later.

Treat the group's own website as a primary source: fine for plain facts
(founding year, repertoire, venue), but attribute or omit anything evaluative or
promotional. Do not inflate a thin evidence base — it is better to write three
well-sourced sentences than a page of unverifiable filler.

## Step 3 — Write the article

Read `references/article-format.md` for the exact skeleton, the link-routing
rules, the citation style, and a full worked example. The essentials:

1. The article **must** begin with both templates, in this order:
   ```
   {{AIGenerated}}
   {{DynamicInfobox|qid=Q1747746}}
   ```
   Use the *input* QID in the infobox — double-check it matches. `{{AIGenerated}}`
   flags the page for human review, which is exactly why every non-obvious claim
   below it needs a citation.
2. Write in a **neutral, encyclopedic, research register**: third person, no
   promotional adjectives, evaluative claims attributed to a source. Only state
   what the sources support; never invent dates, member counts, or award names.
3. Don't restate the whole infobox in prose. Mention the key facts a reader needs
   for the narrative, and spend the body on context the infobox can't show.
   In the **Repertoire** section, when the sources list about five or more dated
   productions, present them as a `wikitable sortable` (Year / Title / Author /
   Notes) below a short prose summary, cited once in the table caption. Keep a
   few productions, or ones without dates, as prose. See the reference file.
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
   references, not to `wikipedia:` interwiki links. Details are in the reference
   file.

## Step 4 — Deliver and self-check

Before handing it over, verify:
- [ ] `{{AIGenerated}}` present, and `{{DynamicInfobox|qid=...}}` carries the
      **input** QID.
- [ ] Lead sentence bolds the group's native name and says what/where it is.
- [ ] Every non-obvious factual claim is covered by a `<ref>`, and the same ref
      isn't repeated sentence after sentence where one paragraph-end citation
      would do. **Each named ref is defined
      exactly once with content**, every reuse is self-closing, and no self-closing
      tag is left without a content definition (a contentless name — e.g. a
      self-closing `<ref name="x" />` in the body plus a self-closing
      `<references />` — is what causes the "has no content" cite error). All use
      the **basic ref format** (no `{{cite ...}}` templates). Wikipedia sources
      are cited with an `oldid` permalink, not a `/wiki/<Title>` URL.
- [ ] Generic terms use `wikipedia:` interwiki links **whose target pages were
      confirmed to exist on English Wikipedia**; amateur-theatre-scene terms use
      local links; nothing is over-linked.
- [ ] If the group has a German Wikipedia article, the page ends with
      `{{Wikipedia article|<title>}}` after the references.
- [ ] Tone is neutral and verifiable — no promotional language, no invented facts.

When file tools are available, save the wikitext to a `.wiki` file in the
outputs directory and present it, so the user can copy it straight into the wiki.
Otherwise return it in a single fenced code block. The Amateur Theatre Wiki is
**English-language**, so write the prose and section headings in English by
default, while keeping every proper name in its native form (e.g.
`Plattdütsche Vereen Visselhövede`, not a translation). For local wikilinks, match
the wiki's existing page titles exactly — including the legal form, as in
`[[Amateurtheaterverband Niedersachsen e. V.]]`; a target that doesn't exist yet
is a normal redlink, not a problem.

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

Read `references/quickstatements.md` first. Do not start a new research round.
Work from the finished `.wiki` article (re-read it, in case the archive script has
updated it), anything already gathered earlier in the conversation with a recorded
source URL, and one `get_statements` call for the item.

1. Extract the facts the item does **not** already have: inception (`P571`),
   headquarters town (`P159`) and a registered-seat street address (`P6375`
   qualifier on `P159`), official name (`P1448`), **member counts** (`P2124`, one
   statement per dated count, each with a `P585` point-in-time qualifier),
   **dissolution** (`P576`, only with explicit evidence), aliases, **every official website
   found** (`P856`, including a new domain or an extra site), and social-media
   profiles. Facts may be stated in the article or **directly implied** by it (e.g.
   a founding year from "1900" in the name plus a cited 125th anniversary in 2025).
   Websites and social-media profiles count as part of the article because
   `{{DynamicInfobox}}` displays them; if they aren't in the research context, one
   fetch of the official homepage to read its profile links is allowed. Skip
   anything already on the item, and never add person-valued statements.
2. **Reference the non-trivial statements** (dates, locations, addresses, names)
   from the ref the article attaches to that fact: `S854` reference URL + `S813`
   retrieved, plus **`S1065` archive URL and `S2960` archive date when the ref has
   an archive.org link**. Facts sourced from Wikipedia or another Wikimedia project
   get only `S143` (imported from Wikimedia project), with no URL or dates.
   Identifiers (website, social media) and aliases get no reference.
3. Build the V1 command block, percent-encode it programmatically onto
   `https://qs-dev.toolforge.org/batch/new?v1=`, save the commands to a `.qs` file
   beside the article, and show the user both. The link opens a draft the user
   reviews and runs while logged in; nothing is saved automatically.

If the article holds a useful fact of a type outside the default set (e.g.
described at URL `P973`, a member organisation `P463`), propose it and ask whether
it should become part of the default set.
