# TWER Decision Register

This is a working register, not approval of any unresolved rule. Consult the canonical PDF before changing entries.

| ID | Decision | Current source status | Safe handling before approval |
|---|---|---|---|
| D-01 | Swing/wave algorithm | Unresolved; A (ATR reversal) + B (minimum movement) recommended for first research implementation; numerical defaults are TEST VALUE | Log the mode and parameter hash; do not call defaults trader rules |
| D-02 | Pullback depth | TEST VALUE 0.20–0.95 of Wave 1 range | Version parameters and log every rejection |
| D-03 | Second-extreme tolerance | TEST VALUE 0.10; denominator itself unresolved | Log both Wave 1 and Wave 2 denominator variants |
| D-04 | Maximum Wave 2 overshoot | Unresolved; cap defaults off | Keep configurable/off pending evidence |
| D-05 | MODEL band/cluster | TEST VALUE band 1 ATR and 3–8 candles; exact cluster boundary unresolved | Log each model revision; never freeze before confirmation close |
| D-06 | Rejection requirement | Strict rejection is a strong inference; whether mandatory is unresolved | Keep STRICT traded and ARRIVAL log-only in separate populations |
| D-07 | Entry prices | Body-edge method is a hypothesis; percentage method is TEST VALUE | Compare both offline; do not silently select based on outcomes |
| D-08 | Entry count | One to three observed; mandatory count unresolved | Start research with one entry; test variants separately |
| D-09 | Stop buffer | Location beyond tail is a strong inference; distance unresolved | Log EXACT_TAIL and R_BASED(0.2) side-by-side; no claimed trader rule |
| D-10 | Break-even/trailing/extended target | Unresolved | Not implemented |
| D-11 | READY TRADE semantics | Integration design choice | Research/alert verdict only; never an order command |
| D-12 | Python vs MQL5 authority | Canonical spec recommends single MQL5 live/backtest path; Python offline research only | TradingAgents consumes exports downstream; no Python live-path duplicate |
| D-13 | Market/news data unavailable | Not fixed by the canonical TWER rules | Explicit INSUFFICIENT_DATA verdict; never fabricate a clean risk check |
| D-14 | Repository Core integration | Not approved | Keep existing Core files unchanged until standalone adapter contract and tests pass |

## Approval rule

No unresolved item becomes an implementation default without an explicit decision and source classification. Every parameter change must produce a distinct config fingerprint and separate research cohort.
