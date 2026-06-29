# Reading the Wikidata item

You need three things from the item: the **name**, a **short description**, and
**outbound links** to seed web research. The structured facts (dates, location,
members) are rendered on-wiki by `{{DynamicInfobox}}`, so do not spend effort
transcribing them — read them only insofar as they help you write or verify a
sentence of prose.

## Use the Wikidata MCP — and only for Wikidata

Read the item through the **Wikidata MCP**. Reserve the MCP for Wikidata requests:
the web research in step 2 of the workflow is ordinary `web_search` / `web_fetch`,
not an MCP job. The MCP tools are deferred, so load them once per session with
`tool_search` (e.g. `tool_search("wikidata get statements")`) before calling them.

The tools you will actually use:

| Tool | When |
| ------ | ------ |
| `get_statements(entity_id, include_external_ids=true)` | **the default first call** — returns the description, aliases, and every direct statement with labels resolved |
| `get_statement_values(entity_id, property_id)` | only when you need a statement's qualifiers or references (e.g. the postal-code qualifier on P159, or the source URL behind a claim) |
| `search_items(query)` | only when the user gave you a **name instead of a QID** — find the QID first, confirm it, then `get_statements` |
| `execute_sparql(sparql)` | only for genuine graph questions (rare here); not needed to read one item |

A single `get_statements` call is normally the whole read. Example:

```text
get_statements(entity_id="Q122798923", include_external_ids=true)
-> Theatergruppe "Kulturfabrik Berching" (Q122798923): description: amateur theatre group in Berching (Bavaria, Germany)
   ... headquarters location (P159): Berching (Q248062)
   ... member of (P463): Verband Bayerischer Amateurtheater (Q2513550)
   ... official website (P856): http://www.kulturfabrik-berching.de/
   ... instance of (P31): theatre troupe (Q2416217)
   ... country (P17): Germany (Q183)
```

Labels come back already resolved, so you rarely need a second call just to turn
a Q-id into a name. The official-website value is your primary research seed.

## Properties worth reading

| Property | Meaning | Use it for |
| ---------- | --------- | ----------- |
| **P31** | instance of | confirm this is a theatre group / troupe / ensemble, not an unrelated entity |
| **P856** | official website | **primary research seed** — fetch it first in step 2 |
| **P571** | inception | founding year for the lead sentence (verify against web sources) |
| **P159** | headquarters location | town/city; its **P281** qualifier is the postal code |
| **P131** | located in admin. territory | region / district |
| **P276** | location | venue, if distinct from HQ |
| **P463** | member of | the umbrella association — usually a **local** wiki link |
| **P2002 / P2013 / P2003** | X(Twitter) / Facebook / Instagram | secondary research seeds |
| **P227 / P214** | GND / VIAF id (needs `include_external_ids=true`) | authority links; pair with `normdata-search` if you want a `{{Normdaten}}` footer |

You rarely need more than P31 (sanity check), P856 (research seed), P463 (the
association to link), and a glance at P159/P571 to phrase the lead. The infobox
handles the rest from the same QID.

## When the MCP can't resolve the item

If the Wikidata MCP is unavailable or returns nothing for the QID:
Say so plainly.

Never fabricate Wikidata contents to paper over a failed read. If you genuinely
cannot determine the group's name, stop and ask.
