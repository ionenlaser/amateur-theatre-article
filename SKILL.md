---
name: amateur-theatre-article
description: >-
  Create a neutral, research-style MediaWiki article about an amateur theatre
  group, starting from a Wikidata QID. Use whenever the user gives a Wikidata
  Q-id (e.g. "Q1747746") and wants a wiki article, page, or stub about a theatre
  troupe / ensemble / Bühne / Theaterverein / Laienspielgruppe / Speeldeel, or
  says things like "write the Amateur Theatre Wiki page for this troupe" or "turn
  this QID into a wiki article". The skill reads the Wikidata item, researches the
  group online via its name and linked websites, and produces referenced
  MediaWiki markup with the {{DynamicInfobox|qid=...}} and {{AIGenerated}}
  templates, interwiki links to English Wikipedia for generic topics, and local
  links for amateur-theatre topics. Trigger even when the user does not name the
  templates. Do NOT use for general Wikidata reconciliation or authority-file
  lookups (normdata-search) or for the Baroque ceiling-painting corpus
  (deckenmalerei-lab).
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
`references/article-format.md` before step 3.

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
   section. **Define each named ref exactly once, with content** —
   `<ref name="x">[URL Title], Site, retrieved DATE.</ref>` — and reuse it
   elsewhere with the self-closing form `<ref name="x" />`. A self-closing
   `<ref name="x" />` whose name has **no content definition anywhere** (including
   a self-closing tag sitting inside the `<references>` block) triggers the
   MediaWiki error *Cite error: `<ref>` tag with name "x" ... has no content*, so
   make sure every name carries its content exactly once. Use the **basic ref
   format only** (`<ref name="x">[URL Title], Site, retrieved DATE.</ref>`); do not
   use `{{cite web}}`, `{{cite news}}`, or other citation templates yet — they are
   not implemented on the wiki. Details are in the reference file.

## Step 4 — Deliver and self-check

Before handing it over, verify:
- [ ] `{{AIGenerated}}` present, and `{{DynamicInfobox|qid=...}}` carries the
      **input** QID.
- [ ] Lead sentence bolds the group's native name and says what/where it is.
- [ ] Every non-obvious factual claim has a `<ref>`. **Each named ref is defined
      exactly once with content**, every reuse is self-closing, and no self-closing
      tag is left without a content definition (a contentless name — e.g. a
      self-closing `<ref name="x" />` in the body plus a self-closing
      `<references />` — is what causes the "has no content" cite error). All use
      the **basic ref format** (no `{{cite ...}}` templates).
- [ ] Generic terms use `wikipedia:` interwiki links **whose target pages were
      confirmed to exist on English Wikipedia**; amateur-theatre-scene terms use
      local links; nothing is over-linked.
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