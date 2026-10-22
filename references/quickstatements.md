# QuickStatements batch (V1 commands)

Target: QuickStatements 3.0 (`qs-dev.toolforge.org`), V1 commands. You write the
commands and the report. `archive_refs.py` (run later by the user) adds archive
pairs; `build_batches.py` writes batch URLs and the `## Batches` section, and
builds the `000_all.*` files. Don't do any of that yourself.

## Inputs

1. The article: a sentence's `<ref>` is its source; the ref definition holds URL and date.
2. The ledger: a fact with a recorded source URL may be used even if it isn't in the article.
3. The Step 1 `get_statements` result: skip anything the item already has.

Facts count when the article states them, directly implies them (a name "Vineta
1900" plus a cited 125th anniversary in 2025 → founded 1900; use the implying
sentence's ref), or when the infobox shows them (websites, social media). Legal
form, registered address, umbrella associations and parent organisation are kept
out of the article on purpose: take them from the ledger with its source URL.

## Default property set

| Fact | Command | Ref |
|---|---|---|
| Inception | `P571` time; with two dates each gets `P1013` (below) | yes |
| Headquarters town | `P159` item | yes |
| Registered-seat address | `P6375` monolingual, as qualifier on `P159` | yes |
| Official name | `P1448` `de:"… e. V."` | yes |
| Legal form | `P1454` item, usually `Q9299236` registered association | yes |
| Umbrella association | `P463` item | yes |
| Parent organisation | `P749` item (the club the group is a section of) | yes |
| Member count | `P2124` quantity + `P585`; `P1480` `Q5727902` if vague | yes |
| Dissolved | `P576` time or `somevalue` | yes |
| Award received | `P166` item + `P585`, optional `P1027`, `P1686`, `P14360` | yes |
| Alias / former name | `Ade` / `Aen` | no |
| Official website | `P856` string + `P407` language of work | no |
| Facebook / Instagram / X | `P2013` / `P2003` / `P2002` string | no |
| YouTube channel ID / handle | `P2397` / `P11245` string | no |
| Mastodon | `P4033` `"user@instance"` | no |

Never add person-valued statements (founders, directors, members). A fact whose
only source is Wikidata is skipped.

## Rules per property

- **P571 inception**: one date → plain `P571`. Two dates → both, each with `P1013`:
  `Q132555` de jure (e. V. founding, or the register entry if both are given),
  `Q712144` de facto (first meeting, rehearsal or performance). At most one of each.
  The de jure date gets `R+`. If the item has one of them without the qualifier,
  repeat it with `P1013` (and `R+` if de jure), then add the other. Skip renamings,
  re-foundings, joining or leaving a parent club, or older local traditions; list
  them under "Skipped".
- **P159 / P6375**: the address only if the source calls it the registered seat, not a venue.
  If the sources name a more precise place than the item's `P159` value (a district
  or Ortsteil instead of the whole city or municipality, e.g. `Q758481` Aubing
  instead of `Q1726` Munich), replace it: `SWITCH_VALUE` old → new, then a line
  adding the reference (and `P6375`, if known). The new value must lie in the old
  one; list the change under "Corrections".
- **P1454 legal form**: when a source (imprint, register, official name) shows the
  group's own form. Not for a section of a larger club. e. V. and GbR: "Known QIDs". Other forms (gGmbH,
  foreign associations): `search_items` + `get_statements` first.
- **P463 / P749**: only an existing item: take it from "Known QIDs" below, otherwise
  `search_items` + `get_statements`; never create one. A member of a regional
  association is usually also in the BDAT through it: add only memberships a
  source names. `P463` for each umbrella or regional
  association the group is a member of; `P749` when the group is a section of a
  larger club. No item → it stays in the article's Organisation section; mention
  it in the report.
- **P2124 members**: one statement per dated count, all years, each with `P585`
  (`/9` year or exact date) on the same line. Split exact counts → their sum.
  Undated count → `P585` = year of the retrieval date; mention it in the report.
  Vague counts ("about 80", "rund 50", "über 100") → the number plus `P1480`
  `Q5727902`. Plain integers (`117`). No ranks.
- **P576 dissolved**: only with an explicit source (register notice, press, own
  announcement, association list). Year precision if that's all; `somevalue` if
  undated. Never from inactivity or missing information; mention suspected
  inactivity in the report instead.
- **P166 awards**: one statement per award and year, always with `P585`. Value =
  the specific prize item, found with `search_items` (native and English name) and
  confirmed with `get_statements` (P31 award/prize, matching conferring body).
  `P1027` conferred by and `P1686` for work where those items exist; `P14360` only
  if the category has an item. **No item → never use a broader item**; read
  `award-items.md`. Nominations (`P1411`) only on request.
