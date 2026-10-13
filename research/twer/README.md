# TWER offline CSV reader

This package is a standalone research adapter. It does not detect setups, connect to MT5, place orders, or modify TradingAgents Core.

## Contract status

The CSV column names in `docs/TWER/OFFLINE-EXPORT-CONTRACT.md` are a **draft proposal**. The TWER specification defines the purpose of `setups.csv`, `transitions.csv`, and `rejects.csv`, and says each row carries the parameter-set hash and population, but it does not prescribe literal header names. Before the EA logger is built, approve the headers and version the contract.

## Run tests

From the repository root with Python 3.11+:

```bash
python -m unittest discover -s tests/twer -v
```

## Use the reader

```python
from research.twer import load_csv, validate_rows

rows = load_csv("setups.csv")
issues = validate_rows(rows, "setups.csv")
if issues:
    print("\\n".join(issues))
```

The reader returns source values as strings to avoid silently rounding prices or changing source data. Validation returns diagnostics and does not mutate rows. Do not aggregate `STRICT` and `ARRIVAL` populations or different parameter hashes into one result without an explicit analysis step.
