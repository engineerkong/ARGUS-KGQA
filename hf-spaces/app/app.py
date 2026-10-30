"""
HeriKGQA demo: a chat interface to the question-answering pipeline over a
frozen, anonymised snapshot of the heritage sensor knowledge graph.

Started by start.sh once PostgreSQL and the Ontop SPARQL endpoint are up
(HERIKG_SPARQL_ENDPOINT). Each browser session keeps its own conversation; one
question is answered at a time, as there is one pipeline (configured per question)
and the LLM endpoint allows few concurrent requests.

The system's configuration options (parse candidates n, retry budget k, history
turns h, answer check) are shown beside the conversation, set to THOROUGH's.

Every answered question is logged (question, answer, configuration, latency) and
can be rated good / fine / bad, with a comment for "bad". Logs go to
HERIKG_LOG_DIR and, when HF_TOKEN and FEEDBACK_REPO are set, are pushed to that
(private) Hugging Face dataset every few minutes.

The parsed intent is shown without its unset fields and the SPARQL without unused
prefixes, so both fit beside the conversation. On screens at least 1024 px wide
(or any screen with "?figure" in the URL) the page is a landscape layout at most
1600 px wide, in larger type, with the conversation, parsed intent and SPARQL shown
in full, so that a screenshot stays legible when scaled to a page.
"""

import json
import os
import re
import sys
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path

import gradio as gr

sys.path.insert(0, str(Path(__file__).resolve().parent / "scripts"))
from pipeline import Config, Pipeline, get_config  # noqa: E402

# Configuration options, defaulting to THOROUGH's (n=3, k=2, h=2, answer check on).
DEFAULT = dict(n=3, k=2, h=2, check=True)
N_MAX, K_MAX, H_MAX = 5, 3, 4
# Side by side (wide screens), the side column is exactly as tall as the
# conversation column: "contain: size" keeps its content from adding height. The
# parsed intent and SPARQL share the height left over, each with one scrollbar
# (CodeMirror's; Gradio's wrapper around it would add a second). Only should even
# their minimum not fit (configuration and feedback both open) does the column scroll.
# Stacked (narrow screens), each has a fixed height.
CSS = """
#side > * { flex: 0 0 auto; }
#rating-row { align-items: center; flex-wrap: nowrap; }
#rating-row .wrap { gap: 6px; }
#rating-row label { padding: 6px 10px; }
#rating-row button { white-space: nowrap; }
.rating-label { color: var(--block-label-text-color); font-size: var(--block-label-text-size); }
#intent, #sparql { display: flex !important; flex-direction: column; overflow: hidden !important; }
#intent > .wrap:not(.full), #sparql > .wrap:not(.full) { flex: 1 1 0; min-height: 0; overflow: hidden; }
#intent .codemirror-wrapper, #sparql .codemirror-wrapper { height: 100%; overflow: hidden !important; }
#intent .cm-editor, #sparql .cm-editor { height: 100%; }
#intent .cm-scroller, #sparql .cm-scroller { overflow: auto; }
@media (min-width: 768px) {
  #layout { flex-wrap: nowrap; }
  #side { contain: size; overflow-y: auto; flex-wrap: nowrap; }
  #side > #details:has(> .label-wrap.open) { flex: 1 1 0; display: flex; flex-direction: column; overflow: visible !important; }
  #details > .label-wrap.open + div { display: flex !important; flex-direction: column; flex: 1 1 0; }
  #details > .label-wrap.open + div > .column { flex: 1 1 0; }
  #details > .label-wrap.open + div > .column > * { flex: 0 0 auto; }
  #details #intent, #details #sparql { flex: 1 1 0; min-height: 6em; }
}
@media (max-width: 767px) {
  #details #intent, #details #sparql { height: 18em; }
}
/* landscape layout (screens >= 1024 px, or ?figure): about twice as wide as high and legible when a
   screenshot is scaled down to a page: conversation on the left; on the right configuration, feedback and
   "New conversation" in one row, and below them the parsed intent beside the SPARQL, both shown in full and
   reaching down to the bottom of the examples */
body.landscape .gradio-container { width: 100% !important; max-width: 1600px !important; margin: 0 auto !important;
  --text-sm: 16px; --text-md: 18px; --text-lg: 20px; --block-label-text-size: 16px; --block-title-text-size: 16px;
  --layout-gap: 12px; }
body.landscape main.fillable { max-width: none !important; }
body.landscape footer { display: none !important; }
body.landscape #layout > .column { flex: 1 1 0 !important; }
body.landscape #layout > #side { display: grid !important; grid-template-columns: 1fr 1fr auto;
  grid-template-rows: auto 1fr; }
body.landscape #side > #details { grid-column: 1 / -1; grid-row: 2; }
body.landscape #side > button { grid-column: 3; grid-row: 1; align-self: stretch; height: auto; }
body.landscape #details > .label-wrap.open + div > .column { display: grid !important; grid-template-columns: 2fr 3fr;
  grid-template-rows: auto 1fr; align-items: stretch; }
body.landscape #details > .label-wrap.open + div > .column > :first-child { grid-column: 1 / -1; }
body.landscape #chat, body.landscape #chat .bubble-wrap { height: auto !important; max-height: none !important; }
body.landscape #chat { min-height: 380px; }
body.landscape #chat .message-row { margin: 8px 16px 4px !important; }
body.landscape #chat .message-wrap { margin-bottom: 4px !important; }
body.landscape #side { contain: none !important; overflow: visible !important; }
body.landscape #side > #details { display: flex !important; flex-direction: column; border: none !important;
  padding: 0 !important; background: none !important; box-shadow: none !important; }
body.landscape #details > .label-wrap.open + div, body.landscape #details > .label-wrap.open + div > .column {
  flex: 1 1 auto !important; }
body.landscape #details > .label-wrap.open + div { display: flex !important; flex-direction: column; }
body.landscape #details #intent, body.landscape #details #sparql { flex: none !important; height: auto !important; }
body.landscape #intent > .wrap:not(.full), body.landscape #sparql > .wrap:not(.full),
body.landscape #intent .codemirror-wrapper, body.landscape #sparql .codemirror-wrapper,
body.landscape #intent .cm-editor, body.landscape #sparql .cm-editor { flex: none !important; height: auto !important;
  overflow: visible !important; }
body.landscape .cm-editor { font-size: 15px; }
body.landscape .cm-editor .cm-line { line-height: 1.3; }
body.landscape #chat .md { font-size: 18px; }
body.landscape .label-wrap span { font-size: 16px; }
body.landscape #layout .gallery { display: grid !important; grid-template-columns: 1fr 1fr; }
body.landscape #layout .gallery > button, body.landscape #layout .gallery > button > div { max-width: none !important;
  display: block !important; font-size: 16px; text-align: left; white-space: nowrap; overflow: hidden;
  text-overflow: ellipsis; }
"""
# Adds the class behind the landscape layout above on screens at least 1024 px wide, or on any screen
# when the URL has "?figure".
LANDSCAPE_JS = ("() => { if (window.innerWidth >= 1024 || new URLSearchParams(location.search).has('figure')) "
                "document.body.classList.add('landscape'); }")
