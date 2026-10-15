# Wikidata enrichment via QuickStatements (V1 commands)

This step is **optional and runs only when the user asks for it**, after the
article is finished and, ideally, after the archive.org post-processing step has
added snapshot links to its references. Never run it automatically.

The target is QuickStatements 3.0 (`qs-dev.toolforge.org`), which runs V1 commands
through the Wikibase REST API. Everything below is the V1 subset that tool accepts.
**Every batch URL goes to QS 3.0**, the award-creation batch included: the
classic QuickStatements tool doesn't support importing commands by URL.

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

Web searches or fetches made only for this step are out of scope, with two
exceptions: if the research context doesn't already list the group's social-media
links, you may fetch the official homepage once and read its profile links; and
for an award that needs a new item, you may research the award itself (see
"Creating items for missing awards").

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
| Founding / inception | `P571` + qualifier `P1013` criterion used = `Q712144` de facto / `Q132555` de jure, when there are two dates | time | **yes** |
| Headquarters town | `P159` | item | **yes** |
| Street address of the registered seat | `P6375` as qualifier on `P159` | monolingual | **yes** |
| Official name | `P1448` | monolingual (`de:"… e. V."`) | **yes** |
| Legal form | `P1454` | item (usually `Q9299236` registered association) | **yes** |
| Member count | `P2124` + qualifier `P585` (point in time), `P1480` `Q5727902` (circa) if vague | quantity | **yes** |
| Dissolved | `P576` | time (or `somevalue`) | **yes** |
| Award received | `P166` + qualifiers `P585`, `P1027`, `P1686`, `P14360` | item | **yes** |
| Alternative / former names | `Ade` / `Aen` | alias | no (cannot be referenced) |
| Official website(s) | `P856` | string (URL) | no |
| Facebook / Instagram / X | `P2013` / `P2003` / `P2002` | string (handle) | no |
| YouTube channel ID | `P2397` | string (`UC…` id) | no |
| YouTube handle | `P11245` | string (handle without `@`) | no |
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
  handle, lowercase, without `@` or query strings. YouTube channel ID (`P2397`):
  only a `/channel/UC…` id, not a video or playlist. YouTube handle (`P11245`):
  the handle from `youtube.com/@<handle>`, without the `@`, query strings or
  trailing path (`/videos`, `/featured`), keeping its case as shown. A channel
  can have both; add each one you actually found, and don't derive one from the
  other.
- **Inception**: when the sources give one founding date, add it as a plain
  `P571`. When they give two relevant dates, add **both**, each with the
  qualifier `P1013` criterion used:
  - `Q132555` **de jure** for the legal founding: the founding or the register
    entry of the e. V. (if both are given, the register entry).
  - `Q712144` **de facto** for when the group itself actually started: its
    first meeting, rehearsals or performance, before it became a legal entity.

  At most one date of each kind. Leave out dates that would need more than this
  qualifier to make sense: a renaming, a re-founding after a break, joining or
  leaving a parent club, or the start of a local theatre tradition older than
  the group. List them under "Skipped" with the reason. QuickStatements can't
  set ranks, so whenever you add two `P571` statements, add a rank task (see
  the report template): the user marks one of them as preferred on Wikidata
  after the upload. Recommend the de jure date, since a register documents it.
  If the item already has one of the two dates without the qualifier, add only
  the missing date with its qualifier, and add a task to put `P1013` on the
  existing statement by hand.
