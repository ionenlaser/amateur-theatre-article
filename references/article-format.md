# Article format

## Skeleton

```mediawiki
{{AIGenerated}}
{{DynamicInfobox|qid=Q#######}}

'''<Native name>''' is a <type> amateur theatre group based in [[wikipedia:<Town>|<Town>]], <region>, Germany.<ref name="site" /> <One or two more sentences: what it does, when founded.>

== History ==
== Repertoire ==
== Venue ==          <!-- only with a named, documented playing space -->
== Organisation ==   <!-- legal form, associations, festivals -->
== Awards ==         <!-- only with documented awards -->

== References ==
<references>
<ref name="site">[<URL> <page title>], <site>, retrieved <date>.</ref>
</references>
```

- Headings in English; proper names native.
- Leave out any section you can't source. Three well-sourced sentences beat padded sections.
- Never add: a hand-written infobox or a list of infobox fields, `{{Wikipedia article}}`
  (the infobox links Wikipedia), an `External links` section (the infobox shows
  websites and social media), categories.
- Mention infobox facts only where the prose needs them.

## Section rules

**Awards**: one or two awards → prose; three or more → bulleted list, oldest first:

```mediawiki
* 2018: ''Amateurtheaterpreis'' of the [[Verband Bayerischer Amateurtheater e. V.]] for ''Der zerbrochne Krug''.<ref name="vbat2018" />
```

- Each award: exact name (native), year, awarding body, production, category/rank, ref.
  The awarding body's winners list is the best source.
- Link the body by the routing rules; link the award only if it has its own article.
- Nominations, shortlists, festival invitations: "nominated for" / "invited to", or under Organisation.
- No "prestigious" and the like. A winning production may also note the prize in
  the repertoire table, but the Awards section is the full record.

**Repertoire**: one or two prose sentences (genres, language, productions per
year, changes over time). With about five or more dated productions, add a table:

```mediawiki
{| class="wikitable sortable"
|+ Productions<ref name="dewiki" />
! Year !! Title !! Author !! Notes
|-
| 2001 || ''Much Ado About Nothing'' || [[wikipedia:William Shakespeare|William Shakespeare]] || First production
|-
| 2006 || ''[[wikipedia:Baal (play)|Baal]]'' || [[wikipedia:Bertolt Brecht|Bertolt Brecht]] ||
|-
| 2009 || ''Der Brandner Kaspar'' || after Franz von Kobell || <ref name="press1" />
|}
```

- **Every** production found, oldest first; revivals get their own row ("revival of 1987 production").
- Caption: `Productions` if complete, `Productions (incomplete)` if there are known
  gaps (name the missing years in the prose), `Selected productions` only if the
  sources themselves give only a selection.
- Columns: Year, Title, Author ("after X" for adaptations), Notes (director, venue,
  award). Drop a column the sources leave empty.
- Titles in italics, in the language performed; add the English title only for well-known plays.
- Ref in the caption for the main source; row refs only for rows from other sources.
- Fewer than five productions, or undated ones: prose.
- Never fill gaps with guesses.

## Links

Rule: would a general encyclopedia have an article on this?

- **Yes → English Wikipedia** via `wikipedia:` (art forms, languages, places, general
  institutions, well-known plays and authors):
  `[[wikipedia:Low German|Low German]]`, `[[wikipedia:Hanover|Hanover]]`,
  `[[wikipedia:Voluntary association#Germany|registered association]]`.
- **No, it belongs to the amateur-theatre scene → local link** (troupes, scene
  festivals, associations): `[[Niedersächsische Amateurtheatertage]]`. Use the
  wiki's exact title, legal form included: `[[Amateurtheaterverband Niedersachsen e. V.]]`,
  `[[Bund Deutscher Amateurtheater (BDAT)]]`. Missing local pages are useful redlinks; no check needed.
- Link each term once, at first mention. Don't link the obvious ("theatre", "Germany").

**Check every `wikipedia:` target in one call** before writing the final file
(titles joined with `|`, up to 50):

```text
https://en.wikipedia.org/w/api.php?action=query&titles=Low_German|Volksstück|Hanover&redirects&prop=pageprops&ppprop=disambiguation&format=json
```

- Entry with `"missing"` → don't link it (e.g. `Volksstück` has no English article).
  Use a confirmed broader or synonymous title, or plain text.
- Redirect to an unrelated topic, or `disambiguation` in pageprops → choose
  another title or plain text.
- Log dropped links as `PROBLEM error`.

## Citations

