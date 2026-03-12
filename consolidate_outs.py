"""consolidate_outs.py

Utility to concatenate per-theme summary files named like
`out_summary_<theme>.txt` into a single `out2.txt` file.
"""
from __future__ import annotations

import glob
import os
from typing import Optional


def consolidate_out_files(output_dir: str = ".", pattern: str = "out_summary_*.txt", output_file: str = "out2.txt") -> Optional[str]:
    """Find files matching `pattern` in `output_dir`, concatenate them into `output_file`.

    Returns the path to the consolidated file, or None if no matching files found.
    """
    search_path = os.path.join(output_dir, pattern)
    files = sorted(glob.glob(search_path))
    if not files:
        return None

    out_path = os.path.join(output_dir, output_file)
    with open(out_path, "w", encoding="utf-8") as out_f:
        for f in files:
            try:
                size = os.path.getsize(f)
            except Exception:
                size = 0
            out_f.write(f"--- FILE: {os.path.basename(f)} ({size} bytes) ---\n")
            try:
                with open(f, "r", encoding="utf-8", errors="replace") as fh:
                    out_f.write(fh.read())
            except Exception:
                out_f.write("[UNREADABLE FILE]\n")
            out_f.write("\n\n")

    return out_path


if __name__ == "__main__":
    result = consolidate_out_files()
    if result:
        print(f"Consolidated summaries written to: {result}")
    else:
        print("No summary files found to consolidate.")
