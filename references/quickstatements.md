# Wikidata enrichment via QuickStatements (V1 commands)

This step is **optional and runs only when the user asks for it**, after the
article is finished and, ideally, after the archive.org post-processing step has
added snapshot links to its references. Never run it automatically.

The target is QuickStatements 3.0 (`qs-dev.toolforge.org`), which runs V1 commands
through the Wikibase REST API. Everything below is the V1 subset that tool accepts.

## Inputs: what you already have, nothing new

To keep this step cheap, **do not start a new research round**. Work from:

1. **The generated `.wiki` article** (re-read the file if it was post-processed, so
   you pick up the archive links). The prose holds the facts, the `<ref>` that
   follows a sentence is its source, and the `<references>` block holds the URLs,
   retrieval dates and archive links.
2. **Context already available in the conversation**: pages fetched, search
   results and notes from the research run that produced the article. A fact from
   there may be used if you recorded its source URL, even if it didn't make it into
   the article text. Reference it with that URL (`S854` + `S813`). Add archive
   pairs only if that URL is also archived in the article's refs.
3. **One `get_statements(<QID>, include_external_ids=true)` call** to see which
   statements the item already has. Skip anything already present.

Web searches or fetches made only for this step are out of scope. The one exception
is cheap: if the research context doesn't already list the group's social-media
links, you may fetch the official homepage once and read its profile links.

## Which facts to extract

Take a fact when the article states it, **implies it directly**, or the research
context supports it with a recorded source:

- **Stated**: "founded on 10 January 1926".
- **Implied**: the founding year follows from the article without guesswork, e.g.
  a name containing the year ("Vineta 1900") together with a cited "125th
  anniversary in 2025". Reference the ref that carries the implying sentence.
- **Shown by the infobox**: social-media profiles and websites are displayed by
  `{{DynamicInfobox}}` from Wikidata, so they belong to the article implicitly even
  though the prose doesn't mention them. Add any profile or website you found.

| Fact | Property | Value kind | Reference? |
|---|---|---|---|
| Founding / inception | `P571` | time | **yes** |
| Headquarters town | `P159` | item | **yes** |
| Street address of the registered seat | `P6375` as qualifier on `P159` | monolingual | **yes** |
| Official name | `P1448` | monolingual (`de:"… e. V."`) | **yes** |
| Member count | `P2124` + qualifier `P585` (point in time) | quantity | **yes** |
| Dissolved | `P576` | time (or `somevalue`) | **yes** |
| Award received | `P166` + qualifiers `P585`, `P1027`, `P1686`, `P14360` | item | **yes** |
| Alternative / former names | `Ade` / `Aen` | alias | no (cannot be referenced) |
| Official website(s) | `P856` | string (URL) | no |
| Facebook / Instagram / X | `P2013` / `P2003` / `P2002` | string (handle) | no |
| YouTube channel | `P2397` | string (`UC…` id) | no |
| Mastodon | `P4033` | string (`user@instance`) | no |

**Reference the non-trivial statements** (dates, places, addresses, names) and leave
identifiers unreferenced: a social-media profile or website proves itself, and a
URL referencing itself is circular. Aliases, labels and descriptions cannot carry
references at all.

Rules:

- **Websites**: add every official website you found that the item doesn't list
  yet, including a new domain the old one now redirects to, or a separate site for
  a festival or youth section. Don't add a URL that differs from an existing one
  only by `http`/`https`, `www.` or a trailing slash.
- **Social media**: take handles only from real profile links (the official site's
  footer, or a profile you opened), never guessed from the name. Facebook (`P2013`):
  the username from `facebook.com/<username>`; for pages of the form
  `facebook.com/<Name>-<digits>/`, use the numeric id. Instagram (`P2003`): the
  handle, lowercase, without `@` or query strings. YouTube (`P2397`): only a
  `/channel/UC…` id, not a video, playlist or `@handle`.
- **Member counts**: add one `P2124` statement **per dated count** the sources
  give, each with a `P585` point-in-time qualifier for the year (`/9`) or exact
  date the count refers to, and its reference. If a website lists counts for
  several years, add all of them, not just the latest. The infobox shows the
  most recent one by its `P585`, so no ranks are needed. Skip a count with no
  date at all, or one only described vaguely ("about", "over 100"). A count
  stated as "over 100" is not a number. Write plain integers (`117`, no
  separators). Always include the `P585` qualifier on the same line: with it,
  two years with the same number stay separate statements.
