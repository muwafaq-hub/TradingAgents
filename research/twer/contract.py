"""Versioned draft schema for MT5 TWER CSV exports."""
SCHEMA_VERSION = "1.0-draft"
POPULATIONS = {"STRICT", "ARRIVAL"}
SIDES = {"BUY", "SELL"}

COMMON = (
    "schema_version", "engine_version", "parameter_set_hash", "population",
    "setup_id", "symbol", "timeframe", "side", "event_time_utc",
    "bar_time_utc", "state", "reason_code",
)
SETUP_COLUMNS = COMMON + (
    "origin_price", "ext1_price", "pullback_price", "ext2_price",
    "model_start_utc", "model_end_utc", "model_tail_price", "model_high",
    "model_low", "model_body_high", "model_body_low", "model_candles",
    "rejection", "b_price", "b_extreme_time_utc", "b_confirm_time_utc",
    "b_revisions", "arm_start_utc", "arm_bars", "entry_count",
    "entry1_price", "entry2_price", "entry3_price", "sl_exact_tail",
    "sl_test", "tp_price", "r_multiple", "atr", "spread_at_signal",
    "score", "grade", "result", "mae", "mfe", "exit_time_utc",
    "time_to_entry_seconds", "time_to_b_seconds", "time_to_exit_seconds",
    "slippage_points",
)
TRANSITION_COLUMNS = COMMON + (
    "transition_id", "from_state", "to_state", "bid", "ask", "close_price",
)
REJECT_COLUMNS = COMMON + (
    "candidate_id", "from_state", "detected_at_utc", "details",
)
SCHEMAS = {
    "setups.csv": SETUP_COLUMNS,
    "transitions.csv": TRANSITION_COLUMNS,
    "rejects.csv": REJECT_COLUMNS,
}
NUMERIC_COLUMNS = {
    "origin_price", "ext1_price", "pullback_price", "ext2_price",
    "model_tail_price", "model_high", "model_low", "model_body_high",
    "model_body_low", "model_candles", "b_price", "b_revisions",
    "arm_bars", "entry_count", "entry1_price", "entry2_price",
    "entry3_price", "sl_exact_tail", "sl_test", "tp_price", "r_multiple",
    "atr", "spread_at_signal", "score", "mae", "mfe",
    "time_to_entry_seconds", "time_to_b_seconds", "time_to_exit_seconds",
    "slippage_points", "bid", "ask", "close_price",
}
REASON_CODES = {
    "H2_TOO_LOW", "PULLBACK_BROKE_ORIGIN", "PULLBACK_OUT_OF_RANGE",
    "NO_MODEL", "MODEL_UNRELIABLE", "NO_STRICT_REJECTION", "NO_B",
    "ENTRY_AMBIGUOUS", "STOP_INVALID", "MISSED_NO_CHASE", "EXPIRED",
    "SPREAD", "SESSION", "SAFETY", "",
}
