# Canonical Specification Alignment Note

This note clarifies the authoritative implementation boundary for the TWER project and takes precedence over any earlier exploratory wording in the architecture draft.

## Critical source requirement

Section 15 of TWER-Algorithmic-Specification-v1.0.pdf recommends that the complete live and backtest decision path reside in one MQL5 Expert Advisor, so Strategy Tester and live behavior cannot diverge. Python is offline-only for reading exported CSV/JSON logs, statistics, human-vs-bot tables, and later research. The specification explicitly warns that a Python component in the live path adds a second runtime and divergence risk.

Therefore:
- MQL5 is the authoritative strategy detector and, in later versions only, any execution path.
- TradingAgents/Python is downstream offline research and advisory analysis, not the source of entry/stop/target levels.
- READY TRADE in this integration is a research/alert verdict only; it is not an order command.
- No LLM may modify or override TWER state, entry, stop, target, or invalidation.
- No live execution is in scope; initial mode remains ALERT_ONLY.
- Do not change TradingAgents Core in this phase.

## Proposed data flow

MT5 EA -> versioned setups/transitions/rejects CSV/JSON and screenshots -> Python offline parser/validator -> optional market/news context analysis -> Research Memory and comparative reports.

Every record must preserve setup ID, timestamps including confirmation time, engine version, parameter-set hash, population (STRICT or ARRIVAL), state/reason codes, and source provenance. Missing or stale data must be marked explicitly.

## Key unresolved decisions from the canonical PDF

The specification marks these as unresolved or experimental; they must not be silently promoted into trader rules:
- Swing/wave definition and minimum size.
- Second-extreme tolerance denominator and overshoot cap.
- MODEL band and candle cluster boundaries.
- Whether rejection is mandatory; ARRIVAL is log-only until approved.
- Entry method and entry count.
- Stop buffer mode; the specification notes that 0.2R is in tension with measured R:R.
- Break-even, trailing, extended target, and session/instrument filters.
- Missing-bar handling and stale/missing advisory-data policy.

All TEST VALUE parameters must be versioned and analyzed as separate cohorts. The 33-trade historical sample is not a forecast or proof of profitability.

## Existing TradingAgents seam (inspected, not modified)

The repository has graph assembly in tradingagents/graph/setup.py, orchestration in tradingagents/graph/trading_graph.py, structured schemas in tradingagents/agents/schemas.py, and configuration in tradingagents/default_config.py. These remain unchanged until a downstream offline adapter is approved.
