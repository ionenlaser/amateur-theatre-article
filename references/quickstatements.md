# Wikidata enrichment via QuickStatements (V1 commands)

This step is **optional and runs only when the user asks for it**, after the
article is finished and, ideally, after the archive.org post-processing step has
added snapshot links to its references. Never run it automatically.

The target is QuickStatements 3.0 (`qs-dev.toolforge.org`), which runs V1 commands
through the Wikibase REST API. Everything below is the V1 subset that tool accepts.

## Inputs: the article and the item, nothing else

To keep this step cheap, **do not research again**. Work only from:

1. **The generated `.wiki` article** (re-read the file if it was post-processed, so
   you pick up the archive links). Every fact and every source you need is already
   in it: the prose holds the facts, the `<ref>` that follows a sentence is its
   source, and the `<references>` block holds the URLs, retrieval dates and archive
   links.
2. **One `get_statements(<QID>, include_external_ids=true)` call** to see which
   statements the item already has. Skip anything already present.

No web search, no web fetch, no reading the cited pages again. If a fact is not in
the article with a ref, it does not go into the batch.

## Which facts to extract

Scan the article for these, in this order. Only take a fact that is stated in the
article and backed by a `<ref>` (identifiers and names excepted, see below):

| Fact | Property | Value kind | Reference? |
|---|---|---|---|
| Founding / inception | `P571` | time | **yes** |
| Headquarters town | `P159` | item | **yes** |
| Street address of the registered seat | `P6375` as qualifier on `P159` | monolingual | **yes** |
| Official name | `P1448` | monolingual (`de:"… e. V."`) | **yes** |
| Alternative / former names | `Ade` / `Aen` | alias | no (cannot be referenced) |
| Official website | `P856` | string (URL) | no |
| Facebook / Instagram / X | `P2013` / `P2003` / `P2002` | string (handle) | no |
| YouTube channel | `P2397` | string (`UC…` id) | no |
| Mastodon | `P4033` | string (`user@instance`) | no |

**Reference the non-trivial statements** (dates, places, addresses, names) and leave
identifiers unreferenced: a social-media profile or website proves itself, and a
URL referencing itself is circular. Aliases, labels and descriptions cannot carry
references at all.

Rules:

- Item values (such as a town for `P159`) must be resolved to a QID. Use the value
  the item already shows in `get_statements` where possible; otherwise one
  `search_items` call. Never guess a QID.
- Time precision: `/9` year, `/10` month, `/11` day. Use year precision unless the
  article gives an exact date with a source.
- A street address goes on `P159` only when the article says it is the group's
  registered seat, not just a venue.
- **No person-valued statements** (founders, directors, members): those people
  almost never have items.
- A fact the article attributes to Wikidata itself (or only to the infobox) is not
  a source; skip it.

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

**Wikipedia source** (an `oldid` permalink, e.g. `https://de.wikipedia.org/w/index.php?title=…&oldid=…`):

| Ref part | Source pair |
|---|---|
| the language edition | `S143 Q48183` (imported from Wikimedia project: German Wikipedia; resolve the QID for other languages) |
| the `oldid` URL | `S4656 "<oldid URL>"` (Wikimedia import URL) |
| `retrieved D` | `S813 +YYYY-MM-DDT00:00:00Z/11` |

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
Q21036369	P571	+1954-00-00T00:00:00Z/9	S143	Q48183	S4656	"https://de.wikipedia.org/w/index.php?title=Kellertheater_Hamburg&oldid=266247510"	S813	+2026-10-14T00:00:00Z/11
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

If the article holds a useful fact outside the table above (for example
described at URL `P973` or a member organisation `P463`), propose it and ask the
user whether it should join the default set before treating it as standard.
