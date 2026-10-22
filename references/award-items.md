# Awards without a Wikidata item

Read this only when an award has no item, or when the user reports a created award QID.

## 1. Decide: propose an item?

All three must hold:

- a **fixed official name** (`Bayerischer Amateurtheaterpreis`, `Kulturpreis der Stadt Achim`);
- an **identifiable awarding body** (association, municipality, foundation, festival);
- **evidence about the award itself** (winners list, statute or call for entries, the
  body's page, press naming the prize); ideally recurring.

Fails (→ report under "Not concrete enough", with the reason): certificates of
thanks, unnamed mentions, newspaper polls with no other trace, "Sonderapplaus",
festival invitations, nominations.

## 2. Check for duplicates

Stop at the first hit:

1. `search_items` on the native name, the English name and variants (with or
   without year, body name, legal form).
2. If the awarding body has an item: SPARQL for items with `P1027` = that body.
3. Output folder: a `*.award-items.qs` with a `CREATE` block whose `Lde` label is
   the same, or a `*.pending.qs` with the same placeholder → reuse that placeholder
   exactly, write no new `CREATE` block.

A hit in 1 or 2 → use that item for `P166` (normal batch).

## 3. Research the award

The only new research allowed in Step 5. A few searches: `"<award>" verliehen`,
`Preisträger`, `Satzung`, `Ausschreibung`. Main reference: the awarding body's page.

## 4. Write `<base>.award-items.qs`

`<base>` = the group that first proposes the award. One `CREATE` block per award.
Add only statements the sources support. Resolve every item value with
`search_items` and confirm with `get_statements`; never guess QIDs or PIDs.

| Statement | Command | Notes |
|---|---|---|
| Labels | `Lde`, `Len` | native name; `Len` the same unless an official English name exists |
| Descriptions | `Dde`, `Den` | e.g. `Den "amateur theatre award of the Verband Bayerischer Amateurtheater"` |
| Aliases | `Ade` | short or former names from sources |
| Instance of | `P31` | most specific existing class: theatre award, culture prize, award |
| Conferred by | `P1027` | skip if the body has no item (never create one) |
| Country | `P17` | |
| Jurisdiction | `P1001` | state, district or municipality covered |
| Official name | `P1448` | `de:"…"` |
| Inception | `P571` | year founded or first awarded |
| Abolished | `P576` | only with explicit evidence |
| Part of | `P361` | festival or competition, if it has an item |
| Named after | `P138` | only if the namesake has an item |
| Prize money | `P2121` | `5000U<euro QID>` + `P585` |
| Interval | `P2257` | `1U<year QID>` annual, `2U<year QID>` biennial |
| Website | `P856` | the award's own page, with `P407` language of work (usually `Q188` German) |

Reference every statement except labels, descriptions, aliases and the website
with `S854` + `S813`. Never create items for awarding bodies or people.

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

## 5. Write `<base>.pending.qs`

The group's `P166` lines for the new award, with the placeholder
`Q<NEW: <Lde label>>`. The label must match the `CREATE` block's `Lde` character
for character. Pending lines never go into `<base>.qs`.

```
Q123456789	P166	Q<NEW: Beispieler Amateurtheaterpreis>	P585	+2018-00-00T00:00:00Z/9	S854	"<winners list URL>"	S813	+2026-10-14T00:00:00Z/11
```

Copy them into the qs-report under "New items proposed".

## Resolving placeholders

Trigger: the user says "<award label> is Q…". Work across the whole output folder,
no new research.

1. `get_statements` on the QID: label = placeholder label, `P31` and `P1027` match
   the `CREATE` block. ⛔ Mismatch → stop and ask. Given only a label → `search_items`.
2. One SPARQL query for items with `P166` = the QID, so no line is added twice.
3. For each `*.pending.qs` with the placeholder: replace it with the QID, append
   those lines to the group's `<base>.qs` (create it if missing), remove them from
   `.pending.qs`. Delete a `.pending.qs` once it's empty.
4. Delete the award's `CREATE` block from its `.award-items.qs`; delete the file if it's empty.
5. In each affected `<base>.qs-report.md`: add the new `P166` rows to "Added
   statements", move the award from "New items proposed" to "Matched to existing
   items" as "<label> → Q… (created <date>)", and rewrite the pending line with the QID.
6. Tell the user to run `build_batches.py` on the folder (or run it, if you have a shell).

Manual alternative for the user:
`sed -i 's/Q<NEW: <label>>/Q…/g' *.pending.qs`, move the lines into each `.qs`, run `build_batches.py`.
