import os
import json
import requests
from typing import Optional, List


def summarize_with_openrouter(data_text: str, context_text: str, api_key: Optional[str] = None,
                              model: Optional[str] = None,
                              model_candidates: Optional[List[str]] = None,
                              timeout: int = 30,
                              system_prompt_override: Optional[str] = None) -> str:
    """Send `data_text` and `context_text` to OpenRouter and return the model's summary.

    The function expects an API key (string). If `api_key` is None, the function will
    read from environment variable `OPENROUTER_API_KEY`.
    """
    if api_key is None:
        api_key = os.environ.get("OPENROUTER_API_KEY")

    if not api_key:
        raise ValueError("OpenRouter API key not provided (argument or OPENROUTER_API_KEY env var)")

    if system_prompt_override:
        system_prompt = system_prompt_override
    else:
        system_prompt = (
            "You are a helpful assistant that summarizes tabular/aggregated data for downstream automated QA. "
            "Produce an LLM-readable, structured summary that preserves key numeric and categorical details, column meanings, and change metrics. "
            "Format the summary so another model can answer a broad set of analytic questions (totals, top-k counts, distributions, examples, and release-change comparisons) using only the summary text. "
            "Use explicit labelled sections (e.g., 'Totals', 'Top-10 by X', 'Distribution of Y', 'Examples', 'Changes between releases') and include units where applicable. "
            "Keep the text concise but include concrete numbers, short lists, and brief examples to enable reliable downstream extraction."
        )

    user_content = (
        "Context and column definitions:\n\n" + context_text + "\n\n"
        "Data to summarize:\n\n" + data_text
    )

    # Build base payload; model will be set per-attempt below
    base_payload = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    urls = [
        "https://openrouter.ai/api/v1/chat/completions",
        "https://api.openrouter.ai/v1/chat/completions",
    ]

    # Determine which models to try
    candidates = ["meta-llama/llama-3.3-70b-instruct:free"]
    if model:
        candidates.append(model)
    if model_candidates:
        for m in model_candidates:
            if m not in candidates:
                candidates.append(m)

    # sensible defaults (free-first) if nothing provided
    if not candidates:
        candidates = ["openai/gpt-oss-20b:free", "openai/gpt-5.2", "openai/gpt-4o-mini"]

    resp = None
    last_err = None
    used_model = None

    for m in candidates:
        payload = dict(base_payload)
        payload["model"] = m
        for url in urls:
            try:
                resp = requests.post(url, headers=headers, data=json.dumps(payload), timeout=timeout)
                if resp.status_code == 404:
                    last_err = requests.HTTPError(f"404 Not Found for url: {url} (model={m})")
                    continue
                resp.raise_for_status()
                used_model = m
                break
            except Exception as e:
                last_err = e
                resp = None
                continue
        if resp is not None:
            break

    if resp is None:
        raise last_err

    body = resp.json()

    # OpenRouter mirrors the chat completions format; extract message text.
    try:
        choices = body.get("choices") or []
        if not choices:
            return json.dumps(body)
        # Try common response shapes
        first = choices[0]
        message = first.get("message") or {}
        content = message.get("content") or first.get("text") or first.get("content") or ""
        if used_model:
            # include a short note about which model was used
            return f"[model_used={used_model}]\n" + content
        return content
    except Exception:
        return json.dumps(body)
