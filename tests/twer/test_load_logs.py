import csv
import tempfile
import unittest
from pathlib import Path

from research.twer.contract import SCHEMAS, SCHEMA_VERSION
from research.twer.load_logs import TwerCSVError, load_csv, validate_rows


def valid_row(kind, identifier="setup-1"):
    row = {name: "" for name in SCHEMAS[kind]}
    row.update({
        "schema_version": SCHEMA_VERSION,
        "engine_version": "fixture-1",
        "parameter_set_hash": "sha256:fixture",
        "population": "STRICT",
        "setup_id": "setup-1",
        "symbol": "EURUSD",
        "timeframe": "M5",
        "side": "SELL",
        "event_time_utc": "2026-01-01T10:05:00Z",
        "bar_time_utc": "2026-01-01T10:05:00+00:00",
        "state": "S14_DONE",
        "reason_code": "",
    })
    if kind == "setups.csv":
        row["setup_id"] = identifier
        row["b_price"] = "1.1000"
        row["b_extreme_time_utc"] = "2026-01-01T10:01:00Z"
        row["b_confirm_time_utc"] = "2026-01-01T10:05:00Z"
    elif kind == "transitions.csv":
        row["transition_id"] = identifier
        row["from_state"] = "S8_REJECTION"
        row["to_state"] = "S9_B"
    else:
        row["candidate_id"] = identifier
    return row


class TwerCSVContractTests(unittest.TestCase):
    def test_valid_setup_row_has_no_errors(self):
        self.assertEqual(validate_rows([valid_row("setups.csv")], "setups.csv"), [])

    def test_duplicate_setup_ids_are_reported(self):
        rows = [valid_row("setups.csv"), valid_row("setups.csv")]
        errors = validate_rows(rows, "setups.csv")
        self.assertTrue(any("duplicate setup_id" in item for item in errors))

    def test_b_confirmation_cannot_precede_extreme(self):
        row = valid_row("setups.csv")
        row["b_confirm_time_utc"] = "2026-01-01T09:59:00Z"
        errors = validate_rows([row], "setups.csv")
        self.assertTrue(any("B confirmation precedes B extreme" in item for item in errors))

    def test_unknown_population_is_reported(self):
        row = valid_row("setups.csv")
        row["population"] = "MIXED"
        errors = validate_rows([row], "setups.csv")
        self.assertTrue(any("invalid population" in item for item in errors))

    def test_non_finite_numeric_is_reported(self):
        row = valid_row("setups.csv")
        row["b_price"] = "NaN"
        errors = validate_rows([row], "setups.csv")
        self.assertTrue(any("b_price must be a finite number" in item for item in errors))

    def test_csv_reader_preserves_raw_values(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "setups.csv"
            row = valid_row("setups.csv")
            with path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=SCHEMAS["setups.csv"])
                writer.writeheader()
                writer.writerow(row)
            loaded = load_csv(path)
            self.assertEqual(loaded[0]["b_price"], "1.1000")
            self.assertEqual(loaded[0]["population"], "STRICT")

    def test_missing_required_header_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "setups.csv"
            path.write_text("setup_id,symbol\nsetup-1,EURUSD\n", encoding="utf-8")
            with self.assertRaises(TwerCSVError):
                load_csv(path)

    def test_transition_requires_from_and_to_states(self):
        row = valid_row("transitions.csv")
        row["to_state"] = ""
        errors = validate_rows([row], "transitions.csv")
        self.assertTrue(any("from_state and to_state are required" in item for item in errors))


if __name__ == "__main__":
    unittest.main()
