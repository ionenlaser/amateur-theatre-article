# Article format, links, citations, and a worked example

## Skeleton

```mediawiki
{{AIGenerated}}
{{DynamicInfobox|qid=Q#######}}

'''<Native name>''' is a <type> amateur theatre group based in
[[wikipedia:<Town>|<Town>]], <region>, Germany.<ref name="site">[<official URL> <page title>], <Group> e.V., retrieved <date>.</ref> <One or two more
lead sentences: what it does, when founded, notable for what.>

== History ==
<Founding, milestones, continuity. Cite each non-obvious fact.>

== Repertoire ==
<Kind of theatre, languages performed, recurring genres, notable productions.>

== Venue ==        <!-- only if the group has a named, documented playing space -->
<Where it performs.>

== Organisation ==
<Legal form (e.V.), membership in associations, festival participation.>

== References ==
<references />

{{Wikipedia article|<German Wikipedia title>|<Native name>}}   <!-- only if a German Wikipedia article exists -->
```

Notes on the skeleton:

- **Wikipedia article note.** If the group has a German Wikipedia article, end
  the page with `{{Wikipedia article|<title>}}` as its very last line, after the
  references. Parameter 1 is the German Wikipedia title, parameter 2 the name shown
  in bold (omit it when identical to the title). It renders "**Name** on German
  Wikipedia" with a link. It's not a source, so it doesn't replace citing
  Wikipedia in `<ref>`s.

- The Amateur Theatre Wiki is English-language, so headings are in English by
  default (`History`, `Repertoire`, `Venue`, `Organisation`, `References`). Keep
  proper names native in either case.
- **No `External links` section.** `{{DynamicInfobox}}` already shows the official
  website and social-media profiles from Wikidata, so don't repeat them in a
  link list. A URL that matters as a source belongs in a `<ref>`.
- Drop any section you cannot source. A short, fully-referenced stub is a better
  outcome than padded sections. Three solid sentences under a single lead can be
  enough for a small group.
- Do not add a hand-written infobox or repeat the infobox's structured fields as
  a list — `{{DynamicInfobox}}` renders them from Wikidata.
- For **local** wikilinks, match the wiki's existing page titles exactly,
  including the legal form: `[[Amateurtheaterverband Niedersachsen e. V.]]`,
  `[[Bund Deutscher Amateurtheater (BDAT)]]`. Confirm the exact title with a quick
  search of the wiki when in doubt; a not-yet-written target shows as a redlink,
  which is fine and even useful for surfacing wanted pages.
- Categories: Don't add categories

### Production tables in the Repertoire section

When the sources list **roughly five or more dated productions**, put them in a
MediaWiki table under `== Repertoire ==` instead of a long sentence of titles.
Keep one or two prose sentences above the table for what the list can't show:
genres, language, how many productions a year, how the repertoire changed.
With fewer productions, or ones without years, stay with prose.

```mediawiki
== Repertoire ==
The group stages one open-air production each summer. Its early seasons were
devoted to Shakespeare; later productions include modern and contemporary drama.<ref name="dewiki" />

{| class="wikitable sortable"
|+ Selected productions<ref name="dewiki" />
! Year !! Title !! Author !! Notes
|-
| 2001 || ''Much Ado About Nothing'' || [[wikipedia:William Shakespeare|William Shakespeare]] || First production
|-
| 2006 || ''[[wikipedia:Baal (play)|Baal]]'' || [[wikipedia:Bertolt Brecht|Bertolt Brecht]] ||
|-
| 2007 || ''[[wikipedia:The Visit (play)|The Visit]]'' || [[wikipedia:Friedrich Dürrenmatt|Friedrich Dürrenmatt]] ||
|}
```

Table rules:

- Use `class="wikitable sortable"`, sorted by year, oldest first. Columns:
  **Year**, **Title**, **Author** (or "after" + author for adaptations), and an
  optional **Notes** column for director, venue, premiere or award. Drop columns
  the sources don't fill. An empty Author column for a whole table helps nobody.
