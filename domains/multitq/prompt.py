"""
MultiTQ domain: what the parser and the answer generator are told (see scripts/domain.py).
The query and time operators come from the compiler and the temporal layer, which execute
the intent; anchored time ("after X …", "in the same month as X") is the temporal layer's
(analysis_temp.anchor_intent / apply_anchor). Every example is a training question, checked
against the knowledge graph.
"""

_SCHEMA = """\
{{
  "target_class": "<one of: {class_list}>",
  "filters": [{{"property": "<property>", "op": "<operator>", "value": "<string, a list for in, or \\"anchor\\">"}}],
  "return_properties": ["<properties of the target class to SELECT>"],
  "joins": [{{"class": "<class>", "via": "<property>", "direction": "outgoing|incoming",
             "return_properties": ["<properties>"], "filters": [ ... ]}}],
  "aggregation": null or {{"type": "count|min|max", "group_by": null or "Class.property", "target": "<class or property>", "distinct": true|false}},
  "order_by": null or {{"variable": "Class.property", "direction": "ASC|DESC"}},
  "limit": null or <integer>,
  "anchor": null or {{"filters": [ ... ], "joins": [ ... ], "pick": "first|last"}},
  "unanswerable": null,
  "explanation": "<one sentence>"
}}"""

_GRAPH = """\
Graph (direct edges):
  Event —[actor]→     Actor       who did it (Actor.label)
  Event —[recipient]→ Recipient   to whom it was done (Recipient.label)
  Event.eventType     what was done: one of the event types listed below, verbatim
  Event.resultTime    the day it happened (2005-01-01 … 2015-12-31)
Variables are named Class.property: Event.resultTime, Actor.label, Recipient.label."""

_RULES = """\
Rules:
  - target_class is always Event, with return_properties ["resultTime"]. Join Actor (via actor, outgoing) and
    Recipient (via recipient, outgoing), each with return_properties ["label"]; put an entity filter on the join
    of its role.
  - Entities: filter label with op equals, using an exact label from the candidate list given with the question.
    Labels name a group of a country as "Group (Country)": "the Australian police" → "Police (Australia)",
    "the Ministry of South Korea" → "Ministry (South Korea)", "citizens of Brazil" → "Citizen (Brazil)".
  - Roles: the one who acts is the Actor. "Whom did X praise?" → Actor X, answer Recipient. "Who praised X?" →
    Recipient X, answer Actor. Passive "Who was praised by X?" → Actor X, answer Recipient.
  - Event type: choose the ONE listed type that matches the verb, verbatim with op equals ("blamed/accused" →
    Accuse, "visited" → Make a visit, "expressed optimism about" → Make optimistic comment, "announced the
    intention to meet" → Express intent to meet or negotiate).
  - first / earliest → order_by Event.resultTime ASC, limit 1. last / most recent / latest → DESC, limit 1.
    Without first/last, return all matching events (no limit).
  - "When / in which year / in which month" questions ask for the time: the same intent, the answer is
    Event.resultTime.
  - Named periods are resultTime filters with bare dates:
      on 4 February 2006 → from 2006-02-04, until 2006-02-04      in March 2006 → from 2006-03-01, until 2006-03-31
      in 2008 → from 2008-01-01, until 2008-12-31
      after 19 September 2007 → from 2007-09-20 (the day after)     after March 2006 → from 2006-04-01
      after 2009 → from 2010-01-01      before 2012-09 → before 2012-09-01      before 2008 → before 2008-01-01
  - Anchored time: "After X, who first …", "Who last … before X did?", "in the same month/year/day as X" refer to
    the time of ANOTHER event, named by X. Put that event in "anchor" (its eventType and entities, usually the
    question's event with X in the role the main question leaves open) and give the main intent a resultTime
    filter with value "anchor" and op after, before, same_day, same_month or same_year. The temporal layer finds
    the anchor's time and turns the filter into dates. pick is "first" (the anchor's first occurrence) unless the
    question says otherwise.
  - unanswerable is always null here."""