- **Dissolution**: add `P576` only when a source explicitly says the association
  was dissolved or wound up (a register notice, a press report, its own
  announcement, an umbrella association's list). Use the date the source gives,
  at year precision if that's all it states; if the source confirms the
  dissolution but gives no date, use `somevalue`. Inactivity alone (dead website,
  no recent productions, no social-media posts) is **not** evidence; mention it
  to the user instead of writing a statement. Never set `P576` from the absence of
  information.
- **Awards**: add one `P166` statement **per award and year** found in the
  article's `Awards` section (or the research context, with a recorded source).
  The value is the award's own item (e.g. a specific prize, not the generic
  "award" class), resolved with `search_items` on the exact award name and
  checked with `get_statements` that it really is that prize (its `P31` is an
  award/prize, and its conferring body matches). **If the award has no item, do
  not create one and do not substitute a broader item**: list it for the user
  as "no Wikidata item yet" instead. Qualifiers, all on the same line:
  - `P585` point in time: the year (`/9`) or exact date the prize was awarded.
    Always include it: it keeps repeated wins of the same prize as separate
    statements.
  - `P14360` award category or rank: only when the prize has categories or
    places (1st prize, audience award) **and** the category has an item.
  Nominations are `P1411` (nominated for), not `P166`; add them only if the
  user asks.
- Item values (such as a town for `P159`) must be resolved to a QID. Use the value
  the item already shows in `get_statements` where possible; otherwise one
  `search_items` call. Never guess a QID.
- Time precision: `/9` year, `/10` month, `/11` day. Use year precision unless a
  source gives an exact date.
- A street address goes on `P159` only when the source says it is the group's
  registered seat, not just a venue.
- **No person-valued statements** (founders, directors, members): those people
  almost never have items.
- A fact whose only source is Wikidata itself is not a source; skip it.

## Turning a `<ref>` into a Wikidata reference

Find the ref the article attaches to the sentence, then build the source pairs from
its definition in `<references>`:

**Web source** (`<ref name="x">[URL Title], Site, retrieved D. [ARCHIVE Archived] on A.</ref>`):

| Ref part | Source pair |
|---|---|
| the cited URL | `S854 "<URL>"` (reference URL) |
| `retrieved D` | `S813 +YYYY-MM-DDT00:00:00Z/11` (retrieved) |
| `[ARCHIVE Archived]`, if present | `S1065 "<ARCHIVE>"` (archive URL) |
| `on A`, if present | `S2960 +YYYY-MM-DDT00:00:00Z/11` (archive date) |

Add `S1065`/`S2960` **only if the ref has an archive link**. Never create one
yourself here.

**Wikimedia source** (a Wikipedia `oldid` permalink or another Wikimedia project;
a non-Wikimedia MediaWiki such as a regional wiki is a normal web source, above):
the reference is **only** `S143 <project QID>` (imported from Wikimedia project),
e.g. `S143 Q48183` for German Wikipedia. Resolve the QID for other language
editions or projects. Add no `S854`/`S4656` URL, no `S813` retrieved date and no
archive pairs.

When a sentence carries two refs, give the statement two reference blocks: start
the second one with `!` (e.g. `!S854`).

## V1 line format

One command per line, fields separated by TAB. The first field is the item QID,
repeated on every line. Do **not** use `CREATE` / `LAST`; QS 3.0 rejects `LAST`.

```
<QID>	<PROPERTY>	<VALUE>	[<QUALIFIER>	<VALUE> ...]	[<SOURCE>	<VALUE> ...]
```

| Value kind | Format | Example |
|---|---|---|
| Item | bare id | `Q1726` |
| String / URL / external id | double-quoted | `"https://www.example.de/"` |
| Monolingual text | `lang:"text"` | `de:"Example e. V."` |
| Time | `+YYYY-MM-DDT00:00:00Z/<precision>` | `+1946-00-00T00:00:00Z/9` |
| Quantity | plain number | `117` |
| Unknown value | `somevalue` | `somevalue` |
| Alias / label / description | `Ade` / `Lde` / `Dde` + quoted text | `Ade "SeTA"` |