EXAMPLES = [
    "How many sensor nodes are installed at site A?",
    "What is the average temperature at site C?",
    "Which two sensor nodes at site B are farthest apart, and how far?",
    "What time period do the readings at site E cover?",
    "Was the temperature at site C anomalous on 2026-07-15 according to its AD-RT rules?",
    "What was the average temperature at site A over the last 24 hours?",
]
NOTE = """**HeriKGQA** answers questions about sensor readings (13 May – 12 August 2026) from five cultural heritage
sites, anonymised as **site A – site E** and moved to fictitious locations. Every number in an answer is computed
by SPARQL or deterministic code, not by the language model. Questions, answers and ratings are logged anonymously."""

# ── pipeline: one backend and vocabulary, configured per question ───────────
PIPELINE = Pipeline(verbose=False, config=get_config("thorough", n=3), keep_history=True)
LOCK = threading.Lock()


def make_config(n: int, k: int, h: int, check: bool) -> Config:
    """The Config for these options: "thorough" for the defaults, else named by them."""
    name = ("thorough" if dict(n=n, k=k, h=h, check=check) == DEFAULT
            else f"custom-n{n}-k{k}-h{h}-{'check' if check else 'nocheck'}")
    return Config(name, parse_candidates=n, max_retries=k, max_history=max(h, 1),
                  answer="llm+check" if check else "llm")

# ── logging ─────────────────────────────────────────────────────────────────
LOG_DIR = Path(os.environ.get("HERIKG_LOG_DIR", Path(__file__).resolve().parent.parent / "logs"))
LOG_DIR.mkdir(parents=True, exist_ok=True)
QUERY_LOG, FEEDBACK_LOG = LOG_DIR / "queries.jsonl", LOG_DIR / "feedback.jsonl"
_log_lock = threading.Lock()
if os.environ.get("HF_TOKEN") and os.environ.get("FEEDBACK_REPO"):
    from huggingface_hub import CommitScheduler
    SCHEDULER = CommitScheduler(repo_id=os.environ["FEEDBACK_REPO"], repo_type="dataset", private=True,
                                folder_path=LOG_DIR, path_in_repo="logs", every=5,
                                token=os.environ["HF_TOKEN"])
    _log_lock = SCHEDULER.lock


