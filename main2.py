# main2.py
# Variant of main.py that produces one summary file per theme.

import os
from parseFile import parseFile
import config
from metrics_cleaner import clean_metrics
from contextGen import generate_context, CONTEXT
from openrouter_client import summarize_with_openrouter
from consolidate_outs import consolidate_out_files
import hashlib
from pathlib import Path


def gather_metrics_data(dir_path: str, max_payload_bytes: int = 5_000_000):
    p = Path(dir_path)
    if not p.exists():
        raise FileNotFoundError(dir_path)

    file_paths = [f for f in p.rglob("*") if f.is_file()]
    total_bytes = 0
    sha = hashlib.sha256()

    for fp in file_paths:
        try:
            stat = fp.stat()
            total_bytes += stat.st_size
            with fp.open("rb") as fh:
                for chunk in iter(lambda: fh.read(8192), b""):
                    sha.update(chunk)
        except Exception:
            sha.update(str(fp).encode("utf-8"))

    sha_hex = sha.hexdigest()
    was_truncated = total_bytes > max_payload_bytes

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


DATA_DIR = "my_data"
OUT_FILE = "out.txt"


def main():
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

    if os.path.exists(OUT_FILE):
        os.remove(OUT_FILE)

    for file in os.listdir(DATA_DIR):
        if file.endswith(".csv"):
            csv_path = os.path.join(DATA_DIR, file)
            parseFile(csv_path, OUT_FILE)

    try:
        metrics_dir = os.path.join("Metrics", "metrics", "2025-01-22.0")

        if os.path.exists(metrics_dir):
            print(f"Found metrics directory: {metrics_dir}; will produce per-theme summaries...")

            api_key = getattr(config, "OPENROUTER_API_KEY", None)

            for theme in CONTEXT.keys():
                theme_dir = os.path.join(metrics_dir, "row_counts", f"theme={theme}")
                out_filename = f"out_summary_{theme}.txt"

                try:
                    if os.path.exists(theme_dir):
                        payload, files_list, total_bytes, sha_hex, was_truncated = gather_metrics_data(theme_dir)
                        data_text = payload
                        print(f"Theme {theme}: files {len(files_list)}, bytes {total_bytes}")
                    else:
                        # Fallback: use whole metrics directory but filter for theme in filenames
                        payload, files_list, total_bytes, sha_hex, was_truncated = gather_metrics_data(metrics_dir)
                        filtered_parts = [p for p in payload.splitlines(True) if f"theme={theme}" in p]
                        data_text = "".join(filtered_parts) or payload

                    context_text = generate_context(theme)

                    if api_key:
                        free_candidates = ["openai/gpt-oss-20b:free", "openai/gpt-4o-mini:latest", "openai/gpt-5.2"]
                        summary = summarize_with_openrouter(
                            data_text,
                            context_text,
                            api_key=api_key,
                            model_candidates=free_candidates,
                        )
                        print(f"--- Summary for theme: {theme} ---")
                        print(summary)
                        with open(out_filename, "w", encoding="utf-8") as sf:
                            sf.write(summary)
                    else:
                        print("OPENROUTER_API_KEY not configured; skipping summary generation for themes.")
                except Exception as e:
                    print(f"Warning: failed to generate summary for theme {theme}: {e}")
            # After attempting per-theme summaries, consolidate any generated files
            try:
                consolidated = consolidate_out_files(output_dir='.', pattern='out_summary_*.txt', output_file='out2.txt')
                if consolidated:
                    print(f"Consolidated summaries into {consolidated}")
                else:
                    print("No per-theme summary files found to consolidate.")
            except Exception as e:
                print(f"Warning: failed to consolidate summary files: {e}")
        else:
            print(f"Metrics directory {metrics_dir} not found; cannot produce per-theme summaries.")
    except Exception as e:
        print("Warning: failed to generate per-theme OpenRouter summaries:", str(e))


if __name__ == "__main__":
    main()
