# TWER Validation Plan

**Status:** Acceptance criteria for future implementation; not test results.
**Scope:** Standalone TWER engine and later advisory/gate adapters. No TradingAgents Core modifications in this phase.

## A. Determinism and data integrity
- Same ordered closed-bar input + same config/version must yield byte-equivalent normalized events.
- Reordering, duplicate timestamps, malformed OHLC, missing required bars, and timezone ambiguity must be rejected or explicitly flagged.
- Structural state must never consume the currently forming bar.
- A replay with future bars removed must produce identical decisions up to the cutoff (anti-lookahead test).

## B. State-machine coverage
- Cover every allowed transition among S0–S14.
- Each invalid transition is rejected with a reason code.
- Invalidation, expiry, target, stop, fill, and `MISSED — NO CHASE` are terminal and cannot silently restart the same setup.
- No entry/stop/target is emitted before its defining state.
- B is not backdated to its extreme; it becomes known only when the confirming close exists.

## C. Strategy invariants
- BUY is the geometric mirror of SELL across all applicable wave, MODEL, entry, stop and target conditions.
- The pullback must obey the approved origin constraint.
- The second-wave extreme must use the selected, versioned tolerance rule.
- MODEL body/tail bounds must come from the documented cluster rule.
- Stop and target are directionally valid and must preserve the approved relationship to MODEL and B.
- A setup reaching B without entry is cancelled and logged `MISSED — NO CHASE`.

## D. Parameter provenance
- Every parameter is labeled `TRADER_RULE`, `SPEC_DEFAULT`, or `TEST_VALUE`.
- A run with any changed parameter has a distinct configuration fingerprint.
- Metrics from distinct parameter cohorts are not pooled without an explicit analysis step.
- No test asserts that experimental numeric defaults are trader-confirmed rules.

## E. READY TRADE gate
- Gate cannot return READY when TWER setup validation fails.
- Gate cannot override TWER levels or mutate engine state.
- Missing/stale news or market-context data follows a documented policy; it cannot be silently treated as a clean risk check.
- Initial adapter is alert-only and contains no order-placement side effects.

## F. Research Memory and audit
- Every gate decision is traceable to setup ID, engine/config versions, timestamps, source bars, advisory outputs, and reason codes.
- Terminal outcomes can be attached idempotently; duplicate delivery must not duplicate records.
- Credentials/secrets are excluded from stored payloads.
- Historical outcome labels are not available to the engine at decision time.

## G. Comparative research
- Evaluate baseline TWER and TWER + advisory filters on identical symbols, intervals, data windows, and execution assumptions.
- Keep walk-forward/out-of-sample windows separate from parameter selection.
- Include transaction costs, spread, slippage, unfilled limits, and missed/no-chase setups.
- Report sample size, uncertainty, drawdown and failure modes; do not infer profitability from the small historical sample alone.

## Release gate
Do not integrate into the TradingAgents graph until the canonical specification and decision register are approved, deterministic unit tests pass, anti-lookahead tests pass, and an alert-only historical replay is auditable.