def _log(path: Path, record: dict) -> None:
    with _log_lock:
        with path.open("a") as f:
            f.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


# ── handlers ────────────────────────────────────────────────────────────────
def new_session():
    return {"session": uuid.uuid4().hex[:12], "history": [], "last": None}


def ask(question, n, k, h, check, chat, state):
    state = state or new_session()
    question = (question or "").strip()
    if not question:
        return ("", chat, state) + (gr.update(),) * 6
    n, k, h = (min(max(int(x), lo), hi) for x, lo, hi in ((n, 1, N_MAX), (k, 0, K_MAX), (h, 0, H_MAX)))
    check = bool(check)
    cfg = make_config(n, k, h, check)
    # The session keeps up to H_MAX turns; the parser gets the last h of them.
    earlier = state["history"][-h:] if h else []
    with LOCK:
        p = PIPELINE
        p.config, p.max_retries, p.max_history = cfg, cfg.max_retries, cfg.max_history
        p.history = list(earlier)
        try:
            r = p.run(question)
            answer = r["answer"]
        except Exception as e:  # e.g. the LLM endpoint is unavailable
            r = {}
            answer = ("Sorry, the language model service is busy right now. Please try again in a minute."
                      if type(e).__name__ == "RateLimitError" else
                      f"Sorry, the question could not be answered ({type(e).__name__}). Please try again.")
        if p.history and p.history[-1]["query"] == question:
            state["history"] = (state["history"] + [p.history[-1]])[-H_MAX:]
    settings = {"n": n, "k": k, "h": h, "answer_check": check}
    turn = {"id": uuid.uuid4().hex[:12], "session": state["session"], "time": _now(),
            "config": cfg.name, "settings": settings,
            "question": question, "answer": answer, "latency_s": r.get("latency_s"),
            "llm_calls": r.get("llm_calls"), "earlier_questions": [t["query"] for t in earlier]}
    _log(QUERY_LOG, {**turn, "intent": r.get("intent"), "sparql": r.get("sparql")})
    state["last"] = turn
    chat = chat + [{"role": "user", "content": question}, {"role": "assistant", "content": answer}]
    # a fresh rating form for the new answer
    return ("", chat, state, *_details(r, settings), gr.update(value=None), gr.update(value=""), "")


def _summary(n="–", k="–", h="–", check="–", calls="–", latency="–") -> str:
    """The configuration and cost line; "–" where there is no answer yet."""
    items = [f"**n** = {n}", f"**k** = {k}", f"**h** = {h}", f"**answer check:** {check}",
             f"**LLM calls:** {calls}", f"**Latency:** {latency}"]
    # a line wraps only between items
    return "&ensp;·&ensp; ".join(i.replace(" ", "&nbsp;") for i in items)


def _unset_dropped(v):
    """v without its unset (null, false, empty) fields, at every level."""
    if isinstance(v, dict):
        v = {k: _unset_dropped(x) for k, x in v.items()}
        return {k: x for k, x in v.items() if x not in (None, "", [], {}, False)}
    if isinstance(v, list):
        return [_unset_dropped(x) for x in v]
    return v


def _compact_intent(intent: dict) -> str:
    """The intent as JSON without its unset fields, one field per line and one join per line."""
    shown = _unset_dropped(intent)
    dump = lambda v: json.dumps(v, ensure_ascii=False)
    lines = [f' "{k}": ' + ("[\n" + ",\n".join(f"  {dump(j)}" for j in v) + "\n ]"
                            if k == "joins" and v else dump(v)) for k, v in shown.items()]
    return "{\n" + ",\n".join(lines) + "\n}"


def _used_prefixes(sparql: str) -> str:
    """The query with only the PREFIX declarations its body uses, without their alignment padding."""
    lines = sparql.splitlines()
    body = "\n".join(l for l in lines if not l.lstrip().upper().startswith("PREFIX"))
    keep = []
    for l in lines:
        m = re.match(r"\s*PREFIX\s+([\w-]*):\s*", l, re.I)
        if m is None:
            keep.append(l)
        elif re.search(rf"(?<![\w-]){re.escape(m.group(1))}:", body):
            keep.append(f"PREFIX {m.group(1)}: {l[m.end():]}")
    return "\n".join(keep).strip()


