import csv
import json
import tempfile
import unittest
from pathlib import Path

from csv_cleaner import clean_csv, normalize_header, unique_headers


class CsvCleanerTests(unittest.TestCase):
    def test_header_normalization_and_uniqueness(self):
        self.assertEqual(normalize_header(" Email Address "), "email_address")
        self.assertEqual(unique_headers(["Name", "Name", ""]), ["name", "name_2", "column"])

    def test_cleaning_pipeline(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "input.csv"
            output = root / "output.csv"
            report = root / "report.json"
            source.write_text(
                " Name , Email \n Alice , a@example.com \n\nAlice,a@example.com\nBob\n",
                encoding="utf-8",
            )

            summary = clean_csv(source, output, report)

            with output.open(newline="", encoding="utf-8") as stream:
                rows = list(csv.reader(stream))
            self.assertEqual(rows, [["name", "email"], ["Alice", "a@example.com"], ["Bob", ""]])
            self.assertEqual(summary["blank_rows_removed"], 1)
            self.assertEqual(summary["duplicate_rows_removed"], 1)
            self.assertEqual(summary["rows_padded_or_trimmed"], 1)
            self.assertEqual(json.loads(report.read_text(encoding="utf-8")), summary)


if __name__ == "__main__":
    unittest.main()