- Titles in italics, in the language the group performed them. Add the English
  title in brackets only when the play is well known under it.
- **Cite the table once**, in its caption (`|+ … <ref …/>`), when one source covers
  every row. Add a ref in a row only for the rows that come from a different source.
  Don't put the same ref in every row.
- Linking follows the usual rules: link a play or author to English Wikipedia only
  when that article exists, and link each one once, at first mention in the table.
- Keep it selective. For a group with decades of productions, list the notable or
  representative ones (first production, anniversaries, award winners, recent
  seasons) and say so in the caption ("Selected productions"). Don't copy a
  complete production history.

## Link routing: interwiki vs. local

The deciding question for every link: **would a general-purpose encyclopedia
have an article on this?**

- **Yes -> interwiki to English Wikipedia**, using the `wikipedia:` prefix:
  `[[wikipedia:Improvisational theatre|improvisational theatre]]`,
  `[[wikipedia:Low German|Low German]]`, `[[wikipedia:Puppetry|puppetry]]`,
  `[[wikipedia:Hanover|Hanover]]`,
  `[[wikipedia:Voluntary association#Germany|registered association]]`.
  These are art forms, languages, places, and general institutions.
- **No, it's specific to the amateur-theatre world this wiki documents -> local
  wikilink**: other troupes the wiki covers, scene-specific festivals and
  meetings, and associations the wiki has pages for, e.g.
  `[[Verband Bayerischer Amateurtheater e. V.]]`,
  `[[Niedersächsische Amateurtheatertage]]`, or a sister group
  `[[English Theatre Buxtehude]]`.

`wikipedia:` is this wiki's interwiki prefix for English Wikipedia; use it
consistently. Link a term **once**, at first mention, and don't link the
blindingly obvious ("theatre", "Germany"). Over-linking reads as noise and is a
common review complaint.

**Verify the target exists before you link it.** A `wikipedia:` link must point at
a real English Wikipedia title; a confident-looking guess is often a dead link.
`[[wikipedia:Volksstück|Volksstück]]`, for instance, looks reasonable but English
Wikipedia has no `Volksstück` article (the concept lives only on German Wikipedia).
Before emitting a `wikipedia:` link, confirm the page exists:

- A quick `web_search` for the title is usually enough — check that a real
  `en.wikipedia.org/wiki/<Title>` article for *that* concept comes up, not a
  German-Wikipedia page, a disambiguation stub, or a redirect to something
  unrelated.
- For a definitive check, look the concept up on Wikidata and confirm it has an
  English-Wikipedia sitelink (e.g. via `execute_sparql`, a row where
  `?article schema:about wd:Q… ; schema:isPartOf <https://en.wikipedia.org/>`).

If the exact title does not exist, link a broader or synonymous article you *have*
confirmed (only if it genuinely exists), or simply leave the term as plain text —
an unlinked word is better than a broken interwiki link. Local wikilinks need no
such check: a missing local page is a normal redlink, even a useful one for
surfacing wanted pages.

## Citations

Every non-obvious factual claim is covered by a `<ref>`. Reuse a source with a named
ref rather than repeating it.

### Don't repeat the same ref after every sentence

When consecutive sentences, or a whole paragraph, all come from the same source,
cite it **once**: after the last sentence it supports, normally at the end of the
paragraph. A paragraph-wide citation covers every sentence before it back to the
previous ref. Repeat a ref inside a paragraph only when the sources change:

```mediawiki
<!-- avoid -->
The group was founded in 1954.<ref name="dewiki" /> It moved into the basement in 1966.<ref name="dewiki" /> At first it staged one play a year.<ref name="dewiki" />

<!-- prefer -->
The group was founded in 1954. It moved into the basement in 1966. At first it staged one play a year.<ref name="dewiki" />

<!-- sources change mid-paragraph: close each run with its own ref -->
The group was founded in 1954 and moved into the basement in 1966.<ref name="dewiki" /> In 2014 it staged 22 productions.<ref name="press" />
```

