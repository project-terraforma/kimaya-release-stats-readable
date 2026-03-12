#!/usr/bin/env python3

import os
import csv
import time
from typing import Optional

from openrouter_client import summarize_with_openrouter

# try to import local config for API keys
try:
    import config
except Exception:
    config = None


def load_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def read_questions(path: str):
    # Return the full rows (dicts) so we can update a response column in-place
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    return rows, reader.fieldnames if reader.fieldnames is not None else []


def main(
    data_path: str,
    questions_path: str,
    out_path: str,
    api_key: Optional[str] = None,
    delay: float = 0.5,
    model: Optional[str] = None,
):
    if api_key is None:
        api_key = os.environ.get("OPENROUTER_API_KEY")
    # fallback to config.py if present
    if not api_key and config is not None:
        api_key = getattr(config, "OPENROUTER_API_KEY", None)

    if not api_key:
        raise RuntimeError("No OpenRouter API key provided via --api-key, OPENROUTER_API_KEY env var, or config.OPENROUTER_API_KEY")

    data_text = load_text(data_path)

    rows, fieldnames = read_questions(questions_path)

    # Ensure we will write a `response` column
    out_fields = list(fieldnames) if fieldnames else []
    if "response" not in [f.lower() for f in out_fields]:
        out_fields.append("response")

    # Determine output path: default to overwrite the questions file unless out_path provided
    if out_path is None:
        out_path = questions_path

    for idx, row in enumerate(rows, start=1):
        # find question text
        q = None
        # prefer explicit 'question' key (case-insensitive)
        for k in row.keys():
            if k and k.strip().lower() == "question":
                q = row[k]
                break
        if q is None:
            # fallback to first column value
            keys = list(row.keys())
            if keys:
                q = row[keys[0]]

        if not q:
            row["response"] = ""
            continue

        prompt_desc = f"Answer the question below based only on the provided data.\nQuestion:\n{q}"
        try:
            short_system = (
                "answer the questions in 1-3 sentences using only the context provided (this should be the out.txt file)"
            )
            resp = summarize_with_openrouter(
                data_text=data_text,
                context_text=prompt_desc,
                api_key=api_key,
                model=model,
                system_prompt_override=short_system,
            )
        except Exception as e:
            resp = f"__ERROR__:{type(e).__name__}: {e}"

        row["response"] = resp
        # polite pause
        time.sleep(delay)

    # Write updated rows back
    with open(out_path, "w", newline="", encoding="utf-8") as outf:
        writer = csv.DictWriter(outf, fieldnames=out_fields)
        writer.writeheader()
        for r in rows:
            # ensure all keys exist
            out_row = {k: r.get(k, "") for k in out_fields}
            writer.writerow(out_row)

    print(f"Wrote responses for {len(rows)} questions to {out_path}")


if __name__ == "__main__":
    # Default in-file configuration — run `python3 getResponses.py` to execute
    DEFAULT_DATA = "out.txt"
    DEFAULT_QUESTIONS = "test_sample_questions.csv"
    # overwrite the questions file to insert `response` by default
    DEFAULT_OUT = DEFAULT_QUESTIONS
    DEFAULT_API_KEY = None  # will fall back to env var or config.OPENROUTER_API_KEY
    DEFAULT_DELAY = 0.5
    DEFAULT_MODEL = "nvidia/nemotron-3-nano-30b-a3b:free"

    main(
        data_path=DEFAULT_DATA,
        questions_path=DEFAULT_QUESTIONS,
        out_path=DEFAULT_OUT,
        api_key=DEFAULT_API_KEY,
        delay=DEFAULT_DELAY,
        model=DEFAULT_MODEL,
    )
