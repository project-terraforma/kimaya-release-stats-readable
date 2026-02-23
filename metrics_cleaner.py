import os
import csv


def _is_empty_row(row):
    return all((cell is None) or (str(cell).strip() == "") for cell in row)


def _ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def clean_csv_file(src_path, dst_path):
    # Read CSV, drop empty rows and duplicate data rows (preserve header and order)
    try:
        with open(src_path, newline='', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            rows = list(reader)
    except Exception as e:
        # If reading fails, return error status
        return ('error', str(e))

    if not rows:
        return ('skipped', 'empty')

    header = rows[0]
    data_rows = rows[1:]

    seen = set()
    unique_rows = []

    for row in data_rows:
        if _is_empty_row(row):
            continue
        key = tuple(cell.strip() if cell is not None else "" for cell in row)
        if key in seen:
            continue
        seen.add(key)
        unique_rows.append(row)

    # Ensure destination directory exists
    _ensure_dir(os.path.dirname(dst_path))

    # Write cleaned CSV (preserve header)
    try:
        with open(dst_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            for row in unique_rows:
                writer.writerow(row)
    except Exception as e:
        return ('error', str(e))

    return ('finished', '')


def clean_metrics(root_dir=None, input_dir='Metrics', output_dir='cleanedData'):
    """Traverse `input_dir` under `root_dir` (or current file dir) and write cleaned CSVs
    to `output_dir` preserving the relative folder structure.
    """
    if root_dir is None:
        root_dir = os.path.dirname(os.path.abspath(__file__))

    src_root = os.path.join(root_dir, input_dir)
    dst_root = os.path.join(root_dir, output_dir)

    if not os.path.exists(src_root):
        return

    for dirpath, dirnames, filenames in os.walk(src_root):
        rel_dir = os.path.relpath(dirpath, src_root)
        if rel_dir == '.':
            rel_dir = ''
        for fname in filenames:
            if not fname.lower().endswith('.csv'):
                continue
            src_path = os.path.join(dirpath, fname)
            rel_path = os.path.join(rel_dir, fname) if rel_dir else fname
            dst_dir = os.path.join(dst_root, rel_dir)
            dst_path = os.path.join(dst_dir, fname)

            # Progress: show which file is being processed
            print(f"Cleaning: {rel_path}")

            status, info = clean_csv_file(src_path, dst_path)

            # Report status after attempting to clean
            if status == 'finished':
                print(f"Finished: {rel_path}")
            elif status == 'skipped':
                print(f"Skipped (empty): {rel_path}")
            else:
                print(f"Error cleaning {rel_path}: {info}")


if __name__ == '__main__':
    clean_metrics()