- **P856 websites**: every official site not on the item (new domain, festival or
  youth site). Skip URLs that differ only by `http`/`https`, `www.` or a trailing slash.
  Qualify each with `P407` language of work: the language(s) the site is written in,
  usually `Q188` German; one `P407` per language for a multilingual site (e.g. a
  Low German site → `Q25433`; resolve other languages via `search_items`). An existing
  `P856` without `P407` → repeat it with the qualifier.
- **Social media**: only from real profile links (site footer/header, an opened
  profile), never guessed.
  - `P2013` Facebook: the username from `facebook.com/<username>`; for `facebook.com/<Name>-<digits>/`, the numeric id.
  - `P2003` Instagram: the handle, lowercase, without `@` or query string.
  - `P2397` YouTube channel ID: only a `/channel/UC…` id.
  - `P11245` YouTube handle: from `youtube.com/@<handle>`, without `@`, query or trailing path, case kept.
  - Add each one found; don't derive one from another.
- **Item values**: use "Known QIDs" below, or reuse the QID shown in
  `get_statements`, otherwise one `search_items`. Never guess.
- **Time precision**: `/9` year, `/10` month, `/11` day. Year unless the source gives an exact date.

## Known QIDs

Use these directly, without a lookup.

| QID | Item | Used for |
|---|---|---|
| `Q9299236` | registered association (e. V.) | `P1454` |
| `Q33134157` | Gesellschaft bürgerlichen Rechts (GbR) | `P1454` |
| `Q132555` | de jure | `P1013` on `P571` |
| `Q712144` | de facto | `P1013` on `P571` |
| `Q5727902` | circa | `P1480` on vague counts |
| `Q41755623` | incorrect value | `P2241` on deprecated statements |
| `Q183` | Germany | `P17` |
| `Q188` | German | `P407` on `P856` |
| `Q48183` | German Wikipedia | `S143` |
| `Q328` | English Wikipedia | `S143` |
| `Q618779` | award | `P31` of award items |
| `Q15383322` | cultural prize | `P31` of award items |

Amateur-theatre associations (`P463` member of, `P1027` conferred by):

| QID | Association |
|---|---|
| `Q1004994` | Bund Deutscher Amateurtheater (BDAT) |
| `Q19769225` | Landesverband Amateurtheater Baden-Württemberg |
| `Q2513550` | Verband Bayerischer Amateurtheater |
| `Q122811369` | Verband Berliner Amateurbühnen |
| `Q122829962` | Brandenburgischer Amateurtheaterverband |
| `Q122829963` | Landesverband Bremer Amateurtheater |
| `Q122829964` | Verband Hamburger Amateurtheater |
| `Q122829965` | Verband Hessischer Amateurtheater |
| `Q122829966` | Landesverband Spiel & Theater Mecklenburg-Vorpommern |
| `Q90135929` | Amateurtheaterverband Niedersachsen |
| `Q122829968` | Amateurtheaterverband Nordrhein-Westfalen |
| `Q122829969` | Landesverband Amateurtheater Rheinland-Pfalz |
| `Q122829970` | Verband Saarländischer Amateurtheater |
| `Q122828970` | Landesverband Amateurtheater Sachsen |
| `Q122829971` | Landeszentrum Freies Theater Sachsen-Anhalt |
| `Q122829972` | Landesverband der Amateurtheater Schleswig-Holstein |
| `Q122829973` | Thüringer Theaterverband |

Awards (`P166`):

| QID | Award | Conferred by |
|---|---|---|
| `Q1204590` | Deutscher Amateurtheaterpreis | `Q1004994` BDAT |
| `Q141739904` | Bayerischer Amateurtheaterpreis | `Q2513550` VBAT |

## References

Take the article's ref for the fact and convert it:

| Source | Reference fields |
|---|---|
| Web page (also non-Wikimedia wikis) | `S854 "<cited URL exactly as in the ref>"` `S813 +YYYY-MM-DDT00:00:00Z/11` |
| Wikipedia / other Wikimedia project | only `S143 <project QID>` (German Wikipedia = `Q48183`, English = `Q328`; resolve others). No URL, no date |

- Two refs on the sentence → two reference blocks; the second one starts with `!S…`.
- No `S1065`/`S2960` archive pairs (the script adds them).
- Websites, social media and aliases get no reference.

## Fixing existing statements

Only when the article's sources contradict the item outright. Otherwise → "Conflicts" in the report.

| Case | Action |
|---|---|
| Wrong value (town, year), old value has no reliable ref (only `S143` or none) | `SWITCH_VALUE`, then a line adding your reference |
| Wrong value, but a reliable ref backs it | don't change; report as conflict |
| Wrong property, right value | `SWITCH_PROPERTY` (same data type only) |
| Outdated value that was once right (old website, former name) | add the new value with `R+`; old stays normal |
| Wrong rank | repeat the statement with `R+` / `R0` / `R-` |
| Value never correct | `R-` + `P2241` reason for deprecated rank (resolve the item via `search_items`) |