A qualifier is added by repeating the existing main statement and appending the
qualifier pair; QuickStatements matches the existing statement:

```
Q122798558	P159	Q1726	P6375	de:"Sudetendeutsche Straße 40, 80937 München"	S854	"<source URL>"	S813	+2026-06-30T00:00:00Z/11
```

## Worked example

Article `Achimer_Speeldäl.wiki` (`Q122834859`) says the group was founded in 1946,
citing:

```mediawiki
<ref name="chronik">[https://www.achimer-speeldael.de/chronik Chronik], Achimer Speeldäl e.V., retrieved 14 October 2026. [https://web.archive.org/web/20261014133712/https://www.achimer-speeldael.de/chronik Archived] on 14 October 2026.</ref>
```

`get_statements` already shows `P571 = 1946`, so inception is skipped. For an item
that lacked it, the line would be:

```
Q122834859	P571	+1946-00-00T00:00:00Z/9	S854	"https://www.achimer-speeldael.de/chronik"	S813	+2026-10-14T00:00:00Z/11	S1065	"https://web.archive.org/web/20261014133712/https://www.achimer-speeldael.de/chronik"	S2960	+2026-10-14T00:00:00Z/11
```

A fact taken from German Wikipedia (Kellertheater Hamburg founded 1954):

```
Q21036369	P571	+1954-00-00T00:00:00Z/9	S143	Q48183
```

Member counts for two years, each with a point-in-time qualifier and its own
reference (here Ruhrbühne Witten, from German Wikipedia, plus a hypothetical
count from the club's site):

```
Q17325980	P2124	117	P585	+2019-00-00T00:00:00Z/9	S143	Q48183
Q17325980	P2124	121	P585	+2024-00-00T00:00:00Z/9	S854	"https://ruhrbuehne-witten.de/verein/"	S813	+2026-10-14T00:00:00Z/11
```

A dissolution with a known year, and one confirmed without a date:

```
Q123456789	P576	+2019-00-00T00:00:00Z/9	S854	"<register notice or press URL>"	S813	+2026-10-14T00:00:00Z/11
Q123456789	P576	somevalue	S854	"<source URL>"	S813	+2026-10-14T00:00:00Z/11
```

Two awards: a prize won twice (each year its own statement) and one with the
awarding body and the honoured production as qualifiers. Placeholder QIDs stand
for items resolved with `search_items`; never guess them:

```
Q123456789	P166	Q<award>	P585	+2012-00-00T00:00:00Z/9	S854	"<winners list URL>"	S813	+2026-10-14T00:00:00Z/11
Q123456789	P166	Q<award>	P585	+2018-00-00T00:00:00Z/9	S854	"<winners list URL>"	S813	+2026-10-14T00:00:00Z/11
Q123456789	P166	Q<other award>	P585	+2022-00-00T00:00:00Z/9	P1027	Q<awarding body>	P1686	Q<production or play>	S854	"<press URL>"	S813	+2026-10-14T00:00:00Z/11	S1065	"<archive URL>"	S2960	+2026-10-14T00:00:00Z/11
```

An alias and a Facebook profile, both unreferenced:

```
Q18289439	Ade	"SeTA"
Q122834860	P2013	"ExampleTheatreBremen"
```

## Building the batch URL

Percent-encode the whole command block programmatically, never by hand. A raw `+`
decodes to a space and corrupts every date:

```python
import urllib.parse
url = "https://qs-dev.toolforge.org/batch/new?v1=" + urllib.parse.quote(commands, safe="")
```

Check that `+` came out as `%2B`.

## Presenting the result

Write the command block to a `.qs` file next to the article (same base name), and
show the user both the readable commands and the batch URL. The URL opens a draft
in QuickStatements: the user must be logged in, reviews it, and runs it themselves.
Nothing is saved automatically.

Below the URL, list any award from the article that was **not** added because
it has no Wikidata item, so the user can decide whether to create one.

If the article holds a useful fact outside the table above (for example
described at URL `P973` or a member organisation `P463`), propose it and ask the
user whether it should join the default set before treating it as standard.
