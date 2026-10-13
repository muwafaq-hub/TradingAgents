# TWER Integration Architecture (Proposal)

**Status:** Design proposal only — no strategy engine implemented yet.
**Branch:** `twer-integration`
**Reference:** `/TWER-Algorithmic-Specification-v1.0.pdf` (canonical supplied PDF).
**Safety boundary:** TradingAgents Core is intentionally unchanged in this phase.

## 1. Objectives

- Preserve the TWER algorithm as a deterministic, versioned rules engine.
- Keep LLM-based market/news/research analysis advisory; no LLM may silently change TWER geometry or thresholds.
- Run first in `ALERT_ONLY` mode, with no broker connection or live order submission.
- Separate trader-stated rules from all `TEST VALUE` research parameters.
- Make all decisions reproducible from timestamped market data, config version, and engine version.

## 2. Proposed module boundary (new isolated package)

Proposed new package: `twer/` at repository root. This avoids changing `tradingagents/` while requirements and tests are being established.

- `twer/models.py`: typed inputs, state, setup, levels, invalidation and event records.
- `twer/config.py`: versioned strategy parameters; each experimental parameter has an explicit provenance label.
- `twer/engine.py`: pure/deterministic state transitions; no network, LLM, broker, file I/O, or wall-clock dependency.
- `twer/validation.py`: invariant and completed-setup validation.
- `twer/serialization.py`: stable JSON representation for logs and downstream adapters.
- `tests/twer/`: synthetic fixtures and deterministic unit tests.
- `docs/TWER/`: canonical specification index, architecture, decision log, and validation plan.

These are proposed paths, not existing files. They are not created as executable code yet.

## 3. Core data contract

### Market input
Each bar includes instrument, timeframe, open/high/low/close, volume if available, exchange/server timestamp, and a stable source identifier. Bars must be ordered, unique, and timezone-explicit. Structural decisions consume closed bars only; live ticks may be used later only for execution/fill/stop/target monitoring.

### Engine configuration
Every parameter records:
- name and value;
- source class: `TRADER_RULE`, `SPEC_DEFAULT`, or `TEST_VALUE`;
- specification/config version;
- optional rationale and validation cohort.

Do not silently promote `TEST_VALUE` into a trader rule. Results from different parameter versions must be separable in research reports.

### Setup/event output
A setup record should include:
- `setup_id`, instrument, timeframe, side (`BUY`/`SELL`);
- current state and prior state;
- O, H1, Wave 2 extreme, MODEL body/tail bounds, B, ARM and candidate entry/stop/target when defined;
- event/bar timestamps and engine/config versions;
- validity, invalidation/no-trade reason codes;
- evidence bar IDs, not only free-form prose.

All levels must be absent until their defining state is reached. No future bar may be referenced in a past decision.

## 4. State machine

The specification's state labels are retained: `S0` through `S14`. The implementation should define explicit transition functions and allowed transitions. Invalid transitions must fail closed and emit a diagnostic event rather than guessing.

SELL is implemented first only if that is agreed for development convenience; BUY must be tested as a geometric mirror before release. The final engine must support both directions symmetrically.

A setup expires, invalidates, fills, reaches target/stop, or becomes `MISSED — NO CHASE` through explicit terminal outcomes. Every terminal outcome has a reason code.

## 5. Proposed analysis boundary

1. TWER engine computes setup facts and candidate levels.
2. Setup validator checks state and invariants.
3. Optional market-context and news-risk agents return separate typed advisory records with source timestamps and confidence/coverage.
4. READY TRADE gate combines valid TWER state with configured risk/context policy.
5. First release produces alerts and writes research records only.

The agents cannot rewrite the engine output. If an advisory service is unavailable, the gate follows an explicit configured fail-open/fail-closed policy; this choice must be settled before coding. It must never fabricate a positive risk check.

## 6. Research Memory contract

Research Memory stores events that reached the explicitly configured READY TRADE threshold, plus separately tagged rejected/invalidated setups if enabled for diagnostics. A record should include engine version, configuration fingerprint, parameter provenance, instrument/timeframe, timestamps, setup geometry, advisory results, gate result, eventual outcome when known, and data-quality flags.

Do not store API secrets, credentials, or unnecessary personal data. Research Memory is for audit and evaluation, not a mechanism for an LLM to modify strategy rules.

## 7. Current TradingAgents integration seam

Repository inspection found a LangGraph workflow in `tradingagents/graph/setup.py` and `tradingagents/graph/trading_graph.py`, structured decision schemas in `tradingagents/agents/schemas.py`, and configuration in `tradingagents/default_config.py`.

No integration into these files is proposed in this phase. After the standalone engine and tests are accepted, evaluate a narrow adapter/node that passes immutable TWER facts into the existing workflow. Do not replace or refactor the current graph, schemas, or trading logic as a prerequisite.

## 8. Decisions required before executable code

- Exact definitions for Wave 1, pullback, Wave 2, second-extreme tolerance, MODEL cluster, rejection, B confirmation and ARM.
- Which numeric defaults are accepted as `SPEC_DEFAULT` versus `TEST_VALUE`.
- Stop buffer model and how spread/slippage are represented.
- Expiry and no-chase behavior in edge cases.
- Missing bars, gaps, duplicate timestamps, market closures, and instrument precision.
- Gate policy when market/news analysis is unavailable or stale.
- Research record retention and the meaning of "trade" in a setup-only simulation.

Until these are explicitly resolved against the canonical PDF and trader-approved rules, unresolved choices must remain configuration switches and the engine must not claim strategy fidelity.

## 9. Rollout

1. Freeze specification and unresolved-decision register.
2. Implement standalone pure functions/state machine.
3. Unit-test state transitions and BUY/SELL symmetry.
4. Run historical replay with closed-bar discipline and anti-lookahead tests.
5. Compare baseline TWER vs TWER plus advisory filters on the same data and cohorts.
6. Enable alert-only shadow operation; do not enable live execution in this project phase.