Format, always (no `{{cite web}}` / `{{cite news}}`; they don't exist on the wiki):

```mediawiki
<ref name="site">[https://example-troupe.de/ Über uns], Theatergruppe Example e. V., retrieved 29 June 2026.</ref>
<ref name="press1">[https://example-paper.de/article Headline], Example-Zeitung, 20 November 2025, retrieved 29 June 2026.</ref>
```

- **One pattern only**: every body ref is self-closing `<ref name="x" />`, and every
  name is defined exactly once inside `<references>…</references>`. (A self-closing
  name with no definition causes the "has no content" cite error.)
- Retrieved date = today.
- **Placement**: when consecutive sentences come from one source, cite it once after
  the last of them. Add a ref where the source changes, and directly after a
  contested, surprising or quoted claim (a figure, an award, a superlative).

  ```mediawiki
  The group was founded in 1954. It moved into the basement in 1966.<ref name="dewiki" /> In 2014 it staged 22 productions.<ref name="press1" />
  ```
- Add an independent source next to an own-site source for the same fact; at most
  two or three refs per sentence; don't cite the same fact in lead and body.
- Evaluations only attributed and from independent sources ("the regional press
  described the 2019 production as …").

**Wikimedia sources** (Wikipedia, Wikidata, Commons, …): cite the revision you read.
Get revids for all titles of one wiki in one call:

```text
https://de.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=ids&titles=Kellertheater_Hamburg|Other_Title&format=json
```

```mediawiki
<ref name="dewiki">[https://de.wikipedia.org/w/index.php?title=Kellertheater_Hamburg&oldid=266247510 Kellertheater Hamburg], German Wikipedia, retrieved 14 October 2026.</ref>
```

Never `/wiki/<Title>` in a ref (interwiki links keep plain titles).

**Other MediaWiki sites** (AW-Wiki, Stadtwikis, GenWiki): ordinary websites. Cite the
plain page URL, never an `oldid` link.

## Wikidata-only stub

When the item is the only source:

```mediawiki
{{AIGenerated}}
{{Stub}}
{{DynamicInfobox|qid=Q123456789}}

'''Theatergruppe Beispieldorf''' is an amateur theatre group in [[wikipedia:Beispieldorf|Beispieldorf]], Bavaria, Germany, founded in 1978.<ref name="wikidata" />

== References ==
<references>
<ref name="wikidata">[https://www.wikidata.org/w/index.php?title=Q123456789&oldid=2345678901 Theatergruppe Beispieldorf (Q123456789)], Wikidata, retrieved 15 October 2026.</ref>
</references>
```

- One to three sentences from statements with plain values (name, type, town, founding year).
- `oldid` = `lastrevid` from Step 1.
- No claims from the description or from missing statements ("no longer active").
  No filler about the town or the genre.
- `{{Stub}}` adds `Category:Stub` itself. Never use it once any other source exists.

## Worked example

```mediawiki
{{AIGenerated}}
{{DynamicInfobox|qid=Q#######}}

'''Plattdütsche Speeldeel Beispieldorf''' is a [[wikipedia:Low German|Low German]] amateur theatre group based in [[wikipedia:Beispieldorf|Beispieldorf]], Lower Saxony, Germany.<ref name="site" /> Founded in 1951, it stages an annual winter production in the local parish hall in the [[wikipedia:Northern Low Saxon|Northern Low Saxon]] dialect.<ref name="site" /><ref name="press1" />

== History ==
The group was founded in 1951 by members of the village [[wikipedia:Heimat|Heimat]] society and has performed continuously since, apart from a pause during the 1970s.<ref name="press1" /> It is a registered association ([[wikipedia:Voluntary association#Germany|e. V.]]).<ref name="site" />

== Repertoire ==
The stage specialises in Low German comedies, with one full-length production each winter; recent seasons have also included a short youth-group piece.<ref name="site" />

== Organisation ==
The group is a member of the [[Amateurtheaterverband Niedersachsen e. V.]] and has taken part in the [[Niedersächsische Amateurtheatertage]].<ref name="press1" />

== References ==
<references>
<ref name="site">[https://example-speeldeel.de/ Über uns], Plattdütsche Speeldeel Beispieldorf, retrieved 29 June 2026.</ref>
<ref name="press1">[https://example-zeitung.de/70-jahre-speeldeel 70 Jahre Speeldeel Beispieldorf], Beispiel-Zeitung, 12 March 2021, retrieved 29 June 2026.</ref>
</references>
```