- **Legal form**: add `P1454` when a source shows the group's own legal form,
  usually `Q9299236` registered association (eingetragener Verein) for a German
  group with "e. V." in its official name, imprint or register entry. Reference
  the source that shows it (often the imprint or the page that gives the
  official name). Don't add it for a group that is only a section of a larger
  club (e.g. a sports club's theatre department): the legal form belongs to the
  parent club. For other legal forms (gGmbH, GbR, a Dutch or Austrian
  association), resolve the item with `search_items` and check it with
  `get_statements` first.
- **Member counts**: add one `P2124` statement **per dated count** the sources
  give, each with a `P585` point-in-time qualifier for the year (`/9`) or exact
  date the count refers to, and its reference. If a website lists counts for
  several years, add all of them, not just the latest. The infobox shows the
  most recent one by its `P585`, so no ranks are needed. When a count is split
  into exact parts (e.g. 25 adult and 15 youth members), add their sum (40) as a
  single statement. When a count has no date, assume it is current: use the
  year of the retrieval date (`S813`) as `P585`, and mention this in the report.
  A vague count ("about 80", "rund 50", "over 100", "mehr als 60") is added too,
  as its number (`80`, `100`) with the qualifier `P1480` sourcing circumstances
  = `Q5727902` circa on the same line. Write plain integers (`117`, no
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
  not substitute a broader item**: either propose a new item for it (see
  "Creating items for missing awards") or list it in the report as "no Wikidata
  item yet". Qualifiers, all on the same line:
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
repeated on every line. `CREATE` / `LAST` belong only in the award-creation batch
(see "Creating items for missing awards"), never in a group's main batch.

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

Two founding dates (a hypothetical group that started playing in 1984 and was
registered as an e. V. in 1991), each with its criterion. The rank task for the
report follows below:

```
Q123456789	P571	+1984-00-00T00:00:00Z/9	P1013	Q712144	S854	"https://example-theater.de/chronik"	S813	+2026-10-14T00:00:00Z/11
Q123456789	P571	+1991-00-00T00:00:00Z/9	P1013	Q132555	S854	"https://example-theater.de/chronik"	S813	+2026-10-14T00:00:00Z/11
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

A vague, undated count ("rund 80 Mitglieder" on the club's site, retrieved in
2026), dated to the retrieval year and marked as circa:

```
Q17325980	P2124	80	P585	+2026-00-00T00:00:00Z/9	P1480	Q5727902	S854	"https://ruhrbuehne-witten.de/verein/"	S813	+2026-10-14T00:00:00Z/11
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

## Creating items for missing awards

When an award from the article has no Wikidata item, decide whether to propose
one.

**Is it concrete enough?** Propose an item only when all of these hold:

- It has a **fixed, official name** (`Bayerischer Amateurtheaterpreis`,
  `Kulturpreis der Stadt Achim`), not a description ("a prize at the festival").
- It has an **identifiable awarding body**: an association, a municipality, a
  foundation, a festival.
- There is **evidence about the award itself**: a winners list, a statute or
  call for entries, the awarding body's page, or press coverage that names the
  prize. Ideally it was awarded more than once or is meant to recur.

Not concrete enough: certificates of thanks, honorary mentions without a prize
name, "Publikumsliebling" polls by a newspaper with no further trace, festival
invitations, nominations. List these in the report as rejected, with the reason.

**Check for duplicates first.** Search the native name, the English name, and
likely variants (with and without the year, the body's name or the legal form)
with `search_items`. If the awarding body has an item, run a SPARQL query for
items with `P1027` = that body, since an award is often labelled differently.
Then look in the output folder: if another group's `*.award-items.qs` already
has a `CREATE` block with the same `Lde` label, or a `*.pending.qs` already uses
the same placeholder, the award is already proposed. Reuse that placeholder
exactly and don't write a second `CREATE` block. Only when all of that comes up
empty is a new item justified.

**Research the award.** A few targeted searches (award name + "verliehen",
"Preisträger", "Satzung", "Ausschreibung") are allowed here. Use the awarding
body's own page as the main reference.

### Typical award statements

Add what the sources support; leave out the rest. Resolve every item value with
`search_items` and check it with `get_statements`; never guess a QID or PID.

| Statement | Property | Value | Notes |
|---|---|---|---|
| Labels | `Lde`, `Len` | text | Native name as `Lde`; `Len` the same name unless an official English one exists |
| Descriptions | `Dde`, `Den` | text | e.g. `Den "amateur theatre award of the Verband Bayerischer Amateurtheater"` |
| Aliases | `Ade` | text | Short forms or former names found in sources |
| Instance of | `P31` | item | The most specific existing class: theatre award, culture prize, or award |
| Conferred by | `P1027` | item | Awarding body; skip if it has no item (don't create one) |
| Country | `P17` | item | |
| Applies to jurisdiction | `P1001` | item | The region or town the prize covers (state, district, municipality) |
| Official name | `P1448` | monolingual | `de:"…"` |
| Inception | `P571` | time | Year the prize was founded or first awarded |
| Dissolved / abolished | `P576` | time | Only with explicit evidence that it was discontinued |
| Part of | `P361` | item | The festival or competition the prize belongs to, if it has an item |
| Named after | `P138` | item | Only if the namesake already has an item |
| Prize money | `P2121` | quantity with unit | e.g. `5000U<euro QID>`; add `P585` for the year the amount applies to |
| Event interval | `P2257` | quantity with unit | e.g. `1U<year QID>` for an annual prize, `2U<year QID>` for biennial |
| Official website | `P856` | URL | The award's own page at the awarding body, if it has one |

Reference every statement except labels, descriptions, aliases and the website
with `S854` + `S813` (and archive pairs if you have them), as for the group.

### Creation batch

Write one `CREATE` block per award to `<base>.award-items.qs`, where `<base>` is
the group whose report first proposed the award:

```
CREATE
LAST	Lde	"Beispieler Amateurtheaterpreis"
LAST	Len	"Beispieler Amateurtheaterpreis"
LAST	Dde	"Preis für Amateurtheater im Landkreis Beispiel"
LAST	Den	"amateur theatre award in the district of Beispiel, Germany"
LAST	P31	Q<theatre award class>	S854	"<awarding body page>"	S813	+2026-10-14T00:00:00Z/11
LAST	P1027	Q<awarding body>	S854	"<awarding body page>"	S813	+2026-10-14T00:00:00Z/11
LAST	P17	Q<Germany>
LAST	P1001	Q<district>	S854	"<awarding body page>"	S813	+2026-10-14T00:00:00Z/11
LAST	P571	+2005-00-00T00:00:00Z/9	S854	"<awarding body page>"	S813	+2026-10-14T00:00:00Z/11
```

Its batch URL uses QS 3.0 like every other batch (see "Building the batch URL").

### Pending lines and the placeholder

A new QID is only known after the creation batch has run, so the group's `P166`
statements for that award **can't go into the same batch**. Write them to
`<base>.pending.qs` (one file per group, next to its `.qs`), with the
placeholder `Q<NEW: <Lde label>>` in place of the award's QID. The label must be
the creation block's `Lde` label, character for character: it is the key that
links the placeholder to the item once it exists.

```
Q123456789	P166	Q<NEW: Beispieler Amateurtheaterpreis>	P585	+2018-00-00T00:00:00Z/9	S854	"<winners list URL>"	S813	+2026-10-14T00:00:00Z/11
```

Show the same lines in the report under "New items proposed". Pending lines
never go into `<base>.qs`: QuickStatements would reject the placeholder.

### Resolving placeholders after the award item is created

Tell the user (in the report and when presenting the batches) how to finish:

1. Open `000_all.award-items.qs.url` (or the group's award-items link) and run
   the batch in QuickStatements while logged in.
2. Note the new QID from the batch result, or find the new item on Wikidata by
   its label.
3. Tell Claude "<award label> is Q…", e.g. "Beispieler Amateurtheaterpreis is
   Q123456789". Claude then fills in the placeholder in every group (below).
   Without Claude: `sed -i 's/Q<NEW: Beispieler Amateurtheaterpreis>/Q123456789/g' *.pending.qs`,
   then move the lines into each group's `.qs` by hand.

When the user gives you the QID, do this for the whole output folder, with no new
research:

1. **Verify the item** with `get_statements`: its label matches the placeholder,
   and its `P31` and `P1027` match the creation block. If they don't, stop and
   ask. If the user gives only the label, find the QID with `search_items`.
2. **Check for existing statements** with one SPARQL query for items with `P166`
   = the new QID, so you don't add a line twice.
3. For each `*.pending.qs` that has the placeholder: replace it with the QID,
   **append those lines to the group's `<base>.qs`** (create the file if
   missing), and remove them from the `.pending.qs`. Delete a `.pending.qs` once
   it's empty.
4. **Delete the award's `CREATE` block** from its `.award-items.qs`, since it has
   run. Delete the file if nothing is left.
5. **Update each affected report**: the main batch line (new command count and
   rebuilt URL), one row per new `P166` under "Added statements", the award
   moved from "New items proposed" to "Matched to existing items" as
   "<label> → Q… (created <date>)", and the pending line rewritten with the QID.
6. Regenerate the folder-wide batch files.

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

Then write the report, below.

If the article holds a useful fact outside the table above (for example
described at URL `P973` or a member organisation `P463`), propose it and ask the
user whether it should join the default set before treating it as standard.

## The QuickStatements report

Write `<base>.qs-report.md` next to the article and the `.qs` file. It is for
the person who reviews and runs the batches, so make every point actionable.
Leave out every section, sub-heading and batch line that would be empty: no
"None.", no "Award items: none." A group with nothing to report beyond the
added statements gets a report with only the title, the batches and the table.

```markdown
# QuickStatements report: <Group name> (<QID>)

Generated <date> from `<base>.wiki`.

## Batches
- Main batch: `<base>.qs`, <n> commands, [open in QuickStatements](<qs-dev URL>)
- Award items: `<base>.award-items.qs`, <n> new items, [open in QuickStatements](<qs-dev URL>)
- Pending: `<base>.pending.qs`, <n> lines waiting for: <award label> (created by
  `<file>.award-items.qs`). After running that batch, tell Claude "<award label>
  is Q…" to fill in the placeholder.

## Added statements
| Property | Value | Source |
|---|---|---|
| P571 inception | 1946 | Chronik (archived) |

## Skipped
- P571 inception: already on the item (1946).
- P571 1969 (renaming to the present name): a renaming is not a founding date.

## Conflicts between the item and the article
- Item says inception 1948; the Chronik and the press say 1946. Not changed;
  check and fix by hand.

## Possible errors on the item
- P856 http://old-domain.de/ no longer resolves; the group now uses
  https://new-domain.de/ (added). Consider deprecating the old one.

## Awards
### Matched to existing items
- Bayerischer Amateurtheaterpreis 2018 → Q<id>
### New items proposed
- *Beispieler Amateurtheaterpreis* (Landkreis Beispiel, since 2005): why it
  qualifies, sources used, and the pending P166 line:
  `Q123456789	P166	Q<NEW: Beispieler Amateurtheaterpreis>	P585	+2018-00-00T00:00:00Z/9	…`
### Not concrete enough
- "Publikumsliebling 2019" (newspaper poll): no awarding statute or winners list.

## Proposals outside the default set
- P463 member of Amateurtheaterverband Niedersachsen e. V. (Q<id>): add?

## Open questions
- …

## Tasks after the upload
- [ ] [Q123456789](https://www.wikidata.org/wiki/Q123456789#P571) Example Theater:
  set P571 1991 (de jure, e. V. registered) to preferred rank; 1984 (de facto)
  stays normal.
```

"Tasks after the upload" lists what QuickStatements can't do and the user must
do by hand on Wikidata once the batch has run: setting a preferred rank between
two inception dates, or adding `P1013` to an existing statement. Write each as
a `- [ ]` checklist line that starts with the item link.

Only report possible errors on the item; the batches never remove or change
existing statements.

## Folder-wide batch files

After writing a group's `.qs` and `.qs-report.md`, regenerate the combined files
for the whole output folder, so one review and one run cover every group. They
start with `000_` so they sort before every group's files:

| File | Content |
|---|---|
| `000_all.qs` | every `<base>.qs`, alphabetically by file name |
| `000_all.qs.url` | the `qs-dev` batch URL for `000_all.qs` |
| `000_all.award-items.qs` | every `<base>.award-items.qs` (only if there are any) |
| `000_all.award-items.qs.url` | the `qs-dev` batch URL for `000_all.award-items.qs` |
| `000_all.pending.qs` | every `<base>.pending.qs` (only if there are any; no URL, since placeholders can't run) |
| `000_all.qs-report.md` | an overview, then every `<base>.qs-report.md` with headings demoted one level |
| `000_all.tasks.md` | every "Tasks after the upload" checklist line from the group reports (only if there are any) |

The `.url` files are internet shortcuts (`[InternetShortcut]` / `URL=…`), so a
file manager opens them in the browser. Rebuild all of them from scratch each
time (the snippet deletes the old `000_` files first), never append, and skip the `000_` files themselves when collecting:

```python
import pathlib, re, urllib.parse, datetime
d = pathlib.Path("<output folder>")
for p in d.glob("000_*"):
    p.unlink()
def group_files(suffix):
    return sorted(p for p in d.glob("*" + suffix)
                  if not p.name.startswith("000_")
                  and not (suffix == ".qs" and p.name.endswith(".award-items.qs")))
def write_batch(name, files, base_url):
    cmds = "\n".join(l for p in files for l in p.read_text().splitlines() if l.strip())
    (d / name).write_text(cmds + "\n")
    url = base_url + urllib.parse.quote(cmds, safe="")
    (d / (name + ".url")).write_text(f"[InternetShortcut]\nURL={url}\n")
    return cmds.count("\n") + 1, url
main = group_files(".qs")
n_main, url_main = write_batch("000_all.qs", main, "https://qs-dev.toolforge.org/batch/new?v1=")
awards = group_files(".award-items.qs")
if awards:
    n_aw, url_aw = write_batch("000_all.award-items.qs", awards, "https://qs-dev.toolforge.org/batch/new?v1=")
pending = group_files(".pending.qs")
if pending:
    (d / "000_all.pending.qs").write_text("".join(p.read_text() for p in pending))
reports = group_files(".qs-report.md")
out = [f"# QuickStatements report: all groups\n\nGenerated {datetime.date.today()} "
       f"from {len(reports)} group reports.\n\n## Batches\n"
       f"- Main batch: `000_all.qs`, {n_main} commands from {len(main)} groups, "
       f"[open in QuickStatements]({url_main})"]
if awards:
    out.append(f"- Award items: `000_all.award-items.qs`, {n_aw} commands from {len(awards)} groups, "
               f"[open in QuickStatements]({url_aw})")
if pending:
    labels = sorted(set(re.findall(r"Q<NEW: ([^>]+)>", "".join(p.read_text() for p in pending))))
    out.append(f"- Pending: `000_all.pending.qs`, waiting for: {', '.join(labels)}. Run the "
               "award-items batch, then tell Claude \"<award label> is Q…\" to fill in the placeholders.")
for p in reports:
    out.append("\n" + re.sub(r"^(#+) ", r"#\1 ", p.read_text().strip(), flags=re.M))
(d / "000_all.qs-report.md").write_text("\n".join(out) + "\n")
tasks = []
for p in reports:
    m = re.search(r"^## Tasks after the upload\n(.*?)(?=^## |\Z)", p.read_text(), re.M | re.S)
    if m:
        tasks.append(m.group(1).strip())
if tasks:
    (d / "000_all.tasks.md").write_text(
        "# Tasks after the upload\n\nDo these on Wikidata once `000_all.qs` has run.\n\n"
        + "\n".join(tasks) + "\n")
```

A combined URL can get long. If QuickStatements doesn't open it, paste the
content of `000_all.qs` into its import box instead. Tell the user the command
count and the URL length.