Never remove anything (`-` prefix, `REMOVE_QUAL`, `REMOVE_REF`). List every change under "Corrections".

## V1 format

One command per line, TAB-separated, the item QID on every line. No `CREATE`/`LAST`
in a group's batch.

```
<QID>	<PROPERTY>	<VALUE>	[R+|R0|R-]	[<QUALIFIER>	<VALUE> ...]	[<SOURCE>	<VALUE> ...]
```

| Kind | Format | Example |
|---|---|---|
| Item | bare id | `Q1726` |
| String / URL / external id | quoted | `"https://www.example.de/"` |
| Monolingual | `lang:"text"` | `de:"Example e. V."` |
| Time | `+YYYY-MM-DDT00:00:00Z/<precision>` | `+1946-00-00T00:00:00Z/9` |
| Quantity | plain number | `117` |
| Unknown | `somevalue` | |
| Alias / label / description | `Ade` / `Lde` / `Dde` + quoted text | `Ade	"SeTA"` |

Repeating an existing statement with extra fields adds qualifiers, references or
the rank to it.

## Examples

```
Q122834859	P571	+1946-00-00T00:00:00Z/9	S854	"https://www.achimer-speeldael.de/chronik"	S813	+2026-10-14T00:00:00Z/11
Q123456789	P571	+1984-00-00T00:00:00Z/9	P1013	Q712144	S854	"https://example-theater.de/chronik"	S813	+2026-10-14T00:00:00Z/11
Q123456789	P571	+1991-00-00T00:00:00Z/9	R+	P1013	Q132555	S854	"https://example-theater.de/chronik"	S813	+2026-10-14T00:00:00Z/11
Q21036369	P571	+1954-00-00T00:00:00Z/9	S143	Q48183
Q122798558	P159	Q1726	P6375	de:"Sudetendeutsche Straße 40, 80937 München"	S854	"<source URL>"	S813	+2026-06-30T00:00:00Z/11
Q17325980	P2124	117	P585	+2019-00-00T00:00:00Z/9	S143	Q48183
Q17325980	P2124	80	P585	+2026-00-00T00:00:00Z/9	P1480	Q5727902	S854	"https://ruhrbuehne-witten.de/verein/"	S813	+2026-10-14T00:00:00Z/11
Q123456789	P576	somevalue	S854	"<source URL>"	S813	+2026-10-14T00:00:00Z/11
Q123456789	P166	Q<award>	P585	+2018-00-00T00:00:00Z/9	P1027	Q<awarding body>	P1686	Q<play>	S854	"<winners list URL>"	S813	+2026-10-14T00:00:00Z/11
Q18289439	Ade	"SeTA"
Q122834860	P856	"https://www.example-theater.de/"	P407	Q188
Q122834860	P2013	"ExampleTheatreBremen"
SWITCH_VALUE	Q123456789	P159	Q<wrong town>	Q<right town>
Q123456789	P159	Q<right town>	S854	"<imprint URL>"	S813	+2026-10-14T00:00:00Z/11
```

## Report (`<base>.qs-report.md`)

For the person who runs the batches; every point actionable. **Leave out empty
sections and sub-headings** (no "None."). No `## Batches` section.

```markdown
# QuickStatements report: <Group name> (<QID>)

Generated <date> from `<base>.wiki`.

## Added statements
| Property | Value | Source |
|---|---|---|
| P571 inception | 1946 | Chronik |

## Skipped
- P571 inception: already on the item (1946).
- P571 1969 (renaming): a renaming is not a founding date.

## Corrections
- P159 headquarters: Q<wrong> → Q<right> (SWITCH_VALUE), per the imprint; old references kept, new one added.

## Conflicts between the item and the article
- Item says inception 1948 with a press reference; the Chronik says 1946. Not changed; check by hand.

## Awards
### Matched to existing items
- Bayerischer Amateurtheaterpreis 2018 → Q<id>
### New items proposed
- *Beispieler Amateurtheaterpreis* (Landkreis Beispiel, since 2005): why it qualifies, sources, pending line:
  `Q123456789	P166	Q<NEW: Beispieler Amateurtheaterpreis>	P585	+2018-00-00T00:00:00Z/9	…`
### Not concrete enough
- "Publikumsliebling 2019" (newspaper poll): no statute or winners list.
### No Wikidata item yet
- …

## Proposals outside the default set
- P973 described at URL https://example-zeitung.de/70-jahre-speeldeel: add?

## Open questions
- …
```
