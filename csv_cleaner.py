#!/usr/bin/env python3
"""Clean a CSV file and produce a transparent JSON summary."""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path


def normalize_header(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_") or "column"


def unique_headers(headers: list[str]) -> list[str]:
    seen: dict[str, int] = {}
    result: list[str] = []
    for header in headers:
        base = normalize_header(header)
        seen[base] = seen.get(base, 0) + 1
        result.append(base if seen[base] == 1 else f"{base}_{seen[base]}")
    return result


def clean_csv(input_path: Path, output_path: Path, report_path: Path) -> dict:
    with input_path.open("r", encoding="utf-8-sig", newline="") as source:
        reader = csv.reader(source)
        try:
            raw_headers = next(reader)
        except StopIteration as exc:
            raise ValueError("The input CSV is empty.") from exc

        headers = unique_headers(raw_headers)
        cleaned_rows: list[list[str]] = []
        seen_rows: set[tuple[str, ...]] = set()
        blank_rows_removed = 0
        duplicates_removed = 0
        padded_or_trimmed_rows = 0

        for raw_row in reader:
            row = [cell.strip() for cell in raw_row]
            if not any(row):
                blank_rows_removed += 1
                continue
            if len(row) != len(headers):
                padded_or_trimmed_rows += 1
                row = (row + [""] * len(headers))[: len(headers)]
            key = tuple(row)
            if key in seen_rows:
                duplicates_removed += 1
                continue
            seen_rows.add(key)
            cleaned_rows.append(row)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as destination:
        writer = csv.writer(destination)
        writer.writerow(headers)
        writer.writerows(cleaned_rows)

    report = {
        "input_file": input_path.name,
        "output_file": output_path.name,
        "columns": headers,
        "rows_written": len(cleaned_rows),
        "blank_rows_removed": blank_rows_removed,
        "duplicate_rows_removed": duplicates_removed,
        "rows_padded_or_trimmed": padded_or_trimmed_rows,
    }
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Normalize headers, trim whitespace, remove blank and duplicate rows, and generate a JSON report."
    )
    parser.add_argument("input_csv", type=Path)
    parser.add_argument("output_csv", type=Path)
    parser.add_argument("--report", type=Path, default=Path("cleaning_report.json"))
    args = parser.parse_args()

    report = clean_csv(args.input_csv, args.output_csv, args.report)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