_EXAMPLES = """\
Q: "Who paid a visit to Laos on 4 February 2006?"
{"target_class": "Event",
 "filters": [{"property": "eventType", "op": "equals", "value": "Make a visit"},
             {"property": "resultTime", "op": "from", "value": "2006-02-04"},
             {"property": "resultTime", "op": "until", "value": "2006-02-04"}],
 "return_properties": ["resultTime"],
 "joins": [{"class": "Actor", "via": "actor", "direction": "outgoing", "return_properties": ["label"], "filters": []},
           {"class": "Recipient", "via": "recipient", "direction": "outgoing", "return_properties": ["label"],
            "filters": [{"property": "label", "op": "equals", "value": "Laos"}]}],
 "aggregation": null, "order_by": null, "limit": null, "anchor": null, "unanswerable": null,
 "explanation": "Visits (Make a visit) with Recipient Laos on that day; the answer is the Actor."}

Q: "Who was the first country that Ethiopia expressed optimism about?"
{"target_class": "Event",
 "filters": [{"property": "eventType", "op": "equals", "value": "Make optimistic comment"}],
 "return_properties": ["resultTime"],
 "joins": [{"class": "Actor", "via": "actor", "direction": "outgoing", "return_properties": ["label"],
            "filters": [{"property": "label", "op": "equals", "value": "Ethiopia"}]},
           {"class": "Recipient", "via": "recipient", "direction": "outgoing", "return_properties": ["label"], "filters": []}],
 "aggregation": null, "order_by": {"variable": "Event.resultTime", "direction": "ASC"}, "limit": 1, "anchor": null,
 "unanswerable": null, "explanation": "Ethiopia's optimistic comments, earliest first; the answer is the Recipient."}

Q: "Could you tell me the exact month when the Election Commission of Nepal started negotiations with the other authorities and officials of Nepal?"
{"target_class": "Event",
 "filters": [{"property": "eventType", "op": "equals", "value": "Engage in negotiation"}],
 "return_properties": ["resultTime"],
 "joins": [{"class": "Actor", "via": "actor", "direction": "outgoing", "return_properties": ["label"],
            "filters": [{"property": "label", "op": "equals", "value": "Election Commission (Nepal)"}]},
           {"class": "Recipient", "via": "recipient", "direction": "outgoing", "return_properties": ["label"],
            "filters": [{"property": "label", "op": "equals", "value": "Other Authorities / Officials (Nepal)"}]}],
 "aggregation": null, "order_by": {"variable": "Event.resultTime", "direction": "ASC"}, "limit": 1, "anchor": null,
 "unanswerable": null, "explanation": "'Started' = the first such negotiation; the answer is its month."}

Q: "Who blamed the Police of Tanzania before 2012-09?"
{"target_class": "Event",
 "filters": [{"property": "eventType", "op": "equals", "value": "Accuse"},
             {"property": "resultTime", "op": "before", "value": "2012-09-01"}],
 "return_properties": ["resultTime"],
 "joins": [{"class": "Actor", "via": "actor", "direction": "outgoing", "return_properties": ["label"], "filters": []},
           {"class": "Recipient", "via": "recipient", "direction": "outgoing", "return_properties": ["label"],
            "filters": [{"property": "label", "op": "equals", "value": "Police (Tanzania)"}]}],
 "aggregation": null, "order_by": null, "limit": null, "anchor": null, "unanswerable": null,
 "explanation": "Accusations of Police (Tanzania) before September 2012; the answer is the Actor."}

Q: "After Mexico, with whom did Yasuo Fukuda first want to establish diplomatic cooperation?"
{"target_class": "Event",
 "filters": [{"property": "eventType", "op": "equals", "value": "Express intent to engage in diplomatic cooperation (such as policy support)"},
             {"property": "resultTime", "op": "after", "value": "anchor"}],
 "return_properties": ["resultTime"],
 "joins": [{"class": "Actor", "via": "actor", "direction": "outgoing", "return_properties": ["label"],
            "filters": [{"property": "label", "op": "equals", "value": "Yasuo Fukuda"}]},
           {"class": "Recipient", "via": "recipient", "direction": "outgoing", "return_properties": ["label"], "filters": []}],
 "aggregation": null, "order_by": {"variable": "Event.resultTime", "direction": "ASC"}, "limit": 1,
 "anchor": {"filters": [{"property": "eventType", "op": "equals", "value": "Express intent to engage in diplomatic cooperation (such as policy support)"}],
            "joins": [{"class": "Actor", "via": "actor", "direction": "outgoing", "return_properties": [],
                       "filters": [{"property": "label", "op": "equals", "value": "Yasuo Fukuda"}]},
                      {"class": "Recipient", "via": "recipient", "direction": "outgoing", "return_properties": [],
                       "filters": [{"property": "label", "op": "equals", "value": "Mexico"}]}],
            "pick": "first"},
 "unanswerable": null, "explanation": "The anchor is Fukuda's same intent towards Mexico; the first such event after it gives the Recipient."}

Q: "Who last blamed the People Associated with the Opposition of Brazil before José Dirceu de Oliveira e Silva did?"
{"target_class": "Event",
 "filters": [{"property": "eventType", "op": "equals", "value": "Accuse"},
             {"property": "resultTime", "op": "before", "value": "anchor"}],
 "return_properties": ["resultTime"],
 "joins": [{"class": "Actor", "via": "actor", "direction": "outgoing", "return_properties": ["label"], "filters": []},
           {"class": "Recipient", "via": "recipient", "direction": "outgoing", "return_properties": ["label"],
            "filters": [{"property": "label", "op": "equals", "value": "People Associated with the Opposition (Brazil)"}]}],
 "aggregation": null, "order_by": {"variable": "Event.resultTime", "direction": "DESC"}, "limit": 1,
 "anchor": {"filters": [{"property": "eventType", "op": "equals", "value": "Accuse"}],
            "joins": [{"class": "Actor", "via": "actor", "direction": "outgoing", "return_properties": [],
                       "filters": [{"property": "label", "op": "equals", "value": "José Dirceu de Oliveira e Silva"}]},
                      {"class": "Recipient", "via": "recipient", "direction": "outgoing", "return_properties": [],
                       "filters": [{"property": "label", "op": "equals", "value": "People Associated with the Opposition (Brazil)"}]}],
            "pick": "first"},
 "unanswerable": null, "explanation": "The anchor is Dirceu's accusation; the last accusation before it gives the Actor."}

Q: "With whom did Nicos Anastasiades announce his intention to meet in the same month of New Democracy?"
{"target_class": "Event",
 "filters": [{"property": "eventType", "op": "equals", "value": "Express intent to meet or negotiate"},
             {"property": "resultTime", "op": "same_month", "value": "anchor"}],
 "return_properties": ["resultTime"],
 "joins": [{"class": "Actor", "via": "actor", "direction": "outgoing", "return_properties": ["label"],
            "filters": [{"property": "label", "op": "equals", "value": "Nicos Anastasiades"}]},
           {"class": "Recipient", "via": "recipient", "direction": "outgoing", "return_properties": ["label"], "filters": []}],
 "aggregation": null, "order_by": null, "limit": null,
 "anchor": {"filters": [{"property": "eventType", "op": "equals", "value": "Express intent to meet or negotiate"}],
            "joins": [{"class": "Actor", "via": "actor", "direction": "outgoing", "return_properties": [],
                       "filters": [{"property": "label", "op": "equals", "value": "Nicos Anastasiades"}]},
                      {"class": "Recipient", "via": "recipient", "direction": "outgoing", "return_properties": [],
                       "filters": [{"property": "label", "op": "equals", "value": "New Democracy"}]}],
            "pick": "first"},
 "unanswerable": null, "explanation": "The anchor is the intent towards New Democracy; the same month's other Recipients answer."}

Q: "In which year did Mahmoud Ahmadinejad last denounce the Israeli Defence Forces?"
{"target_class": "Event",
 "filters": [{"property": "eventType", "op": "equals", "value": "Criticize or denounce"}],
 "return_properties": ["resultTime"],
 "joins": [{"class": "Actor", "via": "actor", "direction": "outgoing", "return_properties": ["label"],
            "filters": [{"property": "label", "op": "equals", "value": "Mahmoud Ahmadinejad"}]},
           {"class": "Recipient", "via": "recipient", "direction": "outgoing", "return_properties": ["label"],
            "filters": [{"property": "label", "op": "equals", "value": "Israeli Defense Forces"}]}],
 "aggregation": null, "order_by": {"variable": "Event.resultTime", "direction": "DESC"}, "limit": 1, "anchor": null,
 "unanswerable": null, "explanation": "The last denunciation; the answer is the year of its resultTime."}"""


