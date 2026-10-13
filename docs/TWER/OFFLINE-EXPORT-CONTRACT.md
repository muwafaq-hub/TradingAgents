# TWER Offline CSV Contract v1 (Draft)

This is a proposed interface for the MT5 EA logger. It is not claimed to be the exact current logger output; align the MQL5 logger headers to this contract or version the contract before implementation.

## Common required columns

Every CSV has: `schema_version,engine_version,parameter_set_hash,population,setup_id,symbol,timeframe,side,event_time_utc,bar_time_utc,state,reason_code`.

- `schema_version` must equal `1.0-draft` for this draft.
- `population` is `STRICT` or `ARRIVAL`; never combine populations silently.
- timestamps must be ISO-8601 with timezone; normalized reports use UTC.
- `parameter_set_hash` identifies the exact parameters and all experimental values.
- raw rows are preserved; derived fields are not written back as source values.
- blanks mean unavailable/not yet defined; they are not numeric zero.
- unknown schema versions and missing required columns are errors.

## File-specific columns

### setups.csv (one row per completed or terminal setup)

Common columns plus:
`origin_price,ext1_price,pullback_price,ext2_price,model_start_utc,model_end_utc,model_tail_price,model_high,model_low,model_body_high,model_body_low,model_candles,rejection,b_price,b_extreme_time_utc,b_confirm_time_utc,b_revisions,arm_start_utc,arm_bars,entry_count,entry1_price,entry2_price,entry3_price,sl_exact_tail,sl_test,tp_price,r_multiple,atr,spread_at_signal,score,grade,result,mae,mfe,exit_time_utc,time_to_entry_seconds,time_to_b_seconds,time_to_exit_seconds,slippage_points`.

### transitions.csv (one row per state transition)

Common columns plus:
`transition_id,from_state,to_state,bid,ask,close_price`.

### rejects.csv (one row per rejected/invalidated candidate)

Common columns plus:
`candidate_id,from_state,detected_at_utc,details`.

The PDF specifies the purpose of each file and that rows carry the parameter-set hash and population, but does not prescribe literal header spellings. These names are therefore a proposed versioned contract, not a claim about existing EA output.

## Validation rules

- Preserve B extreme time separately from B confirmation time; B cannot be treated as confirmed before the confirming close.
- setup IDs and transition IDs must not be duplicated within their files.
- `side` is `BUY` or `SELL`; `population` is `STRICT` or `ARRIVAL`.
- numeric values may be blank when not reached; nonblank numeric values must parse as finite numbers.
- a B confirmation time before its extreme time is invalid.
- unknown reason codes are warnings for review, not silently rewritten.
- the adapter is offline-only: no order placement, MT5 control, or mutation of strategy levels.

## Versioning

Before the EA logger is implemented, approve the exact headers and bump `schema_version` for incompatible changes. Include engine version and parameter-set hash on every row.
