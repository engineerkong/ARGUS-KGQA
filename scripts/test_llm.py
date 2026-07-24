"""
Measure the LLM endpoint's response latency. Uses the same env vars and client
config as the pipeline (see 1_semantic_parser.py / 3_answer_generator.py), so a
green run here means the pipeline can reach the model too.

    python scripts/test_llm.py            # one round-trip, non-streaming
    python scripts/test_llm.py -n 5       # 5 round-trips, report min/mean/max
    python scripts/test_llm.py --stream   # also measure time-to-first-token

Env: OLLAMA_BASE_URL, OPENAI_API_KEY, OLLAMA_MODEL, ARGUS_LLM_TIMEOUT.
"""

from __future__ import annotations
import argparse
import os
import sys
import time

from openai import OpenAI

BASE_URL = os.environ.get("OLLAMA_BASE_URL", "https://ollama.fit.fraunhofer.de/api")
API_KEY  = os.environ.get("OPENAI_API_KEY", "no-key")
MODEL    = os.environ.get("OLLAMA_MODEL", "gpt-oss:120b")
TIMEOUT  = float(os.environ.get("ARGUS_LLM_TIMEOUT", "120"))

PROMPT = "Reply with the single word: pong."


def _client() -> OpenAI:
    # No retries here: we want to see real failures/latency, not silent recovery.
    return OpenAI(base_url=BASE_URL, api_key=API_KEY, timeout=TIMEOUT, max_retries=0)


def _one_shot(client: OpenAI) -> tuple[float, str]:
    start = time.perf_counter()
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": PROMPT}],
        temperature=0,
    )
    elapsed = time.perf_counter() - start
    return elapsed, resp.choices[0].message.content or ""


def _one_stream(client: OpenAI) -> tuple[float, float, str]:
    start = time.perf_counter()
    ttft = None
    chunks: list[str] = []
    stream = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": PROMPT}],
        temperature=0,
        stream=True,
    )
    for chunk in stream:
        delta = chunk.choices[0].delta.content if chunk.choices else None
        if delta:
            if ttft is None:
                ttft = time.perf_counter() - start
            chunks.append(delta)
    total = time.perf_counter() - start
    return (ttft if ttft is not None else total), total, "".join(chunks)


def main() -> int:
    ap = argparse.ArgumentParser(description="Measure LLM endpoint response latency.")
    ap.add_argument("-n", "--num", type=int, default=1, help="number of requests")
    ap.add_argument("--stream", action="store_true", help="measure time-to-first-token")
    args = ap.parse_args()

    print(f"endpoint : {BASE_URL}")
    print(f"model    : {MODEL}")
    print(f"timeout  : {TIMEOUT}s")
    print(f"requests : {args.num} ({'streaming' if args.stream else 'non-streaming'})")
    print("-" * 60)

    client = _client()
    latencies: list[float] = []
    ttfts: list[float] = []

    for i in range(1, args.num + 1):
        try:
            if args.stream:
                ttft, total, reply = _one_stream(client)
                ttfts.append(ttft)
                latencies.append(total)
                print(f"#{i}: ttft {ttft:6.2f}s  total {total:6.2f}s  reply={reply.strip()!r}")
            else:
                total, reply = _one_shot(client)
                latencies.append(total)
                print(f"#{i}: {total:6.2f}s  reply={reply.strip()!r}")
        except Exception as e:
            print(f"#{i}: FAILED after {TIMEOUT}s cap — {type(e).__name__}: {e}")

    print("-" * 60)
    if not latencies:
        print("all requests failed — endpoint unreachable or misconfigured")
        return 1

    n = len(latencies)
    print(f"ok {n}/{args.num}  "
          f"min {min(latencies):.2f}s  mean {sum(latencies)/n:.2f}s  max {max(latencies):.2f}s")
    if ttfts:
        print(f"ttft            min {min(ttfts):.2f}s  mean {sum(ttfts)/len(ttfts):.2f}s  max {max(ttfts):.2f}s")
    return 0 if n == args.num else 2


if __name__ == "__main__":
    sys.exit(main())
