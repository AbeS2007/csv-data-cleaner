# CSV Cleaner

A dependency-free Python command-line tool for common spreadsheet cleanup tasks.

It:

- normalizes column headers to consistent `snake_case` names;
- trims whitespace from every cell;
- removes completely blank rows;
- removes exact duplicate rows;
- safely pads short rows and trims extra cells;
- writes a JSON report describing every cleanup action.

## Run it

```bash
python csv_cleaner.py sample_input.csv cleaned_output.csv --report cleaning_report.json
```

The script uses only Python's standard library and leaves the original file unchanged.

## Included example

`sample_input.csv` contains inconsistent headers, extra spaces, a blank row, a duplicate row, and one short row. The included cleaned output and report show the result.