Exceptions: put a ref straight after a sentence holding a contested, surprising or
quoted claim (a superlative, an award, a figure), even when the same source closes
the paragraph. A short article that relies on one source can end up with a single
ref per paragraph, and that's fine.

Use the **basic ref format only** — a bracketed external link plus a short plain
description. Citation templates such as `{{cite web}}` / `{{cite news}}` are **not
implemented on the wiki yet**, so do not use them; they would render as visible
template-call text.

```mediawiki
<ref name="site">[https://example-troupe.de/ Über uns], Theatergruppe Example e.V., retrieved 29 June 2026.</ref>
```

Reuse: `<ref name="site" />`

### Wikipedia sources: cite the revision (`oldid`)

When a Wikipedia article (any language) is a source, link the **exact revision you
read**, not the live page, so reviewers see the text the claim was based on even
after the article changes. Look up the current revision id:

```text
https://de.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=ids&titles=Kellertheater_Hamburg&format=json
-> "revid": 266247510
```

and cite it as:

```mediawiki
<ref name="dewiki">[https://de.wikipedia.org/w/index.php?title=Kellertheater_Hamburg&oldid=266247510 Kellertheater Hamburg], German Wikipedia, retrieved 14 October 2026.</ref>
```

Never use `https://de.wikipedia.org/wiki/<Title>` in a reference. This rule is for
references only; `[[wikipedia:...]]` interwiki links keep using plain titles.

**Only Wikimedia projects get `oldid` permalinks.** Regional, city or club wikis that
happen to run MediaWiki (AW-Wiki, Stadtwikis, GenWiki, …) are not Wikimedia
projects. Cite them like any other website, with the plain page URL as it appears
in the browser:

```mediawiki
<ref name="awwiki">[https://www.aw-wiki.de/index.php/Theatergruppe_1983_Westum_e.V. Theatergruppe 1983 Westum e.V.], AW-Wiki, retrieved 14 October 2026.</ref>
```

An `index.php?…&oldid=…` URL on such a wiki often can't be captured by the
archive script, and in the QuickStatements step it would wrongly look like a
Wikimedia source. Those sources get `S854` + `S813` (plus archive pairs) like any
web page, never `S143`.

### Define each name once, with content; reuse it self-closing

The full citation (bracketed link + description) must appear **exactly once** for
each ref name. Every other appearance of that name is the self-closing
`<ref name="site" />`. If a name is *only* ever used self-closing — with no
definition carrying content anywhere on the page — MediaWiki raises:

> Cite error: `<ref>` tag with name "site" defined in `<references>` group "" has no content.

Two valid patterns; pick one and apply it to every source:

- **Define at first use** — put the content in the body the first time the source
  is cited, then reuse self-closing, and close with a self-closing `<references />`:

  ```mediawiki
  ... based in Munich.<ref name="site">[https://example-troupe.de/ Über uns], Theatergruppe Example e.V., retrieved 29 June 2026.</ref>
  ...
  == References ==
  <references />
  ```

- **Define in the references block** — keep the body refs all self-closing and give
  every name its content inside a `<references>...</references>` block (note: this
  block is **not** self-closing):

  ```mediawiki
  ... based in Munich.<ref name="site" />
  ...
  == References ==
  <references>
  <ref name="site">[https://example-troupe.de/ Über uns], Theatergruppe Example e.V., retrieved 29 June 2026.</ref>
  </references>
  ```

The failure mode to avoid is the mix that leaves a name contentless: a self-closing
`<ref name="site" />` in the body **and** a self-closing `<references />`, with the
content defined nowhere.

For a news article, keep the same shape — title, work, date — without a template:

