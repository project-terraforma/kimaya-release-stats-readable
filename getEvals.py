from __future__ import annotations

import csv
import re
import time
import sys
from typing import Optional, List, Tuple

import config
from typing import Optional


def load_text(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""

try:
    import google.generativeai as genai
except Exception:
    genai = None

MODEL = "gemini-2.5-pro"


def configure_gemini(api_key: str):
    if genai is None:
        raise RuntimeError("google.generativeai package not available")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(MODEL)


def extract_numeric_grade(text: str) -> Optional[int]:
    if not text:
        return None
    # Accept any single digit 0-4 (Gemini may return any integer between 0 and 4)
    m = re.search(r"\b([0-4])\b", text)
    if m:
        return int(m.group(1))
    return None


def grade_with_gemini(model, question: str, response: str, context: Optional[str] = None, max_retries: int = 3) -> Tuple[int, str]:
    # Include the provided context and instruct the grader to use ONLY that context
    prompt = (
        "You will be given a CONTEXT, a QUESTION and a MODEL RESPONSE.\n"
        "Use ONLY the CONTEXT to determine whether the RESPONSE is accurate and not fabricated.\n"
        "Apply this grading scheme exactly:\n"
        "0: Model response is inaccurate and gives incorrect information or invents data not in the CONTEXT.\n"
        "2: Some of the response is correct relative to the CONTEXT, but most parts are incorrect or fabricated.\n"
        "4: Model response answers the question properly using only the given CONTEXT (accurate and not fabricated).\n\n"
        "Return ONLY a single integer between 0 and 4, and nothing else.\n\n"
        "If the CONTEXT does not contain information needed to answer the question, judge whether the response invents facts (give 0) or correctly states that the data is insufficient (give 4).\n\n"
        "Context:\n" + (context or "") + "\n\n"
        f"Question:\n{question}\n\nResponse:\n{response}\n\n"
    )

    text = ""
    for attempt in range(max_retries):
        try:
            messages = [{"role": "user", "parts": [{"text": prompt}]}]
            resp = model.generate_content(messages)
            if resp and hasattr(resp, "parts") and resp.parts:
                text = getattr(resp.parts[0], "text", "") or ""
                grade = extract_numeric_grade(text.strip())
                if grade is not None:
                    return grade, text
            time.sleep(1 + attempt)
        except Exception as e:
            # capture exception text and continue retrying
            text = str(e)
            time.sleep(1 + attempt)
    # fallback
    return 0, text


def ensure_row_length(row: List[str], length: int = 7) -> List[str]:
    if len(row) >= length:
        return row
    return row + [""] * (length - len(row))


def main(csv_path: str = "test_sample_questions.csv") -> None:
    api_key = getattr(config, "GEMINI_API_KEY", None)
    if not api_key:
        print("GEMINI_API_KEY not found in config.py", file=sys.stderr)
        raise SystemExit(1)
    if genai is None:
        print("google.generativeai is not installed; cannot call Gemini", file=sys.stderr)
        raise SystemExit(1)

    model = configure_gemini(api_key)

    # load context file (default name out2.txt)
    context_text = load_text("out2.txt")

    with open(csv_path, "r", encoding="utf-8", newline="") as f:
        rows = list(csv.reader(f))
    if not rows:
        print("CSV is empty", file=sys.stderr)
        return

    header = rows[0]
    data_rows = rows[1:]

    # determine which columns to use: prefer `baseline` for grading, then response2, then response
    hdr_lower = [h.strip().lower() for h in header]
    question_idx = hdr_lower.index("question") if "question" in hdr_lower else 0
    if "baseline" in hdr_lower:
        response_idx = hdr_lower.index("baseline")
    elif "response2" in hdr_lower:
        response_idx = hdr_lower.index("response2")
    else:
        response_idx = hdr_lower.index("response") if "response" in hdr_lower else 1
    grade_idx = hdr_lower.index("grade2") if "grade2" in hdr_lower else 2

    # ensure header contains grade column; if not, append grade2
    out_header = list(header)
    if grade_idx >= len(out_header) or not out_header[grade_idx].strip():
        # extend header to include grade2
        if grade_idx >= len(out_header):
            out_header += [""] * (grade_idx - len(out_header) + 1)
        out_header[grade_idx] = "grade2"

    # add a raw/debug column name derived from the grade column (e.g., grade2_raw)
    grade_col_name = out_header[grade_idx]
    raw_col_name = f"{grade_col_name}_raw"
    if raw_col_name.lower() not in [h.lower() for h in out_header]:
        out_header.append(raw_col_name)
    raw_idx = [h.strip().lower() for h in out_header].index(raw_col_name.lower())

    updated: List[List[str]] = []
    total = len(data_rows)
    for idx, row in enumerate(data_rows, start=1):
        # ensure row is long enough to hold grade
        row = ensure_row_length(row, grade_idx + 1)
        question = row[question_idx].strip() if len(row) > question_idx else ""
        response_text = row[response_idx].strip() if len(row) > response_idx else ""

        grade, raw = grade_with_gemini(model, question, response_text, context=context_text)
        # Accept any integer in [0,4]; fallback to 0 on unexpected values
        if not isinstance(grade, int) or not (0 <= grade <= 4):
            grade = 0
        # write grade into selected grade column and raw text into debug column
        row = ensure_row_length(row, max(grade_idx, raw_idx) + 1)
        row[grade_idx] = str(grade)
        row[raw_idx] = raw
        updated.append(row)
        # print grade and a truncated version of the raw reasoning so user can monitor progress
        safe_raw = (raw or "").strip().replace("\n", " ")
        if len(safe_raw) > 500:
            display_raw = safe_raw[:500] + "... (truncated)"
        else:
            display_raw = safe_raw
        print(f"Processed {idx}/{total}: grade={grade}")
        print("Reason:", display_raw)
        time.sleep(0.2)

    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(out_header)
        writer.writerows(updated)

    # write compact scores file with grade and reasoning/raw reply
    scores_path = "scores.csv"
    with open(scores_path, "w", encoding="utf-8", newline="") as sf:
        sw = csv.writer(sf)
        sw.writerow(["grade", "reason"])
        for r in updated:
            g = r[grade_idx] if len(r) > grade_idx else ""
            reason = r[raw_idx] if len(r) > raw_idx else ""
            sw.writerow([g, reason])


if __name__ == "__main__":
    main()
