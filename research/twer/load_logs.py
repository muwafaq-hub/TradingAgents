"""Offline-only CSV reader for the proposed TWER export contract.

No network, broker, MT5, LLM, or TradingAgents Core dependencies.
"""
import csv
import math
from datetime import datetime
from pathlib import Path

from .contract import (
    COMMON, NUMERIC_COLUMNS, POPULATIONS, REASON_CODES, SCHEMA_VERSION,
    SCHEMAS, SIDES,
)


class TwerCSVError(ValueError):
    """Raised when an export is structurally unsafe to analyze."""


def _parse_time(value, field, row_number, errors):
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None or parsed.utcoffset() is None:
            errors.append(f"row {row_number}: {field} must include a timezone")
            return None
        if parsed.utcoffset().total_seconds() != 0:
            errors.append(f"row {row_number}: {field} must be UTC (offset +00:00)")
            return None
        return parsed
    except ValueError:
        errors.append(f"row {row_number}: invalid ISO-8601 timestamp in {field}")
        return None


def load_csv(path, kind=None):
    """Load one known export CSV, returning raw row dictionaries unchanged."""
    path = Path(path)
    kind = kind or path.name
    if kind not in SCHEMAS:
        raise TwerCSVError(f"unsupported export file: {kind}")
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise TwerCSVError(f"{path}: missing CSV header")
        missing = [name for name in SCHEMAS[kind] if name not in reader.fieldnames]
        if missing:
            raise TwerCSVError(f"{path}: missing required columns: {', '.join(missing)}")
        return [dict(row) for row in reader]


def validate_rows(rows, kind):
    """Return a list of diagnostic strings; do not mutate source rows."""
    if kind not in SCHEMAS:
        raise TwerCSVError(f"unsupported export file: {kind}")
    errors, seen = [], set()
    id_field = {
        "setups.csv": "setup_id",
        "transitions.csv": "transition_id",
        "rejects.csv": "candidate_id",
    }[kind]
    for index, row in enumerate(rows, start=2):
        required_values = ("schema_version", "engine_version", "parameter_set_hash", "population", "setup_id", "symbol", "timeframe", "side", "event_time_utc", "bar_time_utc", "state")
        for field in required_values:
            if not row.get(field, "").strip():
                errors.append(f"row {index}: {field} is required")
        if row.get("schema_version") != SCHEMA_VERSION:
            errors.append(f"row {index}: unsupported schema_version {row.get('schema_version')!r}")
        if not row.get("engine_version", "").strip():
            errors.append(f"row {index}: engine_version is required")
        if not row.get("parameter_set_hash", "").strip():
            errors.append(f"row {index}: parameter_set_hash is required")
        if row.get("population") not in POPULATIONS:
            errors.append(f"row {index}: invalid population {row.get('population')!r}")
        if row.get("side") not in SIDES:
            errors.append(f"row {index}: invalid side {row.get('side')!r}")
        identifier = row.get(id_field, "").strip()
        if not identifier:
            errors.append(f"row {index}: {id_field} is required")
        elif identifier in seen:
            errors.append(f"row {index}: duplicate {id_field} {identifier!r}")
        else:
            seen.add(identifier)
        if row.get("reason_code", "") not in REASON_CODES:
            errors.append(f"row {index}: unknown reason_code {row.get('reason_code')!r}")
        for field in NUMERIC_COLUMNS:
            value = row.get(field, "")
            if value is None or not value.strip():
                continue
            try:
                number = float(value)
                if not math.isfinite(number):
                    raise ValueError
            except ValueError:
                errors.append(f"row {index}: {field} must be a finite number")
        event = _parse_time(row.get("event_time_utc", ""), "event_time_utc", index, errors)
        _parse_time(row.get("bar_time_utc", ""), "bar_time_utc", index, errors)
        if kind == "setups.csv":
            extreme = _parse_time(row.get("b_extreme_time_utc", ""), "b_extreme_time_utc", index, errors)
            confirm = _parse_time(row.get("b_confirm_time_utc", ""), "b_confirm_time_utc", index, errors)
            if extreme and confirm and confirm < extreme:
                errors.append(f"row {index}: B confirmation precedes B extreme")
            if row.get("b_price", "").strip() and not confirm:
                errors.append(f"row {index}: b_price is present but B confirmation time is missing/invalid")
        elif kind == "transitions.csv":
            if not row.get("from_state", "").strip() or not row.get("to_state", "").strip():
                errors.append(f"row {index}: from_state and to_state are required")
    return errors


def load_export_bundle(directory):
    """Load and validate setups/transitions/rejects; return rows and diagnostics."""
    directory = Path(directory)
    result = {"rows": {}, "errors": {}}
    for name in SCHEMAS:
        path = directory / name
        if not path.exists():
            result["errors"][name] = [f"missing export file: {path}"]
            continue
        try:
            rows = load_csv(path)
            result["rows"][name] = rows
            result["errors"][name] = validate_rows(rows, name)
        except (OSError, TwerCSVError) as exc:
            result["errors"][name] = [str(exc)]
    return result