def _details(r: dict, s: dict) -> tuple[str, str, str]:
    """Summary line, parsed intent (JSON) and SPARQL of an answer."""
    if not r:
        return _summary(), "", ""
    summary = _summary(s["n"], s["k"], s["h"], "on" if s["answer_check"] else "off",
                       r.get("llm_calls", "–"), f"{r['latency_s']} s" if r.get("latency_s") is not None else "–")
    intent = _compact_intent(r["intent"]) if r.get("intent") else ""
    sparql = _used_prefixes(str(r.get("sparql") or ""))
    return summary, intent, sparql


def rate(rating, comment, state):
    """Rate the latest answer, once."""
    last = (state or {}).get("last")
    if not last:
        return gr.update(), "Ask a question first, then rate its answer.", state
    if last.get("rated"):
        return gr.update(), "This answer has already been rated.", state
    if not rating:
        return gr.update(), "Please choose a rating.", state
    if rating == "bad" and not (comment or "").strip():
        return gr.update(), "Please tell us briefly what went wrong.", state
    _log(FEEDBACK_LOG, {**last, "rating": rating, "comment": (comment or "").strip(), "rated_at": _now()})
    last["rated"] = True
    return gr.update(value=""), "Thank you for your feedback.", state


def reset(state):
    state = new_session()
    return [], state, _summary(), "", "", gr.update(value=None), gr.update(value=""), ""


# ── interface ───────────────────────────────────────────────────────────────
with gr.Blocks(title="HeriKGQA", css=CSS, js=LANDSCAPE_JS) as demo:
    gr.Markdown("# HeriKGQA\n" + NOTE)
    state = gr.State(None)  # created on the first question (new_session)
    with gr.Row(elem_id="layout", equal_height=True):
        with gr.Column(scale=3):
            chat = gr.Chatbot(type="messages", height=460, label="Conversation", elem_id="chat")
            with gr.Row():
                box = gr.Textbox(placeholder="Ask about a statistic, a place, a time or an anomaly…",
                                 show_label=False, scale=5)
                send = gr.Button("Ask", variant="primary", scale=1, min_width=80)
            gr.Examples(EXAMPLES, inputs=box, label="Examples")
        with gr.Column(scale=2, elem_id="side"):
            with gr.Accordion("Configuration", open=False):
                with gr.Row():
                    n_opt = gr.Dropdown(list(range(1, N_MAX + 1)), value=DEFAULT["n"], label="Parse candidates n",
                                        info="parses voted on", min_width=100)
                    k_opt = gr.Dropdown(list(range(0, K_MAX + 1)), value=DEFAULT["k"], label="Retry budget k",
                                        info="re-parses on failure", min_width=100)
                    h_opt = gr.Dropdown(list(range(0, H_MAX + 1)), value=DEFAULT["h"], label="History turns h",
                                        info="earlier turns used", min_width=100)
                check_opt = gr.Checkbox(value=DEFAULT["check"], label="Answer check",
                                        info="numbers, timestamps and verdict checked against the evidence")
            with gr.Accordion("Feedback", open=False):  # rates the latest answer
                gr.Markdown("How good was this answer?", elem_classes="rating-label")
                with gr.Row(elem_id="rating-row"):
                    rating = gr.Radio(["good", "fine", "bad"], show_label=False, container=False, scale=1)
                    submit = gr.Button("Send rating", size="md", scale=0, min_width=100)
                comment = gr.Textbox(label="What went wrong? (required for 'bad')", lines=2)
                thanks = gr.Markdown()
            with gr.Accordion("How this answer was computed", open=True, elem_id="details"):
                summary = gr.Markdown(_summary())
                intent_box = gr.Code(label="Parsed intent", language="json", interactive=False, elem_id="intent",
                                     wrap_lines=True, show_line_numbers=False)
                sparql_box = gr.Code(label="SPARQL", language="sql", interactive=False, elem_id="sparql",
                                     wrap_lines=True, show_line_numbers=False)
            clear = gr.Button("New conversation")

    for trigger in (send.click, box.submit):
        trigger(ask, [box, n_opt, k_opt, h_opt, check_opt, chat, state],
                [box, chat, state, summary, intent_box, sparql_box, rating, comment, thanks])
    submit.click(rate, [rating, comment, state], [comment, thanks, state])
    clear.click(reset, [state], [chat, state, summary, intent_box, sparql_box, rating, comment, thanks])

demo.queue(default_concurrency_limit=1, max_size=32)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", "7860")))