def parse_system(class_list: str, query_operators: str, time_operators: str) -> str:
    return f"""You are a semantic parser for a temporal knowledge graph of dated political events (MultiTQ, ICEWS 2005-2015):
each Event is an Actor doing one event type to a Recipient on one day.

Given a natural-language question, output ONLY a valid JSON object (no markdown fences) with this exact schema:

{_SCHEMA.format(class_list=class_list)}

Operator guide:
{query_operators}
{time_operators}
  after / before / same_day / same_month / same_year with the value "anchor" — relative to the anchor event's time (see Rules)

{_GRAPH}

{_RULES}

--- EXAMPLES ---

{_EXAMPLES}

--- END EXAMPLES ---
"""


def answer_system(query_guide: str, time_guide: str) -> str:
    return f"""You are a concise analyst of a knowledge graph of dated political events (who did what to whom, and when).

You are given a user question, SPARQL results, and a numeric summary.

Rules:
- Answer the question directly in 1-2 short sentences, naming the entity or entities, or the date, that answer it.
- For "when" questions give the date at the granularity asked: the year for "which year", the year and month for "which month", the full date otherwise.
- For "first"/"last" questions the results are already ordered and limited: the first row is the answer.
- If the results are empty or contain an error, say that it cannot be determined from the knowledge graph.
- Use the entity labels as written in the results. Do NOT output URIs or explain the query.

{query_guide}

{time_guide}
"""


def vocabulary(backend) -> str | None:
    rows = backend.query("PREFIX mtq: <http://herikgqa.org/multitq/ontology#> "
                         "SELECT DISTINCT ?t WHERE { ?e mtq:eventType ?t } ORDER BY ?t")
    types = [r["t"] for r in rows if "error" not in r and r.get("t")]
    if not types:
        return None
    return ("Event types in this knowledge graph (Event.eventType — use one verbatim with op equals):\n"
            + "; ".join(types))