```mediawiki
<ref name="press">[https://example-paper.de/article Headline of the article], Example-Zeitung, 20 November 2025, retrieved 29 June 2026.</ref>
```

Guidance:

- Cite every useful source you find. When an independent source (local
  newspaper, city wiki, association page) confirms a fact already cited to the
  group's own site or Wikipedia, add it as a second ref on that sentence. Don't
  go beyond two or three refs on one sentence, and don't re-cite the same fact in
  lead and body.
- Prefer independent sources (press, association pages, a linked Wikipedia
  article's own sources) for anything evaluative; use the group's own site for
  plain facts and attribute it.
- Use a real retrieval date (today's date) rather than a placeholder.
- Close with `<references />` when refs are defined inline at first use, or with a
  populated `<references>...</references>` block when you collect them there. Either
  is fine — just be consistent and make sure every name carries its content exactly
  once, so no name is left contentless (see "Define each name once" above).

## Neutral, research register

`{{AIGenerated}}` tells human reviewers the text was machine-drafted, so the
single most valuable property of the output is **verifiability**:

- Third person throughout; no "we", no address to the reader.
- No peacock terms ("renowned", "beloved", "vibrant", "must-see"). State what the
  group is and does and let facts carry it.
- Attribute opinions and superlatives to whoever said them
  ("the regional press described the 2019 production as ...<ref .../>"),
  never assert them in the wiki's own voice.
- Only claims you can source. If a date or figure is uncertain, omit it or
  attribute it — do not guess. A missing fact is recoverable by a human editor;
  a fabricated one is a defect the `{{AIGenerated}}` flag is meant to catch.

## Worked example

Input: `Q#######` resolving to a Low German village stage in Lower Saxony with an
official website and a short local-press history. After reading the item (name +
site) and researching, the article might read:

```mediawiki
{{AIGenerated}}
{{DynamicInfobox|qid=Q#######}}

'''Plattdütsche Speeldeel Beispieldorf''' is a [[wikipedia:Low German|Low German]]
amateur theatre group based in [[wikipedia:Beispieldorf|Beispieldorf]], Lower Saxony,
Germany.<ref name="site" /> Founded in 1951, it stages an annual winter
production in the local parish hall and performs in the regional
[[wikipedia:Northern Low Saxon|Northern Low Saxon]] dialect.<ref name="site" /><ref name="press" />

== History ==
The group was founded in 1951 by members of the village
[[wikipedia:Heimat|Heimat]] society and has performed continuously since, apart from a
pause during the 1970s.<ref name="press" /> It is a registered association
([[wikipedia:Voluntary association#Germany|e.V.]]).<ref name="site" />

== Repertoire ==
The stage specialises in Low German comedies, with one full-length production
each winter; recent seasons have also included a short youth-group piece.<ref name="site" />

== Organisation ==
The group is a member of the [[Amateurtheaterverband Niedersachsen e. V.]] and has
taken part in the [[Niedersächsische Amateurtheatertage]].<ref name="press" />

== References ==
<references>
<ref name="site">[https://example-speeldeel.de/ Über uns], Plattdütsche Speeldeel Beispieldorf, retrieved 29 June 2026.</ref>
<ref name="press">[https://example-zeitung.de/70-jahre-speeldeel 70 Jahre Speeldeel Beispieldorf], Beispiel-Zeitung, 12 March 2021, retrieved 29 June 2026.</ref>
</references>
```

In that example, note how `Low German`, the place, the dialect, `Heimat`, and the
`e.V.` legal form all point to **English Wikipedia** via `wikipedia:` (general
knowledge) — each of those titles should be confirmed to exist before shipping —
while the association and the festival point to **local** wiki pages
(amateur-theatre scene). The body refs are all self-closing and their content is
defined once in the `<references>` block, so every name resolves and none triggers
a "has no content" error. Each factual claim is referenced with the basic ref
format, the tone states rather than sells, and the two mandatory templates head
the page with the input QID in the infobox.
