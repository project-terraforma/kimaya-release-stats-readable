# calls parseFile given a file (.csv) and returns the out to out.txt
# repeats calls for every .csv file in my_data folder and appends the out to out.txt
# checks if out.txt exists, if so, deletes it before writing new data

# imports
# main.py

import os
from parseFile import parseFile
#from pinecone import Pinecone
import config
from metrics_cleaner import clean_metrics
from contextGen import generate_context
from openrouter_client import summarize_with_openrouter
import hashlib
from pathlib import Path


def gather_metrics_data(dir_path: str, max_payload_bytes: int = 5_000_000):
    """Walk `dir_path` and produce a tuple:
    (payload_text, files_list, total_bytes, sha256_hex, was_truncated)

    If total size > `max_payload_bytes`, payload_text will be a best-effort truncated
    representation: a small header + first 2048 bytes of each file, and was_truncated=True.
    """
    p = Path(dir_path)
    if not p.exists():
        raise FileNotFoundError(dir_path)

    file_paths = [f for f in p.rglob("*") if f.is_file()]
    total_bytes = 0
    sha = hashlib.sha256()

    # First compute hash and total size without loading everything into memory
    for fp in file_paths:
        try:
            stat = fp.stat()
            total_bytes += stat.st_size
            # Update hash streaming
            with fp.open("rb") as fh:
                for chunk in iter(lambda: fh.read(8192), b""):
                    sha.update(chunk)
        except Exception:
            # ignore unreadable files but include path
            sha.update(str(fp).encode("utf-8"))

    sha_hex = sha.hexdigest()

    was_truncated = total_bytes > max_payload_bytes

    # Build payload_text based on size
    parts = []
    parts.append(f"Metrics directory: {dir_path}\nFiles: {len(file_paths)}\nTotalBytes: {total_bytes}\nSHA256: {sha_hex}\n\n")

    if was_truncated:
        parts.append("NOTE: Payload truncated — including file names and file-heads only.\n\n")

    for fp in file_paths:
        parts.append(f"--- FILE: {fp.relative_to(p)} ({fp.stat().st_size} bytes) ---\n")
        try:
            if was_truncated:
                with fp.open("r", encoding="utf-8", errors="replace") as fh:
                    head = fh.read(2048)
                    parts.append(head)
                    parts.append("\n\n")
            else:
                with fp.open("r", encoding="utf-8", errors="replace") as fh:
                    parts.append(fh.read())
                    parts.append("\n\n")
        except Exception:
            parts.append("[UNREADABLE FILE]\n\n")

    payload_text = "".join(parts)
    return payload_text, [str(x) for x in file_paths], total_bytes, sha_hex, was_truncated

# Use API key from config.py (set PINECONE_API in that file)
# Pinecone related calls commented out for local testing of cleaner
# pc = Pinecone(api_key=config.PINECONE_API)
# index = pc.Index("quickstart")

DATA_DIR = "my_data"
OUT_FILE = "out.txt"


def main():
    # Clean metrics CSVs before any other processing — skip if cleaned data exists
    def _cleaned_data_exists(output_dir: str = "cleanedData") -> bool:
        for root, _, files in os.walk(output_dir):
            for f in files:
                if f.lower().endswith(".csv"):
                    return True
        return False

    try:
        if not _cleaned_data_exists():
            clean_metrics()
        else:
            print("Cleaned data already exists under cleanedData/ — skipping metrics_cleaner.clean_metrics()")
    except Exception:
        pass
    # Delete out.txt if it exists
    if os.path.exists(OUT_FILE):
        os.remove(OUT_FILE)

    # Process each CSV file
    for file in os.listdir(DATA_DIR):
        if file.endswith(".csv"):
            csv_path = os.path.join(DATA_DIR, file)
            parseFile(csv_path, OUT_FILE)

    # After aggregating parsed output, attempt to produce an LLM-readable summary
    try:
        metrics_dir = os.path.join("Metrics", "metrics", "2025-01-22.0")

        # If the metrics directory exists, gather its data and verify against OUT_FILE
        if os.path.exists(metrics_dir):
            print(f"Found metrics directory: {metrics_dir}; gathering files...")
            metrics_payload, files_list, total_bytes, sha_hex, was_truncated = gather_metrics_data(metrics_dir)

            print(f"Metrics files: {len(files_list)}, total bytes: {total_bytes}, sha256: {sha_hex}")

            # Read out.txt if it exists and compute its hash
            out_exists = os.path.exists(OUT_FILE)
            out_sha = None
            if out_exists:
                sha_out = hashlib.sha256()
                with open(OUT_FILE, "rb") as ofh:
                    for chunk in iter(lambda: ofh.read(8192), b""):
                        sha_out.update(chunk)
                out_sha = sha_out.hexdigest()
                print(f"OUT_FILE {OUT_FILE} sha256: {out_sha}")

            if out_exists and out_sha == sha_hex:
                print("Verification: `out.txt` matches concatenated metrics directory (OK). Using out.txt for summarization.")
                with open(OUT_FILE, "r", encoding="utf-8") as f:
                    data_text = f.read()
            else:
                print("Verification: mismatch or out.txt missing — using metrics directory content for summarization.")
                data_text = metrics_payload

            # Use a sensible default theme; adjust as needed
            context_text = generate_context("addresses")

            # Use API key from config if present, otherwise environment var will be used
            api_key = getattr(config, "OPENROUTER_API_KEY", None)

            if api_key:
                # Try free models first for testing; OpenRouter account policy may still block some.
                free_candidates = ["openai/gpt-oss-20b:free", "openai/gpt-4o-mini:latest", "openai/gpt-5.2"]
                summary = summarize_with_openrouter(
                    data_text,
                    context_text,
                    api_key=api_key,
                    model_candidates=free_candidates,
                )
                print("--- OpenRouter Summary ---")
                print(summary)
                # save summary to file
                with open("out_summary.txt", "w", encoding="utf-8") as sf:
                    sf.write(summary)
            else:
                print("OPENROUTER_API_KEY not configured; skipping summary generation.")
        else:
            print(f"Metrics directory {metrics_dir} not found; falling back to existing out.txt if present.")
            if os.path.exists(OUT_FILE):
                with open(OUT_FILE, "r", encoding="utf-8") as f:
                    data_text = f.read()
                context_text = generate_context("addresses")
                api_key = getattr(config, "OPENROUTER_API_KEY", None)
                if api_key:
                    summary = summarize_with_openrouter(data_text, context_text, api_key=api_key)
                    print("--- OpenRouter Summary ---")
                    print(summary)
                    with open("out_summary.txt", "w", encoding="utf-8") as sf:
                        sf.write(summary)
                else:
                    print("OPENROUTER_API_KEY not configured; skipping summary generation.")
    except Exception as e:
        print("Warning: failed to generate OpenRouter summary:", str(e))


if __name__ == "__main__":
    main()
